# 贡献指南 / Contributing to ADV·BATTERY

[简体中文](README.md) · [English](README_EN.md) · [日本語](README_JA.md) · [한국어](README_KO.md) · [Español](README_ES.md) · [Deutsch](README_DE.md) · [Français](README_FR.md)

## 中文：如何提交建议

欢迎报告失效链接、错误 DOI、遗漏数据集、缺失的论文关联、错误的实验条件、标签问题，以及多语言翻译问题。可以通过 [Issues](https://github.com/jimjury/ADV-BATTERY-Dataset-Collection/issues) 提交。

建议提供：

1. 数据集名称（中/英文均可）、发布机构以及**原始数据源链接**。
2. 原始数据访问或下载入口，并说明是否需注册、申请或付费。
3. DOI（如官方提供；不确定请留空，**不要猜测**）。
4. 关联论文的准确标题、DOI / 正式出版页，以及明确的关联依据。
5. 电池体系、容量、温度、倍率、采样时间、故障类别等实验条件的原始依据；不确定项注明未核验。
6. 官方许可和访问限制，或明确写出“尚未核验”。

不同记录的重复判断优先使用稳定 ID、数据集 DOI、原始数据地址及版本信息；相似标题只能作为疑似重复，不得直接合并不同版本。

**安全事项：** 不要在 Issue/PR 中提交账号密码、cookie、token、带密钥的共享链接、个人数据、未经许可的论文 PDF 或第三方实验原始数据文件。新增资源必须经过人工审核；创建 Issue 不会自动更新目录。

## English: how to contribute

We welcome reports of broken URLs, incorrect DOIs, missing datasets, incomplete dataset–paper links, unsupported experimental claims, wrong topic labels and translation mistakes. Open an [Issue](https://github.com/jimjury/ADV-BATTERY-Dataset-Collection/issues) or propose a pull request.

For a new dataset or correction, please provide:

1. **Official dataset title, provider/institution, and primary source URL.**
2. Access or download URL, indicating whether registration, approval or payment is required.
3. Dataset DOI **only if documented by the original provider**; never fabricate a DOI.
4. Associated publication title, DOI or publisher page, and evidence connecting it to the dataset.
5. Source-backed battery chemistry, capacity, temperature, C-rate, sampling interval or fault labels where available. Mark unknown information as unverified.
6. Licensing and redistribution restrictions, or explicitly state that they have not been checked.

Deduplication is based on stable identifiers, canonical DOIs, original source URLs and version metadata. Similar titles alone are insufficient to merge distinct records.

**Security and copyright:** Do not submit secrets, credentials, tokenized URLs, personal data, unauthorized research PDFs or raw third-party datasets. New entries require human review; opening an Issue does not automatically change the official catalogue.

## 翻译维护 / Translation maintenance

Seven language-specific README files are generated automatically from one public data catalogue. For terminology corrections, edit the human-facing text in [`scripts/readme_locales.py`](scripts/readme_locales.py), not dataset IDs or source links. See the [localization guide](docs/I18N.md).

Maintainers should review proposed entries in the original ADV·BATTERY catalogue, regenerate the public index, run the validation scripts and test both website versions when resource data changes. See [`docs/MAINTENANCE.md`](docs/MAINTENANCE.md).
