# 独立净书复现谱例

## 颤音的可见范围与连续／重奏

2026-10-20原创四小节4/4双谱表，CC0，无参考音乐转写；26书面音、一个跨行逻辑Trill、一个tie连接、两个独立tr奏法。m2 F5全音符连m3 F5二分，波线到m3第三拍G♯5；m4两个E5二分分别起颤。固定Leland／Leland Text和两行预算，非出版模板。

- [源MusicXML](trill-source.musicxml)、[原生保留版](trill-continuation.mscx)／[图](trill-continuation.png)：新行只续波线，结合tie可读，不宣称优于括起的续行tr提醒。
- [提前收线拒绝版](trill-endpoint-rejected.mscx)／[图](trill-endpoint-rejected.png)：只插入Trill内两绘制段，末段off2.x为−12sp并保有效高度；在二分音符结束前收线，误示停止。完整MIDI相同仍拒绝。

移除两个Segment可还原完整源XML；非Trill图元和第一行Trill图元精确保持。续行31→17个波纹字形不等于逻辑分段／颤动次数；高度残差约0.083 SVG单位（180dpi约0.042像素）。首版默认offset控制改变高度，不当单因素证据；最终取宿主保存精度后，拒绝版重载SVG／PNG／MusicXML／MIDI保持。源与原生导出的音高、起点、时长、tie经voice映射核对；颤音实际生成102次NoteOn，不要求与26书面音相等。两图原生180dpi，仅白底与同框裁切(70,75,1420,740)，没有符号图片重排。见[专题](../TRILL_READING.md)和[证据](../trill_reading_evidence.json)；CLI沿用下文，用独立配置／路径。未做导回、试听、打印、用户评价或软件适配；官谱／教材不在CC0许可中。

## 奏法的贴音关系与动态通道

2026-10-20原创四小节4/4双谱表，CC0，无参考音乐转写；26音、22奏法、3动态、1逻辑渐强。固定Leland／Leland Text、spatium1.57mm及两系统预算，非出版预设。m1八分断奏，m2高音tenuto，m3上下干分别断奏／tenuto，m4短重音；输入明确指定相应奏法的上／下方，非全部无条件自动方向。渐强从m2起至m3第三拍，SVG有三个绘制图元，不能据此建三个逻辑范围。

- [源MusicXML](articulation-source.musicxml)、[原生保留版](articulation-ownership.mscx)／[图](articulation-ownership.png)：按音与声部分配奏法；不宣称全部细节已达最佳出版。
- [全平拒绝版](articulation-flat-dots-rejected.mscx)／[图](articulation-flat-dots-rejected.png)：只给m1八个Articulation设offset／关闭autoplace，向其中最高点统一，最大上移约4.5sp，低处点与音分离。不是“所有对齐均错误”的模板。

恢复8个子树可还原源XML；实际7个奏法图元移动，全部非奏法图形保持。源／原生26事件经显式voice映射核对，完整MIDI相同；MusicXML只奏法位置属性不同。拒绝版另做原生保存重载，SVG／PNG像素／MusicXML／MIDI保持，这不改变其拒绝判断；保留版本轮未另重载。两图180dpi原生PNG，仅白底合成及同框裁切(70,90,1420,750)，没有图片重排／缩放符号。见[专题](../DYNAMICS_ARTICULATION.md)与[证据](../dynamics_articulation_evidence.json)。复现沿用下文CLI，用独立路径／配置；未做MusicXML重导入、试听、打印或用户偏好评价，官谱／教材不在CC0许可中。

## 震音的时值、逻辑半程与梁长

2026-10-20原创三小节4/4双谱表，CC0，无参考音乐摘录。固定Leland／Leland Text、spatium 1.57mm、A4同满行预算；该预算为控制，非出版模板。m1上部16个C5／G5交替十六分，m2两个whole端点c16、各实际1/2 slot，m3 whole C5 r16；文字明确有节制十六分。下部m2前两拍四分、后两拍八个十六分，其余四分。37书写头、2个震音、无Tuplet，播放66起音。

- [保留版](tremolo-reading-source.mscx)／[图](tremolo-reading-source.png)：m2第二头在横区间35.8%仍正确对下部第三拍；不能按可见whole相加成八拍。
- [短梁备选](tremolo-shorter-strokes.mscx)／[图](tremolo-shorter-strokes.png)：仅Style/tremoloStrokeLengthMultiplier=0.38；两音梁缩短，单音斜划和其它SVG图元保持。原版也有效，此值不作用户全局预设。
- [几何居中拒绝版](tremolo-visual-midpoint-rejected.mscx)／[图](tremolo-visual-midpoint-rejected.png)：仅m2第二Chord offset x≈4.431sp，移到首列／右界几何中点，失去第三拍对齐；完整MIDI相同仍拒绝。

两个修改均可逆回原XML；三版实际事件／MIDI相同。短梁版另做原生重载，样式、分类／实际时长、SVG除标题说明、PNG像素、MusicXML／MIDI保持。MusicXML重导入保住c16／r16与slot、无新Tuplet，却未保短梁样式，并因附加乐器设置改变NoteOff／CC。原输入m3单音重复间隔实测119tick而非理想120，不宣称精确计量播放或由此判自由震音。见[专题第11节](../NOTATION_DETAILS.md)和[证据](../tremolo_reading_evidence.json)。三图为180dpi原生PNG，仅合白底、同框裁页边，未缩放／移动符号。按本页CLI用独立输出／配置复现；未做打印、音响或用户审美验收，官谱／教材不在CC0许可中。

## 跨表琶音：成员、分组与下表降号

2026-10-20原创两小节4/4双谱表，CC0，无参考音乐转写；固定Leland／Leland Text、spatium 1.57mm、A4满行预算（控制条件，非出版模板）。m1低部C2以tie延续到m2；m2下部E♭3／G♭3／B♭3、上部E4／G4／B♭4另起。8头、2休止、7实际起音。文字明确拍上展开，原生间隔70ms，不是一般时序规范。

- [自动跨表](arpeggio-continuous.mscx)／[图](arpeggio-continuous.png)：成员正确，下表降号与线相交。
- [局部留白](arpeggio-continuous-clear.mscx)／[图](arpeggio-continuous-clear.png)：本例改善候选，仅共同Segment leadingSpace=1.4sp＋线offset=(-1.4,0)sp，保住对齐／成员，非全局预设。
- [两组展开](arpeggio-separate.mscx)／[图](arpeggio-separate.png)：独立动作的正例，两手同时开始、各自展开，非连续版的等价美化；保留变音造成的两线错列。
- [拉长拒绝版](arpeggio-extent-rejected.mscx)／[图](arpeggio-extent-rejected.png)：仅在留白版加userLen2=4.5sp，线达到延续低音，误示成员，完整MIDI相同仍拒绝。

三种受控修改可逆回原XML；四版计量事件、tie、StaffLines／页预算保持。自动／留白／拉长完整MIDI一致，两组版不同。留白版单独做过原生重载，SVG除标题说明、PNG像素、MusicXML／MIDI保持；实际连续版MusicXML重导入却丢下表琶音和原生时序，不能替代原工程。详见[跨谱表专题](../CROSS_STAFF_STUDY.md)与[证据](../arpeggio_reading_evidence.json)。四PNG为180dpi原生渲染，仅合白底、同框裁页边，保留两小节完整两手；未移动／缩放符号。复现沿用下文CLI，输出与配置用独立路径；未做用户／打印／音响验收，官谱／教材不在CC0许可中。

## 装饰音与小字形计量音：相同头数仍能改错音乐

2026-10-20新增原创两小节4/4，CC0，无参考音乐转写；固定Leland／Leland Text、spatium 1.57mm和相同A4满行预算（控制条件，非稀疏终行推荐）。[保留版](grace-identity-source.mscx)／[图](grace-identity-source.png)在m1第二拍G4前放三个grace16；[计量改写反例](grace-as-measured-rejected.mscx)／[图](grace-as-measured-rejected.png)将它们改成普通small十六分，同时把G4改成十六分以保持拍数。后者不是等价美化，不采用。

两版都有19头／19个MIDI起音，每表每小节4拍，三个小头同为0.7缩放；但16计量＋3grace变成19计量，G4逻辑起点1→7/4、时长1→1/4个四分，MIDI也不同。原版正常主音与下手计量列对齐，实际MIDI却先奏装饰，故不能按播放起点重排正常音列。八个上下共同拍点按头中心核查，缩放不同可使原点相异而中心仍齐；全部StaffLines和页面尺寸相同，其它列会重分配。

保留版单独做过原生重载，grace类型／目标／事件、SVG除标题、PNG像素、完整MusicXML／MIDI保持。两图仅合白底、同框裁页边，完整保留两手，未缩放／移动符号。这是身份与时间映射练习，未配装饰slur／拍上文字，未作完整出版／用户／打印验收。理由、官方格式定义及限制见[装饰音专题](../NOTATION_DETAILS.md)，哈希和实际导出见[证据](../grace_reading_evidence.json)。复现沿用本页CLI，独立路径／配置；官谱和教材不在本CC0许可中。

## 长短三连音：保留长音，还是拆开换完整连梁

2026-10-20新增原创两小节4/4双谱表，CC0，无官谱／用户音乐转写。固定Leland／Leland Text、spatium 1.57mm、A4和同一满行宽度预算（lastSystemFillLimit=0仅作控制）。上部每拍一个真实3:2八分单位组，下部普通四分作参照；m1示范数字3，m2真实组不变但隐藏数字／括号并写sim.。

- [保留长短](long-short-triplets.mscx)／[图](long-short-triplets.png)：四分＋八分，本例对已建立重复型倾向保留。
- [拆长音共梁](long-short-split-beams.mscx)／[图](long-short-split-beams.png)：每个四分拆为两个tie八分再与短音共梁，多8个头／8条tie；用于说明细分的备选，不是纯梁几何或通用改善。

两版书写音符24／32，按tie合并均24个实际起音；真实组8个、每小节4拍、完整MIDI一致。全部StaffLines及页面尺寸相同，其它时间列／干向会重新布局；保留版单独做过原生重载，SVG／PNG／MIDI及MusicXML保持。图只将180dpi原生PNG合白底、同框裁去页边，保留整行两手，未缩放／移动符号。详见[节拍阅读](../RHYTHM_READING.md)与[证据](../flag_reading_evidence.json)，导出方式同本页下文，使用独立路径／配置。未作用户审美／打印／试奏验收；教材、官谱不在本CC0许可中。

## 指法归属、替指与同指多音

2026-10-20新增原创四小节3/4双谱表，CC0，无参考旋律摘录；固定Leland／Leland Text、spatium 1.57mm，指法沿用宿主文本样式。20音、19个Note下Fingering、一个3:2组：m1和弦纵排，m2持音5→4替指，m3连音数与指法，m4同一拇指取E4／F4。仅作记谱／净书练习，不承诺最佳生理手型。

- [原生基线](fingerings-automatic.mscx)／[图](fingerings-automatic.png)：保留合理堆叠与两处富文本符号，原生重载SVG／PNG／MIDI保持。
- [贴近音头的拒绝版](fingerings-near-notes-rejected.mscx)／[图](fingerings-near-notes-rejected.png)：仅m4目标Fingering加autoplace=0及offset(-1.6,0.2)sp，却碰小节线，不采用。
- [删符号的拒绝版](fingerings-stripped-rejected.mscx)／[图](fingerings-stripped-rejected.png)：只去两个sym，数字／所属音／MIDI保持却丢替指与同指多音含义，不采用。
- [实际MusicXML输出](fingerings-export.musicxml)→[重导入MSCX](fingerings-musicxml-roundtrip.mscx)／[图](fingerings-musicxml-roundtrip.png)：字形名称变普通文字，源谱不可用其替换。书写事件保持，播放另引入gateTime等配置，完整MIDI不相同，勿沿用前三版的一致结论。

四张图均180dpi原生PNG，只合白底、用相同较高裁框保留两系统，包括重导入后更大的间隔；未缩放／移动符号。XML公开副本仅规范LF换行。判断、范围和一手规范链接见[指法专题](../FINGERING_STUDY.md)，原生／MusicXML／MIDI核对见[fingering_evidence.json](../fingering_evidence.json)。复现命令同下文；所有输出使用独立路径和配置，原谱与教材不在此CC0许可中。

## 连音省写与嵌套：保留分法，分开标记层级

2026-10-20新增原创四小节4/4双谱表，CC0，无参考音乐摘录，固定Leland／Leland Text、spatium 1.57mm、上干和两小节一系统。干向及断行只是本练习的控制条件。m1建立四组三连八分，m2重复；m3换成3／5／普通二分／3；m4外层3:2的最后一份内含5:4，再接二分休止。

- [全显示基线](tuplets-all-shown.mscx)／[图](tuplets-all-shown.png)：m4自动外层括号穿过内层5，是本例要处理的实际干扰。
- [只省重复数字](tuplets-selective.mscx)／[图](tuplets-selective.png)：只将m2四个Tuplet的numberType改2；中间控制，m4干扰尚在。
- [省写并分开嵌套](tuplets-selective-clear.mscx)／[图](tuplets-selective-clear.png)：在上一版上，只给m4外层增加p1／p2，均x=0、y=-1.2sp；本例倾向的候选，非全局数值规则或用户已采用方案。
- [全隐藏反例](tuplets-all-hidden.mscx)／[图](tuplets-all-hidden.png)：隐藏全部数字和括号，播放不变却失去引入／变化／嵌套信息，不作通用美化。

60音、1休止、13个真实Tuplet与嵌套时值已按独立有理数配方、原生栈及MusicXML核对；完整MIDI相同。只有Tuplet图元改变，候选原生保存重载SVG／PNG／MIDI保持。m4局部括号移动没有反映在本次导出的MusicXML整小节树中，勿以该格式往返代替原生工程。四张图仅合白底、同框裁页边，保留两系统完整音乐，未缩放／移动符号。具体阅读理由及限度见[连音应用](../TUPLET_READING.md)与[证据](../tuplet_reading_evidence.json)；原生导出命令同本页下文，使用独立配置及输出目录。参考谱和教材不在本CC0许可中。

## 提示变音与来路：行中、跨行、简单反复

2026-10-20新增原创六小节3/4双谱表，CC0。[自动版](accidental-state-automatic.mscx)／[图](accidental-state-automatic.png)、[选择性提示](accidental-state-selective.mscx)／[图](accidental-state-selective.png)、[额外给行中tie重复版](accidental-state-extra-tied.mscx)／[图](accidental-state-extra-tied.png)。m1–2同系统，m3–4跨系统，m5–6两次反复。选择版只在m4 tie接收F♯加普通升号、m5反复起点C加括起还原；额外版再给m2行中tie接收C♯加升号。后者是反例，不作通用美化。

保持Leland／Leland Text、spatium 1.57mm、A4与同宿主。32逻辑音、两tie和反复等结构核对，原生输入只差Accidental节点；三版MIDI逐字节相同。m4提示会使后面自动升号省去，故显示核查不能只看添加点。选择版保存重载MusicXML音乐、SVG（除标题）、PNG像素与MIDI相同；其余两版未作此次重载。全部图只合白底并同框裁页边；稀疏宽行用于隔开试验条件，不是理想页模板，末系统未强撑满。判断及限制见[提示变音专题](../ACCIDENTAL_CONTEXT.md)，证据见[accidental_state_evidence.json](../accidental_state_evidence.json)。原官谱／教材和用户音乐不属于此CC0许可。

## 共同时间列极简复现

`mixed-subdivision.mscx` 是本线自制的极简6/8钢琴谱，不含用户或参考谱的音乐摘录。四小节左手均为六个C3八分，右手均用G4，仅第三小节后半的细分改变。内置Leland/Leland Text，无变音、歌词、手工位移、特殊隐藏谱表。用于研究共同时间列和弹性分配，不是改好的排版或审美目标。

2026-10-10由本机Evolution原生导出PNG和SVG；SVG标记MuseScore 3.7.0。第三小节左手间距约17.26/17.26/17.26/21.57/21.57pt，前后普通小节约17.07pt。完整结果见 [SPACING_STUDY](../SPACING_STUDY.md) 与 [spacing_evidence.json](../spacing_evidence.json)。

复现时使用独立输出/配置目录，将实际宿主路径替换后执行下面两个命令。禁止覆盖原谱或当前GUI工程；命令中的fixture为本目录文件。保持字体和页面设置，变更条件需另记录。

```text
MuseScore3Evo.exe -s -m -c <独立配置目录> -r 180 -o <独立输出目录>/probe.svg <本目录>/mixed-subdivision.mscx
MuseScore3Evo.exe -s -m -c <独立配置目录> -r 180 -o <独立输出目录>/probe.png <本目录>/mixed-subdivision.mscx
```

宿主可能在文件名添加页号（本次为`probe-1.svg/png`）。PNG含透明背景时需合成白底查看；不能将黑色背景预览当渲染失败。SVG中的`class="Note"`及其transform可定位实际符头；本fixture的下手24头处于同一Y，可按X排序、每六个分一小节。输出SVG坐标为360dpi，除以5转换pt；其它版本先核查viewBox与物理尺寸，不能盲用换算。

新方案需要保留基线和相同宽度预算，分别验语义、同步、净空和视觉收益。不能通过给原谱加入隐藏发音/休止或缩短括号span强行取得等距。是否需要软件改动须由实际候选比较决定。

## 弧线与换行自制练习

[curves-source.musicxml](curves-source.musicxml)是原创四小节、双谱表材料，CC0；没有摘录用户或参考谱音乐。[curves-and-break.mscx](curves-and-break.mscx)是当前宿主导入后固定内置Leland/Leland Text、在m2后加一次换行的版本。谱表高度约7mm，仅是该练习的输入条件。可以直接读取原生文件；需连续版时，复制后去掉上谱表m2末唯一LayoutBreak，勿改用户工程。

题目包含：m1前两音tie，后两同音slur＋tenuto；m2–3长slur与低音tie；m4跨休止slur。[连续版图](curves-unbroken.png)和[跨行图](curves-split.png)均为180dpi原生PNG合白底后只裁去标题／页脚，保留完整音乐，未移动音符或调整曲线。

两版19个音头、1个休止、2条逻辑tie、3条逻辑slur相同，XML除一次LayoutBreak外完全一致；MusicXML重新导出核对音高、时值、起点、奏法和连接范围通过。SVG的tie/slur绘制段数由2/3变为3/4。图不是所有曲线规范均已验收的证明。详见[弧线专题](../CURVES_STUDY.md)与[证据](../curves_evidence.json)。仅本目录原创曲谱与其渲染使用CC0，参考官谱和教材不在此许可中。

## 独立声部的休止：拒绝案例

[voices-rests-source.musicxml](voices-rests-source.musicxml)为原创四小节双谱表练习，CC0。上谱表是两条持续独立的线，下表是低音；第二部在m1先停一拍、m3先停两拍。[保留版](voices-rests-shown.mscx)与[隐藏版](voices-rests-hidden.mscx)仅差这两个Rest的`visible=0`，固定Leland/Leland Text。隐藏版是此织体下不合适的编辑反例，不是改善候选；不能据此反向规定所有临时附加旋律都须显示休止。

两版29个事件含26个音头和3个逻辑休止，重新导出MusicXML核对音高、起点、时值、谱表及voice均同源练习一致。SVG可见Rest由3减为1。未做音频文件比较。[保留图](voices-rests-shown.png)与[隐藏图](voices-rests-hidden.png)均由当前宿主180dpi原生PNG合白底、使用同一裁框保留完整音乐，没有移动符号。完整理由见[钢琴织体专题](../PIANO_TEXTURE_STUDY.md)，宿主哈希与保护检查见[piano_texture_evidence.json](../piano_texture_evidence.json)。导出方式同本页前述命令，替换为相应自制输入，并使用独立配置和输出目录。

## 实际间距候选与迁移反例

以下均为原创自制音乐及其原生渲染，CC0，不包含用户或官谱音乐；完整条件见[间距候选](../SPACING_CANDIDATES.md)，哈希及限定核查见[spacing_candidates_evidence.json](../spacing_candidates_evidence.json)。保持真实内置Leland/Leland Text和同一版心。所有PNG仅合白底并裁去无关页边，未移动音乐符号。

- 极简：原输入为本页的[mixed-subdivision.mscx](mixed-subdivision.mscx)，[原排法图](mixed-subdivision-original.png)与[候选图](mixed-subdivision-balanced.png)对应；[候选原生谱](mixed-subdivision-balanced.mscx)仅改3个共同Segment前置间距和4个小节stretch。43个事件读回一致，16个共同起音同X，原生保存重载后几何/像素一致。
- 变音/双音：[源谱](chromatic-spacing-source.mscx)、[尝试](chromatic-spacing-attempt.mscx)及[源图](chromatic-spacing-source.png)、[尝试图](chromatic-spacing-attempt.png)。51个事件读回一致；复制极简设置没有解决末端宽间隔，不作为改善方案。
- 密集相邻和弦：[源谱](dense-spacing-source.mscx)、[复制设置](dense-spacing-copied-settings.mscx)、[仅在m2换行](dense-spacing-two-systems.mscx)及相应[源图](dense-spacing-source.png)、[3+1图](dense-spacing-copied-settings.png)、[2+2图](dense-spacing-two-systems.png)。各67个事件读回一致；2+2仅差一次LayoutBreak，所用垂直预算比原单行多，不能混作同一行的比较。

事件核对限这些每谱表单声部、无连音/附点/曲线的练习；不代表一般多声部归一化或碰撞校验器。原生导出方式同本页前述命令，输入替换为相应自制谱，使用独立配置与输出目录。具体试验数值只供复现，不当作通用净书默认值。

后续[变音参数实验](../ACCIDENTAL_SPACING.md)沿用`chromatic-spacing-source.mscx/png`基线，新增[更紧实验谱](chromatic-tight-accidentals.mscx)与[同裁框图](chromatic-tight-accidentals.png)，CC0。原生XML仅新增`accidentalNoteDistance=0.1`、`accidentalDistance=0.1`；这是分离符号占位与细分弹性的实验，**不推荐为全谱预设**。四条件音乐／记法、共同起点及联合版保存重载的限定检查见[证据](../accidental_spacing_evidence.json)。相同研究还重导本目录密集源谱，证明正常侧头对齐时，整组头的外框中心仍可偏移；没有增加新的音乐材料。

## 梁的坡度与导入层级：两个不同问题

[beam-shape-source.musicxml](beam-shape-source.musicxml)是原创八小节双谱表练习，CC0；[原生自动版](beam-shape-auto.mscx)和[全局平梁版](beam-shape-all-flat.mscx)除`Style/beamNoSlope` 0／1外完整XML相同，固定Leland／Leland Text。上部故意固定上干、四小节一系统、关闭页面纵向伸展，均是本fixture的控制条件，不是用户审美或真实乐曲默认值。原生PNG为[自动版](beam-shape-auto.png)和[平梁版](beam-shape-all-flat.png)，同一裁框保留两系统全部音乐，只合白底，未移动符号。

两原生版86个事件、MusicXML非布局内容及全部beam标签一致；Note／Rest／BarLine／StaffLines几何相同。自动版已按部分凹形、同音首尾、重复型等条件使用平梁，全局平梁会拉长普通上／下行组的一端。理由、干长与斜梁厚度测量见[梁干专题](../BEAM_STEM_STUDY.md)；[证据](../beam_rhythm_evidence.json)记录精度、范围与未做项目。

**MusicXML原输入与原生导入结果并非记法完全等同。** m7／8第四层要求单独断开的end／begin在导入后丢失，第三层仍保留。源输入共有44个梁层分段起点，原生导出及SVG为40；具体8个标签差异已记录。音高／时值等保持，下谱表单线voice标签2→5及未指定干向→up单独核对。不能由两个原生版互相一致反推导入无损，也不能以MusicXML往返作为一般原工程的完整保护。

复现坡度对照可直接按本页导出命令运行两个`.mscx`；复现导入限制则先把原始`.musicxml`导成独立`.mscx`，再导出独立MusicXML，检查m7／8第2、3、6、7个起音的`beam number="4"`。本轮没有修改宿主或为第四层制作视觉补丁。源码／宿主哈希、正文页和参考谱复核见证据；原书、官谱和用户音乐不在本fixture许可中。

## 双部二度的附点归属与变化同音自动样张

[自动版](seconds-dots-automatic.mscx)／[图](seconds-dots-automatic.png)与[m2换列候选](seconds-dots-between.mscx)／[图](seconds-dots-between.png)为原创八小节3/4，CC0，无参考摘录；固定Leland／Leland Text及版心，m4后换行。m1–6分别保留普通／交叠和单部／双部带点，m7／8观察双部及单和弦的C／C♯。仅m2候选增加两个Chord offset（上干部x=-1.4，下干部x=2.5，y=0），让点隔开两部；不是全局错位预设。

29音、19附点、MusicXML非布局、MIDI及候选保存重载均按此情境核查；两张PNG同裁框保留完整两系统。最终使用固定新宿主`7b4e6f…aa25`，不能与此前`fec7e2…cd77`的输出拼成参数对照；按本页原生CLI重画时记录实际宿主。理由、额外占宽和未做的斜接／分叉干候选见[二度归属](../SECONDS_OWNERSHIP.md)及[证据](../seconds_ownership_evidence.json)。

## 同音异时值与附点：按情境共头

以下是独立原创四小节3/4练习，CC0，无用户／官谱摘录；同一Leland／Leland Text和版心。上表两voice，下表一voice，31个音符、8个逻辑附点：

- [分头基线](unison-dots-separate.mscx)／[图](unison-dots-separate.png)：自动头型，四处异时值同音各自分头。
- [选择性共头](unison-dots-selective.mscx)／[图](unison-dots-selective.png)：只给m2／3上部首音加`headType=quarter`；用于反复梁组中可考虑的共头候选，未获用户选择。
- [全部共头](unison-dots-all-shared.mscx)／[图](unison-dots-all-shared.png)：再覆盖m1／4。本例不推荐将孤立交会也合头，不是所有共头的错误模板。

三版原生XML仅差上述headType节点；事件、附点、voice／谱表等与当前MusicXML对应，预期的显式normal／filled头型标签单独核对，其余非布局内容相同。MIDI逐字节相同，31条SVG Note绘制命令对应31／29／27个独立墨迹位置；选择性版保存重载保持。PNG只合白底、同裁框保留完整两手。原生导出方式同本页命令，使用独立配置及输出；这些检查不证明三版一样易读。完整理由和范围见[同音附点专题](../UNISON_DOTS_STUDY.md)及[证据](../unison_dots_evidence.json)。
