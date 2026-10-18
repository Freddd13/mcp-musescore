# 本机研究材料的位置

2026-10-18按用户要求，将本对话旧临时目录迁到E盘项目内。原谱和书籍仍从用户提供的OneDrive位置只读，不迁移原件。

| 材料 | 当前位置 |
| --- | --- |
| 2026-10-08至10-10的渲染、试验、教材图页、脚本 | `E:\programming\funcodes\mcp-musescore\tmp\engraving\legacy-2026-10-08` |
| 146份官谱的页面渲染和阅读辅助文本 | `E:\programming\funcodes\mcp-musescore\tmp\engraving\corpus\A编号` |
| 迁移逐文件记录 | `tmp/engraving/cache-migration.json` |

旧路径前缀 `C:\Users\Fred\.codex\visualizations\2026\10\08\01a11a5f-d840-7eb3-84c2-39e9d493a830` 对应上表的legacy目录。历史JSON、命令日志、旧脚本保留当时路径作为证据；查找旧图时替换此前缀即可，不重新执行会写C盘的旧脚本。当前文档中的图集入口已改为E盘。

迁移核查：685个文件、133,438,772字节，逐文件SHA-256一致，原C盘任务目录已不存在。本机完整清单保留在迁移记录中。此结论仅覆盖本对话该目录；其它任务和运行时公共依赖不属于本次缓存。

新临时数据统一使用`tmp/engraving/`，该目录被Git忽略，避免把书页和参考谱渲染提交到仓库。Python使用`-B`并将TEMP/TMP指向这里。跨电脑复查可用[只读准备脚本](../../tools/engraving/corpus.py)重新渲染；生成图不等于完成阅读。
