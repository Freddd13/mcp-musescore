# 个人出版风格音乐字体计划

更新日期：2026-10-08。状态：**计划已确定，供分支对话推进；尚未制作或安装个人字体。**

本对话当前执行的是 [钢琴净书研究线](ENGRAVING_PLAN.md)，不是字体实现。本文件保留已确认的字体决定和交接材料；后续字体对话更新本文件的状态、结果与下一步。

## 1. 已确认的目标与边界

用户喜欢 Animenz 新官谱的 Chaconne 风格，并选择开发个人字体：**以开放授权的 Finale Maestro 为底，保留完整字库，先独立设计常规符头，再渐进扩展常用字形。**

暂用独立家族名 `Kumo Engrave`，配套文本音乐字体为 `Kumo Engrave Text`；发布前核查命名冲突，不复用保留名称。目标是符合用户偏好的出版谱视觉语言，不承诺复制 Chaconne，也不宣称字体本身能够完成净书。

- 参考 PDF 只用于观察比例、黑白关系、印刷效果和上下文表现。不提取、描摹或重新包装其嵌入 Chaconne 字形。
- 不修改用户 PDF、MSCZ、现有内置字体、全局字体或当前 MuseScore 设置。试验使用独立字体家族、独立配置和工程副本。
- 先保留基础字库覆盖，渐进替换批准进入试验的字形，不从零重做完整字库。
- 不将字体名称替换与整套默认样式重置混为同一操作；后者可能覆盖用户已有调整。

## 2. 字体调查与合法来源

| 字体 | 已核查事实 | 本线用途 |
| --- | --- | --- |
| Chaconne | 主要新官谱样本嵌入字体名称已确认；并非所有年代样本都相同 | 审美参考，不作为字体文件来源 |
| Chaconne Ex | 官方定位为 SMuFL 后继，支持 OTF／Windows；2026-10-08 查看官方商店标价 16,500 日元 | 可购买的参考候选，当前未取得或测试，不保证与旧版字形完全相同 |
| Finale Maestro／Text | Evolution 已内置，厂家公开 OFL 许可及免费安装包 | 本计划基础字体与现成对照 |
| Sebastian | 作者提供字体、SMuFL JSON 和 UFO 源，OFL 许可 | 独立研究对照，不预先判定为最接近 Chaconne |
| Bravura | SMuFL 参考字体，开放授权，外观偏厚重 | 覆盖与机制对照，不因它是 Dorico 默认字体就视为目标答案 |

来源：

- [Chaconne Ex 产品](https://chaconne-ex.stonemusic.jp/)、[官方商店](https://stonemusic.stores.jp/items/67176151ce1b810155a57f25)、[官方支持](https://www.stonemusic.jp/chaconne-ex-support/)。价格、版本与许可在真正采用时重新核查；目前没有确认获授权的免费 Chaconne 分享。
- [MakeMusic 字体许可和安装包](https://makemusic.zendesk.com/hc/en-us/articles/1500013053461-MakeMusic-Fonts-and-Licensing-Information)。页面提供 Windows MMFonts.msi；本机 Evolution 试用 Finale Maestro 无需先安装另一个软件。
- [Sebastian 作者仓库](https://github.com/fkretlow/sebastian)、[发布页](https://github.com/fkretlow/sebastian/releases)。
- [Bravura 官方仓库](https://github.com/steinbergmedia/bravura)、[SMuFL 字体目录](https://www.smufl.org/fonts/)。

以上调查不足以证明某个免费字体是“最接近 Chaconne”；需要同一音乐、同一谱距与配套参数的实际对照。

## 3. 基础资产、许可与可重复构建

软件仓库：`E:\programming\funcodes\muse3_dev\MuseScore`。当前基础资产位于 `fonts/finalemaestro/`：

- `FinaleMaestro.otf`、`FinaleMaestro.json`
- `FinaleMaestroText-Regular.otf`、`Finale Maestro Text.json`
- `OFL.txt`

本地 OFL 包含 Finale、Maestro 等保留名称。衍生字体须使用新名称、保留原版权与许可、补充修改者记录，并继续按 OFL 分发；文档／乐谱本身不因使用该字体而必须采用 OFL。[OFL 官方说明](https://openfontlicense.org/ofl-faq/)

开工先固定基础文件版本和哈希，并记录来源。字体工作放在本项目独立目录 `fonts/kumo-engrave/`，不替换软件仓库的基础资产。保存可编辑矢量源、构建脚本、度量／锚点定义、版本日志与生成产物。基础 OTF 不等于已有可编辑源；工具链选择需先做一次未改字形的转换／构建回归，确认没有覆盖、轮廓或度量退化，再开始设计。

构建交付包括 `Kumo Engrave.otf`、`Kumo Engrave.json`、配套 Text OTF／JSON、OFL、来源和版本说明。修改后的内部 family／full／PostScript 名称须统一，避免与已安装字体冲突。每轮记录具体替换的字形、度量及参数，不把整体转换引起的变化误当作设计收益。

## 4. 渐进字形设计与净书配套

### 阶段 F1：符头原型

独立设计常规实心、半音符与全音符符头，其他符号先保留基础字体。观察参考中的宽高、倾斜、曲率、实心面积、空心孔与谱线关系，用真实谱例评价，不照描轮廓。

先形成多个可解释的候选，逐项改变设计因素，并让用户依据同曲局部及整页对照评审。上线目标是实际谱面偏好和可靠辨识，不是单个放大字形相似度。

### 阶段 F2：扩展高频符号

符头试验通过后，按实际需求扩展 G／F 谱号、升降还原记号、休止及力度。检查与基础字库的风格一致性；其余字符保留覆盖，不因为未重画就删除。

### 阶段 F3：度量、Text 与建议参数

字形轮廓变化时同步核查字宽、外框、符干接点、旗尾接点、切出区域和相关锚点，更新字体特定 SMuFL JSON。不能只替换可见轮廓而沿用已不适合的锚点。

- [SMuFL 字体外框](https://w3c-cg.github.io/smufl/latest/specification/glyphbboxes.html)
- [SMuFL 锚点](https://www.w3.org/2019/03/smufl13/specification/glyphswithanchors.html)
- [建议净书参数](https://www.w3.org/2021/03/smufl14/specification/engravingdefaults.html)

配套 Text 字体用于行内音乐符号、速度标记等混排，单独验证尺寸、基线和组合力度；不能假定普通音乐字库改名后就是合格 Text 字体。尚未改动的 Text 字形可沿用开放授权基础内容，保持来源与家族命名完整。

`engravingDefaults` 是建议值，不是跨软件相同数字必然得到相同轮廓的保证。例如现有引擎的弧线输入参数不能直接理解为最终墨迹中点厚度。建议线宽与个人 MSS 分开记录，并明确可能覆盖哪些已有设置。

## 5. Evolution 安装与副本试验

已核查的软件源码 `ScoreFont::scanUserFonts()` 支持私有 Score Fonts 路径和系统 SMuFL 路径。私有目录每个子文件夹的名称需与 OTF／TTF 基本文件名匹配，并提供可识别的 JSON；当前分支不同于 MuseScore 4 的 MusicFonts 路径，不能照搬教程。

未来安装步骤：

1. 先用隔离配置及测试字体目录验证加载，不安装到用户全局字体目录。
2. 准备 `Kumo Engrave/` 子目录，放入同名 OTF／JSON；Text 字体的注册与解析必须另行实际验证，不能仅凭符号字体扫描成功宣称 Text 已适配。
3. 在独立副本选择新字体，分别测试“只换字体”和“加载配套参数”；读回有效样式，说明二者差别。
4. 生成原生 Windows PNG／SVG／PDF 对照。保持固定宿主版本；offscreen 曾发生系统字体回退，不能拿该结果评价正常使用效果。
5. 通过后再交付用户安装说明及卸载／恢复方法；不得删除用户已有字体或覆盖原谱。

音乐字体变更可能影响分页。既有同曲试验只改 Finale Maestro/Text 就从 8 页变为 9 页，不能把换字体后的布局变化视为字体质量排名。

## 6. 验收与交付

- 字体层：基础字库覆盖不退化，正常码位和内部命名正确，轮廓／外框／字宽与 JSON 一致，保留许可。
- 连接层：线上／线间音、上／下符干、二度和弦、附点、加线、多层旗尾／连梁无不应出现的断接或黑疙瘩。
- 组合层：密集变音、多声部、跨谱表、装饰音、复合力度、行内速度混排及缺字回退可用。
- 版面层：同一音乐、同一宿主下分别评价字形和配套参数；局部按 sp 比例对照，整页按相同物理比例对照。
- 音乐与保护层：原 PDF／MSCZ 不变，副本音乐语义不变，现有内置字体和用户设置不被替换。
- 使用层：实际打印检查细线、空心符头内孔与密集段辨识，单独记录用户评审和打印验收状态；不能宣称尚未完成的检查已通过。

交付为可编辑源、可重复构建说明、独立 OTF／JSON 和 Text 包、可选 MSS、许可／来源、安装指南及谱例报告。字体成果与净书助手分开版本化，允许不启用个人字体时仍使用净书规则。

## 7. 分支对话交接与下一步

字体线开始时先读取本文件与 [ENGRAVING_PLAN.md](ENGRAVING_PLAN.md) 的边界，核查仓库状态和基础许可，保留并发改动。近期任务是固定基础资产、验证构建与加载、做三个常规符头的独立原型；不是修改 MuseScore 内置字体引擎。

参考 PDF 目录：`C:\Users\Fred\OneDrive - yunzd\cloudreve\Sheets\【2021-】新官谱`。主要样本为 Idol、Sincerely、IRIS OUT 和 Shirushi；具体文件名、用户只读材料和历史报告位置列于净书计划第 8 节。分支到别的电脑时这些绝对路径可能不可用，不得伪称已读取。

净书线提供真实阅读需求、情境与验收谱例；字体线反馈字形度量、锚点、建议参数及版本变化。不要同时重画字形、改变谱表大小和重排系统后把整体改善归因于字体。后续每轮在本文件记录实际状态、证据及下一步。
