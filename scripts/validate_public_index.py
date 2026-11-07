#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate the public battery dataset index. Python 3.8+, standard library only."""
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit
from build_public_index import TAGS, validate, clean_url
from readme_locales import LOCALES, LANGUAGE_LINKS

ROOT=Path(__file__).resolve().parent.parent

def read_json(name):
    return json.loads((ROOT/"data"/(name+".json")).read_text(encoding="utf-8"))

def assert_file_links(path):
    text=path.read_text(encoding="utf-8")
    # Only local Markdown links: [label](relative/path#anchor). External links use <...>.
    candidates=re.findall(r"\]\(([^()<>\n]+)\)",text)
    checked=0
    for link in candidates:
        if link.startswith(("#","https://","http://","mailto:")):
            continue
        part,_,anchor=link.partition("#")
        target=(path.parent/part).resolve()
        assert target.is_relative_to(ROOT.resolve()) if hasattr(target,"is_relative_to") else str(target).startswith(str(ROOT.resolve())), (path,link)
        assert target.is_file(), (path,link,"target missing")
        if anchor and part.endswith("TOPICS.md"):
            assert anchor.upper() in TAGS,(path,link,"bad topic anchor")
        if anchor and part.endswith("DATASET_DETAILS.md"):
            assert re.fullmatch(r"dataset-[0-9]+",anchor),(path,link,"bad dataset anchor")
        checked+=1
    return checked

def main():
    ds,ps,rs=read_json("datasets"),read_json("papers"),read_json("relations")
    with (ROOT/"data/source_41_mapping.csv").open(encoding="utf-8-sig",newline="") as f:
        src=list(csv.DictReader(f))
    validate(ds,ps,rs,src)
    for name,rows in (("datasets",ds),("papers",ps),("relations",rs)):
        with (ROOT/"data"/(name+".csv")).open(encoding="utf-8-sig",newline="") as f:
            cr=list(csv.DictReader(f))
        assert len(cr)==len(rows), (name,"CSV / JSON row count mismatch")
    info=read_json("catalog_info")
    assert info["resource_count"]==len(ds)
    assert info["publication_record_count"]==len(ps)
    assert info["explicit_relation_count"]==len(rs)
    assert info["source_mapping_count"]==len(src)
    bytype=Counter(d["resource_type"] for d in ds)
    assert set(bytype).issubset({"dataset","portal","tool"}),bytype
    assert info["dataset_count"]==bytype["dataset"]
    assert info["portal_count"]==bytype["portal"]
    assert info["tool_count"]==bytype["tool"]
    readme=(ROOT/"README.md").read_text("utf-8")
    readme_en=(ROOT/"README_EN.md").read_text("utf-8")
    details=(ROOT/"docs/DATASET_DETAILS.md").read_text("utf-8")
    topics=(ROOT/"docs/TOPICS.md").read_text("utf-8")
    papers_md=(ROOT/"docs/PAPERS.md").read_text("utf-8")
    localized=[(ROOT/f"README_{locale}.md").read_text("utf-8") for locale in LOCALES]
    for txt in [readme,readme_en,*localized]:
        for _,language_path in LANGUAGE_LINKS:
            assert "]("+language_path+")" in txt, ("language link missing",language_path)
        count=len(re.findall(r"^\| \d{2,} \|",txt,flags=re.M))
        assert count==len(ds),("README table entries",count,len(ds))
    assert len(re.findall(r'<a id="dataset-\d{2,}"></a>',details))==len(ds)
    assert len(re.findall(r"^\| \d{3} \|",papers_md,flags=re.M))==len(ps)
    for k in TAGS:
        assert re.search(r"^## "+re.escape(k)+r"$",topics,flags=re.M), ("missing topic",k)
    paths=list(ROOT.rglob("*"))
    assert not any(p.is_symlink() for p in paths),"Unexpected symlink in public repo"
    prohibited={"engine","staging","history","releases","inputs","baseline","operator_backups"}
    assert not any(p.is_dir() and p.name in prohibited for p in paths),"Private directory detected"
    banned_ext={".pdf",".xlsx",".xls",".zip",".rar",".7z",".p12",".pem",".db",".sqlite3"}
    assert not any(p.is_file() and p.suffix.lower() in banned_ext for p in paths),"Forbidden file type"
    for name in ["README.md","README_EN.md","NOTICE.md","CONTRIBUTING.md","data/datasets.json","data/papers.json","data/relations.json","docs/GITHUB_UPLOAD_GUIDE_ZH.md",".github/workflows/validate.yml"]:
        assert (ROOT/name).is_file(),("Missing essential file",name)
    source=(ROOT/"data/datasets.json").read_text(encoding="utf-8")
    for dangerous in [r"F:\\Anaconda",r"C:\\Users\\",r"ghp_[a-zA-Z0-9]{20,}",r"sk-[a-zA-Z0-9]{20,}",r'"password"\s*:\s*"[^"]+']:
        assert not re.search(dangerous,source,re.I),("Sensitive data pattern",dangerous)
    # All data entry links are HTTP(S) and have no credential query keys.
    assert all(clean_url(d["source_url"]) and clean_url(d["access_url"]) for d in ds)
    mdcount=0
    for path in list(ROOT.glob("*.md")) + list((ROOT/"docs").glob("*.md")):
        mdcount+=assert_file_links(path)
    print("PUBLIC CATALOGUE PASS")
    print("resources",len(ds),"datasets",bytype["dataset"],"portals",bytype["portal"],"tools",bytype["tool"])
    print("publication/catalogue records",len(ps),"explicit relations",len(rs),"source mappings",len(src))
    print("local Markdown links checked:",mdcount)
    print("Sensitive/private-file and URL-scheme checks: PASS")
if __name__=="__main__":
    main()
