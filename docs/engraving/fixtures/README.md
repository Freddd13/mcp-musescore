# 独立净书复现谱例

## 十二对十一与联合时间轴间距

2026-10-23原创CC0两小节4/4、33音及两个八分休止，固定Leland／Leland Text、1.57mm sp、A4满行预算；音符独立设计，不是官谱转写。上方十二个普通三十二分、下方11:6十六分在同一时段运行，后者中途换谱号。

- [默认保留](poly12-11-auto.mscx)：共同开始与到达正确；未证明间距最佳。
- [隐藏谱号诊断](poly12-11-hidden-clef-diagnostic.mscx)：仅隐藏换号，内部音高解释仍切到高音谱号；不能采用。
- [单头移位拒绝](poly12-11-arrival-shift-rejected.mscx)：仅下部到达Chord左移5/6sp，同MIDI却误示先后。
- [两列留白试排](poly12-11-edge-reserve.mscx)：两目标ChordRest列各加1.25sp leadingSpace，主要重分小节预算，本例不采用。
- [四层原生图](poly12-11-comparison.png)：180dpi合白底、统一裁框保全部墨迹，标签在音乐之外，无符号移位或缩放。

四版33音的原生配方／MusicXML／完整MIDI核查分别记录；默认和留白版原生保存重载的SVG、原始RGBA、MusicXML除日期和MIDI相同。MusicXML分数精确，480 PPQ MIDI有小于半tick的正常舍入。隐藏谱号诊断的内部间距可用非线性弹性加最低宽度重建，但总宽只标定一个整体拉伸量；不证明一般排版最优、运行时分支或源码构建对应。无交换导回、打印、试听或用户采用。详见[研究](../POLYRHYTHM_SPACING_STUDY.md)和[证据](../polyrhythm_spacing_evidence.json)。

## 跨表共同梁、短干与拍内休止

2026-10-20原创CC0两小节4/4，26音、2个可见十六分休止及2个隐藏空表整休止容器；单线跨手，含八分／十六分／三十二分混合，非独立对位。固定Leland／Leland Text、spatium 1.57mm、同一水平预算，无官谱转写。

- [斜梁对照](cross-beam-baseline.mscx)／[图](cross-beam-baseline.png)：显式表边距6.5sp，最短音头谱位参考点→干端2sp，两处短休止在上表。
- [紧凑平梁与休止位置](cross-beam-flat-guided.mscx)／[图](cross-beam-flat-guided.png)：同表距、最短2.5sp；两Rest设staffMove1，靠近随后下表音。本短例倾向此版，非用户偏好或全谱平梁预设。
- [稍宽斜梁与休止位置](cross-beam-sloped-guided.mscx)／[图](cross-beam-sloped-guided.png)：表边距8sp、最短2.75sp；保坡度但多占高，另一可行备选。
- [切梁休止拒绝版](cross-beam-rest-cut-rejected.mscx)／[图](cross-beam-rest-cut-rejected.png)：仅改紧凑版拍中Rest的自动放置／y偏移，实际字形边界点进入填充梁，其它SVG图元保持；同完整MIDI仍拒绝，不是禁止所有中央休止。

九份探针／候选（其中以上四版随库保存）保26个预期起音与完整MIDI，所有音符非位置XML字段保持；两候选另经原生保存重载，SVG除标题、原始RGBA像素及MusicXML事件记录保持。XML的Rest仍staff1／voice1而default-y改变，不能仅据staff判移位丢失；本轮没有XML导回、试听、打印或偏好评测。图为180dpi原生合白底，同框(50,70,1450,500)，完整保留全部墨迹，无符号搬移／缩放。见[条件与理由](../CROSS_STAFF_STUDY.md#8-续读中部梁不是把所有东西放在中间)及[证据](../cross_staff_beams_evidence.json)；教材／官谱不属于本CC0材料。

## 同一谱表的八度作用域

2026-10-20原创CC0两小节4/4，16个写出音，固定Leland／Leland Text、spatium 1.57mm与同一满行宽度。上层E6／F6长值后接四分，内层C4／D4全音符，低表四分作时间参照；没有转写官谱，也没有模拟参考中的接收tie。

- [实际音高双表](octave-scope-at-pitch.mscx)／[图](octave-scope-at-pitch.png)：本孤立高音例倾向保留加线。
- [短八度错误控制](octave-scope-unsafe-staff-ottava.mscx)／[图](octave-scope-unsafe-staff-ottava.png)：只降低上层并加原生Ottava，内层D4字段／图面位置不动，实际却变D5，故拒绝；不是宿主错误证明。
- [分表八度版](octave-scope-separate-staff.mscx)／[图](octave-scope-separate-staff.png)：高层独立，保全部实际音乐，但增加一表，不是本例更美观的结论。

三版各16次NoteOn。实际音高／分表版的XML时间／实际音高／时长及合并轨道MIDI音符事件保持；轨道配置不同，不称完整MIDI字节相同。分表版另经原生保存重载，一页、SVG除标题、RGBA像素、完整MIDI及音乐XML记录保持。图为原生180dpi合白底，同框(50,50,1450,650)完整保留谱表，无符号缩放／搬动。无MusicXML导回、试听、打印或偏好评测。见[整页判断及规范](../INTEGRATED_READING_NINELIE.md)和[证据](../integrated_reading_ninelie_evidence.json)。教材／官谱不属于本CC0材料。

## 选择延音踏板的跨行持音提醒

2026-10-20原创CC0八小节4/4、双谱表，m1的A2／A3由选择延音踏板保持到m8边界，手在四分长度后释放，m5不重奏该八度。范围用TextLine显示，未模拟CC66／实际留声；同一Leland／Leland Text和两系统预算，不是用户片段转写。

- [无重述基线](sustain-baseline.mscx)／[图](sustain-baseline.png)：范围可读，需要回看初始音高。
- [括起小提示](sustain-bracket-reminder.mscx)／[图](sustain-bracket-reminder.png)：只将m5整休止换为两个不播放的括起小音头；是提醒记法提议，非纯几何移动。
- [普通音头控制](sustain-ordinary-note-control.mscx)／[图](sustain-ordinary-note-control.png)：相同位置改普通全音符但仍设不播放，原生MIDI相同而图面易误读，导回MusicXML还多出两个起音，故本例不采用。

原生三版均34次NoteOn；提醒版保存重载图／MIDI保持。提醒的cue与括号在实际XML往返保住，但释音、初始化控制和续行文字仍变化；不能称整个交换无损。构造时TextLine锚点及附点顺序的无效尝试另存私有缓存，最终核实际线条及单个时值。完整依据、原生保护与用户实曲保留判断见[专题](../SUSTAIN_CONTINUATION.md)和[证据](../sustain_continuation_evidence.json)；教材／官谱不属于本CC0材料。

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

## 谱号位置、轮廓与必要的可见参照

以下均为原创四小节3/4钢琴练习，CC0，无参考／用户音乐摘录；固定Leland／Leland Text、1.57mm sp，2+2分行。PNG由固定宿主180dpi原生输出合白底，四图统一裁框`(76,122,1412,733)`，保留全部两手及两系统，没有移动或缩放符号。

- [边界换号保留版](clef-boundaries.mscx)／[图](clef-boundaries.png)：m1休止后新组前换G，m2末预告F，下行直接F；m4短暂加线保留。
- [组中延后拒绝例](clef-late-in-group-rejected.mscx)／[图](clef-late-in-group-rejected.png)：只将m1换号延后一个八分，切开原可完整识别的二音组。
- [单音阈值频繁换号拒绝例](clef-frequent-rejected.mscx)／[图](clef-frequent-rejected.png)：少了加线，却反复改变音程参照；不代表所有频繁换号都错。
- [隐藏必要换号拒绝例](clef-hidden-change-rejected.mscx)／[图](clef-hidden-change-rejected.png)：后续音头仍依隐藏G定位，读者却只看到F；相同播放不能保护识谱。

四版XML除Clef节点外相同，实际MusicXML36条音休止及35个MIDI起音的时间／音高另与独立配方一致，完整MIDI相同。保留版原生保存重载的图形、原始RGBA、音乐、谱号和MIDI保持；没有MusicXML导回、试听或用户采用。首版输入构造错误保留在私有目录，未发布为有效练习或软件缺陷。具体理由、原生CLI、保护范围见[CLEF_READING](../CLEF_READING.md)及[证据](../clef_reading_evidence.json)。

## 矩形休止的立／挂：位置与读法

以下为原创两小节4/4、双谱表练习，CC0，无参考／用户音乐摘录。固定Leland／Leland Text、1.57mm sp；m1上表整小节休止，m2先二分休止再二分音符，下表八个四分音符。PNG由180dpi原生输出合白底，同裁框保留全部两手，没有移动或缩放音乐符号。

- [常规位置](rest-reading-baseline.mscx)／[图](rest-reading-baseline.png)：全休止挂在线下，二分休止立在线上。
- [半sp拒绝例](rest-reading-half-space-rejected.mscx)／[图](rest-reading-half-space-rejected.png)：只上移m2半休止0.5sp，实际仍两拍，却呈全休止式悬挂。
- [整sp位置控制](rest-reading-whole-space-control.mscx)／[图](rest-reading-whole-space-control.png)：只上移1sp，仍立在线上；此单部没有抬高需要，控制不当推荐候选。

三版11条音休止与9次MIDI起音的时间／音高对独立配方一致，完整MIDI相同；SVG除目标Rest／标题外相同。半sp拒绝版实际原生重载的图形、原始RGBA、音乐及MIDI保持，没有MusicXML导回、音响／打印或用户采用。完整理由、源码许可范围和坐标核查见[SYMBOL_READING](../SYMBOL_READING.md)及[证据](../symbol_reading_evidence.json)。

## 拼写、确认符号与邻位错头

原创CC0两小节4/4、五升调号的钢琴练习；固定Leland／Leland Text、1.57mm sp、A4，均1页1系统。两版仅两颗Note的tpc由F重升变G还原，数值pitch、时值、结构与其它原生字段不变。

- [功能拼写](spelling-functional.mscx)／[图](spelling-functional.png)：属七三度叠置、旋律相邻级进；本语境保留。
- [等音简化拒绝例](spelling-enharmonic-rejected.mscx)／[图](spelling-enharmonic-rejected.png)：相同键却改变音程读法，局部变音从2增到4，下方和弦需要邻位错头。它是记法反例，不能当纯外观压缩。

两版各17条音符与17次MIDI起音对独立配方一致，完整MIDI相同；拼写差别也按预期读回，并未称记法不变。十条谱线几何一致，180dpi原生图只合白底并统一裁框(145,130,1400,376)。功能版原生重载的拼写、SVG、原始RGBA与完整MIDI保持；没有拒绝版重载、交换导回、试听／打印或用户采用。理由和保护边界见[音高拼写](../ACCIDENTAL_SPELLING.md)及[证据](../accidental_spelling_evidence.json)。

## 行首已有留白与显示变音占位

原创CC0四小节4/4、钢琴双表，Leland／Leland Text、1.57mm sp。七个显示控制只增加非必要的USER还原号；固定整行宽、两行各两小节，是诊断材料，不是出版排版模板。

- [基线](leading-base.mscx)；曲首[一个](leading-opening-one.mscx)／[三个](leading-opening-three.mscx)；[曲首对照图](leading-opening-comparison.png)。
- 后续行首[一个](leading-row-one.mscx)／[三个](leading-row-three.mscx)；[对照图](leading-row-comparison.png)。
- 行中小节[一个](leading-inside-one.mscx)／[三个](leading-inside-three.mscx)；[对照图](leading-inside-comparison.png)。
- 正确首ChordRest Segment的[单符号留白控制](leading-one-reserve.mscx)和[三个超额压缩拒绝例](leading-three-overreserve-rejected.mscx)；[四层对照图](leading-reserve-controls.png)。前者本例可行但未作用户采用，后者虽共同头列／MIDI相同仍挤到拍号。

九个输入各40音对独立配方，完整MIDI相同；两局部控制实际保存重载。单符号版SVG图元及原始RGBA完全相同，三符号版一个还原号的SVG x因精度变化0.001单位，RGBA相同。PNG均原生180dpi合白、统一裁框，不移动或缩放谱面符号。没有交换导回、实曲迁移、试听或打印。理由、首次Segment目标构造错误和实际配置环境见[行首研究](../LEADING_RESERVE.md)及[证据](../leading_reserve_evidence.json)。

## 跨表弧的路径、干端与有效手动形状

原创CC0两小节2/4、两条完整独立部，固定Leland／Leland Text、1.57mm sp。下降十六分线和上行八分线分别跨表，不包含官谱／用户音乐。

- [自动基线](cross-slur-auto.mscx)：尾部穿过两条梁。
- [干侧控制](cross-slur-stem-control.mscx)：避梁但归属／轮廓有代价，本例不作主候选。
- [保留的头到头外绕](cross-slur-head-route.mscx)：只改该Slur的局部绘制点和自动避碰。
- [同框三层原生图](cross-slur-routing-comparison.png)：180dpi输出合白底、共同裁框，不移动或缩放符号；英文标签在音乐之外。

实际全部十条件保14音、拼写、显示谱表、梁、连接及完整MIDI，非Slur绘图相同；保留版原生保存重载的图形／RGBA／音乐／MIDI相同。其余尝试保存在忽略目录；没有交换导回、打印或用户采用。具体阅读取舍与自动避碰连动见[跨表弧研究](../CROSS_STAFF_SLUR_ROUTING.md)，这些点位不作通用预设。

## 五连内部进入与局部脉冲间距

原创CC0两小节2/4、21音及2休止，固定Leland／Leland Text和空间条件。两5:4三十二分组与另一表q3/4进入共存。

- [默认](five-four-spacing-default.mscx)／[局部候选](five-four-spacing-pulse-candidate.mscx)／[原生同框图](five-four-spacing-comparison.png)。
- 默认共同时间本已正确，候选只重分两五组的共同区域，保护组端点、普通三十二分及末十六分的区别，并同步调整下方位置。
- 发布120mm两版各实际保存重载，SVG绘图、原始RGBA、MusicXML除日期及完整MIDI保持。三宽度研究、改变音乐的诊断和首次构造失败见[专题](../FIVE_FOUR_SPACING_STUDY.md)及[证据](../five_four_spacing_evidence.json)。offset依赖当次宽度，不解决窄版最低小节预算；未作用户采用、试听／打印或实曲迁移。


## 20对6：局部脉冲与小节预算

原创CC0两小节4/4、双表34音，上方四组5:4十六分，下方六个入口0／1／1½／2／3／3½拍，第二小节两表各四个四分。固定Leland／Leland Text、1.57mm sp、140mm版心。

- [默认](twenty-to-six-default.mscx)／[局部候选](twenty-to-six-pulse-candidate.mscx)／[同框图](twenty-to-six-comparison.png)。
- 候选重分q0到q3.8内部，联动两手23个Chord偏移，再补第一小节stretch；不是单参数因果或全局等距默认。
- 两份发布输入都经过原生保存，再次重载的SVG／原始RGBA／完整MIDI／MusicXML除日期精确保持。四个5及完整两手和后续小节均在图内。

三宽度、初步移位的连带变化、两探针和限定检查见[研究](../TWENTY_TO_SIX_SPACING_STUDY.md)与[证据](../twenty_to_six_spacing_evidence.json)。没有参考音乐摘录、实际工程迁移、打印或用户采用；100mm内部候选仍两行。

## 20对6：单变音与密集二度和弦

接前一无变音练习，仍为原创CC0两小节4/4及四五连／六入口；固定Leland／Leland Text、1.57mm sp、140mm版心。

- 单变音34次音符起音、三个必要符号：[默认](twenty-to-six-single-default.mscx)／[保护占位候选](twenty-to-six-single-candidate.mscx)／[原生同框图](twenty-to-six-single-comparison.png)。两份均原生保存并再次重载验证，候选补第一小节预算，后续变化小于0.001sp。
- 密集版38次音符起音、九个必要符号：[保留默认](twenty-to-six-cluster-default.mscx)／[拒绝的均匀目标](twenty-to-six-cluster-uniform-rejected.mscx)／[同框图](twenty-to-six-cluster-comparison.png)。两份仅原生四格式导出核查，未认证保存重载。必要占位仍在，拒绝版把后续头推右约3.175sp。

[研究与理由](../TWENTY_TO_SIX_OCCUPANCY_STUDY.md)、[实际配方及证据](../twenty_to_six_occupancy_evidence.json)。10完整条件、53次成功CLI；没有参考音乐摘录、用户原件改动、实曲迁移、打印或用户采用。

## 全局Spacing的五档参数控制

原创CC0钢琴双表、一小节8/4；上表五个C5为四分／八分／八分／二分／全音符，下表整小节休止。固定Leland／Leland Text、1.57mm sp与180mm版心，末系统不撑满。只改变全局measureSpacing，用于理解控制意义。

- [0.8诊断输入](spacing-factor-080.mscx)／[1.0](spacing-factor-100.mscx)／[1.2](spacing-factor-120.mscx)／[1.62](spacing-factor-162.mscx)／[2.0](spacing-factor-200.mscx)；[五层原生同框图](spacing-factor-comparison.png)。
- 五版独立配方及五个实际MIDI起点保持，完整MIDI相同；0.8与1.0的原始RGBA相同，界面最低1，0.8仅作诊断。1.2／1.62发布输入已原生保存并重载，SVG／RGBA／完整MIDI／MusicXML除编码日期保持。其余三版仅核四格式导出。
- 图保完整双表与同一物理比例，文字标签位于音乐之外；只合白底并裁页空白。它是参数控制，不是美化候选、审美选择或全谱预设；[理由与手册缺图](../MUSESCORE3_LAYOUT_READING.md)、[来源及证据](../musescore3_layout_reading_evidence.json)。

## 三十二分的内梁层级

原创CC0四小节4/4双表，84书面音／83攻击，Leland／Leland Text、1.57mm sp、180mm版心，实际三系统。

- [全连续](inner-beams-continuous.mscx)／[四加四](inner-beams-four.mscx)／[完整分层](inner-beams-nested.mscx)。
- [快层两手同框](inner-beams-comparison.png)／[四小节上下文](inner-beams-full-context.png)：180dpi原生PNG合白底，共同裁框及比例，标签置于音乐外。

各版本只差BeamMode；发布输入为原生保存版并更正共同source说明，均实际重载核SVG与再次保存。原生、MIDI配方及MusicXML导回的逐层梁保持；首存手写输入的精度差异、完整核查与候选理由见[专题](../INNER_BEAM_HIERARCHY_STUDY.md)及[证据](../inner_beam_hierarchy_evidence.json)。没有实曲迁移、打印或用户采用。

## 部分梁连音的短括号

独立原创CC0四小节4/4钢琴双表，52书面音／52攻击、两系统。固定Leland／Leland Text、1.57mm谱间及180mm版心。

- [A裸数字](partial-tuplet-bare.mscx)／[B短括号](partial-tuplet-short.mscx)：两份原生保存且重载输入；只差两处部分梁括号显示，完整六连控制保裸数字。
- [自动探针](partial-tuplet-auto-probe.mscx)：手写输入仅核SVG／MusicXML导出，未认证重载。
- [第一行两手对照](partial-tuplet-brackets-comparison.png)／[四小节上下文](partial-tuplet-brackets-full-context.png)：共同原生保存基线、180dpi、同框同物理比例。

[理由与范围](../PARTIAL_TUPLET_BRACKETS_STUDY.md)及[证据](../partial_tuplet_brackets_evidence.json)记录22次CLI、精确分数配方、逐层梁、MIDI量化、原生重载及自动漏显的具体条件；没有实际打印、实曲迁移或用户采用。

## 嵌套三连的范围与垂直层级

2026-10-29原创CC0三小节4/4、29音，固定Leland／1.57mm／180mm版心。主梁六音的实际末拍1/9×3＋1/6×2＋1/3；次梁3＋2＋1，下方三连八分保三处共同列。

- [A内层省略](nested-tuplet-implicit.mscx)、[B显示但自动同高](nested-tuplet-auto-position.mscx)、[C外层分层](nested-tuplet-tiered.mscx)及[同框图](nested-tuplet-comparison.png)。

三版保存／重载、分数时值、音位和完整MIDI保持，480PPQ最大误差2/3tick；C仅在B上外层p1/p2上移1.25sp，B同高相叠不采用。图为180dpi原生保存重载后合白底／同框裁切，无符号移位缩放。初次错误次梁指令探针保私有，不发布；最终30次CLI、总60次。[判断](../NESTED_TUPLET_SCOPE_STUDY.md)及[证据](../nested_tuplet_scope_evidence.json)，原官谱与用户谱不属本CC0资产。
