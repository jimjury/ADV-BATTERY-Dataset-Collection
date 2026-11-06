# ADV·BATTERY — GitHub 与 V2 联动及发布指南

> 2026-11-06 配套文件。GitHub 仓库：[https://github.com/jimjury/ADV-BATTERY-Dataset-Collection](https://github.com/jimjury/ADV-BATTERY-Dataset-Collection)。
>
> **状态说明：** 本仓库上传 `docs/index.html` 并不自动意味着 GitHub Pages 已启用。只有仓库所有者在设置中首次启用 Pages 后，`https://jimjury.github.io/ADV-BATTERY-Dataset-Collection/` 才会生效。

## 双向入口

- **GitHub → V2：** 中文与英文 README 顶部的 V2 在线版链接，目标 `https://jimjury.github.io/ADV-BATTERY-Dataset-Collection/`。
- **V2 → GitHub：** 站点导航的“GitHub 目录 ↗”和页脚“投稿纠错 ↗”，都打开 `https://github.com/jimjury/ADV-BATTERY-Dataset-Collection`。
- **在线 V2 / 离线 V2：** 功能相同；浏览器收藏、笔记和个人论文只保存在浏览器本地，不在 GitHub 仓库同步。设备/网址变化时使用工作区导出/导入备份。

## 首次启用 GitHub Pages

1. 确认仓库有 `docs/index.html` 文件。
2. 访问 [GitHub Pages 设置](https://github.com/jimjury/ADV-BATTERY-Dataset-Collection/settings/pages)。
3. 在 `Build and deployment → Source` 选择 **Deploy from a branch**。
4. 在 `Branch` 选择 **main**、`Folder` 选择 **/docs**，点击 **Save**。
5. 等部署完成后打开 [https://jimjury.github.io/ADV-BATTERY-Dataset-Collection/](https://jimjury.github.io/ADV-BATTERY-Dataset-Collection/)，检查首页、数据集、论文和“GitHub 目录 ↗”链接。
6. 如果 Pages 选项不可用，请检查账号/仓库权限及 GitHub Pages 可用性；未经验证不要声称已上线。

## 日常更新

1. 在本地管理中心新增/修改候选数据，人工审核并备份。
2. 运行 `04_BUILD_HTML.bat`，重新构建本地 V2 与通用版。
3. 运行 `05_EXPORT_GITHUB.bat`，从统一正式资料库导出 `engine/exports/github_publish/`。
4. 在 GitHub Desktop 的本仓库工作副本里同步导出内容并提交，保持 `.github/`、`data/`、`docs/` 的目录结构不变。
5. 确认 Actions 中 `Validate ADV BATTERY public catalogue` 成功，确认 Pages 重建成功。
6. 依次检查 GitHub README 与线上 V2 的资源数量及双向链接。

**唯一数据源：** 只通过本地 `engine/catalog/` 维护正式资源；GitHub 表格、CSV/JSON、`docs/index.html` 都是公开导出副本。不要把第三方原始电池数据、后台草稿、API 密钥或浏览器私人笔记上传到 GitHub。

## 故障与回滚

- GitHub Actions 失败：检查 `python scripts/build_public_index.py --check` 和 `python scripts/validate_public_index.py`。
- Pages 返回 404：检查是否启用、是否选择 `main /docs` 以及 `docs/index.html` 是否存在。
- 线上与离线资源数量不一致：先运行本地构建和公开导出，再完整提交新的索引及 HTML。
- 浏览器收藏看似消失：不同 origin 不共享 localStorage，从旧 V2 导出 JSON 后，在新的 V2 导入。
- 线上回滚通过 GitHub 提交历史恢复；本地数据备份应独立保存。
