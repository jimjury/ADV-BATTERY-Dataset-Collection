#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build an ADV-BATTERY GitHub-public metadata repository from the local catalog.
Python 3.8+, standard library only. No raw third-party datasets are transferred.
"""
import argparse
import csv
import html
import json
import re
import sys
from datetime import date
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlsplit, parse_qsl

TAGS = {
    "SOC": ("SOC 估计", "State of charge"),
    "SOH": ("SOH 估计", "State of health"),
    "RUL": ("剩余寿命", "Remaining useful life"),
    "EIS": ("电化学阻抗谱", "Electrochemical impedance spectroscopy"),
    "FAST": ("快充", "Fast charging"),
    "FIELD": ("实车数据", "Real-world vehicle data"),
    "MODEL": ("电池建模", "Battery modeling"),
    "SAFETY": ("电池安全", "Safety and fault diagnosis"),
}
TAGS_ORDER = ["SOC", "SOH", "RUL", "EIS", "FAST", "FIELD", "MODEL", "SAFETY"]
TYPE_ZH = {"dataset": "数据集", "portal": "数据门户", "tool": "工具"}
TYPE_EN = {"dataset": "Dataset", "portal": "Data portal", "tool": "Tool"}
ACCESS_LABEL_ZH = {"checked": "已登记核验", "verified": "已登记核验", "catalogued": "已收录"}
STRIP_QUERY = {"access_token", "authorization", "api_key", "apikey", "token", "secret", "password", "session", "auth", "key"}

def clean_url(url):
    url = (url or "").strip()
    if not url:
        return ""
    try:
        s = urlsplit(url)
        if s.scheme not in ("https", "http") or not s.netloc or any(ord(c) < 32 for c in url):
            return ""
        if s.username is not None or s.password is not None:
            return ""
        if any(k.lower() in STRIP_QUERY for k,v in parse_qsl(s.query, keep_blank_values=True)):
            return ""
        return url
    except Exception:
        return ""

def text_safe(value):
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()

def md(value):
    return html.escape(text_safe(value), quote=False).replace("|", "&#124;").replace("`", "&#96;")

def disp(value):
    v=text_safe(value)
    return "—" if not v or v in ("—", "None", "null") else md(v)

def link(url, label):
    if not clean_url(url):
        return "—"
    # GitHub Markdown supports angle-quoted destinations (including query strings).
    return "[%s](<%s>)" % (md(label), clean_url(url).replace(">", "%3E"))

def abbrev(s, limit=58):
    s = text_safe(s)
    return s if len(s) <= limit else s[:limit-1].rstrip() + "…"

def get_type(d):
    return d.get("resource_type", "dataset")

def tags_text(d):
    return " · ".join("[" + x + "](docs/TOPICS.md#" + x.lower() + ")" for x in d["research_tags"]) if d["research_tags"] else "—"

def tags_plain(d):
    return " / ".join(d["research_tags"]) or "—"

def papers_for(d, papers_by_id):
    pids=d["related_paper_ids"]
    return [papers_by_id[k] for k in pids if k in papers_by_id]

def primary_paper(d, papers_by_id, english=False):
    papers=papers_for(d,papers_by_id)
    if not papers:
        return "—"
    # Dataset archive entries should not be represented as journal articles.
    p=papers[0]
    t=abbrev(p["title"], 48)
    val=link(p["url"], t)
    if val=="—":
        val=md(t)
    if p.get("is_dataset_record"):
        val += (" (数据记录)" if not english else " (data record)")
    if len(papers)>1:
        val += " +" + str(len(papers)-1)
    return val

def read_catalog(catalog):
    root=Path(catalog)
    def get(name):
        return json.loads((root / (name+".json")).read_text(encoding="utf-8"))
    dsource=get("datasets")["items"]
    psource=get("papers")["items"]
    rsource=get("relations")["items"]
    provenance=get("provenance")
    raw_src=next((s for s in provenance.get("external_source_imports",[]) if "PythoniLover" in s.get("source","")),None)
    mapping=raw_src.get("index_entries",[]) if raw_src else []
    byid={r["dataset_id"]:r for r in mapping}
    related=defaultdict(list)
    for r in rsource:
        pair=r["dataset_id"],r["paper_id"]
        if pair[1] not in related[pair[0]]:
            related[pair[0]].append(pair[1])
    for p in psource:
        pid=p["id"]
        dsid=p.get("data",{}).get("datasetId")
        if dsid and pid not in related[dsid]:
            related[dsid].append(pid)
    papers=[]
    for i,p in enumerate(psource, 1):
        x=p.get("data",{})
        papers.append({
            "index": i, "id":p["id"],"title":text_safe(x.get("title")),
            "authors":text_safe(x.get("authors")),"journal_or_source":text_safe(x.get("journal")),
            "year":x.get("year") if isinstance(x.get("year"),int) and x.get("year")>0 else None,
            "doi":text_safe(x.get("doi")),"url":clean_url(x.get("url")),
            "record_type":text_safe(x.get("kind")),"keywords":[text_safe(t) for t in x.get("keywords",[]) if text_safe(t)],
            "is_dataset_record":bool("数据集" in text_safe(x.get("kind")) or p["id"].startswith("doi:10.5281/zenodo") and "Zenodo" in text_safe(x.get("journal"))),
            "linked_dataset_ids":[],
        })
    papers_by_id={p["id"]:p for p in papers}
    datasets=[]
    for i, item in enumerate(dsource,1):
        x=item["data"]
        meta=item.get("overrides",{}).get("workbench",{}).get("meta",{})
        match=byid.get(item["id"])
        pids=[pid for pid in related.get(item["id"],[]) if pid in papers_by_id]
        datasets.append({
            "index":i, "id":item["id"],"name_zh":text_safe(x.get("cn")),
            "name_en":text_safe(x.get("title")),"institution":text_safe(x.get("institution")),
            "country":text_safe(x.get("country")),
            "year":x.get("year") if isinstance(x.get("year"),int) and x.get("year")>0 else None,
            "resource_type":text_safe(meta.get("resourceType") or "dataset"),
            "research_tags":[t for t in meta.get("tasks",[]) if t in TAGS],
            "chemistry":text_safe(x.get("chemistry")),
            "formats":[text_safe(s) for s in (x.get("formats") or [])],
            "size_note":text_safe(x.get("size")),
            "cells_note":text_safe(x.get("cells")),
            "test_conditions_note":text_safe(x.get("conditions")),
            "description_zh":text_safe(x.get("description")),
            "task_note":text_safe(x.get("task")),
            "source_url":clean_url(x.get("source")),
            "access_url":clean_url(x.get("download")),
            "dataset_doi":text_safe(x.get("datasetDoi")),
            "license_as_recorded":text_safe(x.get("license")),
            "source_catalog_status":text_safe(meta.get("sourceStatus")),
            "download_catalog_status":text_safe(meta.get("downloadStatus")),
            "related_paper_ids":pids,
            "source_41_index":match["index"] if match else None,
        })
    dsids={d["id"] for d in datasets}
    for d in datasets:
        for pid in d["related_paper_ids"]:
            p=papers_by_id[pid]
            if d["id"] not in p["linked_dataset_ids"]:
                p["linked_dataset_ids"].append(d["id"])
    relations=[]
    for rel in rsource:
        relations.append({
            "id":rel["id"],"dataset_id":rel["dataset_id"],
            "paper_id":rel["paper_id"],"relation_type":rel.get("relation_type",""),
            "review_status":rel.get("review_status",""),
            "evidence_url":clean_url(rel.get("evidence_url")),
        })
    mapping_export=[{
        "source_number": x.get("index"), "dataset_id":x.get("dataset_id",""),
        "source_provider":text_safe(x.get("provider")),
        "source_url":clean_url(x.get("url")),
        "matching_decision":text_safe(x.get("decision")),
        "paper_status":text_safe(x.get("paper_status")),
    } for x in mapping]
    return datasets,papers,relations,mapping_export

def validate(ds,ps,rs,src):
    assert len({d["id"] for d in ds})==len(ds),"Duplicate dataset ID"
    assert len({p["id"] for p in ps})==len(ps),"Duplicate paper ID"
    assert len({(r["dataset_id"],r["paper_id"]) for r in rs})==len(rs),"Duplicate relation"
    dsids={d["id"] for d in ds}
    pids={p["id"] for p in ps}
    for d in ds:
        assert d["name_en"] or d["name_zh"],d["id"]
        assert clean_url(d["source_url"]), ("invalid source URL",d["id"])
        assert clean_url(d["access_url"]), ("invalid access URL",d["id"])
        assert set(d["research_tags"]).issubset(TAGS),d["id"]
        assert set(d["related_paper_ids"]).issubset(pids),d["id"]
    for r in rs:
        assert r["dataset_id"] in dsids,r
        assert r["paper_id"] in pids,r
    for p in ps:
        assert p["title"],p["id"]
        assert set(p["linked_dataset_ids"]).issubset(dsids),p["id"]
        if p["url"]:
            assert clean_url(p["url"]),p["id"]
    assert len({x["source_number"] for x in src})==len(src), "Source index collisions"
    assert set(x["dataset_id"] for x in src).issubset(dsids),"Unknown source item mapping"
    return True

def render_readme(ds,ps,rs,english=False,snapshot_date="2026-11-06"):
    byp={p["id"]:p for p in ps}
    counts=Counter(d["resource_type"] for d in ds)
    tagcounts=Counter(x for d in ds for x in d["research_tags"])
    title="# ADV·BATTERY | Open Battery Dataset Collection\n\n" if english else "# ADV·BATTERY｜公开电池数据资源索引\n\n"
    intro=("**An open, traceable directory of battery data sources, associated publications, and research topics.**\n\n"
           if english else "**开放数据，关联文献，服务电池科研。**\n\n")
    n=len(ds); np=len(ps); nr=len(rs)
    summary=(f"**{n} resources** · **{counts['dataset']} datasets** · **{counts['portal']} portals + {counts['tool']} tool** · **{np} publication/catalogue records** · **{nr} registered dataset–publication relations**\n\n"
             if english else
             f"**{n} 条数据资源** · **{counts['dataset']} 条数据集** · **{counts['portal']} 个数据门户 + {counts['tool']} 个工具** · **{np} 条文献/目录记录** · **{nr} 条已登记数据—文献关联**\n\n")
    notes=(
        "> **Scope:** This repository hosts **metadata, descriptions and links only**, not third-party raw datasets. Original providers control downloads, licensing and access. Availability has **not** been exhaustively live-tested; these are catalogue records, not a promise of downloadable files. Last catalogue export: **2026-11-06**.\n\n"
        if english else
        "> **注意：** 本仓库只整理**数据集目录、研究标签和原始链接**，不托管第三方原始实验数据。开放访问不等于可任意转载或用于商业用途；下载与许可以发布方为准。链接**未全部逐一实时测试**。资料库快照：**2026-11-06**。\n\n"
    )
    notes=notes.replace("2026-11-06",snapshot_date)
    other=("[中文版](README.md) · [Research topics](docs/TOPICS.md) · [Full details](docs/DATASET_DETAILS.md) · [Publications](docs/PAPERS.md) · [Source & terms](NOTICE.md)\n\n" if english else
           "[English version](README_EN.md) · [按研究标签浏览](docs/TOPICS.md) · [80 条资源详情](docs/DATASET_DETAILS.md) · [108 条文献索引](docs/PAPERS.md) · [来源与使用说明](NOTICE.md)\n\n")
    online=("**[V2 research workbench (online)](https://jimjury.github.io/ADV-BATTERY-Dataset-Collection/)** · [Connection and setup](docs/GITHUB_V2_LINK_SETUP.md)  \n"\
            "GitHub Pages must be enabled once under Settings → Pages (main /docs).\n\n"\
            if english else\
            "**[V2 科研工作台在线版](https://jimjury.github.io/ADV-BATTERY-Dataset-Collection/)** · [联动、发布与启用说明](docs/GITHUB_V2_LINK_SETUP.md)  \n"\
            "首次使用需在 Settings → Pages 选择 main /docs；未启用前在线网址尚不可访问。\n\n")
    toc=("## Contents\n\n1. [How to use](#how-to-use)\n2. [Full resource directory](#full-resource-directory)\n3. [Explore by topic](#explore-by-topic)\n4. [Coverage and caveats](#coverage-and-caveats)\n5. [Maintaining the collection](#maintaining-the-collection)\n\n"
         if english else
         "## 目录\n\n1. [新手如何使用](#新手如何使用)\n2. [完整资源目录](#完整资源目录)\n3. [按研究方向查找](#按研究方向查找)\n4. [来源与核验说明](#来源与核验说明)\n5. [参与维护与更新](#参与维护与更新)\n\n")
    how=("## How to use\n\n1. Filter by a topic like SOC, SOH or RUL, or search an institution in the table.\n2. Open the **Data access** link; it may point to a landing page, not a direct downloadable archive.\n3. Check the linked paper and data provider's licence, protocol and version before use.\n\n"
         if english else
         "## 新手如何使用\n\n1. 在下表按机构、数据名称或 **SOC / SOH / RUL** 等标签寻找资源。\n2. 点击“**数据入口**”到原始仓库；部分链接是资料页或需要单独申请，并非可直接下载的 ZIP。\n3. 阅读相关论文，核对电池类型、实验条件、数据版本及许可证，再用于科研。\n\n")
    head=("## Full resource directory\n\n"
          "| # | Dataset / resource | Institution | Year | Type | Topic tags | Data access | Associated reference |\n"
          "|---:|---|---|---:|---|---|---|---|\n"
          if english else
          "## 完整资源目录\n\n"
          "| 序号 | 数据集 / 资源名称 | 发布机构 | 年份 | 类型 | 研究标签 | 数据入口 | 关联文献 |\n"
          "|---:|---|---|---:|---|---|---|---|\n")
    rows=[]
    for d in ds:
        name=d["name_en"] if english else (d["name_zh"] or d["name_en"])
        typ=(TYPE_EN if english else TYPE_ZH).get(get_type(d),get_type(d))
        rows.append(f"| {d['index']:02d} | [{md(name)}](docs/DATASET_DETAILS.md#dataset-{d['index']:02d}) | {disp(d['institution'])} | {disp(d['year'])} | {typ} | {tags_text(d)} | {link(d['access_url'], 'Access' if english else '数据入口')} | {primary_paper(d,byp,english)} |")
    table="\n".join(rows)+"\n\n"
    counts_title="## Explore by topic\n\n" if english else "## 按研究方向查找\n\n"
    topicrows=["| Topic | Items | Description |","|---|---:|---|"] if english else ["| 标签 | 相关资源数 | 研究方向 |","|---|---:|---|"]
    for key in TAGS_ORDER:
        topicrows.append(f"| [{key}](docs/TOPICS.md#{key.lower()}) | {tagcounts[key]} | {md(TAGS[key][1] if english else TAGS[key][0])} |")
    topic_body="\n".join(topicrows)+"\n\n"
    topic_note=("_Topic membership is non-exclusive and reflects the existing catalogue labels; it does not prove all raw files contain a specific measured field._\n\n" if english else "_同一资源可以有多个研究标签；标签来自现有资料库，不代表已经核对所有原始文件是否具备相应字段。_\n\n")
    license_sec=(("## Coverage and caveats\n\n"
                 "- **80 resources** include **76 dataset entries** and **4 resource pages** (3 portals + 1 tool).\n"
                 "- **108 records** include research papers, method reviews and dataset catalogue/citation records; they are not all peer-reviewed papers.\n"
                 "- **69 explicit relations** were carried over from the curated catalogue; relationships have different review statuses.\n"
                 "- This directory incorporates a [41-entry community list](https://github.com/PythoniLover/battery-dataset-collection) after deduplication (**14 matched existing items, 27 added**). See [source mapping](docs/SOURCE_41_MAPPING.md).\n"
                 "- Year, author, licence and completeness can vary between dataset versions and associated publications. The text is a catalogue snapshot rather than a full independent audit. See [NOTICE](NOTICE.md).\n\n"
                 "## Maintaining the collection\n\n"
                 "The maintained source of truth is the local ADV·BATTERY catalogue. Use [update instructions](docs/MAINTENANCE.md), then run `python scripts/build_public_index.py --check` and `python scripts/validate_public_index.py`. Contribution suggestions are welcome via [CONTRIBUTING](CONTRIBUTING.md).\n")
                 if english else
                 "## 来源与核验说明\n\n"
                 "- **80 条资源**包括 **76 条数据集条目**和 **4 个资料入口**（3 个门户、1 个工具），不是 80 份打包的数据文件。\n"
                 "- **108 条文献/目录记录**包含研究论文、综述、数据集正式记录等，并不全是同行评议论文。\n"
                 "- **69 条显式关联**保留了原资料库中的审核状态，并非全部经过独立验证。\n"
                 "- 整合了 [PythoniLover 的 41 条来源目录](https://github.com/PythoniLover/battery-dataset-collection)，其中 **14 条匹配原记录、27 条新增**，详见 [来源对应表](docs/SOURCE_41_MAPPING.md)。\n"
                 "- 某些资源仅提供元数据页面、索引或受限入口；论文年份和数据版本年份也可能不同。详见 [来源、免责声明与许可](NOTICE.md)。\n\n"
                 "## 参与维护与更新\n\n"
                 "本目录由 ADV·BATTERY 正式资料库导出。提交新资源请参考 [贡献指南](CONTRIBUTING.md)；同步本地最新版请参考 [维护说明](docs/MAINTENANCE.md)，并使用 `python scripts/build_public_index.py --check` 和 `python scripts/validate_public_index.py` 验证。\n")
    other=other.replace("80 条资源详情",f"{len(ds)} 条资源详情").replace("108 条文献索引",f"{len(ps)} 条文献索引")
    license_sec=(license_sec.replace("80 resources", f"{len(ds)} resources")
        .replace("76 dataset entries", f"{counts['dataset']} dataset entries")
        .replace("4 resource pages", f"{counts['portal']+counts['tool']} resource pages")
        .replace("3 portals + 1 tool", f"{counts['portal']} portals + {counts['tool']} tool")
        .replace("108 records",f"{len(ps)} records")
        .replace("69 explicit relations",f"{len(rs)} explicit relations")
        .replace("80 条资源",f"{len(ds)} 条资源")
        .replace("76 条数据集条目",f"{counts['dataset']} 条数据集条目")
        .replace("4 个资料入口",f"{counts['portal']+counts['tool']} 个资料入口")
        .replace("3 个门户、1 个工具",f"{counts['portal']} 个门户、{counts['tool']} 个工具")
        .replace("108 条文献/目录记录",f"{len(ps)} 条文献/目录记录")
        .replace("69 条显式关联",f"{len(rs)} 条显式关联"))
    return title + intro + summary + notes + other + online + toc + how + head + table + counts_title + topic_body + topic_note + license_sec

def render_topics(ds):
    lines=["# 按研究方向浏览 / Explore by research topic","",
        "此处使用 ADV·BATTERY 正式资料库中已有的 8 种研究标签。资源可能属于多个方向；标签不等于对原始文件内容的逐项核验。","",
        "[返回首页](../README.md) · [English README](../README_EN.md)",""]
    for key in TAGS_ORDER:
        entries=[d for d in ds if key in d["research_tags"]]
        lines.extend([f"## {key}","", f"**{TAGS[key][0]} / {TAGS[key][1]}**","",
           f"**{len(entries)} 条相关资源**（含门户和工具，如适用）。","",
           "| # | 数据集 / 资源名称 | 年份 | 机构 | 数据入口 |",
           "|---:|---|---:|---|---|"])
        for d in entries:
            lines.append(f"| {d['index']:02d} | [{md(d['name_zh'] or d['name_en'])}](DATASET_DETAILS.md#dataset-{d['index']:02d}) | {disp(d['year'])} | {disp(d['institution'])} | {link(d['access_url'],'访问')} |")
        lines.append("")
    return "\n".join(lines)+"\n"

def render_details(ds,ps):
    papers_by_id={p["id"]:p for p in ps}
    lines=[f"# ADV·BATTERY 资源详情索引（{len(ds)} 条）","",
        "从正式资料库按源文件字段导出。**以下电池体系、实验条件、大小、许可证文字均为目录记录，并未逐项重新下载原始文件核对。** 不明字段按原值呈现，不作推测。","",
        "[返回首页](../README.md) · [研究方向](TOPICS.md) · [全部文献](PAPERS.md)",""]
    for d in ds:
        lines.extend([f'<a id="dataset-{d["index"]:02d}"></a>',
                      f'## {d["index"]:02d}. {md(d["name_zh"] or d["name_en"])}',"",
                      f"**英文名称：** {disp(d['name_en'])}  ",
                      f"**内部稳定 ID：** `{d['id']}`  ",
                      f"**资源类型：** {TYPE_ZH.get(d['resource_type'],d['resource_type'])}  ",
                      f"**发布机构：** {disp(d['institution'])}  ",
                      f"**年份（目录记录）：** {disp(d['year'])}  ",
                      f"**国家/地区：** {disp(d['country'])}  ",
                      f"**研究标签：** {tags_plain(d)}  ",
                      f"**电池体系：** {disp(d['chemistry'])}  ",
                      f"**样本规模/电芯：** {disp(d['cells_note'])}  ",
                      f"**测试条件：** {disp(d['test_conditions_note'])}  ",
                      f"**数据格式：** {disp(', '.join(d['formats']))}  ",
                      f"**规模备注：** {disp(d['size_note'])}  ",
                      f"**数据集 DOI：** {link('https://doi.org/'+d['dataset_doi'],d['dataset_doi']) if d['dataset_doi'] else '—'}  ",
                      f"**来源站：** {link(d['source_url'],'来源主页')}  ",
                      f"**获取入口：** {link(d['access_url'],'数据入口（可能为资料页）')}  ",
                      f"**许可记录（未统一核验）：** {disp(d['license_as_recorded'])}  ",
                      f"**来源收录状态：** {disp(d['source_catalog_status'])}；**下载记录状态：** {disp(d['download_catalog_status'])}  ",
                      f"**原 41 条来源编号：** {d['source_41_index'] if d['source_41_index'] else '—'}","",
                      f"**资料库描述：** {disp(d['description_zh'])}","",
                      "**原资料库关联文献：**"])
        related=papers_for(d,papers_by_id)
        if related:
            for p in related:
                suffix="（数据集记录，非期刊论文）" if p["is_dataset_record"] else ""
                lines.append(f"- {link(p['url'],p['title']) if p['url'] else md(p['title'])} ({p['year'] or '年份未记载'}){suffix}；`{p['id']}`")
        else:
            lines.append("- 暂无已登记直接关联；不代表该数据集没有发表论文。")
        lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines)+"\n"

def render_papers(ps):
    lines=[f"# 文献与数据目录记录（{len(ps)} 条）","",
           "这里按 ADV·BATTERY 正式资料库顺序展示全部记录，**包含研究论文、综述、数据集 DOI 记录等，不表示 108 篇均为正式研究论文**。`关联数据集`仅列资料库已登记关联；空白不代表无关。","",
           "[返回首页](../README.md) · [资源详情](DATASET_DETAILS.md)","",
           "| # | 文献 / 目录记录 | 年份 | 记录类型 | DOI / 原始地址 | 关联数据资源 ID |",
           "|---:|---|---:|---|---|---|"]
    for p in ps:
        paper_link=link(p["url"],abbrev(p["title"],92)) if p["url"] else md(abbrev(p["title"],92))
        doc_link=link("https://doi.org/"+p["doi"],p["doi"]) if p["doi"] else link(p["url"],"来源")
        assoc=", ".join("`"+v+"`" for v in p["linked_dataset_ids"]) or "—"
        lines.append(f"| {p['index']:03d} | {paper_link} | {disp(p['year'])} | {disp(p['record_type'])} | {doc_link} | {assoc} |")
    lines.extend(["","","> 注意：表内 DOI 与链接为原资料库记录，仅能反映已有整理工作，不构成对每篇文献、数据许可或下载链接现时可用性的独立保证。",""])
    return "\n".join(lines)

def render_notice(ds,ps,rs,snapshot_date="2026-11-06"):
    notice="""# 来源说明、许可与科研使用提醒 / Source and usage notice

## 本仓库包含什么

本仓库公开的是 **80 条电池数据资源的目录信息**、**108 条文献/目录记录**、**69 条关联关系**及标签分类。这里不上传第三方原始电池数据、不转存论文 PDF、不镜像数据仓库。

## 来源与致谢

- 第一手资料：各数据集的官方发布机构、原始数据仓库（NASA、CALCE、Mendeley Data、Zenodo、Figshare、大学仓库、机构网页等）。每条资源保留各自的来源与数据入口。
- 二次来源索引：[PythoniLover/battery-dataset-collection](https://github.com/PythoniLover/battery-dataset-collection)，提供 41 条社区整理的原始资源目录。本项目对其中 41 条进行了映射、去重和扩充；**14 条匹配已有资源，27 条成为新增资源记录**。对应关系列于 [source_41_mapping.csv](data/source_41_mapping.csv)。
- ADV·BATTERY 本地资料库：其余资源与论文记录来自此前逐步构建的项目。

**请在引用实验数据时优先引用原始数据发布者及对应论文，而非仅引用本目录或社区汇总页。**

## 许可与责任

- 外部数据集、论文和平台的版权、许可协议、账号限制、访问条款仍由各自发布方决定。
- 表中的 `license_as_recorded` 是原有资料库记录的文字，**并不表示本仓库已对每个许可证做法律核验**。
- 公开可访问 ≠ 任意再分发 ≠ 已获商业使用授权。
- “数据入口”可能是资料页、代码页、仅元数据记录、受限共享文件夹或直接下载链接。
- 部分关联状态为 `pending` 或 `source-recorded`，说明记录曾被收录，但不代表每条都已独立核验。
- 本仓库不提供统一适用于全部第三方数据的许可证。

## 精度与时效

- 导出基线：2026-11-06。
- 总表的年份可能是数据版本年份或目录登记年份，与论文发表年份不同。
- 部分条目缺少电池材料、容量、采样频率或下载可用性验证；本仓库保留未知，不自动推断。
- 如果需要复现科研实验，请从原站确认数据格式、采样频率、实验条件、标签构造方法和最终用户许可。

## GitHub 仓库自身许可

此初始包**暂不包含 LICENSE 文件**。仓库所有者可以在确认自己对文字、代码和整理成果的权利后，为自己的原创内容选择 MIT / CC BY 4.0 等适当许可证。任何自选许可证都不能改变第三方原始数据的许可。

## English

This directory lists dataset references and metadata, not the original third-party datasets. Rights, licences, access requirements, and provenance remain with the original publishers. The catalogue has not independently checked every current download link or licence. Cite the original dataset and companion publication when conducting research.
"""
    return notice.replace("80 条",f"{len(ds)} 条").replace("108 条",f"{len(ps)} 条").replace("69 条",f"{len(rs)} 条").replace("2026-11-06",snapshot_date)

def render_contribute():
    return """# 贡献指南 / Contributing

欢迎报告失效链接、错误的 DOI、遗漏的数据集、新的论文对应关系、更新的研究标签等。

建议提供：

1. 数据集名称（中/英文均可）、发布机构以及**原始数据站链接**。
2. DOI（如果官方提供）；DOI 不明可留空，**不要猜测**。
3. 关联论文的准确标题、DOI / 正式出版页，以及它为何与该数据集相关。
4. 电池体系、容量、温度、倍率等字段的来源依据（原始页面或论文具体位置）。
5. 官方许可/访问条件，或注明“尚未核验”。

重复判断按稳定 ID、标准 DOI 和数据源 URL 进行；相似标题只标记疑似重复。不可因名称相似直接合并不同版本的数据集。

**安全事项：** 不要在 Issue/PR 中提交付费账号、cookie、带 token 的共享链接、个人数据、未经许可的论文 PDF 或外部实验数据原始文件。

正式资料库维护人员应在本地 ADV·BATTERY 审核新记录、运行双网站测试并生成公开仓库索引；详见 [维护说明](docs/MAINTENANCE.md)。
"""

def render_maintenance():
    return """# 公共 GitHub 索引维护与同步 SOP

## 一、哪些文件是权威来源？

**ADV·BATTERY 本地工程中的 `engine/catalog/` 才是最初的正式事实来源。** 本 GitHub 仓库是其**公开目录快照**。

- `data/datasets.json`：80 条资源的公开字段快照。
- `data/papers.json`：108 条文献与目录记录的公开字段快照。
- `data/relations.json`：69 条明确记录的关联。
- `data/source_41_mapping.csv`：来源 41 条数据的去重映射。
- `README.md` / `README_EN.md` / `docs/*.md` / `data/*.csv`：由同一脚本生成，不要长期维护多份独立手工数据。

本 GitHub 包**没有包含**原本地项目的 `admin/`、`staging/`、`history/`、`releases/`、API 密钥、个人笔记等。

## 二、从本地 ADV·BATTERY 同步更新

确保本地已有可发布的通过审核的正式资料库，例如：

```powershell
python scripts/build_public_index.py --catalog "D:\\ADV_BATTERY\\engine\\catalog" --write
python scripts/validate_public_index.py
python scripts/build_public_index.py --check
```

注意：`--catalog` 路径是**包含 datasets.json 等正式数据 JSON 的文件夹**，不是 `catalog` 的上级。命令不会修改这个目录，只读取白名单字段，更新**本公开仓库**。

## 三、不想访问原工程时

可直接修改此仓库的 `data/datasets.json` / `data/papers.json` / `data/relations.json`，再运行：

```powershell
python scripts/build_public_index.py --write
python scripts/validate_public_index.py
python scripts/build_public_index.py --check
```

不过这可能导致 GitHub 公共目录和本地网站**数据分叉**。更推荐在本地管理中心审批入库，然后统一重新导出。

## 四、改动和发布检查

- [ ] 修改前留存当前公开仓库版本。
- [ ] 数据集稳定 ID 未被意外删除或重命名。
- [ ] 数据来源网址、版本、论文 DOI 有明确出处。
- [ ] 不将论文 DOI 当作数据集下载地址。
- [ ] 研究任务标签来自可核实记录；不凭标题推断原始数据一定含某字段。
- [ ] `python scripts/validate_public_index.py` 通过。
- [ ] `python scripts/build_public_index.py --check` 通过。
- [ ] 手动打开 GitHub 首页，核对总数、分类、表格链接。
- [ ] 检查没有 PDF 原文、raw data、私人草稿、密钥、token 和本机绝对路径被提交。
- [ ] 写清楚本次新增、合并、修正数量，及尚未验证项目。

## 五、遇到错误

- 中文乱码：所有 Python 文件使用 `encoding="utf-8"`；CSV 以 UTF-8 with BOM 导出，便于 Windows Excel 打开。
- 统计数字不一致：通过脚本从公开 JSON **动态生成**，不要直接手改 `README.md` 的数字。
- 链接失效：先在原站查最新版本；旧 DOI 保持引用记录，不要直接改成相似标题的其他数据。
- GitHub 页面只看到压缩包：需要**解压后上传里面的文件和目录**，不能只上传 ZIP。
- 提交的文件不显示：确认 `README.md` 位于仓库根目录，而不是多一层空的外包目录。

## 六、双网站独立于 GitHub 目录

GitHub 目录**不会自动更新**两版离线 HTML。每次新增数据，请遵循本地管理中心的审批、构建、浏览器检查、发布流程；之后再同步 GitHub，避免两个渠道出现不同记录。
"""

def render_upload():
    return """# GitHub 网页上传操作指南（Windows，零命令行）

**推荐仓库名：** `ADV-BATTERY-Dataset-Collection`。名称只是建议，今后可以调整。以下操作只发布数据目录，**不上传第三方真实电池数据文件**。

## 第 0 步：先确认你要公开什么

这份 ZIP 已排除了：`engine/` 管理中心、`staging/` 草稿、`history/` 审核日志、私人备份、API Key、其他项目源代码和原始实验文件。

公开内容包括 **80 条资源目录、108 条论文/目录记录、69 条关联、41 条来源对照**以及使用说明。公开仓库任何人均可访问这些信息；请确认你希望这些**索引资料**公开。

## 第 1 步：解压上传包

在 Windows 文件资源管理器中右击 `ADV_BATTERY_GitHub_可上传完整仓库.zip` → **全部解压缩**。

进入其中的 `ADV-BATTERY-Dataset-Collection` 文件夹，你应该直接看到：

- `README.md`
- `README_EN.md`
- `NOTICE.md`
- `CONTRIBUTING.md`
- `data/`
- `docs/`
- `scripts/`
- `.github/`

**注意：这里的 `data/` 是 CSV/JSON 目录索引，不是电池数据原文件。**

## 第 2 步：在 GitHub 创建公开仓库

1. 浏览器登录 [GitHub](https://github.com/)。
2. 打开 [新建仓库页面](https://github.com/new)。
3. `Repository name` 填 `ADV-BATTERY-Dataset-Collection`。
4. `Description` 建议填写：

   `A curated, research-oriented index of 80 battery data resources with source links, publications, and SOC/SOH/RUL tags.`

5. `Visibility` 选择 **Public**（公开）。
6. **不要勾选**初始化 README、`.gitignore` 或 License；本包已包含前两个文件，许可证应另外确认。
7. 点击 `Create repository`。

## 第 3 步：把全部目录文件放上 GitHub

1. 打开新仓库主页，找 `uploading an existing file`；或在仓库里点 **Add file → Upload files**。
2. 把解压后的 `ADV-BATTERY-Dataset-Collection` 文件夹内**所有内容**（不是 ZIP 文件，也不是外包文件夹本身）拖到网页上传区域。GitHub 支持选择文件或文件夹拖放。
3. 检查待上传列表，至少有 `README.md`、`README_EN.md`、`data/datasets.json`、`docs/TOPICS.md`。
4. `Commit message` 填：`Initial public catalogue: 80 battery resources`。
5. 点击 `Commit changes`（有的界面会显示 `Propose changes`，按页面提示完成提交）。

官方文档称浏览器一次最多上传 **100 个文件**、单文件不超过 **25 MiB**；本包远低于这两个限制。

## 第 4 步：验收 GitHub 展示

仓库首页应自动显示 `README.md` 的排版：

- 标题 `ADV·BATTERY｜公开电池数据资源索引`
- 统计：**80 资源 / 76 数据集 + 4 入口 / 108 文献记录 / 69 关联**
- 完整 80 行资源表格
- 八个研究标签的检索入口
- 可以点击 `README_EN.md` 查看英文版

再点几个实际链接验证页面可跳转（部分外部网站可能需要登录或网络环境）。

如果首页只出现一个 ZIP 下载文件，说明上传的是压缩包：请重新上传**解压后的文件与文件夹**。

## 第 5 步：完善仓库主页

在仓库右侧 **About** 的设置里：
- Description：沿用第二步文字
- Topics：`battery-dataset`、`lithium-ion-battery`、`soc`、`soh`、`rul`、`battery-health`、`battery-research`
- Website：如果你**已经**发布了 ADV·BATTERY 的正式公开网址，可填写；否则留空，别填本机 `127.0.0.1`。

你无需安装 Python、Git 或 Node.js 就能完成**首次上传**。Python 脚本仅供未来自动维护目录。

## 第 6 步：之后更新数据

先在本地 ADV·BATTERY 管理中心完成数据审核与双 HTML 构建，随后参照 [维护说明](MAINTENANCE.md) 更新公共仓库的 CSV/JSON/Markdown。更新文件以后可以通过 GitHub 网页继续上传替换，或使用 GitHub Desktop 管理版本。

**下一轮建议：** 把新建的 GitHub 仓库页面截图发给我，我再对照页面指导你检查 README 和所有子目录是否完整。
"""

def render_source_mapping(source_map, datasets):
    byid={d["id"]:d for d in datasets}
    counts=Counter(x.get("matching_decision","") for x in source_map)
    lines=["# 41 条社区数据目录对应关系 / Source mapping",
           "",
           "来源：[PythoniLover/battery-dataset-collection](https://github.com/PythoniLover/battery-dataset-collection)。",
           "",
           f"**{len(source_map)} 条来源记录**：{counts['existing']} 条对应已有数据资源，{counts['new']} 条新增，{counts['new-version']} 条独立版本。",
           "",
           "该对应关系根据原始来源目录与本项目已有清单建立；它不等同于逐个下载验证或保证每个第三方链接有效。",
           "",
           "[返回首页](../README.md) · [CSV 表格](../data/source_41_mapping.csv)",
           "",
           "| 来源编号 | 原发布机构 | ADV·BATTERY 对应名称 | 稳定 ID | 处理结论 | 原始链接 |",
           "|---:|---|---|---|---|---|"]
    state={"existing":"匹配已有记录","new":"新增","new-version":"独立数据版本"}
    for item in source_map:
        d=byid.get(item["dataset_id"])
        lines.append(f"| {item['source_number']} | {disp(item['source_provider'])} | "
          f"{md(d['name_zh'] or d['name_en']) if d else '—'} | "
          f"`{md(item['dataset_id'])}` | {state.get(item.get('matching_decision'),disp(item.get('matching_decision')))} | "
          f"{link(item['source_url'],'原始来源')} |")
    lines.append("")
    return "\n".join(lines)+"\n"

def repo_gitignore():
    return """# Keep the public GitHub index metadata-only.
__pycache__/
*.py[cod]
.venv/
venv/
.env
.env.*
*.key
*.pem
*.p12
*.pfx
local_settings.json
machine_paths.json
secrets.*
.idea/
.vscode/
*.log
.DS_Store
Thumbs.db

# Do not leak private ADV-BATTERY workspace files
engine/
staging/
history/
operator_backups/
catalog-backups/
inputs/
baseline/
releases/
*.pdf
*.rar
*.7z
*.zip
*.xlsx
*.xls
*.db
*.sqlite
*.sqlite3
"""

def build_repo(ds,ps,rs,source_map,output,info,check=False):
    root=Path(output)
    export_files={}
    info=dict(info)
    info.update({"resource_count":len(ds),"dataset_count":sum(d["resource_type"]=="dataset" for d in ds),
                 "portal_count":sum(d["resource_type"]=="portal" for d in ds),
                 "tool_count":sum(d["resource_type"]=="tool" for d in ds),
                 "publication_record_count":len(ps),"explicit_relation_count":len(rs),
                 "source_mapping_count":len(source_map)})
    export_files["data/catalog_info.json"]=json.dumps(info,ensure_ascii=False,indent=2)+"\n"
    export_files["NOTICE.md"]=render_notice(ds,ps,rs,info["snapshot_date"])
    export_files["data/datasets.json"]=json.dumps(ds,ensure_ascii=False,indent=2)+"\n"
    export_files["data/papers.json"]=json.dumps(ps,ensure_ascii=False,indent=2)+"\n"
    export_files["data/relations.json"]=json.dumps(rs,ensure_ascii=False,indent=2)+"\n"

    def csv_text(records,columns):
        import io
        out=io.StringIO()
        writer=csv.DictWriter(out,fieldnames=columns,lineterminator="\n",extrasaction="ignore")
        writer.writeheader()
        for row in records:
            cooked={}
            for k in columns:
                v=row.get(k)
                if isinstance(v,list):
                    v="; ".join(str(x) for x in v)
                elif v is None: v=""
                cooked[k]=v
            writer.writerow(cooked)
        return "\ufeff"+out.getvalue()
    export_files["data/datasets.csv"]=csv_text(ds,[
        "index","id","name_zh","name_en","institution","country","year","resource_type",
        "research_tags","chemistry","formats","size_note","cells_note","test_conditions_note",
        "source_url","access_url","dataset_doi","license_as_recorded",
        "source_catalog_status","download_catalog_status","related_paper_ids","source_41_index"
    ])
    export_files["data/papers.csv"]=csv_text(ps,[
        "index","id","title","authors","journal_or_source","year","doi","url","record_type","keywords","linked_dataset_ids"
    ])
    export_files["data/relations.csv"]=csv_text(rs,[
        "id","dataset_id","paper_id","relation_type","review_status","evidence_url"
    ])
    export_files["data/source_41_mapping.csv"]=csv_text(source_map,[
        "source_number","dataset_id","source_provider","source_url","matching_decision","paper_status"
    ])
    export_files["README.md"]=render_readme(ds,ps,rs,snapshot_date=info["snapshot_date"])
    export_files["README_EN.md"]=render_readme(ds,ps,rs,english=True,snapshot_date=info["snapshot_date"])
    export_files["docs/TOPICS.md"]=render_topics(ds)
    export_files["docs/DATASET_DETAILS.md"]=render_details(ds,ps)
    export_files["docs/PAPERS.md"]=render_papers(ps)
    export_files["docs/SOURCE_41_MAPPING.md"]=render_source_mapping(source_map,ds)
    # Maintainer documents shouldn't be overwritten on data regeneration.
    if not check:
        static={
            "CONTRIBUTING.md":render_contribute(),
            "docs/MAINTENANCE.md":render_maintenance(),
            "docs/GITHUB_UPLOAD_GUIDE_ZH.md":render_upload(),
            ".gitignore":repo_gitignore()
        }
        for name,value in static.items():
            if not (root/name).exists():
                export_files[name]=value
    changed=[]
    for path,content in export_files.items():
        target=root/path
        if check:
            if not target.exists() or target.read_text(encoding="utf-8")!=content:
                changed.append(path)
        else:
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_text(content,encoding="utf-8")
    if check and changed:
        for x in changed:
            print("OUT OF SYNC:",x)
        raise SystemExit(1)
    print(("CHECK OK" if check else "GENERATED"),len(export_files),"files; resources",len(ds),"papers",len(ps),"relations",len(rs),"source map",len(source_map))

def main():
    parser=argparse.ArgumentParser(description="Public index generator; Python 3.8+, no dependencies")
    parser.add_argument("--catalog",help="Path to local ADV-BATTERY/engine/catalog, read-only")
    parser.add_argument("--write",action="store_true",help="Regenerate metadata and Markdown files")
    parser.add_argument("--check",action="store_true",help="Verify generated artifacts match metadata")
    parser.add_argument("--root",default=str(Path(__file__).resolve().parent.parent),help="Public repository root")
    a=parser.parse_args()
    root=Path(a.root)
    info_path=root/"data/catalog_info.json"
    if info_path.exists():
        info=json.loads(info_path.read_text(encoding="utf-8"))
    else:
        info={"snapshot_date":"2026-11-06","source_of_truth":"ADV-BATTERY local catalog"}
    if a.write:
        info["snapshot_date"]=date.today().isoformat()
    if a.catalog:
        ds,ps,rs,src=read_catalog(a.catalog)
    else:
        def load(name):
            return json.loads((root/"data"/(name+".json")).read_text(encoding="utf-8"))
        ds,ps,rs=load("datasets"),load("papers"),load("relations")
        with (root/"data/source_41_mapping.csv").open(encoding="utf-8-sig",newline="") as f:
            src=list(csv.DictReader(f))
    validate(ds,ps,rs,src)
    if a.check:
        build_repo(ds,ps,rs,src,root,info,check=True)
    elif a.write:
        build_repo(ds,ps,rs,src,root,info,check=False)
    else:
        print("Use --write to generate or --check to verify. --catalog may point to original catalog.")
if __name__=="__main__":
    main()
