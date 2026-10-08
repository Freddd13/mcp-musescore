# Shell 效率：2026-10-08

用户要求尝试 Git Bash，并按本机实测选择后续工具。每种 shell 七次独立启动，禁用 profile，运行同样的 `git status --porcelain` 与 `rg --files`，丢弃标准输出；用 .NET Stopwatch 测进程完整耗时。

| Shell | 路径 | 中位 ms | 平均 ms |
| --- | --- | ---: | ---: |
| Git Bash | E:\Git\bin\bash.exe | 509.1 | 569.9 |
| Windows PowerShell | C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe | 706.9 | 714.2 |
| pwsh | C:\Program Files\PowerShell\7\pwsh.exe | 807.4 | 819.6 |

样本 ms：Bash `[1003.5,487.8,472.6,509.1,514.8,489.4,512.1]`；旧 PowerShell `[781.1,701.6,690.0,723.7,754.3,706.9,641.7]`；pwsh `[807.4,788.3,781.7,780.7,814.9,869.6,894.8]`。首轮冷启动、缓存与安全软件会影响结果，故使用中位数比较。Bash 比旧 PowerShell 中位约快 28%，比 pwsh 约快 37%。这不包括执行工具自身调度开销，也不证明长编译/下载/Windows API 操作一定更快。

后续 Git 和文本工作优先 Git Bash，Windows 原生文件/进程/安装用 pwsh -NoProfile。当前执行器直接指定 Bash 会误调用 WSL；可从无 profile 的 PowerShell 明确调用 `E:\Git\bin\bash.exe --noprofile --norc`。这会增加外层启动开销，应按完整任务观察；不为 shell 选择修改 WSL 系统配置。无 profile 环境需要 Unix 工具时可将 `/usr/bin` 加入该 Bash 进程的 PATH。
