# Kumo Engrave 符头原型 0.1.0

这是基于 MakeMusic Finale Maestro 的 OFL 衍生字体。第一轮只独立重画三个常规符头，其余音乐符号保留基础字库；没有提取、描摹或重新包装 Chaconne。它是可供同曲评审的原型，尚未定稿。

## 四种家族

| 目录 | 音乐字体 | 用途 |
| --- | --- | --- |
| `control/` | Kumo Engrave Control | 只改名称，不改轮廓、字宽或锚点，排除构建与加载误差 |
| `balanced/` | Kumo Engrave | 常规实心、半音符、全音符的四段三次贝塞尔椭圆轮廓 |
| `open/` | Kumo Engrave Open | 外轮廓与 balanced 相同，半／全音符内孔纵向参数增大 12% |
| `jp/` | Kumo Engrave JP | 当前主方向：依据 Chaconne Ex 官方公开样本观察，独立设计更饱满的黑符头、较通透的半符头、外平内斜的全符头 |

保留每个字的 advance、side bearing，以及常规符头上下符干接点。外框按实际构建轮廓回写 JSON；光学切出区域和分叉符干锚点随新轮廓调整。普通黑符头和空心符头的倾角、内孔倾角分别设计；仅调内孔可以改变黑白关系而不扩大外轮廓。这些是可控设计变量，不代表已获用户认可或已经接近目标字体。

基础覆盖为音乐字体 **2745** 字、Text 字体 **373** 字。其他符头（交叉、菱形、超长时值等）、谱号、变音记号、休止、旗尾、力度尚未重新设计。符干、符杠、弧线和系统分页由 MuseScore 与谱面样式决定，不能靠换这三个符头解决。

## 现在怎样试用

适用于支持私有 Score Fonts 的个人 MuseScore 3 Evolution 分支；不照搬 MuseScore 4 的安装路径。**当前主试用候选为 Kumo Engrave JP；只选择新的音乐符号字体，音乐 Text 继续用内置 `Finale Maestro Text`。** [设计依据与范围](DESIGN_BRIEF.md)单独记录。

1. 构建或取得 `dist/kumo-engrave-0.1.0-prototypes.zip`，解压到一个新目录。
2. 在 Evolution **编辑 → 偏好设置 → 通用／路径** 查看／指定 Score Fonts（乐谱字体）目录。将 `jp/Kumo Engrave JP` 完整子文件夹复制进去；文件夹名、OTF 和 JSON 的基本名称必须相同。可选复制其他三个音乐家族用于对照。不需安装进 Windows 字体目录，也不需要 MCP 或 skill。
3. 重启 Evolution；打开乐谱的**独立副本**。进入 **格式 → 样式 → 乐谱**，音乐符号字体选 `Kumo Engrave JP`，音乐 Text 字体选 `Finale Maestro Text`。界面的译名可能因语言版本不同。
4. 第一轮关闭“使用所选字体的推荐样式／自动优化样式”选项，只换字体。保留现有谱距、页边距、符杠、弧线等参数。导出／打印副本比较，勿覆盖原谱。
5. 恢复时把副本的音乐符号字体改回原家族；不必删除任何字体。发送 MSCZ 给其他电脑时另附字体包，否则可能回退。

**配套 Text 的已知限制：** 包内保留各家族的改名 Text OTF／JSON，供后续兼容试验。Maestro Text 原字库缺少 `dynamicMezzo`（U+E521）；Evolution `libmscore/sym.cpp` 为 `Finale Maestro Text` 配置 Leland Text 回退，而改名家族没有这条规则。`TextFragment::font()` 遇到缺字还会回退到 Bravura Text。实测改名对照的 mf／mp 等字形及间距因此变化，可能牵动布局。Text 文件“注册成功”不等于混排完全等效；暂不把改名 Text 作为默认搭配。后续优先在字体层补齐所需码位／组合测试，只有必要时才考虑通用回退接口，不添加硬编码私人家族名。

## 构建与检查

代码使用 Python 3.7+、fontTools 4.38.0；本机可用 `C:\software\miniconda3\python.exe`，无需改现有环境。新环境运行 `python -m pip install -r fonts/kumo-engrave/requirements.txt`。

```powershell
python fonts/kumo-engrave/build.py
python fonts/kumo-engrave/validate.py
python fonts/kumo-engrave/build.py --package-only
```

第一步生成 `dist/`；第二步检查所有字形覆盖、轮廓变化范围、hmtx／CFF 字宽、SMuFL 外框与普通接杆锚点；第三步将最新报告和安装说明打包，核验报告中的 OTF 哈希与当前文件一致。`dist/` 是可再生目录，不提交生成二进制。Git 仓库保存固定基础 OTF、许可和 SHA-256、可编辑参数、构建脚本与测试谱。局部 `.gitattributes` 禁止对 vendor 底本做换行转换／文本差异检查，保留原 JSON 的空白和原字节；自有源码使用 LF。不要移动／重置底本文件来“修复”哈希失败，应先确认来源。

编辑 `source/design.json` 可改外轮廓盒、倾斜和空心孔尺寸。`build.py` 保留未修改 CFF CharStrings，不整体描摹或转曲重编字库；重新编码符头时正确减去 Type 2 的 nominalWidthX，避免显示正常却字宽错误。家族／Full／PostScript／版本名称同时更新，不使用 OFL 保留名称命名衍生字体。

## 原生谱例验证

```powershell
python fonts/kumo-engrave/render_proofs.py --musescore "路径\MuseScore3Evo.exe" --output "全新的输出目录" --score "只读原谱.mscz"
python fonts/kumo-engrave/review_proofs.py "上述输出目录"
```

`render_proofs.py` 使用 Windows Qt 原生渲染、静音独立配置和私有字体目录，导出 PNG／SVG；只在生成副本中更改两个字体样式项。默认 `--text-mode fixed` 保持所有样本的 `Finale Maestro Text`，使对照只反映符头。加 `--text-mode paired` 可复现改名 Text 的回退差异。脚本拒绝复用已有输出目录，以保留此前结果；不改全局字体、用户配置或原谱。

`review_proofs.py` 另外需要 Pillow（本机 Codex bundled Python 已有）。比较前先合成白纸，避免把透明像素的不可见 RGB 差异当成字体差异。固定 Text 模式要求原版与只改名 Control 的每一页像素完全相同。

自写 8 小节测试谱覆盖线上／线间、加线、上下接杆、和弦、空心长音、16 分连梁、装饰音、附点与延音、多声部、变音和 mf／pp。用户谱的隔离副本补充跨谱表、32 分音符、密集和弦及第 148–149 小节四谱表压力情境。测试谱已检查每个 4/4 小节的时值及多声部游标。未来仍需专项二度／分叉接杆及不同缩放渲染回归，不能用全页浏览代替所有连接检查。

## 验收记录与下一轮

2026-10-09，在本机 0.17 宿主上验证实际注册与原生输出；保持 Text 后，对照结果见 [验证记录](VERIFICATION.md)。用户原 MSCZ／PDF 只读，哈希检查不变。Maestro、Control、三个候选（含 JP）都输出 9 页。页数相同不足以证明每一处布局相同。用户原 PDF 的 8 页来自另一次已有样式渲染，不能当成同宿主字体对照。

以后更新字体不需重装／重新配置 MCP 或 skill。字体 OTF 与 JSON 应成对更新到私有目录并重启 Evolution；先备份旧家族目录，试验副本保留明确版本。换到新家族名时再在副本选择该家族。MCP 本身更新的步骤仍以项目 Codex 安装文档为准。

尚未完成：用户审美评审、真实打印、F2 谱号等重画、配套 Text 缺字修复，以及推荐 MSS 参数定稿。当前推荐候选不自动安装／应用到原谱。先在实际谱距下选外轮廓及空心孔方向，再扩展符号，避免改完一套后才发现符头不合偏好。

## 许可与来源

字体按 **SIL OFL 1.1** 分发；基础版权／保留名称与完整许可在 `vendor/OFL.txt` 和每个分发家族的 `OFL.txt`。新增轮廓 Copyright 2026 Freddd13。源码采用本项目 MIT 许可，字体资产继续适用 OFL，不被 MIT 替代。

来源及固定版本见 `BASELINE.json`。基础资产来自 Freddd13/MuseScore 的 MakeMusic 字体目录；厂家合法公开来源见 [MakeMusic 字体与许可说明](https://makemusic.zendesk.com/hc/en-us/articles/1500013053461-MakeMusic-Fonts-and-Licensing-Information)。Chaconne 仅用于视觉风格讨论；本包不包含其文件、轮廓或元数据。

完整方向见 [字体计划](../../docs/FONT_PLAN.md)；净书线提供情境和阅读规则，见 [净书计划](../../docs/ENGRAVING_PLAN.md)。
