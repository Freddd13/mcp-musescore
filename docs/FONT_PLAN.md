# 个人出版风格音乐字体计划

更新日期：2026-10-19。状态：**用户已否定0.2及0.3，要求直接按新官谱实际字形做。当前 Kumo Score Study 0.480 本机小样处理112个码位，完整保留Leland底库；全目录角色仍在逐项结案，尚非完整字体。**

**用户新增要求：实际大小必须合理，尤其mf及八度等不能因换字库悄悄缩小。** 已确认0.470的Music/Text尺寸适配错误；0.480修复19个Text字形，用户谱mf由原字体约51%恢复到96%，8/8va与踏板接近原有大小。Music502字形/度量完全不变，原谱字号、音乐和附件保持。后续每次更新均用同宿主、同谱距和完整上下文看实际尺寸，来源字形相同或字框相同不能代替这一步。规范学习及净书线不得把这项字体缺陷误归因用户排版设置。详见 [TEXT_SIZING](../fonts/kumo-engrave/TEXT_SIZING.md)。

验收补充：当前安装目录的新二进制4d739629…已通过0.480全套字体/用户谱和大小验证，旧崩溃版本与新通过版本分开记录。156低匹配代表图已保存明确角色对应，45个原页情境核查；9项Leland回退实际轮廓/度量保持。其余图录与成员语义仍未逐一完成，滑音仍有原生复用trill波形的已知缺口。详见 [COVERAGE_RECONCILIATION](../fonts/kumo-engrave/COVERAGE_RECONCILIATION.md)。

0.470将sf、八度、括号与速度/swing等9个旧轮廓改为原字符曲线。六个单字符及三项混排均通过最终OTF/原PDF比较，95个字形含三次曲线；Coda和下方重音断音的替代映射仍拒绝保留旧形。固定宿主全套原生与用户谱副本通过，原件/音乐/附件保持；当前宿主异常仍未解决。见 [REMAINING_CURVES](../fonts/kumo-engrave/REMAINING_CURVES.md)。

0.460补齐32分下符尾/内部下符尾与上下marcato-tenuto，35个旧字形改用通过原图核对的曲线/直线；39项来源/最终OTF比较通过，5个错映射拒绝保留旧形。A064全路径复核补回128个可见对象，864组24张联系表已浏览，10项弧线情境异常仍单列。固定宿主原生/用户谱副本验证完成，当前宿主兼容仍未完成。详见 [CURVE_REFINEMENT](../fonts/kumo-engrave/CURVE_REFINEMENT.md)。

0.450从全目录候选补入16码位：圈叉、呼吸、marcato-staccato、32分上符尾、滑音段、两道震音、力度字母、反复点及大括号。五个字符的曲线与原图投影对照通过；一个震音错误映射明确回退实际渲染。固定宿主原生/用户谱副本验证完成，当前宿主的导入崩溃另存证据，未称通过。滑音复用trill波线、震音走几何、大括号有专门倍率，已告知净书线。来源与边界见 [OBSERVED_SYMBOLS](../fonts/kumo-engrave/OBSERVED_SYMBOLS.md)。

0.440把A064已核查的现成曲线接入实际可用字库，覆盖常规符头、谱号、主要休止/旗尾、拍号、力度、踏板与波线等；41个字形含1,212段三次曲线。40项来源/派生对照及当前宿主原生测试通过，用户谱副本的音乐和附件保持。来源误判、校准、宿主SHA与下一步见 [VECTOR_STUDY](../fonts/kumo-engrave/VECTOR_STUDY.md)。

0.430已修正颤音波线基线和重复周期，适配两个Leland方向端部并保留其三次曲线；真实长短琶音、跨系统trill、当前安装宿主和用户谱独立副本均已渲染。用户原件及归档附件保持，Study8页/Control9页不作布局质量排名。详见 [WAVE_STUDY](../fonts/kumo-engrave/WAVE_STUDY.md)。接下来重点为剩余音乐角色、A064曲线候选和放大轮廓质量；不把92字视为全目标完成。

最新进展见 [全目录研究与未完成项](../fonts/kumo-engrave/CORPUS_STUDY.md)。已只读清点146份PDF、1,135页；Chaconne选样134个有墨迹编码已做图录和用途分类，不能等同于134种符号，也不能由一次编码归类推断同名字体在其它PDF的编码相同。发现A064《in the pool》全五页均为矢量路径，字符扫描无法覆盖；必须补路径谱例审计。

**本段是当前执行方向，优先于下文保留的早期独立造型计划：** 用户已要求忠实于所给官谱，当前使用实际PDF文字对象渲染产生本机轮廓；没有读取或保存FontFile字体程序，也不将参考轮廓标为本项目OFL公开发布资产。默认 `build.py`、旧profiles和原型ZIP保持原样。原PDF/MSCZ只读，所有实验在忽略的 `dist/` 内。字体层保持Leland未改部分，不同时变更谱面布局。

接续顺序：继续核查整目录同码异形、普通文字/音乐数字和复合标记；补足实际出现但尚未覆盖的角色；改善剩余轮廓和端部，并持续检查用户谱独立副本与宿主兼容。0.2/0.3的被否定结果和7字方法验证都保留为历史证据，不再让用户反复在已否定候选里选择。

A064早期路径研究读取7,299个可见填充对象，32个候选先验证转换机制；0.420尚未纳入。0.440已进一步确认用途、比例和基线，正式接入上述42个字形。诊断索引字库本身仍不能作为可安装乐谱字体使用。

0.420补充：已浏览269个此前遗漏的字体组的638个样本对象，定位八度8、音符括号和十六分swing，并在原页区分标题里的角括号、星号与音符装饰。13个样本无墨迹字体组进一步遍历全部34个对象，仍无渲染墨迹，源哈希不变。新增sf、8va/8、音符括号、等号/近似等号、五种swing及短下符尾备选；派生两种加线休止。X头接杆改为分别落在上下实心支臂，避免继承旧字形的连接点。

普通连音数字走 `Text(Tid::TUPLET)`；实际震音由 `Tremolo::basePath` 绘制。音乐字体中的相似符号不能替代这两条实现路径；已向净书任务说明，字体线不顺便修改本体。当前额外字符入口见 [TEXT_EXTRAS](../fonts/kumo-engrave/TEXT_EXTRAS.md)。

本对话执行字体线；[钢琴净书研究线](ENGRAVING_PLAN.md) 在另一任务并行推进。实现位于 [fonts/kumo-engrave](../fonts/kumo-engrave/README.md)，两线独立提交，互相交换验收案例与机制发现。

最新实际PDF参照与局部可行性证据见 [PDF_REFERENCE_STUDY](../fonts/kumo-engrave/PDF_REFERENCE_STUDY.md)。不再推荐0.3，也不把原字体购买作为研究用户所给PDF的前置条件。

上轮具体修订和两种对照图的读法见 [EX_REDRAW](../fonts/kumo-engrave/EX_REDRAW.md)。0.3修正26个0.2轮廓，不再把“越细越干净”当作目标。原生对照固定personal 0.21与内置Leland Text，不同时调整梁、间距或页面参数；全音符advance的373→438变化单独记录。

## 1. 已确认的目标与边界

用户喜欢 Animenz 新官谱的 Chaconne 风格。初版使用开放授权 Finale Maestro；2026-10-09 用户认为其整体不够干净，明确改为 **以 Leland 为新版底库，保留 Leland 的完整字库，扩展常用字形**。旧 Maestro 家族与 0.1 包保留，供历史对照。

本轮新增 `Kumo Piano` / `Kumo Piano Control`，以 Leland 0.80 为基础；独立替换 38 个字形（含符头、G/F 谱号、休止、变音、旗尾、琶音、发音符号、延长号），未改字符沿用 Leland。观察范围扩展至 14 份官谱的 33 页，详见 [官谱到设计的依据](../fonts/kumo-engrave/ANIMENZ_REFERENCE.md)。参考以实际 Animenz 成品谱为主，Ex 字形表仅是补充，不把二者说成同一版本。

2026-10-09 用户在第一轮符头对照后明确要求“按 chonnex 的来”：视觉目标具体化为 **Chaconne Ex 官方谱例与字形表展示的风格**，不以两种初版候选的主观偏好为定稿依据。已读取官方字形表第9页，新增 `Kumo Engrave JP`，保留 Control／初版候选作工程对照；[设计依据](../fonts/kumo-engrave/DESIGN_BRIEF.md)记录观察到参数的理由。旧官谱不能自动代表 Ex 全套设计。目标方向与字形来源分开记录。

当前独立家族名为 `Kumo Piano EX`，配套 `Kumo Piano Text` 暂作兼容研究；旧 `Kumo Engrave` 家族保留。不复用基础字体保留名称。目标是符合用户偏好的出版谱视觉语言，不承诺复制 Chaconne，也不宣称字体本身能够完成净书。

- 参考 PDF 只用于观察比例、黑白关系、印刷效果和上下文表现。不提取、描摹或重新包装其嵌入 Chaconne 字形。
- 不修改用户 PDF、MSCZ、现有内置字体、全局字体或当前 MuseScore 设置。试验使用独立字体家族、独立配置和工程副本。
- 先保留基础字库覆盖，渐进替换批准进入试验的字形，不从零重做完整字库。
- 不将字体名称替换与整套默认样式重置混为同一操作；后者可能覆盖用户已有调整。

## 2. 字体调查与合法来源

| 字体 | 已核查事实 | 本线用途 |
| --- | --- | --- |
| Chaconne | 主要新官谱样本嵌入字体名称已确认；并非所有年代样本都相同 | 审美参考，不作为字体文件来源 |
| Chaconne Ex | 官方定位为 SMuFL 后继，支持 OTF／Windows；2026-10-08 查看官方商店标价 16,500 日元 | 可购买的参考候选，当前未取得或测试，不保证与旧版字形完全相同 |
| Finale Maestro／Text | Evolution 已内置，厂家公开 OFL 许可及免费安装包 | 0.1 历史底库与现成对照 |
| Leland／Text | 本地软件仓库为 0.80，OFL；保留名称 Leland；音乐 493 字、Text 182 字 | 用户最新确认的基础；未删减覆盖，不能称与 Maestro 的覆盖完全相同 |
| Sebastian | 作者提供字体、SMuFL JSON 和 UFO 源，OFL 许可 | 独立研究对照，不预先判定为最接近 Chaconne |
| Bravura | SMuFL 参考字体，开放授权，外观偏厚重 | 覆盖与机制对照，不因它是 Dorico 默认字体就视为目标答案 |

来源：

- [Chaconne Ex 产品](https://chaconne-ex.stonemusic.jp/)、[官方商店](https://stonemusic.stores.jp/items/67176151ce1b810155a57f25)、[官方支持](https://www.stonemusic.jp/chaconne-ex-support/)。价格、版本与许可在真正采用时重新核查；目前没有确认获授权的免费 Chaconne 分享。
- [MakeMusic 字体许可和安装包](https://makemusic.zendesk.com/hc/en-us/articles/1500013053461-MakeMusic-Fonts-and-Licensing-Information)。页面提供 Windows MMFonts.msi；本机 Evolution 试用 Finale Maestro 无需先安装另一个软件。
- [Sebastian 作者仓库](https://github.com/fkretlow/sebastian)、[发布页](https://github.com/fkretlow/sebastian/releases)。
- [Bravura 官方仓库](https://github.com/steinbergmedia/bravura)、[SMuFL 字体目录](https://www.smufl.org/fonts/)。

以上调查不足以证明某个免费字体是“最接近 Chaconne”；需要同一音乐、同一谱距与配套参数的实际对照。

## 3. 基础资产、许可与可重复构建

软件仓库：`E:\programming\funcodes\muse3_dev\MuseScore`。旧版基础资产位于 `fonts/finalemaestro/`：

- `FinaleMaestro.otf`、`FinaleMaestro.json`
- `FinaleMaestroText-Regular.otf`、`Finale Maestro Text.json`
- `OFL.txt`

0.2 新底库来自 `fonts/leland/`：`Leland.otf`、`LelandText.otf`、`leland_metadata.json`、`LICENSE.txt` 与 `FONTLOG.txt`，只读复制到插件项目 `vendor/leland/`；哈希、来源提交和版本记在 `LELAND_BASELINE.json`。新家族不使用保留名称 Leland，不替换软件内置资产。源矢量为 `source/piano_palette.py` 与 `source/design.json`。

本地 OFL 包含 Finale、Maestro 等保留名称。衍生字体须使用新名称、保留原版权与许可、补充修改者记录，并继续按 OFL 分发；文档／乐谱本身不因使用该字体而必须采用 OFL。[OFL 官方说明](https://openfontlicense.org/ofl-faq/)

开工先固定基础文件版本和哈希，并记录来源。字体工作放在本项目独立目录 `fonts/kumo-engrave/`，不替换软件仓库的基础资产。保存可编辑矢量源、构建脚本、度量／锚点定义、版本日志与生成产物。基础 OTF 不等于已有可编辑源；工具链选择需先做一次未改字形的转换／构建回归，确认没有覆盖、轮廓或度量退化，再开始设计。

构建交付包括 `Kumo Piano.otf`、`Kumo Piano.json`、配套 Text OTF／JSON、OFL、来源和版本说明。修改后的内部 family／full／PostScript 名称须统一，避免与已安装字体冲突。每轮记录具体替换的字形、度量及参数，不把整体转换引起的变化误当作设计收益。

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

安装与副本试验步骤（当前原型详见 [安装指南](../fonts/kumo-engrave/README.md)）：

1. 先用隔离配置及测试字体目录验证加载，不安装到用户全局字体目录。
2. 准备 `Kumo Piano/` 子目录，放入同名 OTF／JSON；Text 字体的注册与解析必须另行实际验证，不能仅凭符号字体扫描成功宣称 Text 已适配。
3. 在独立副本选择新字体，分别测试“只换字体”和“加载配套参数”；读回有效样式，说明二者差别。
4. 生成原生 Windows PNG／SVG／PDF 对照。保持固定宿主版本；offscreen 曾发生系统字体回退，不能拿该结果评价正常使用效果。
5. 通过后再交付用户安装说明及卸载／恢复方法；不得删除用户已有字体或覆盖原谱。

音乐字体变更可能影响分页。既有同曲试验只改 Finale Maestro/Text 就从 8 页变为 9 页，不能把换字体后的布局变化视为字体质量排名。

2026-10-09 的 0.17 隔离原生试验已验证三家族及 Text 注册。发现只改名 Text 也改变部分力度：Maestro Text 缺 `dynamicMezzo` U+E521，内置家族的 Qt 字体回退并不自动传给新家族。旧 0.1 的推荐配套方式为 **Kumo Engrave 音乐字体 + 内置 Finale Maestro Text**；改名 Text 暂留作兼容研究。固定 Text 后，Control 与 Maestro 在测试谱 1 页、用户谱 9 页均逐像素一致。两种新符头候选的用户谱均 9 页，仍需检查局部碰撞和分页变化，不能由保留 hmtx 推断布局绝对不变。

## 6. 验收与交付

- 字体层：基础字库覆盖不退化，正常码位和内部命名正确，轮廓／外框／字宽与 JSON 一致，保留许可。
- 连接层：线上／线间音、上／下符干、二度和弦、附点、加线、多层旗尾／连梁无不应出现的断接或黑疙瘩。
- 组合层：密集变音、多声部、跨谱表、装饰音、复合力度、行内速度混排及缺字回退可用。
- 版面层：同一音乐、同一宿主下分别评价字形和配套参数；局部按 sp 比例对照，整页按相同物理比例对照。
- 音乐与保护层：原 PDF／MSCZ 不变，副本音乐语义不变，现有内置字体和用户设置不被替换。
- 使用层：实际打印检查细线、空心符头内孔与密集段辨识，单独记录用户评审和打印验收状态；不能宣称尚未完成的检查已通过。

交付为可编辑源、可重复构建说明、独立 OTF／JSON 和 Text 包、可选 MSS、许可／来源、安装指南及谱例报告。字体成果与净书助手分开版本化，允许不启用个人字体时仍使用净书规则。

## 7. 分支对话交接与下一步

字体线已读取两线边界并核查基础许可。0.1 Maestro 基础资产固定到软件提交 `1146859d0`，三个常规符头独立原型及构建／验证／原生试验脚本已落盘；不需修改 MuseScore 内置字体引擎。源码及字体报告见 [验证记录](../fonts/kumo-engrave/VERIFICATION.md)。

下一步按顺序进行：

0. **最新决定优先：** 继续以 Leland/Animenz 官谱推进，不再把 JP/Maestro 作为主方向；用户已否定0.2，先以用户官谱的实际字形/局部原生小样修正具体形状。已发现宿主 `bracket.cpp` 对精确名称 Leland 特判 brace 最大跨谱表数与 bracket 端部；6 谱表用户谱的改名 Control 因此可能改变分页。该发现已通知净书线，字体线不添加本体硬编码；使用改名 Control 作为新字形的严格基准，并单独记录与内置 Leland 的差异。

1. 按0.3直接字形和原生对照收集审美反馈，优先修正谱号、休止、旗尾和连续琶音；参考更多实际 Animenz 官谱，不能因首批 38 字完成就宣称全字库设计完成。
2. 增补二度和弦、分叉接杆及不同输出缩放专项；实际打印核查谱线穿孔与墨色。净书线提供的 m41 力度、m148–149 四谱表案例纳入回归，并保留音乐内容／标记时间和归属。
3. 配套 Leland Text 虽含 mezzo，改名后的用户谱仍在八度线等混排出现差异；0.2 推荐内置 Leland Text。后续优先在字体层补覆盖／混排，独立验收；不为私人家族添加硬编码本体规则。
4. 继续 F2 踏板、装饰、力度、数字及组合发音系列；32/64 分旗尾与较少见形态需补足观察。F3 推荐样式单独版本化，不自动覆盖已有 MSS。

参考 PDF 目录：`C:\Users\Fred\OneDrive - yunzd\cloudreve\Sheets\【2021-】新官谱`。首批样本为 Idol、Sincerely、IRIS OUT 和 Shirushi；0.2 已扩展到 14 份谱子，完整列表见官谱设计依据；具体文件名、用户只读材料和历史报告位置列于净书计划第 8 节。分支到别的电脑时这些绝对路径可能不可用，不得伪称已读取。

净书线提供真实阅读需求、情境与验收谱例；字体线反馈字形度量、锚点、建议参数及版本变化。不要同时重画字形、改变谱表大小和重排系统后把整体改善归因于字体。后续每轮在本文件记录实际状态、证据及下一步。
