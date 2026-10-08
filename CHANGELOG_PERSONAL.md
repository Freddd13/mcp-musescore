# 个人开发更新日志

## MCP 桥 2.1.0 — 2026-10-08

- 基线：cab6a74；开发分支 codex/musescore-evolution。软件基线 origin/3.x 的 02346d2dd，本机 personal 0.11.0 工作未提交。本轮两边 pull 后开发，保留软件现有改动。提交定位：`feat(codex): adapt MuseScore Evolution bridge and skill`，通过 `git log --all --grep='adapt MuseScore Evolution bridge'` 查询。
- 方案：只改本项目 Python/QML/skill，未修改 MuseScore 原生源码。使用 QtWebSockets 替代软件未提供的 api.websocketserver；插件绑定 127.0.0.1:8765。向本机 0.10/0.11 的独立安装添加缺失 Qt5WebSockets.dll，先核对 SDK 与安装 Qt5Core 哈希一致，不替换已有 DLL。
- 接口：保留原 27 工具，增加 get_capabilities、get_score_data、set_tempo，共 30。保留 get_score 的 LilyPond 阅读输出，修复读谱/导航解包。增加逐音 tieForward/tieBack、tuning、veloType/veloOffset、书面时值和 ticksPerQuarter。读谱改为独立游标，不触碰乐谱选择和撤销。
- 兼容修复：TempoText 先加入谱段再设置 tempo，避免个人分支 setter 对空 segment 解引用；自定义单谱表选区按原生末谱表排除规则转换；原生 undo 不在新事务中调用。setTempo 加入 Python 批处理类型并验证原生 5–999 BPM 范围。
- 可靠性：并发请求串行配对；连接/接收超时；只读允许恢复重试，写入响应丢失不自动重放并返回 outcomeUnknown。批处理失败返回失败下标及完成数，前面成功的动作仍保留。修正 set_staff_mute 和 set_instrument_sound 的真实能力说明，未删除工具/文件。
- Codex：服务器初始化说明、Codex skill 更新、一键安装器、用户级/项目级 skill 复制、已有 skill 备份、WhatIf、Windows/Git Bash helper、探测失败退出码。保留上游 README 与 Claude 配置作为历史兼容资料，中文入口与当前能力说明置于前。
- 文档：[用户安装与操作](docs/CODEX_SETUP.md)、[实现原理与钢琴扩展方案](docs/ARCHITECTURE_AND_PIANO.md)、[shell 实测](docs/SHELL_BENCHMARK.md)，并同步软件 personal/USER_GUIDE.md 的 MCP 使用说明。
- 验证：Python 3.13 / FastMCP 4.0.11 / websockets 17.2；17 项测试通过，包含 in-memory MCP、真实 WebSocket mock、独立 Python 子进程 stdio、并发响应配对、写响应丢失不重放及超时。实际 0.10/0.11 offscreen 宿主验证 Qt 模块加载、能力读取、读谱保持选择、单谱表范围、批处理失败、撤销及速度写入；0.11 另核验实际速度图值和音符插入。skill validator、安装器 WhatIf 和实际仅环境安装通过。
- 范围：未完成用户桌面中真实乐谱的长期交互、声卡/SF2 听感或 Codex MCP App 渲染验收；原生宿主测试静音，真实网络收发用 mock 和 stdio 验证。get_score_data 的小节筛选在 Python 侧，QML 仍读全谱；密集大谱需后续分段 API。和声临时提示、演奏属性批量写入与净书定向工具是下一轮路线，尚未实现。
- 用户执行偏好：七次短任务实测 Bash 509 ms、旧 PowerShell 707 ms、pwsh 807 ms（中位）；优先 Git Bash 做 Git/文本工作，Windows 原生任务用 pwsh -NoProfile。完整任务仍需计入执行器外层开销。
- 结束复核：并发软件任务已提交 0.11.0（36c3fa12a），当前 VERSION 正在准备 0.12.0。Plugin API 与 TempoText setter 没有新的未提交修改，无需再改本轮桥接接口；0.12 新安装与长期使用尚待实际核验。软件工作保持独立，本次未混入其源码提交。
