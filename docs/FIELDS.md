# 公开数据字段说明 / Metadata schema

本项目的机器可读文件位于 `data/`，为 ADV·BATTERY 本地正式资料库的**公开白名单导出**。

| 文件 | 内容 | 关键字段 |
|---|---|---|
| `datasets.json` / `.csv` | 资源条目（当前 80 条） | `id`, `name_zh`, `name_en`, `year`, `institution`, `resource_type`, `research_tags`, `source_url`, `access_url`, `dataset_doi`, `related_paper_ids` |
| `papers.json` / `.csv` | 文献及目录记录（当前 108 条） | `id`, `title`, `journal_or_source`, `doi`, `url`, `record_type`, `linked_dataset_ids` |
| `relations.json` / `.csv` | 登记关系（当前 69 条） | `dataset_id`, `paper_id`, `relation_type`, `review_status`, `evidence_url` |
| `source_41_mapping.csv` | 原 41 条社区汇编的去重对应关系 | `source_number`, `dataset_id`, `matching_decision`, `source_url` |

这些条数描述的是 **2026-11-06 初始快照**；后续更新请以 `data/catalog_info.json` 和 README 动态统计为准。

## 重要字段解释

- **`id`**：ADV·BATTERY 的稳定资源 ID；更新时不要随意改动。
- **`resource_type`**：`dataset`、`portal`、`tool`。**80 条资源不等于 80 份实验数据文件**。
- **`research_tags`**：原资料库已有的 8 类研究方向标签；多标签可以并存。
- **`source_url`**：原始信息发布页；**`access_url`**：获取数据的入口，可能也是元数据页、网盘、项目入口，并不保证直链下载。
- **`dataset_doi`**：数据集自身的 DOI（可空）；不得与论文 DOI 混淆。
- **`license_as_recorded`**：资料库登记的来源许可文字，未经本 GitHub 包全面法律核验；实际使用遵守原发布方条款。
- **`source_catalog_status`**、**`download_catalog_status`**：原资料库记录状态，不是第三方网站的实时在线证明。
- **`related_paper_ids`**：正式资料库中登记的直接关联 ID，可能包括数据集正式记录而非论文。
- **`source_41_index`**：若本条匹配来自 [41 条社区目录](https://github.com/PythoniLover/battery-dataset-collection)，则记录原序号，否则为空。

**未知值允许留空，不能依据题目推测温度、容量、倍率或数据字段。**

## 维护

直接修改 GitHub 快照只影响公开索引，不会同步至两版离线 HTML。推荐先在本地审核资料库，再执行：

```powershell
python scripts/build_public_index.py --catalog "D:\ADV_BATTERY\engine\catalog" --write
python scripts/validate_public_index.py
python scripts/build_public_index.py --check
```
