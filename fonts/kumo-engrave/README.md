# Kumo Piano EX 音乐字体草案 0.3.0

**当前候选为 `Kumo Piano EX`：用户已否定0.2过细、不像目标的观感；0.3直接对照Chaconne Ex官方字形修订。** 新版仍基于Leland 0.80，旧Kumo Piano和Maestro原型保留。相对0.2重改26个轮廓，见 [直接字形对照](EX_REDRAW.md)。 按用户要求，以实际 Animenz 官谱为视觉参考，独立绘制 38 个常用字形：三种符头、G/F 谱号、七种休止、五种变音、四种旗尾、四种琶音、附点、十种上下发音符号、两种上下延长号。其余字形沿用 Leland。参考扩展到 14 份谱子的 33 页，出处与设计决定见 [ANIMENZ_REFERENCE.md](ANIMENZ_REFERENCE.md)。没有提取、描摹或重新包装 Chaconne。

这是可安装评审的造型草案；原生加载、字库与连接测试通过，不代表已经与官谱接近或获得审美认可。真实打印和更多共享符头／组合记号验收仍待完成。

## 七种家族

| 目录 | 音乐字体 | 用途 |
| --- | --- | --- |
| `ex/` | **Kumo Piano EX** | 当前0.3：直接观察Chaconne Ex，修正头型和粗细层次 |
| `piano/` | Kumo Piano | 被用户否定的0.2造型，保留作对照 |
| `leland-control/` | Kumo Piano Control | Leland 只改名，用于与新版保持相同宿主名称分支的对照 |
| `control/` | Kumo Engrave Control | 只改名称，不改轮廓、字宽或锚点，排除构建与加载误差 |
| `balanced/` | Kumo Engrave | 常规实心、半音符、全音符的四段三次贝塞尔椭圆轮廓 |
| `open/` | Kumo Engrave Open | 外轮廓与 balanced 相同，半／全音符内孔纵向参数增大 12% |
| `jp/` | Kumo Engrave JP | 旧版方向：Maestro 底库，仅三种符头；依据 Ex 官方样本观察 |

除EX全音符 advance 从373改为438单位，其余字宽、side bearing和常规符头上下符干接点保留。外框按实际构建轮廓回写 JSON；光学切出区域和分叉符干锚点随新轮廓调整。普通黑符头和空心符头的倾角、内孔倾角分别设计；仅调内孔可以改变黑白关系而不扩大外轮廓。这些是可控设计变量，不代表已获用户认可或已经接近目标字体。

新版完整保留 Leland 的音乐 **493** 字、Text **182** 字；旧 Maestro 家族保留 2745/373 字。两套底库覆盖不同，没有把旧 Maestro 全字库混入新版。交叉／菱形等特殊符头、32/64 分旗尾、踏板、装饰符号、力度、数字和组合发音等仍沿用 Leland；少见缺字依宿主回退。符干、符杠、弧线和系统分页主要由 MuseScore 与谱面样式决定。

## 现在怎样试用

适用于支持私有 Score Fonts 的个人 MuseScore 3 Evolution 分支；不照搬 MuseScore 4 的安装路径。**当前试用选 `Kumo Piano EX`，音乐 Text 保持内置 `Leland Text`。** 包内改名 Text（含 `Kumo Piano EX Text`）仍作兼容试验：0.2常用测试谱曾一致，但用户谱有混排差异；EX本轮也未新增配套Text全谱等价验证，暂不作为默认搭配。

1. 构建或取得 `dist/v03/kumo-engrave-0.3.0-prototypes.zip`，解压到一个新目录；旧 0.1/0.2 包保留。
2. 在 Evolution **编辑 → 偏好设置 → 通用／路径** 查看／指定 Score Fonts（乐谱字体）目录。将 `ex/Kumo Piano EX` 与 `ex/Kumo Piano EX Text` 两个完整子文件夹复制进去；文件夹名、OTF 和 JSON 的基本名称必须相同。可选复制 `leland-control/` 中两个家族用于对照。不需安装进 Windows 字体目录，也不需要 MCP 或 skill。
3. 重启 Evolution；打开乐谱的**独立副本**。进入 **格式 → 样式 → 乐谱**，音乐符号字体选 `Kumo Piano EX`，音乐 Text 字体选内置 `Leland Text`。界面的译名可能因语言版本不同。
4. 第一轮关闭“使用所选字体的推荐样式／自动优化样式”选项，只换字体。保留现有谱距、页边距、符杠、弧线等参数。导出／打印副本比较，勿覆盖原谱。
5. 恢复时把副本的音乐符号字体改回原家族；不必删除任何字体。发送 MSCZ 给其他电脑时另附字体包，否则可能回退。

**旧 Maestro 家族的 Text 限制仍保留：** Maestro Text 缺少 `dynamicMezzo` U+E521，改名后没有内置家族的 Qt 替代规则。旧 JP/Open/Balanced 仍应搭配内置 `Finale Maestro Text`。新版 Leland Text 底库含 mezzo；并非通过修改本体或为私人家族写回退规则解决。

**宿主名称特判：** `bracket.cpp` 只对精确名称 `Leland` 限制大括号最大跨谱表数为 4、调整普通括号端部伸出。用户谱含 6 个 Staff，只改名的 Control 也可能从 8 页变 9 页；前 3 页及整个双谱表测试谱完全相同。评价新字形应与 `Kumo Piano Control` 比较，不能把内置 Leland 与改名字体的整页差异全部归因轮廓。已通知净书线，本轮不修改本体。

## 构建与检查

代码使用 Python 3.7+、fontTools 4.38.0；本机可用 `C:\software\miniconda3\python.exe`，无需改现有环境。新环境运行 `python -m pip install -r fonts/kumo-engrave/requirements.txt`。

```powershell
python fonts/kumo-engrave/build.py --output fonts/kumo-engrave/dist/v03
python fonts/kumo-engrave/validate.py --output fonts/kumo-engrave/dist/v03
python fonts/kumo-engrave/build.py --output fonts/kumo-engrave/dist/v03 --package-only
```

第一步生成 `dist/v03/`；第二步检查所有字形覆盖、轮廓变化范围、hmtx／CFF 字宽、SMuFL 外框与普通接杆锚点；第三步将最新报告和安装说明打包，核验报告中的 OTF 哈希与当前文件一致。`dist/` 是可再生目录，不提交生成二进制。Git 仓库保存固定基础 OTF、许可和 SHA-256、可编辑参数、构建脚本与测试谱。局部 `.gitattributes` 禁止对 vendor 底本做换行转换／文本差异检查，保留原 JSON 的空白和原字节；自有源码使用 LF。不要移动／重置底本文件来“修复”哈希失败，应先确认来源。

编辑 `source/design.json` 可改符头外框、倾斜和空心孔尺寸；旧 `source/piano_palette.py` 与新版 `source/ex_palette.py` 保存可编辑曲线／多边形与可变宽带。`build.py` 保留未修改 CFF CharStrings，不整体转曲重编字库；重新编码时正确减去 Type 2 的 nominalWidthX。Leland 基础文件与许可哈希固定在 `LELAND_BASELINE.json`，原 FONTLOG 随包保留并追加本轮变更。

## 原生谱例验证

```powershell
python fonts/kumo-engrave/render_proofs.py --musescore "路径\MuseScore3Evo.exe" --output "全新的输出目录" --score "只读原谱.mscz" --fonts fonts/kumo-engrave/dist/v03 --profiles leland-control,piano,ex --fixture fonts/kumo-engrave/fixtures/piano-palette.musicxml --fixed-text "Leland Text"
python fonts/kumo-engrave/review_ex.py --proofs "上述输出目录" --fonts fonts/kumo-engrave/dist/v03 --output fonts/kumo-engrave/dist/review-0.3
```

`render_proofs.py` 使用 Windows Qt 原生渲染、静音独立配置和私有字体目录，导出 PNG／SVG；只在生成副本中更改两个字体样式项。上述命令固定内置 `Leland Text`，隔离新版音乐字形的变化。不传 `--fixed-text` 时仍使用旧 Maestro 试验的默认 Text；新版应明确指定。加 `--text-mode paired` 可复现改名 Text 的混排差异。脚本拒绝复用已有输出目录，以保留此前结果；不改全局字体、用户配置或原谱。

`review_proofs.py` 另外需要 Pillow（本机 Codex bundled Python 已有）。比较前先合成白纸，避免把透明像素的不可见 RGB 差异当成字体差异。固定 Text 模式要求双谱表测试谱的内置字体与改名 Control 像素相同；完整用户谱逐页记录差异，并结合宿主名称分支分析，不能要求所有改名家族无条件同页。

自写 8 小节测试谱覆盖线上／线间、加线、上下接杆、和弦、空心长音、16 分连梁、装饰音、附点与延音、多声部、变音和 mf／pp。用户谱的隔离副本补充跨谱表、32 分音符、密集和弦及第 148–149 小节四谱表压力情境。测试谱已检查每个 4/4 小节的时值及多声部游标。未来仍需专项二度／分叉接杆及不同缩放渲染回归，不能用全页浏览代替所有连接检查。

## 验收记录与下一轮

2026-10-09，在本机 0.17 宿主上验证实际注册与原生输出；保持 Text 后，对照结果见 [验证记录](VERIFICATION.md)。用户原 MSCZ／PDF 只读，哈希检查不变。Maestro、Control、三个候选（含 JP）都输出 9 页。页数相同不足以证明每一处布局相同。用户原 PDF 的 8 页来自另一次已有样式渲染，不能当成同宿主字体对照。

以后更新字体不需重装／重新配置 MCP 或 skill。字体 OTF 与 JSON 应成对更新到私有目录并重启 Evolution；先备份旧家族目录，试验副本保留明确版本。换到新家族名时再在副本选择该家族。MCP 本身更新的步骤仍以项目 Codex 安装文档为准。

0.2 新增自写 20 小节测试谱 `fixtures/piano-palette.musicxml`，覆盖休止系列、上下旗尾、无／上／下方向琶音、发音、延长号、踏板、mf/mp 与密集变音和弦。用 `--fixture` 选择；`--profiles leland-control,piano --fixed-text "Leland Text"` 隔离音乐字形，`--text-mode paired` 单独验收配套 Text。详见 [验证记录](VERIFICATION.md)。

0.3的两张本机评审图在 `dist/review-0.3/`，可直接看图，无须先安装。新增原生复核命令见 [直接字形对照](EX_REDRAW.md)，详细证据见 [验证记录](VERIFICATION.md)。

尚未完成：本轮用户审美评审、真实打印、踏板／装饰符号／力度／数字及组合发音重画、共享符头专项，以及推荐 MSS 参数定稿。当前草案不自动安装／应用到原谱。

## 许可与来源

字体按 **SIL OFL 1.1** 分发；基础版权／保留名称与完整许可在 `vendor/OFL.txt` 和每个分发家族的 `OFL.txt`。新增轮廓 Copyright 2026 Freddd13。源码采用本项目 MIT 许可，字体资产继续适用 OFL，不被 MIT 替代。

来源及固定版本见 `BASELINE.json`。基础资产来自 Freddd13/MuseScore 的 MakeMusic 字体目录；厂家合法公开来源见 [MakeMusic 字体与许可说明](https://makemusic.zendesk.com/hc/en-us/articles/1500013053461-MakeMusic-Fonts-and-Licensing-Information)。Chaconne 仅用于视觉风格讨论；本包不包含其文件、轮廓或元数据。

新版底库来源和 SHA-256 见 `LELAND_BASELINE.json`，Leland 原版权、OFL 许可及保留名称记录在 `vendor/leland/LICENSE.txt`。两个底库的许可分别随所属家族分发；新家族名是 Kumo Piano。

完整方向见 [字体计划](../../docs/FONT_PLAN.md)；净书线提供情境和阅读规则，见 [净书计划](../../docs/ENGRAVING_PLAN.md)。
