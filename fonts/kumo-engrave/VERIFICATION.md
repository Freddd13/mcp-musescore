# 0.3 EX修订验证（2026-10-18）

用户已否定0.2过细/不像目标，0.3只是新的候选，未获本轮审美认可。参见 [EX直接字形修订](EX_REDRAW.md)。

- 七家族均通过完整覆盖、变更白名单、CFF/hmtx、实际bbox、正常干接点检查。EX相对Leland替换38个码位，相对0.2改26个轮廓；非声明字形不变。黑/半仍保留325 advance及原接点；全符头advance明确373→438，不宣称所有字宽保持。
- 新普通符头按实际曲线采样维护cutout；半/全孔方向与外轮廓相反、孔边界均位于外形内；常规上下干接点在实体内并避开白孔。其它共享头/二度和更多尺寸仍待专项。
- 原生宿主为personal 0.21，SHA256 `7581cb761217c5c2ef6fc802cf7aafbbe8fe1133c8553967b07e22cc3e74f034`。固定内置Leland Text、Windows Qt、180dpi、同一输入和独立配置；只在副本设置音乐/Text字体。自动优化样式未启用。最终证据 `dist/proofs-v03-final-r3/`。
- 五种家族各有fixture 1页；当前用户谱分别为Maestro 9页、内置Leland 8页、Control 9页、0.2形状8页、EX 8页。双谱表fixture的Leland与Control逐像素一致。既有Leland名字/括号分支限制依然存在，不将整份用户谱的改名Control页数差异全归因字形。
- `review_ex.py`核验最终OTF字节与原生加载文件相同、有效字体名/Text及页数；形状板来自官方PDF栅格且只用于等高形状对照；原生板保持同裁图坐标/尺度，未分别拉伸头型。官谱/参考图不放Git或字体包。
- 独立重建全部家族文件与build-report逐字节一致，具体数量在verification.json。本轮未重新做配套改名Text的全谱等价测试，推荐仍为内置Leland Text。
- 2026-10-18读入的用户MSCZ SHA256为 `4a62cc33723b1c19a207102f27425c983e9fd40d570a2ff65d7a818b82ac91ad`，与10日旧输入不同；本轮各次原生试验读前/读后相同，未回写原件。不得据旧报告声称该文件跨八天始终不变。

本轮交付两种少量图片，可直接看图给反馈，无需先安装/打印。未完成审美确认、实际打印和全字库逐字仿制；未改本体、用户原PDF/MSCZ、内置字体或用户全局设置。0.2机器记录保留为verification-0.2.json，0.1历史也保留。

---

# 0.2 新版验证（2026-10-10）

当前主候选是 **Kumo Piano（Leland 底库）＋内置 Leland Text**。以下是本轮实测，不覆盖下面 0.1 的历史记录。

- 固定 Leland 0.80 的文件哈希；完整保留音乐 493 字、Text 182 字的 glyph order／cmap／hmtx。独立替换 38 个音乐码位，未授权范围的轮廓不变；每个 CFF 字宽与 hmtx 一致，实际外框回写 JSON，普通接杆锚点保留。
- 采用相同 personal 0.17 宿主（SHA-256 `bbc3b4a139a802a98096fc0d01eee5ab5d460c38e4340d2b282e72696348c0f5`），独立 ScoreFonts／配置、Windows Qt 原生 PNG/SVG。当前软件其它开发已推进至后续版本；本轮不混用宿主结果。
- 自写 20 小节、2 谱表、完整 4/4 测试谱：38 个系列中的常用形态及上下／多层休止、无方向与上下方向琶音、密集变音、发音、延长号、踏板和 mf/mp。MusicXML 导入后核查琶音 subtype 0/1/2；原生 SVG 使用了新谱号／符头／琶音路径，未仅凭 Qt 注册认定字形被采用。放大检查了普通接杆与连续波纹；专项共享符头及纸面墨色未完成。
- 固定 Text 模式：4 家族各输出测试谱 1 页；用户谱 Maestro 9 页、内置 Leland 8 页、改名 Leland Control 9 页、新 Piano 8 页。没有把页数减少列为质量通过条件。
- 改名 Control 与内置 Leland 的整份双谱表测试谱逐像素一致，用户谱前 3 页一致、第 4 页起不同。源码 `bracket.cpp:125` 的 Leland 名称特判将 brace 跨谱表数截为 4；201/268 的 bracket 端部伸出也只对 Leland 特判。用户源有 6 个 Staff。新字形的严格对照基准使用同样落入私人家族分支的 `Kumo Piano Control`；该本体候选问题已通知净书任务，本轮未修改本体。
- 反事实原生验证：两个副本仅将 bracket span >4 改为 4，保留全部 6 个 Staff 音乐子树、字体、Text 和其它配置。两者都输出 8 页，8 页逐像素一致，确认本工程的这项 Control 分页差异由括号跨度／名称分支触发。这不代表推荐修改原谱的括号，也不能代替对其它工程的定位。代码 `verify_bracket_branch.py`，报告 `dist/bracket-cause-probe/report.json`。
- 单独测试配套改名 Text：两种音乐家族共 19 页（Control 的 1+9，Piano 的 1+8），测试谱两页完全相同；用户谱中 12/17 页出现局部差异。第 1 页 SVG 差异定位为 OttavaSegment。Leland Text 虽含 mezzo，Qt 家族替代与其它混排仍不随改名自动继承；继续推荐内置 Leland Text，不能宣称配套 Text 全部兼容。
- 在独立目录 `dist/repeat-v02-final/` 重建：六种家族共 64 个 OTF／JSON／许可／出处／FONTLOG／SVG 文件，以及 build-report，逐字节一致。
- 最终音乐／Text OTF 字节与两组原生试验加载的文件一致，原 MSCZ 和 PDF SHA-256 均与既有记录相同。官谱读前读后哈希亦不变。

最终原生报告保存在本项目忽略目录 `dist/proofs-v02-final/` 和 `dist/proofs-v02-final-text/`；这组使用最后修订的琶音箭头和渐变粗细延长号。复核脚本 `verify_release.py --fixed dist/proofs-v02-final --paired dist/proofs-v02-final-text`（在字体目录执行）只读这些结果，将报告及同尺度对照输出到 `dist/review-0.2/`。早期原生结果仍在本机私有可视化目录保留。分发机器没有这些路径时应先自行运行 `render_proofs.py`，不能照抄“已验证”。

尚未通过：用户审美认可、实际打印、共享符头/二度接杆专项、特殊符头、32/64 分旗尾与所有组合记号、推荐 MSS。官谱方向的独立绘制不等于商业字体的精确复刻。

---

# 0.1.0 技术验证与观察

更新：2026-10-09。本报告区分构建正确性、原生兼容和审美选择；用户现已明确以 **Chaconne Ex** 为视觉目标，初版候选仍为工程与参数对照，不能称为目标字体的完成版。

## 已通过的检查

- 底本 5 文件 SHA-256 与 `BASELINE.json` 一致；音乐 2745 字、Text 373 字及 cmap／glyph order 完整保留。
- Control 音乐／Text 全轮廓不变；候选音乐仅 E0A2／E0A3／E0A4 三字改变，候选 Text 全轮廓不变。全部 hmtx 和每个 CFF CharString 字宽一致。
- 候选外框由实际曲线计算；普通上下符干锚点不变，cutout／分叉接点按新轮廓维护。512 点分析检查各空心孔完全在外轮廓内。Open 与常规候选外轮廓一致，黑符头一致，仅空心孔改变。
- 在另一新目录重建，8 OTF、8 JSON、4 SVG 共 20 文件逐字节一致。构建不受运行时日期影响。
- 本机 `msvc.install_piano_0_17_x64/bin/MuseScore3Evo.exe`，Windows Qt 平台，180 dpi，独立配置／字体目录导出。5 变体 × 测试谱和用户谱 = 10 组，PNG 与 SVG 各 50 页；注册探针确认音乐与选用 Text 字体存在，样式家族与预期一致。
- **固定 Finale Maestro Text** 时，原版与 Control 的测试谱 1 页、用户谱 9 页，白纸合成后逐像素一致。该结果比“家族名显示正确”更强，但仅覆盖此宿主及这些谱例。
- 所有副本创建前后去除 Style 的 XML 完全相同；只设置字体样式项。用户原 MSCZ 与原 PDF 哈希不变（值见 `verification.json`），原谱没有被回写。

实际最新原生证据保存在本机 Codex 本任务目录的 `font-native-017-jp/`，包含 `native-report.json`、`review-report.json`、探针、各页 PNG／SVG、独立 MSCX 副本及三张同尺度对照。较早的固定 Text 初版在 `font-native-017-fixed-text/` 保留。谱例图、参考图及完整用户工程不提交 Git。

## Text 回退发现

首次试验同时换音乐／Text（`font-native-017-v1/`），各字体注册均成功，用户谱均 9 页。然而只改名 Control 在测试谱 mf 和用户谱若干力度处仍有像素差异，其他大部分内容不变。

查得底本 Text 缺 `dynamicMezzo` U+E521，而 `libmscore/sym.cpp` 将 `Finale Maestro Text` 替代到 `Leland Text`，`libmscore/textbase.cpp` 缺字符检查会选择 `Bravura Text`。新家族不继承前一条固定名字的替代，混排不能只靠改名保证相同。保持内置 Text 后所有 Control 页完全一致，支持差异与 Text 替代链相关的判断。尚未逐字探测每种文本实际用了哪个回退字库，不能对全字库兼容作更宽保证。

结论：0.1.0 推荐只换音乐字体，Text 保持 Finale Maestro Text；分发的改名 Text 为 F3 兼容试验资产。下一步在字体层补必需字符覆盖并核验组合力度／速度／音符混排，不急着改本体。

## 图像观察与实际局限

测试谱的上下接杆、加线、多声部、和弦、附点／延音及 16 分连梁已渲染检查，没有发现明显断杆；用户第 148–149 小节的跨谱表快速音型、32 分连梁及四谱表长音也已输出并浏览（新输出第 9 页）。这不等于每个小尺寸和每种二度／分叉连接已验收。

空心符头被谱线穿过时，内孔很容易显得闭塞；Open 把孔纵向增大 12%，外轮廓不变，便于隔离辨识与墨色差异。当前四段椭圆原型曲率较规律，仍需按目标观察打磨，而不能仅凭整体倾斜近似判断达成 Chaconne Ex 风格。全音符相邻排列还应检查黑白节奏与半／全音符辨识。

三候选（含 JP）和 Maestro 都是 9 页，但实际曲线／cutout 变化可改变局部避让及谱表位置；相同 advance 不保证排版固定。净书研究需绑定具体 OTF、JSON 与宿主版本，不把原 PDF 的页码当作新渲染的对象定位。

未完成：实际打印；用户目标方向的新轮廓评审；不同 dpi／谱距专项；二度、分叉符干的充分覆盖；F2 谱号／变音／休止／力度设计；Text 修复；完整建议 MSS。原型不会自动改用户的全局字体或当前乐谱。
