# 公共 GitHub 索引维护与同步 SOP

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
python scripts/build_public_index.py --catalog "D:\ADV_BATTERY\engine\catalog" --write
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
