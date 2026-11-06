# GitHub 网页上传操作指南（Windows，零命令行）

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
