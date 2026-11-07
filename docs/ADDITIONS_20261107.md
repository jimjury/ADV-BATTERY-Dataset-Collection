# 2026-11-07 资源补充及去重说明

[返回中文目录](../README.md) · [科研工作台](index.html)

> 本次整理了 6 个由用户提供的链接；5 条新增索引、1 条沿用原有索引。**链接数量不等于新实验数据集数量**。原始第三方数据及大文件不在本仓库托管。

| 来源 | 处理方式 | ADV·BATTERY ID | 研究类型 | 证据与局限 |
|---|---|---|---|---|
| [Zenodo 10656500](https://zenodo.org/records/10656500) | 已有资源，沿用 ID | `buaa-fault-515ev-2025` | 实车故障诊断 / SAFETY + FIELD | 2024 年数据记录（515 辆车/1820 万条），2025 年关联论文；不重复计数 |
| [NLR Battery Failure Databank](https://www.nlr.gov/transportation/battery-failure) | 新增独立数据集 | `nlr-battery-failure-databank` | 热失控/滥用测试 SAFETY | 官方工作簿标注 2024-02；未下载 XLSX 逐行核验 |
| [Zenodo 18232447](https://zenodo.org/records/18232447) | 新增独立数据集 | `rwth-thermal-runaway-literature-db` | 热失控统计 SAFETY | 1703 实验/257 文献/203 变量为关联论文报告；CSV/XLSX 与统计 JSON/MAT |
| [Sandia SNL Study](https://www.batteryarchive.org/snl_study.html) | 新增独立研究数据集入口 | `batteryarchive-snl-aging-study` | 循环退化 SOH/RUL | LFP/NCA/NMC 的长期 18650 循环研究；数据下载需遵循平台限制 |
| [BatteryArchive Cycling](https://www.batteryarchive.org/cycle_list.html?t=0001) | 新增**分类入口**，非单独实验 | `batteryarchive-cycling-directory` | 目录 SOH/RUL | 动态列表，没有已核实的独立发布年份或唯一数据 DOI |
| [BatteryArchive Disruptive](https://www.batteryarchive.org/disruptive_list.html?t=0001) | 新增**分类入口**，非单独实验 | `batteryarchive-disruptive-directory` | 目录 SAFETY | 动态列表，访问原始数据以各研究页为准 |

新关联论文（均可从 DOI 核对）：

- [The battery failure databank: Insights from an open-access database of thermal runaway behaviors of Li-ion cells and a resource for benchmarking risks](https://doi.org/10.1016/j.jpowsour.2024.234106) — Journal of Power Sources，2024。
- [Thermal Runaway in Batteries: A Database-Driven Literature Review and Exploratory Statistical Analysis](https://doi.org/10.3390/batteries12070240) — Batteries，2026。
- [Degradation of Commercial Lithium-Ion Cells as a Function of Chemistry and Cycling Conditions](https://doi.org/10.1149/1945-7111/abae37) — Journal of the Electrochemical Society，2020。

**统计口径（更新后）：** 85 条资源 = 79 个数据集 + 5 个数据门户/分类入口 + 1 个工具；111 条论文及目录记录；72 条明确关联。数据并非全都可直接下载，不等同于 85 个独立实验。

**核验状态：** 本次核验来源说明、出版物 DOI、分类性质；没有下载数十 GB 原始电池文件，没有确认每个第三方动态列表的具体记录或其可下载性。下载、使用和转引遵循原发布方条款。
