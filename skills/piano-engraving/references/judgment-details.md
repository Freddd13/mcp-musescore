# 按问题读取的判断提醒

这些段落从 skill 正文移到这里，保留条件、反例与来源。只读当前问题对应的小节；随后用定位器返回的知识库文件追到具体谱例。相同外形不代表相同音乐角色，旧实验数值也不是通用预设。

目录：[作品定义](#interpretation) · [符号](#symbols) · [拼写](#spelling) · [持音](#sustain) · [页面](#layout) · [输出](#output) · [间距](#spacing) · [节奏](#rhythm) · [跨表](#cross-staff) · [力度](#markings) · [装饰](#ornaments) · [速度](#tempo) · [自由段](#free-passage) · [换号](#clefs) · [八度](#octaves) · [导航](#navigation)

<a id="interpretation"></a>

## 作品定义与作者说明

遇缩写／脚注先查本谱首次出现、前言和局部限定。作品已有明确定义时采用，不反复让用户解释，也不让通用缩写歧义压过该定义；名称已知、动作范围和播放是否实现分别记录。作者后来确认的音乐功能应更新旧假说，软件对象类型不能压过该说明。`curves`中的`SUSTAIN_AND_RESTS.md`记录本谱A八度由选择延音踏板保持、两条Slur表示持续的作者确认：不按普通分句处理或因同端点去重，精确释放／逐条对应仍不擅补，也不将含义说明记成线形偏好或采用候选。不以MIDI相同代替这些判断。

<a id="symbols"></a>

`INTEGRATED_READING_RUMBLING_AETHER.md`：Aether两组六个小音约60%同字形字号、m51三下＋三上，兼有首处低音保持；不凭小字猜借时或填普通8。

`INTEGRATED_READING_DEAREST_HERO.md`：P11组是两梁16／11:6；短次梁7.53pt会被>8探针漏掉。原图、完整时长、层次与实际矢量共同核，单一字符／矩形阈值不能直接定语义。

`INTEGRATED_READING_MELISSA_MERRY.md`：M局部3只管三头，普通尾8另算；N完整独立七连梁保裸7。B两音附点二分震音整对三拍，变化处写出。

`INTEGRATED_READING_KIMI_KIZUNA.md`：N前八分接收之后八双梁头占一拍半，优先完整8:6；22整小节与11半小节分别计量。不能把错位和弦头当两个先后音，亦不按相似梁形补齐头数。

`INTEGRATED_READING_KEY_KICK.md`的计量音型加gliss.与叉头波线分判。p326偏好动作线，但替换须明确保总时长、端点身份和独立停止；开头5:4及末尾四个十六分加一四分的书面组织不证明逐键精确指法。

`glissandi`／`piano`的`INTEGRATED_READING_DEPARTURES.md`将竖琴拼写／七踏板／滑奏限定于弦与脚的动作条件。可迁移预读与范围清楚，不向钢琴套禁用重升降号等专用惯例。

`notation`的`INTEGRATED_READING_CRY_DAISY.md`把震音两端按共同持续计量；内部／预置钢琴的结果音、键与触弦动作分开。管风琴Ped.、8′／16′及manual说明按乐器语境读，不成为普通钢琴的踏板缺省。

`notation`／`piano`的`INTEGRATED_READING_BUTTERFLY_SILENCE.md`补F约75%小头的3拍计量、G正常头与小头华彩：字号本身不决定grace、cue或播放，大小头同刻的PDF绘图也不直接等于两次攻击。小头、缩谱表及指挥总谱压成一表各有用途；先确认实际演奏者与阅读任务。

## 字形和谱位的身份

`notation`／`ornaments`的`SKILL_TRANSFER_NOTATION.md`补T06成对情境：m65正常头10／5需保一休止九音及组外八分，拆行不重开小节；尾声24头约0.75，放大图曾掩盖尺度差，现按实际矩阵及自由收尾上下文纠正。字号、梁层或时值总和先触发核查，不能直接决定grace／不播放cue，亦不自动补24:16；同时保护背景持续与真正落点。

小音符先辨功能：`notation`经`NOTATION_DETAILS.md`接入`EDITORIAL_ALTERNATIVES.md`的ossia、条件性playing cue和主次线提示。字号、括号或cue字段不能独自决定是否演奏；替代读法与主谱同时播放、把密集段改成小谱表都可能改变内容，不混入外观净书。本轮仅教材条件，未有原生／交换验证。

符头形状、休止与谱线的关系都参与读法，不按duration／MIDI不变就判外观安全。`notation`／`rhythm`中的`SYMBOL_READING.md`连接空心头、线重、加线及普通五线谱休止的条件：整／二分矩形休止的立／挂关系要保住；同拍内几个休止可局部同高，独立部与跨梁又可纵移。原创半sp上移反例保9次起音和完整MIDI仍似全休止，整sp控制不等于本例需要抬高。核目标谱线及有效基准，不按offset是否整数批量修改；特殊谱型、其它Rest字形和cue另查。

<a id="spelling"></a>

## 音名、变音与等音换写

`notation`的`ACCIDENTAL_EDGE_CASES.md`补不同表调号和特殊音高符号的边界：先核定义、基准、所属表、状态与取消。必要音高修饰不照搬提示变音的上方写法，不按MIDI整数、字体或tuning字段猜制度，也不为普通钢琴制造微分音。

变音多不等于拼写错。`notation`中的`ACCIDENTAL_SPELLING.md`以Idol／IRIS OUT和原创原生例说明：重升可保持和声三度或邻音组形；只换两个tpc，17次起音和完整MIDI相同，却多出确认符号并形成邻位错头。半音阶上行升／下行降是条件惯例，不能压过和声或全句一致性。等音换写单列为记法提议，不当作无损压缩；读回后续符号和行页，不能从12个MIDI音级重建原拼写。通常同一人同表的手／voice切换也不自动重置变音，其它制度与范围先查本谱说明。

<a id="sustain"></a>

`INTEGRATED_READING_WORLD_REASON.md`：Reason C／I干奏随后明确踏板，不覆盖整段；交替全音震音共享4q，WORLD末前休止保真实层与时点。

`INTEGRATED_READING_RUMBLING_AETHER.md`：Rumbling末二分tie接收后二分休止，旧整小节休止勘误；小音组首低音保持另保护。

`INTEGRATED_READING_EVERLASTING_HEROES.md`：Heroes L四whole有重音、无跨小节tie，四次书面起音应保；末tie接收8后是休止和延长等待。

`INTEGRATED_READING_SAKAYUME_SAYONARA.md`：同页attacca后先接旧低音；末上部四次全音重奏对低部tie，随后sfz跨小节tie及最后两表延长休止分别保留，不把空白当废小节。

`INTEGRATED_READING_RESONANCE_RISING.md`：Resonance末尾两全音的上下音均tie；裁图漏弧顶不等于重奏。Rising上部开放持续与下部收尾分读；震音端点共享时段。

`INTEGRATED_READING_GOD_POKEMON.md`的H与I改变低音持续、低八度、休止、踏板及手。相似材料用于检查一致性前先核音乐差异；不能直接复制再现或假定演奏等效。

`curves`／`piano`／`cross-staff`的`INTEGRATED_READING_EONIAN_EUTERPE.md`保长低音与延迟短型、慢层和快线／手括形。吉他的同音双弦、技术slur、制音、泛音与定弦各有动作定义；相同音高／外形不提供自动去重或同一执行依据。

`curves`／`piano`的`INTEGRATED_READING_LAZY_EIEN.md`保开放余响、完整tie、legato与短动作弧的区别。竖琴制音小音指停止哪根弦，等音双弦仍是两个动作对象；播放相同／无起音不提供自动去重依据。

`piano`／`notation`的`INTEGRATED_READING_COLORS_CROSSING.md`把排练缩谱减密与独奏净书分开：供读cue、替代执行、持续与必弹活动层须先识别用途。不能依据缩谱规范删独奏音、cue化或不播放；L的明确等待、D的三层入口和短拍tie接收仍保留。

`piano`的`INTEGRATED_READING_CATCH_CHANGE.md`补低部休止／踏板释放以后，上表完整tie和手持层仍可继续；末尾两条旧低音链旁还有新的二分攻击。逐层核接收、新攻击和释放；斜虚线落向已有tie链，不据此补一颗新攻击或换成gliss.。

`piano`／`curves`／`tempo`的`SKILL_TRANSFER_CONTINUITY.md`补T07：干奏下可有手持长和弦，开放弧到休止与完整tie接收分读；I与K踏板模式分别建立，simile不能跨模式复制。ad lib.两音震音的两个附点二分共同占三拍，再接一拍；不顺次相加或由三梁指定攻击次数。


## 持音、提示与结束边界

`piano`／`curves`中的`LILYPOND_KEYBOARD_CASES.md`补LS04：On／Off配方保持时，线端仍可延长、末钩可改变，人看到的释放位置也可能改变。先分别核实际控制与可见范围，不由MIDI相同或线尾位置补作者未知时点；LS01隐藏音弧端与LS07隐藏干tie不可混用。

`SUSTAIN_CONTINUATION.md`接入Here整曲：完整tie、开放留声弧、两个踏板标签、中途一次释放再启与末端双星分别核。不能由两颗星的高低擅配控制，也不能把完整tie一律解释成手持；sus.名称／花体字形与独立延续线有规范问题可比较，但先保实际动作与未知，不将另一作品S.P.的作者定义外推。

持续提醒先分中途续行与结束边界，再分手持、中踏板已保持、无声按键与新攻击。括起持音还可能说明手已释放；菱形无声按键不能按“同样没有起音”互换。`piano`／`curves`中的`SUSTAIN_CONTINUATION.md`保留用户m135不加提示的判断，并用原创例区分字形大小、括号、cue身份和play设置；捕捉子集不等于挂接的全部和弦。增加提示是记法提议，原生与交换分别核查，不能仅由括号／sost.字串识别踏板。

<a id="layout"></a>

`INTEGRATED_READING_EVERLASTING_HEROES.md`：N在p7页末、Heroes p5末快速段续页，翻页未核；可比新页起段，但须核两页容量和两手。

`INTEGRATED_READING_SILHOUETTE_SIRIUS.md`：p4末三个pp四分引子可与p5J比较完整小节组合，先核次页五变六小节的预算；常规奇数右页下p4／p5同开页，跨页阅读候选不能称为物理翻页已改善。

`INTEGRATED_READING_KURA_KUUSOU.md`：H半小节同页跨行增加计数负担，完整留行须权衡相邻系统容量；提议未原生重排，不将方向写成已改善，也不推出固定小节数。

`INTEGRATED_READING_KIGEKI_KILLY.md`：Killy H页末无结束小节线，p4／5的2＋2合一个4/4。优先比较完整小节续页，查整页密度；十／六拍变八／八拍不证明容量相等，页界也不等于物理翻页。

`INTEGRATED_READING_FUBUKI_CASTLE.md`分别核3＋1跨页、2＋2同页拆小节。先读完整计量和真实行末线，再比较同页容纳或续接提示；加提示不能独自消除跨页操作代价。

`layout`的`INTEGRATED_READING_LAZY_EIEN.md`核同一4/4在两行各写两拍，右端无小节线、另一手也对应。先合逻辑小节再量宽度；优先比较续行提示，整小节版需连相邻行重排。

`overview`／`layout`的`SKILL_TRANSFER_PAGES.md`补T08：纸面p4／5可同一对开，真实D.S.却需回p3再去p5。先列实际来路和媒介；写出返回16小节、约增四系统是条件性纸谱候选。延长、事件间隔与空手窗口分查，行中H／J／K不为齐头先重排。

## 页面的空间层级

`PAGE_FLOW_STUDY.md`接入Link整曲及Adabana：伴奏准备、旋律进入、页末和实际翻纸不同；较早四小节上表休止距页界仍有12小节，不证明空手窗口。首音乐页左右和媒介须明确。拆小节符合完整拍和开放行尾，也未必满足Gould所限的全部例外；九小节跨两行不直接等于三小节分两行，不把出版身份当规范豁免。

`layout`／`navigation`／`sources`的`MOLA_READING.md`保留完整英文对照：乐团分谱与独奏用途分开，中文仅偶数左页上角有误；line／voice与纸幅端点另核。行首编号、长休止数量／范围和排练字母各有定位任务，影视／音乐剧逐小节编号是明确例外。等待中保速度／拍号及有用cue，准备与下一次进入分判；钢琴另一手已可见时不自动复制cue。谱高按五线底至顶，换封面／分行后核物理对开与横向持续、纵向同步和标记归属。系统读量可预期不推出固定小节数／等距头。

行尾不一定是逻辑小节终点。`layout`中的A011整首实例以时值、开放行尾、跨行tie和矢量共同确认两拍处拆行，两个可见半段仍是一个4/4小节。保住计数、变音与导航，不按系统号重置，也不把按竖线／可见区间所得的数量当工程小节数。拆行是有代价的候选，普通完整小节安排仍可比较；不由出版实例声称当前宿主已有此能力。

页面问题先分表内、系统间和最外印刷内容；同宽截图不等于相同物理谱高。谱线等距不等于实际白带等宽，而没有贯穿整行的白带也不证明碰撞；按局部轮廓与归属判断，不把外框或空白比例当美观分数。`layout`专题连接`PAGE_HIERARCHY.md`的实际正反例；PDF对象先核真实可见页，完整页外图元也可能混入统计。

<a id="output"></a>

T08在后续整曲核查中漏看末尾贴谱线的tie，后由两手放大图和三次贝塞尔路径纠正；冻结相邻页初判未改写。外框0.162pt没有包住弧顶，不能以缩图或提取外框宣告缺线／重奏，先查实际墨迹。

## 输出管线与疑似断口

线重／弧端看似灰淡或断开时，先核完整上下文、裁图与矢量，再比较同物理尺寸／输出管线。相同几何的原生PNG与PDF栅格化可显不同黑度；曲线提取框甚至可能只反映端点，不能据零高外框判没有墨迹。`curves`／`baseline`中的`OUTPUT_READING.md`有真实保留反例，不为预览表象补接或加粗工程。

<a id="spacing"></a>

`INTEGRATED_READING_WORLD_REASON.md`：WORLD I保八分步幅；Reason十四16保升号前缀，再现换密度不照搬宽度。

`INTEGRATED_READING_RUMBLING_AETHER.md`：Aether m20–24六8近稳；6/8重复首宽格另核长值／附点／加线，不以出版身份认定最优。

`INTEGRATED_READING_EVERLASTING_HEROES.md`：C重复宽处受加线限制，压到5.932pt解析上会交叠；O／G／H稳定活动仍保。

`INTEGRATED_READING_TABI_TAMASHII.md`：H／I／J快层有稳定步幅，慢线、和弦及接收独立；F近头3.546pt仍先后，实际干轴8.352pt。

`INTEGRATED_READING_SUZUME_SWORDLAND.md`：M二度移头与q2tie接收空间同看；D交替头距不同，实际六干轴近等距。速度改变不按播放秒数重画书面间距。

`INTEGRATED_READING_STYX_SUGAR.md`：跨表头距0.709pt仍可先后1/6q，六符干轴序保留；21下部q1/2/3在上部成员之间。J普通8为前缀／细分让空间，不按头距方差吸齐。

`INTEGRATED_READING_SPECIALZ_GHIBLI.md`：F下部q1/2在上七连3/7与4/7之间，保真实中间列及组形；E／X普通16稳定，二度移头不增攻击。

`INTEGRATED_READING_SNOW_SPARKLE.md`：普通16、普通32、三连8和七连16分别比较，先保稳定活动与必要还原号占位；黑度相近不证明同值，慢层保持与进入另核。

`INTEGRATED_READING_SILHOUETTE_SIRIUS.md`：先保稳定活动；C下部q2.5夹在五连q2.4与q2.6之间，不能按最近符头吸齐。白头可占一个快列，和弦多头也只一时点；混合值与普通16分判。

`INTEGRATED_READING_SHINZOU_SHIRUSHI.md`：同1q的7／6／5单步可不同宽；25快音＋6三连攻击共28列，只在q0/q2/q8/3同起。先保组形、共同到达和中间先后；B8、M16、K32与必要前缀分别判断。

`INTEGRATED_READING_SAKAYUME_SAYONARA.md`：12/8的24个普通16与六连分判；活动角色可换到下表。保重升号／换号真实占位，再查小节预算，头原点不能当干轴。

`INTEGRATED_READING_RESONANCE_RISING.md`：B／F组内稳定但相邻小节预算不同；I普通8、L末8／附点8不混成全16。先认角色与真实值，再查前缀和整行预算；R20补谱表／系统／框等不同空间层级。

`INTEGRATED_READING_RAILGUN_PIERCE.md`：Railgun14列含普通8，不能全按16匀；R22两图只说明时值层级重分预算，另查前缀、共同列及局部弹性。

`INTEGRATED_READING_KISS_CHANCE.md`／`NESTED_TUPLET_SCOPE_STUDY.md`：Kiss普通16骨架约6.894–7.092pt；Chance不同预算下列宽可大不同，先核角色／前缀净空，不移同刻头。

`INTEGRATED_READING_NAGI_NIER.md`：Nagi L16步幅约9.900–9.918pt；X前缀局部占位可保。NieR12/8二连第二音落在下部普通8之间，不能最近邻吸齐。

`INTEGRATED_READING_SOUL_WAR.md`：War较紧F升号前局部12.591pt，较宽J约14pt仍保组形；先查前缀自身和预算，不按单一均匀度误报。

`INTEGRATED_READING_DEAREST_HERO.md`：保活动层及P12／11各自组形，既有首到达−3.545pt仍是局部候选；整齐不能掩盖真实共同末点。

`INTEGRATED_READING_MIIRO_MIXED.md`：Miiro A各16列保稳定活动；8.682–8.899pt是本例观测，别直接泛化。

`INTEGRATED_READING_MELISSA_MERRY.md`：保H稳定8、I升号占位；F头距13.806pt而实际干轴9pt，先分前缀／连接侧。

`INTEGRATED_READING_KYOURAN_CONAN.md`：H／J／L保稳定快层，J首步还原号有占位；Conan F是12普通16再四分，不把13列都当同值。

`INTEGRATED_READING_KURA_KUUSOU.md`：Kuusou同拍6对5保真正共同拍点与内部先后，不逐头吸齐。Kura H完整比例为条件重建，跨线后头位同列不足以证明时间同步，先核音乐再动坐标。

`INTEGRATED_READING_KONOSUBA_KUCHIZUKE.md`：J首小节无前缀约8pt、有前缀10–15pt，先给符号合理占位；K两手16列共同。连续层稳定与每步几何相等分开，保真实移头／前缀，不直接套官谱坐标。

`INTEGRATED_READING_KIMI_KIZUNA.md`：22组头距5.513–9.971pt、实际干轴9.720–10.560pt；先查跨表连接侧，不能为头距统一拉宽。U末15列是14十六分＋一八分，起点近稳不证明全同值。

`INTEGRATED_READING_KIGEKI_KILLY.md`：快层最大宽步可由另一手还原号或换谱号占位解释；先查完整两手与行预算。advance框能定位字符，不能证明最小墨迹净空，亦不能把另一行的均匀步长直接复制。

`INTEGRATED_READING_KEY_KICK.md`的R相邻3/4小节线间65.340／54.720pt，扣到首头后均48.798pt：先区分前缀和音符区，不能把拍号占位报成同值音组拉散；P／I稳定活动层仍应保留。

`INTEGRATED_READING_IMAGINATION_POOL.md`的跨表11:6，头左缘1.080–10.575pt而干轴5.400–6.000pt，先保干向／连接造成的头位；B共头与M不同休止又分别有节奏职责，不从头距或轮廓数量直接触发均匀化／删音。

`INTEGRATED_READING_ICHIBAN_IDOL.md`有F跨表5＋11头仍稳定的普通16，以及5:3中途加入四分仍保近稳组形的正例；先辨实际比值和相邻时点，不能逐头配对或将变音所需宽度一律抹平。

`LEGATO_RAVEL_READING.md`用二度和弦、重复四分与四连对普通八分作对照：先把同刻错头归组，再核另一层细分和变音占位；同类重复的必要宽窄可保留。各层独立等距后逐列吸附会制造假重合。

`INTEGRATED_READING_GURENGE_HACKING.md`：F普通16及G普通8分别近稳，保下层进入与持续，小节边界另判；逐组选择时间参照，不因慢层复杂就认定需要扩大一格。

`INTEGRATED_READING_GRAND_GREAT.md`的M跨表交替，头距6.894–17.352pt而干轴11.664–12.546pt；保脉冲及先后。先选实际阅读参照，不吸两手为同列或把头x均分。

`INTEGRATED_READING_GOD_POKEMON.md`的五连对八分保近稳快层，下层中间进入未撑洞，普通16略宽。可作为同构原生例的正向参照；不能推制作软件或把几何等距当单独目标。

`INTEGRATED_READING_FUBUKI_CASTLE.md`的K内部十六分近稳，跨小节距离另含小节线与下层变音预算。分组内、拍间、边界和重复材料检查，不拿全行方差直接选候选。

`INTEGRATED_READING_FATE_FRIEREN.md`的交替和弦头位一宽一窄，实际干轴近等距。先确定读者跟随的光学参照；相反干向不能按同一头x均分。

`INTEGRATED_READING_EVERYDAY_EXTRA.md`核五连对八分：后半拍位于快音第3／4之间，却未撑宽该格；同20头在下行宽约26%又近均匀。先看实际占位与行预算，保护两手顺序，不按中间事件数直接判宽格。

`spacing`的`INTEGRATED_READING_EONIAN_EUTERPE.md`量54头重复疏密及加线净空：压最短会碰线，拉最宽又需额外37.44pt，保留。EONIAN中小节三音轻微长短列候选；下层复杂不直接证明更细中间时间点或唯一成因。

`spacing`的`INTEGRATED_READING_LAZY_EIEN.md`实测普通16分与续行6组近稳定，按各自单位／行预算保留。Lazy半音运行比例缺失，10:6／9:6仅条件重建，不能按几何步长生成已确认时间。

`spacing`的`INTEGRATED_READING_DEPARTURES.md`对照两个13组：窄处变音前宽格明显，宽处近稳，先比较整行重分／符号占位。末头多一个降号，不能标为同输入；有理由列候选，不直接归因引擎。

`spacing`的`INTEGRATED_READING_CRY_DAISY.md`比较同源同字号25头：跨度差约14%，局部六／七组仍稳定，保留按行容量变化。先把首组六连中的休止归组，再评局部突变，不固定全曲步长。

`spacing`的`INTEGRATED_READING_COLORS_CROSSING.md`提供三次重复七连：同一格因下层中间进入稍宽，组形仍稳定，可保留；更匀候选仍须保该列。缩写震音要辨整段持续及是否无定量，不能按两头或假定播放次数估宽。

`spacing`／`layout`的`MUSESCORE3_LAYOUT_READING.md`用五档原生参数控制区分整体松紧与时值曲线：Spacing=1.62不使所测四分／八分距比变成1.62。源码的Beam Local relayout只改该组内部ChordRest，不能当两手共同列优化；真实配对先保护，再比较局部重分。手册文字与当前源码／原生结果冲突时，记录版本与具体证据，不按同名参数传值。

`spacing`／`layout`的`INTEGRATED_READING_DANGO_HANEZEVE.md`提供同一五头主题的对照：五／六小节行改变整体展开约26%，组内长短形状仍熟悉。先匹配实际音值及背景，再分组内稳定与整行预算；不复制原点距离，不将所有宽度变化归因于符号密度。`piano`同例保留B的独立入口休止，并把Gould多人共表规则与键盘共干／辅助旋律干的条件分开。

`spacing`中的`TWENTY_TO_SIX_OCCUPANCY_STUDY.md`补实际占位取舍：单变音保护三处符号空间、重分余白并补预算后有局部候选；密集二度和弦普通格已稳定，保留默认。全区均匀目标没有造成预想碰撞，却把下一小节推右约3.175sp，故因收益与预算拒绝。实际占位、剩余空白及后续分配分查，正常侧头不用整组外框中心替代；0.01sp缓冲和本例offset均不是预设。

`spacing`中的`TWENTY_TO_SIX_SPACING_STUDY.md`补可行联合候选：同一4/4四五连／六入口在三宽度默认均有宽格。只改Chord offset会使后续小节移动约0.12／0.15sp，须重新核预算；本例再补一个测得的Measure stretch才保持区域外位置。发布两版已原生重载，100mm仍两行；这组参数不直接迁移到带变音、和弦或曲线的材料。

`spacing`的`SKILL_TRANSFER_PAGES.md`补四组五连20头与下层六入口：快层内部稳定，整拍共列，半拍进入在邻头之间；不是把两手逐头吸齐。组内距与含组界距分列，原PDF参照未变成当前宿主候选。

## 间距的必要构型与余宽

`spacing`／`curves`／`layout`的`AUTOMATED_ENGRAVING_JUDGMENT.md`用于候选取舍与出版变体：无碰撞仍须能辨归属；稳定跟读、再现识别和全页网格分开。手写教学分数不是当前评分器结果，不按单个综合分替代读回；版本或音乐来源不同的对照，也不能当单参数或像素标准答案。

SPACING_TRANSFER接入T02的A132 p4应用：相邻快组近稳、谱号所在格较宽，所查共同书面列保持；接收头不是新攻击。找到占位原因不等于证明当前预算最小，先保音乐／共同列，再有条件比较符号周围空白与局部余宽；不由一个比率或advance框自动判错／通过。主agent预选后复核不当独立盲测。

SPACING_MODELS接入时间—空间专题：普通同值稳定感、软件比例布局选项与距离直接承担时长的记法分开。分段尺度须明确时间／范围、各段内部仍成比例；累计时标不作单段时长。特殊体例可声明音在点线后仍从单位起点发声，不能仅由X差误报。保住用户稳定跟读目标，不据特殊记法全谱删干／平梁／改秒尺。

`spacing`的`FIVE_FOUR_SPACING_STUDY.md`补三宽度与一个有条件正面候选：另一表的真实中间进入可拆开联合轴，但默认同步本来正确。只在确定范围内重分，并保护另一手插入／共同点；offset随当前预算重算，后处理不自动修最低小节宽度或换行。含组末的五间隔与只量内部四间隔不能直接比较比率，不把普通尾音也拉成五连同距。

`spacing`／`rhythm`经专题连接`POLYRHYTHM_SPACING_STUDY.md`：共同起止正确时，同值音仍可能在联合事件轴上跨不同段数，非线性弹性和最低宽度会产生波动。先分必要占位与分配机制，不以藏谱号、只移一头或盲加leadingSpace“修匀”；该属性是后续分配的输入，不是最终坐标承诺。模型和原生结果的适用宽度／上下文另核，不将一个复现升级为通用算法。

异分先找真正同刻的开始／到达，再看内部空间，不按第几个头互相吸齐。`spacing`／`rhythm`经专题连接My Dearest的12／11例：首处共同二分到达错列而后六处对齐，可提出局部候选；正常头的同刻核查与拍上装饰的显示约定分开。用相同字形／矩阵或有效正常侧比较几何，不将教材共同细分轴变成全谱等宽网格，也不以官谱局部差异反推软件原因。

先选阅读目标：稳定跟读、光学黑白均衡和严格线性时间轴不同；传统排法可从长音借宽给复杂短音。`spacing`经专题连接`SPACING_MODELS.md`的实际图／片段与A102：比例参照、均匀伸缩、符号占位和整行撑满不能合成一个开关。官方示例也核音乐／音区、避碰设置及是否撑满；未固定预算的更宽截图、主动取消头占宽的重叠图，都不作一般优劣或默认故障证据。

间距先核实际时值，不能只看旗梁等级或显示数字。`spacing`／`rhythm`经专题接入两首整读：unravel F首5组的八分休止占两份，三个十六分占三份；后接6组的相同书写音值并不同长。括号应交代梁外的休止范围，延伸梁已覆盖全组时又可省，不能按“有Rest”统一处理。再现布局也先核材料和前沿确实对应，不把一个固定小节线网格铺满全谱。

先区分谱头后的非计量留白与真正拍间隔。`spacing`经专题链接到`LEADING_RESERVE.md`：一个还原号可在该原创例中使用已有预算，三个强求首头不动却挤到拍号。容量不足允许共同时间列后移，不能只拉一只手；行中小节线本身也可移动，绝对首头位移不等于新增占宽。具体负留白值不作预设，也未证明所有变音或实曲已优化。

比较重复材料先读角色、时值和共同列。`layout`／`piano`经专题连接A011整首案例：主题换到下表、快层带短休止／共头／较长末音，C／H对应行的分配复现而相邻行并不统一。不能把所有可见头或PDF字符当独立时点，也不把某处同值间隔的较大比率单独标错。寻行、再现识别、两手同步和实际净空分别解释，旧测量不是新谱的参数模板。

间距先分必要构型、时间列余宽与整行预算。局部leadingSpace和stretch不按数值直接相加，也不保证单调改善；相同页数仍可能重排后半首。`spacing`中的`SPACING_TRANSFER.md`以实曲变音／三连共存片段保住变音净空、重分普通间隔，保留必要不均匀，并拒绝前部更紧和后文重排版。比较时还看末次起音到小节末，五个相邻距离或更小比率不能代替完整音乐／行页及阅读收益。

`spacing`的`LILYPOND_KEYBOARD_CASES.md`补单位与二度条件：LilyPond旧snippet的force-hshift单位说法与同版属性／源码有差异，实际按音头宽度缩放，不能照抄为MuseScore的sp。普通高低关系与声部交叠的带点部左右选择分别判断，不按一个全局开关统一；看局部覆盖和连接成员后再决定是否恢复自动处理。

<a id="rhythm"></a>

`INTEGRATED_READING_WORLD_REASON.md`：WORLD／Reason K完整3／5先保裸数；Reason p3s6只前三16为三连、梁尾8普通，比较短括号。

`INTEGRATED_READING_RUMBLING_AETHER.md`：3/4两两、6/8三三；Rumbling部分6／3只圈实际组，F末普通16不算32。

`INTEGRATED_READING_EVERLASTING_HEROES.md`：C六音组为普通6＋6＋4；fff四普通8在前三连之后。完整3／5梁保简洁；末7:6／12:10先核意图。

`INTEGRATED_READING_TABI_TAMASHII.md`：部分3／5只管内层成员；Tabi裸8前32休止在外，严格8:7仅条件读法，先核意图再写全比例。

`INTEGRATED_READING_SUZUME_SWORDLAND.md`：X9是32休止＋八头，现有括号保留；部分6／5／3普通峰顶在外。同构省6可保，震音后换型未重申比例先核意图。

`INTEGRATED_READING_STYX_SUGAR.md`：整小节21连16可保裸21；部分9不含普通8峰顶，部分3可前后接普通8，各核内梁与实际成员。

`INTEGRATED_READING_SPECIALZ_GHIBLI.md`：7／6连16与9／11连32分读。V两音震音书面成员共享时段，三笔不独立证明实际交替数；p7s2普通音之间三连16可比较短括号。

`INTEGRATED_READING_SNOW_SPARKLE.md`：同型三音梁已有基准可省3；首次混合四分＋两个16可局部重申。两个8休止＋两个16也可合三连一拍。连续5有内梁及逐组数字时，优先级低于普通32之后首个5或J主梁前三连32；严格部分梁体例与编辑取舍分记。

`INTEGRATED_READING_SILHOUETTE_SIRIUS.md`：C／D q3上部8休止属于旧附点二分层，快速声部同刻仍有8音；先分层再核时值。完整独立5／7／9保裸数，部分3与组外普通8共主梁才优先短括号。

`INTEGRATED_READING_SHINZOU_SHIRUSHI.md`：8:6前八32后有普通16；部分3只管两普通16和休止之后的后三连32，10含一个休止。完整独立7／6／5裸数保留。先看所有梁层、组外音和另一手拍点，不按数字猜分母。

`INTEGRATED_READING_SAKAYUME_SAYONARA.md`：跨表六连可3下＋3上，也可三头和弦＋五单音为六时点八头；五音加16休止也成完整6。保清楚的完整梁；普通8与后三连共梁才比较局部短括号。

`INTEGRATED_READING_RESONANCE_RISING.md`：J首梁普通8之后七个16依下部拍点占1.5q，优先7:6及仅七音短括号；下一梁仅末三为三连。前一系统三束独立5已清楚，保裸5，不能泛加括号。

`INTEGRATED_READING_RAILGUN_PIERCE.md`：跨表6可能含1下表＋5上表，峰顶普通8在外；短括号按成员，三连休止也在范围内。

`INTEGRATED_READING_KISS_CHANCE.md`／`NESTED_TUPLET_SCOPE_STUDY.md`：ChanceH第二束梁前五32按5:4，后两16普通；原创嵌套C外括号放远，显内3仍可能同高相叠。

`INTEGRATED_READING_NAGI_NIER.md`：NieR H两音附点二分震音共3q，端点不相加；Amusement短第三层只围前两32。12/8二连8各3/4q，普通8为1/2q。

`INTEGRATED_READING_DEAREST_HERO.md`：K末五16＋一8只套单层3为7/6拍，先核梁的3＋2＋1与三处会合，再提出内层3候选，不擅改均分六连。

`INTEGRATED_READING_MIIRO_MIXED.md`：区分一四分／半四分弱起和白头交替震音；L先于恢复4/4。

`INTEGRATED_READING_MELISSA_MERRY.md`：K下部八次攻击占九份三连，与上部共享列；后六八分省3，不能按普通8误报异分。3/4与6/8拍组、休止条件另判。

`INTEGRATED_READING_KYOURAN_CONAN.md`：Conan主梁9列中只有中间7是连音，主梁4列中只有前三是三连；按Gould200比较短括号，不改普通首尾时值。完整六头梁另保范围。 `PARTIAL_TUPLET_BRACKETS_STUDY.md`已有2/2原创原生候选：首选短括号，保音符位置与完整MIDI；自动漏显已复现，现有属性可处理。范围清楚收益与新增括线代价一起判断，复杂上下文另验。

`INTEGRATED_READING_KURA_KUUSOU.md`：Gould210–211的跨线连音，后半首音可能晚于小节开始；不能只数音头就推同步。Kuusou H同一小节四组三连＋续行四组，两半二分休止，优先比较完整小节留行。

`INTEGRATED_READING_KONOSUBA_KUCHIZUKE.md`：Kuchizuke J是24个普通八分分八组三头并跨小节，保重心位移，不当3:2或默认4＋4。KonoSuba Q下降梁含四普通32、三连16及末普通8，短括号只管中三头。

`INTEGRATED_READING_KIMI_KIZUNA.md`：I三连在上层休止中、四十六分在下层四分中，为轮流细分；E前9头主梁含四普通32＋五5:4:32，按Gould200比较短括形，只包后五头。

`INTEGRATED_READING_KEY_KICK.md`的R有效拍序为3、4、3、3、3、4、3个四分，行末C是预告；Y的5/8按3＋2，后续6/8五起音含一四分仍为六份。按有效状态和时值读，再判断梁／弧范围，别由字母或头数套循环。

`INTEGRATED_READING_KAWAKI_JANE.md`的L前八音组三梁，在9/8中按剩余附点拍重建为8:12三十二分；它与8:6十六分同长，当前三梁不能直接填8:6。D前5:6与传统4:6又须分别读。保稳定16／九八分活动层，比较首处完整比例；同音弧接收和休止也占书面列，不把18时点叫18攻击。

`INNER_BEAM_HIERARCHY_STUDY.md`把普通四分拍的八个32分比较为8／8／8、8／4／4、8／4／2。先核细分和另一手落点；本例优先完整分层，四加四保留备选，连续音阶无内部重音的例外另判。三版只有BeamMode差，保存及MusicXML导回逐层保持；分梁是可见记法建议，不夹在间距整理里默改。

`INTEGRATED_READING_TANJIRO_KANTAI.md`的C保32脉冲，却可比较4＋4的内梁分隔：保主梁，在中点断开第二、第三层，原生与交换逐层核。H16／G8:6与9:8／I震音不套同一计数；`GOULD_READING_CLOSEOUT.md`给出任务—事实—条件—动作代价的回查流程。

`INTEGRATED_READING_HIKARU_HISTORY.md`纠正6/8与圆舞曲文字的混淆；N前第二13组12头，末八分占两份，下层也有末值变化。先数时值份数和梁层，再检查总时长、两手真正共同点及其余先后。

`INTEGRATED_READING_GURENGE_HACKING.md`：普通梁旁两条悬空线可缩写附点8两音震音，整对共同占3/4拍；后接二分对与七连另计。先辨重复身份，不按条数或头数顺次相加。

`INTEGRATED_READING_GRAND_GREAT.md`的I先四组三连8建立十二头、后省3，再转普通16；变化处重新给3。九9:8十六分、五5:4十六分及梁外四分分别计量；不得从数字省略或15个头推同一比例。

`INTEGRATED_READING_FUBUKI_CASTLE.md`的七连后是梁外普通四分；三连尾组却与普通八分共主梁。完整梁与部分梁各判范围，不能按一串黑头直接套连音比例。

`INTEGRATED_READING_EVERYDAY_EXTRA.md`核整行6/4的14上＋8下32分；末尾19个跨表16分后另有全音符延长。无竖线长段、独立持音、ad lib.与行中a tempo先分清，再谈拍数；不可自动补删凑4/4。

`rhythm`／`notation`的`INTEGRATED_READING_EONIAN_EUTERPE.md`核普通前导、五次起音的六份、tie接收、6／7／普通32分／三连及5／4跨表。八分休止旁的slur不作第二梁；两音震音每对两头各写完整时长，不能相加。

`rhythm`／`beams`的`INTEGRATED_READING_LAZY_EIEN.md`保四个普通16分梁组与1／7／13重音，八分3＋3＋2不必改梁；六连第一组八分和弦＋四16分只有五次起音。

`rhythm`／`beams`的`INTEGRATED_READING_DEPARTURES.md`实见15／16双梁组后各接一个单梁八分。数字不管整条主梁；先澄清括号范围，比例15:14／16:14只在末八分普通、全小节四拍的假设下成立，不生成已确认播放值。

`rhythm`的`INTEGRATED_READING_CATCH_CHANGE.md`核Change J：首小节八分休止后14头，只有开头三颗十六分三连，接普通细分；后续变13头与9头。先数这次的梁、数字、末值，再比步长；相似大弧不传播连音比例。三拍弱起也不补成四拍。

`rhythm`经`INTEGRATED_READING_BUTTERFLY_SILENCE.md`核局部六连只占一次拱形的一段、9括形包括起首休止，以及64普通六十四分的华彩名义4拍。先核梁层、端点、普通侧翼和Rest；自由表情不自动改成超长连音。延长落点、Meno和拾音又可先后出现，不把它们全部吸到小节线。

`rhythm`／`tempo`的`INTEGRATED_READING_BOY_BLUMENKRANZ.md`纠正BOY：附点十六分＋三十二分解释为3组内八分＋十六分，总量八分、3:1到2:1。先核梁数／单位，不与两颗十六分swing或真正Tuplet混用；显式快组不再套一次解释。C跨行2＋2拍与F／Coda另起谱头分判。`piano`同例的Blumenkranz J保留新持续／奏法，不能由同型再现恢复开头的休止和无踏板。

## 熟悉节奏与计数边界

`rhythm`中的`SKILL_TRANSFER_RHYTHM.md`记录G五头初判误数为四头后的纠正。短组看不清时先核休止、实际头数与主／副梁层数，再解释分组或比例。动作slur可罩五音，主梁仍按2＋3认拍，断梁处也可保平顺头距；异分与普通层仅在实际相同有理时位配对，tie接收和休止不算新攻击。

同一个数字跨作品未必同单位或比例。Owari p7参照由三连变普通十六分，p8又有6对3真实共列；lit末7含五头加十六分休止，Variation3比例仍列记法疑问。先核整个小节、书写单位与各层，不从头数补ratio；完整比值属于另列记法提议。

梁的计数分组与奏法重心可能不同。Kakyoin B首小节八分梁4+4，tenuto在1／4／7，标记位置的3+3+2不强制重划梁；tenuto也不等于确定力度数值。省写先回找建立的模式及变化边界，不能由同一个simile字样统一力度与踏板。

反复的三音小组先查前面的休止与实际梁层。`INTEGRATED_READING_NINELIE.md`第8–10节中，A小节初错开与I逐拍再进入不同；J首个两拍单元15头，两个5:4组和普通三十二分并置，末音又是十六分。外侧slur不是整个连音的括号。保留真正单位与进入，不按头数、梁等级或弧的总宽拉成同一种网格；源PDF读法尚未成为MuseScore同构候选。

判断跨拍先看完整拍位、重音、复杂度和熟悉型；不以跨拍即拆或局部短—长—短即合并。`rhythm`／`notation`的Mixed Nuts例中，D／H保留长值，B／F的第三拍tie接收又有计数用途；少头／少tie不直接等于间距更好。续行和拍内接收也不算新攻击，先核实际书写时间与连接。

同页的5连组、局部8va、弧和尾部休止须按各自角色／范围读；Mixed Nuts旧“8组”已由完整末小节和旗梁细图校正。不要只凭单个数字或紧裁图补Tuplet比例、起音数、全曲swing或软件字段。

<a id="markings"></a>

`INTEGRATED_READING_TABI_TAMASHII.md`：Tabi sfz在q0、mp在8休止后q0.5，纠正早期“同位置”概括；独立层不吸到统一段首。

`INTEGRATED_READING_SUZUME_SWORDLAND.md`：H下fsub.q0／上mpq0.5，Swordland低f q2与上mp分别读；J p／rit.第三bar半休止后q2，不移段首。

`INTEGRATED_READING_STYX_SUGAR.md`：STYX G mp右移避accent，PDF字形x不独证迟入；L sfz q0／上p q0.5分别读。Sugar末f nonlegato在q2.25首16。

`INTEGRATED_READING_SPECIALZ_GHIBLI.md`：SPECIALZ末p在q3.5首16，更早附点quarter是旧接收；Ghibli I前低mf和上p分别开始，不统一段号。

`INTEGRATED_READING_SNOW_SPARKLE.md`：Sparkle E／D.S.前f在q11/3，Snow M ff在q0休止处；入口不必等于新攻击或段号。

`INTEGRATED_READING_SILHOUETTE_SIRIUS.md`：C首sfz纠正旧ff；Sirius末sfzq0→mfq1.5、末bar ffq2。旧tie接收／上部休止也可有生效点，段号不替代局部位置。

`INTEGRATED_READING_SHINZOU_SHIRUSHI.md`：Shinzou ff提前8q3.5，M q1而N f q0在休止；Shirushi a tempo q2旧tie接收、mpq2.5新八分，L另起。不能统一移到段号／新攻击。

`INTEGRATED_READING_SAKAYUME_SAYONARA.md`：力度可在q31/8提前32、q0休止或独立层q2生效；不统一移到段号。Sayonara marcato两手共同攻击／休止，保刻意断口。

`INTEGRATED_READING_RAILGUN_PIERCE.md`：段号、8va、力度常先后错开；Railgun H前sub.p／O前fff在q5/2，不统一移到新段号。

`INTEGRATED_READING_KISS_CHANCE.md`／`NESTED_TUPLET_SCOPE_STUDY.md`：Kiss末开放持续弧不补造接收；分层p／mf及重复dim→pp→mf保护实际归属，不去重。

`INTEGRATED_READING_NAGI_NIER.md`：Nagi X p在旧8tie接收处，后14普通16；Zff从双线前两16开始。段落字母、新攻击、小节线不决定所有力度时点。

`INTEGRATED_READING_SOUL_WAR.md`：Soul F旧mp／pp纠正为mf／pp，pp在前8接收之后进入新线；War J先sfz四分和弦、再mf六8，后续低部sfz另属其层。

`INTEGRATED_READING_MIIRO_MIXED.md`：B／E不同层力度保归属；con pedale不授权删断奏点。

`markings`／`tempo`的`INTEGRATED_READING_DEPARTURES.md`纠正C的pp／mp，保护慢干、迟进入与F前先变速／减弱。先核X归属，再理Y通道；局部手提示、段号和八度不自动合锚。

`markings`／`beams`的`SKILL_TRANSFER_MARKINGS.md`补同高干端tenuto正例，以及梁内换手的细角括形：先认归属和作用范围，再判交叉或高度。渐强终点须看两层共同事件；段前引入的力度不自动吸到段号。

## 力度进程与不同入口

先认同一动态进程，再决定哪些标记应共用通道。`markings`的unlasting实例有同表mf／ff和休止前后p sub.／pp：位置不齐可正在表达不同层与时点，不合并／移齐。长限定短语与延续线一起读，分散词的X不自动是新力度或速度事件；起点给全短语及新行提醒可作候选，不能冒充一律禁止分词的规范。几何、逻辑范围与播放scope分查。

<a id="cross-staff"></a>

`INTEGRATED_READING_EVERLASTING_HEROES.md`：C两个六音组各五下＋一上，近干仍先后。先滤PDF负x内容，再按完整梁／头／干核可见事件。

`INTEGRATED_READING_TABI_TAMASHII.md`：Tamashii尾7／7／5／5首5为四上＋一下、次5全下；按完整成员与r.h.接手，不能按谱表截组。

`INTEGRATED_READING_STYX_SUGAR.md`：Sugar六连是下上交替六个八度和弦，按时间／干侧／梁接点跟读。STYX D慢旋律纠正在下表向上符干／r.h.层，上表为快16。

`INTEGRATED_READING_SPECIALZ_GHIBLI.md`：Totoro低长音后转高音谱号读中音，再恢复低谱号准备下一低音，删号成本需比较加线。跨标题旧持续及Arrietty3/4旧tie先保留。

`INTEGRATED_READING_SNOW_SPARKLE.md`：Coda15首时点另有低部普通四分角色，不加成第十六个快头。局部l.h.不扩大上部8va到下表，慢保持、手交接和活动层分别读。

`INTEGRATED_READING_SILHOUETTE_SIRIUS.md`：P空心二分头兼下干三连8，保慢旋律与十二快列，PDF叠画不加攻击。慢声虚线、滑奏、八度、手括号逐一读范围。

`INTEGRATED_READING_SHINZOU_SHIRUSHI.md`：15:8跨表首头支持另一角色反向干，两次近重合PDF字符只算一个快时点；I斜虚线给慢旋律路径。梁拍组与短弧音型可错开；二分震音两端共享时段。

`INTEGRATED_READING_MELISSA_MERRY.md`：F跨表干轴与头位分判，别靠压头距追求均匀；长干、发夹和手括形要看完整通道。

`INTEGRATED_READING_HOMURA_HYORI.md`的叉头滑奏从2/4跨到下一C，H在再下一小节；保不定音高、实际接收及一完整小节准备，不能吸到段首。

`LEGATO_RAVEL_READING.md`保Chabrier局部第三表及其前导空小节，为独立低部建立阅读位置；按角色清晰度与相邻转换评估压回双表。手括形、括起休止、连音和另置谱号分别读，括号不等于可删。

`INTEGRATED_READING_FATE_FRIEREN.md`的平梁若为两向干等长而上移，会压到谱线；保净空与实际拍组。比较梁高、谱表距和完整行容量，不能单独设统一干长。

`piano`／`cross-staff`的`INTEGRATED_READING_CRY_DAISY.md`保留F慢线附加干和说明晚进入的首拍休止；允许省写不等于应删。局部r.h.／l.h.、括号路线音及跨表梁分别说明手、提示与运动，不改整表归属或增加攻击。

## 跨表梁、短干与休止

`CROSS_STAFF_SLUR_ROUTING.md`有原创原生保留／未采用例：干侧零梁接触仍须看整组归属，头到头外绕需要真实空间。局部autoplace关闭不冻结原有效曲率，需补肩部并核最终墨迹，不能只复制已有offset或全谱关自动排版。保留例保护14音、其它绘图及完整MIDI且重载成立，不是实曲迁移或所有弧的预设。

参考谱也须检查实际墨迹。`cross-staff`／`curves`连接unlasting H前的弧穿梁：先比较全组一侧及所属干端的路径，保护连接与两部，不能以全局抬高保证解决；发夹不得已穿干的例外不通用于slur／梁。没有原生替代或软件定位时，交付具体诊断与候选，不宣称宿主缺陷已证。

跨表先分单线跨手与独立两部，再比较共同梁两方向短端、坡度、副梁和表距；不要见短干便全谱加行距或抹平。拍内短休止可邻近后续音所在表，整拍／独立部另判；中央共同休止可行，但不应切梁或挤占已繁忙的动态通道。`cross-staff`的`CROSS_STAFF_STUDY.md`第8–12节有同距平梁／稍宽斜梁及同MIDI拒绝例；该例全局Style仅用于短练习，不能直接推广全曲。

<a id="ornaments"></a>

`INTEGRATED_READING_DEAREST_HERO.md`：Dearest星号只指前三小音拍上；I的tr、波线及p／mp前景分层，续行(tr)是条件候选。

`INTEGRATED_READING_KYOURAN_CONAN.md`：末尾E♮5全音符、G5二分、C6四分各有tr、不同主音；保三次新动作，不把“跨行织体”当同一逻辑持续。

## 颤音、辅助音与续行

装饰记号先分主音、辅助音、起音／收尾和连续／重奏。颤音波线交代范围，tie交代不重新起音，单独升降号或括起小头不一定修饰主音或是顺次弹过的grace；不按黑线长度、相同tr字串或MIDI不变自动缩线／合并。跨行只有波线时结合tie与邻层判可读性，书中更推荐的续行提示也不直接变成纠错命令。相关反例从`ornaments`读取。

<a id="tempo"></a>

`INTEGRATED_READING_EVERLASTING_HEROES.md`：F168在完整主题，mf和三连引入先行；I／J的四8引入也在正式界线前，不把标记齐移段首。

`INTEGRATED_READING_TABI_TAMASHII.md`：附点四分57／43与A四分130分读，无已印等式；Tempo I先于M，上部休止也可承新速度。

`INTEGRATED_READING_SUZUME_SWORDLAND.md`：O／Q／R为八分78／90／128，S为四分78；四分81在V前旧小节休止／震音起点。未印等式不擅补直接关系。

`INTEGRATED_READING_SPECIALZ_GHIBLI.md`：75先于Wind Rises题名及Z，80先于Y且在2/4q0八分休止；换拍、换调、第一次攻击各有实际位置。

`INTEGRATED_READING_SAKAYUME_SAYONARA.md`：Sakayume长短式为附点16＋32转三连8＋16；M／N等式新旧方向仍待核，不机械按左右算BPM。Sayonara明确N72／O170可行中生效。

`INTEGRATED_READING_RESONANCE_RISING.md`：Rising末系统a tempo在q0半休止，p二分q2才进；N的mp在q3/2。先恢复计数，标记不吸附新音或段号。

`INTEGRATED_READING_RAILGUN_PIERCE.md`：Pierce più lento后G恢复局部基准，先q0和弦再q1快层；保持后末四分拾起仍需保护。

`INTEGRATED_READING_KISS_CHANCE.md`／`NESTED_TUPLET_SCOPE_STUDY.md`：ChanceD／G从上方休止恢复，H后旧8接收已恢复；I新Poco meno之后不能机械回开头66。

`INTEGRATED_READING_NAGI_NIER.md`：Nagi118后恢复在q7/2最后8；NieR148早于下一页曲名，S等式方向仍歧义，64／144两解须核作者演奏／工程。

`INTEGRATED_READING_SOUL_WAR.md`：Soul G128之后a tempo从拍内q1恢复，H140从下一系统首小节q7/2最后8开始，不能吸到下一条小节线；War性格字样不自动赋新BPM。

`INTEGRATED_READING_KURA_KUUSOU.md`：L是普通八分对的长短演奏说明，旧附点八分说法已改；M NoBounce从前4/4末八分起，过短2/4后结束。freely、a tempo与N原速＋均分分别保状态和锚点。

`INTEGRATED_READING_KONOSUBA_KUCHIZUKE.md`：M旧四分＝新附点四分，旧96变新附点四分96／四分144；行中B／K／T分别保真实锚点，不能吸附到行首。

`INTEGRATED_READING_KIGEKI_KILLY.md`：Kigeki开头解释的是十六分。F附点四分＝四分及返回逆式在新左／旧左体例均可互逆，配对不能证明方向；先确认再补old/new、箭头或BPM，不按PDF自动改播放。

`INTEGRATED_READING_ICHIBAN_IDOL.md`核Meno从前一小节最后四分开始，J的mp／K的166也先落于弱起；八度线另有更早结束点。恢复文字不能统一吸到下一琶音或段号。

`INTEGRATED_READING_HOMURA_HYORI.md`的M在2/4→9/8写八分＝八分，渐快另在随后生效；首头为前和弦tie接收。先认旗、点和单位，再核实际时间关系，不能从换拍或段号猜换速。

`INTEGRATED_READING_GOD_POKEMON.md`中标题、拍速、调号与弱起各有时点；Sea拍速先于标题，Cycling先速度后弱起。按真实进入保留锚点，不为标题齐头搬动状态。

`tempo`的`INTEGRATED_READING_CRY_DAISY.md`区分A前长短解释、H均分、J重设，与p4先a tempo准备再J的不同位置。解释后的半拍总量不变，不按2:1播放比例生成头距，也不再处理已明确的连音。

`tempo`的`INTEGRATED_READING_DANGO_HANEZEVE.md`把G段号的tie接收、半拍后新和弦附近的a tempo及第三拍p旋律入口分读；保留先后，不吸齐到小节线。再现／延长本身不证明恢复速度；条件性补明须先确认音乐意图。

## 换拍、速度与停顿

换拍先确认是细分不变还是大拍不变；速度等式有新旧体例，移到新行后的整串位置不能独自决定方向。可见单位、原生速度对象与实际导出分查，不把四分BPM不同判为等值关系错误，也不拿曲首名义速度替代边界实际速度。速度可从休止／引入开始；延长要有承载对象，严格同步与自由活动的陪伴等待分查。`tempo`参考提供用户F的保留、E的小偏差及官谱体例未定反例；不得据此统一所有速度字重、补a tempo或移动延长号。

先分类有等号的小音符：它也可能是swing／straight的演奏解释。`tempo`／`rhythm`接入A003的十六分长短说明与恢复，`overview`有完整六页案例。书写单位、约定长短与真实播放时点分查，不把演奏2:1变成头距2:1，不给显式三连再套swing，也不因straight两边相同就删恢复提示。范围／播放不能从PDF字样横坐标补出；真正变速和特殊比例记谱另核。

<a id="free-passage"></a>

`INTEGRATED_READING_SOUL_WAR.md`：Soul计量3＋5＋5与后面adlibitum的29头长运行分读；保背景、局部小3、动作和收束，不凭头数自动补比例。

`TIME_SPACE_AND_REPETITION.md`的近似音高／选择续记区分音区参照与自由顺序：少线／交叉头须有定义，框须说明选取、重复、退出及同步。圈排练字母不自动是选择框，固定钢琴段不为省墨改成近似音高或任选序。

## 自由段与等待

FREE_PASSAGE_READING接入TIME_SPACE_AND_REPETITION：独立反复分同速、异速及同步子组，收到信号立即退出或完成当前循环后退出须查本谱定义；续线稍过边界未必多余，波线也不自动是单主音颤音。计量重复、一次自由运行与自由循环不能仅按短音外形互换。

`FREE_PASSAGE_READING.md`接入Last Stardust与Here：局部a tempo不自动等于Tempo I，保拍单位和实际恢复点；自由文字不自动取消全页计拍。未tie相连的两次长和弦不由“陪伴等待”自动合并，non Ped也不允许假定踏板会保住被删持续。背景、开放弧、手持和控制范围先分清，再谈线形／间距。

自由段先分省拍号、局部自由、senza misura与独立速度，再读活动／持续层及返回点。陪伴长值可代表等待，不因延长号x不同拆音移齐；工程隐藏计量／速度不直接等于读者须看见的拍号／节拍。跨表音可画在空容器上，Part也不等同演奏者；原生连接按实际版本结构核对。`piano`／`tempo`中的`FREE_PASSAGE_READING.md`有用户尾页保留证据及官谱对照。波线还可能指音组自由反复，先看材料和说明，不能一概识别为trill。

<a id="clefs"></a>

`INTEGRATED_READING_SUZUME_SWORDLAND.md`：M低音后换高号读中和弦，再低号准备新低音；D换号不取消六连，替代需比较加线和完整两手。

`INTEGRATED_READING_KYOURAN_CONAN.md`：I的F号保A♭2／A♭3起点，重复高型有稳定轮廓；改G会增加低头加线或频繁换号。先核四降调号及完整材料，不按最高头阈值报错。

`INTEGRATED_READING_KONOSUBA_KUCHIZUKE.md`：H换G后C4一条下加线，D5在谱内；留F会使D5五条上加线。按整个连续型和手判断，不能只看重复最低头。

`INTEGRATED_READING_IRIS_KAIBUTSU.md`的K保频繁换号：选定F5若统一低音需六加线，当前高音下穿插C4仅一加线。先比较实际音区、连续材料和恢复点，再评价换号次数；这是选定音的书写比较，尚未渲染替代。

`clefs`／`octaves`的`SKILL_TRANSFER_CLEFS.md`以完整运行和低入口比较换号；正常短值身份不能只由缩图大小判断。短8va结束后同谱位的新音已恢复原八度，可按上下文比较loco；谱下8va的可见低八度读法与内部播放分查。

## 换谱号与连续音程轮廓

换号先看连续材料、手／声部和其它层占位，再比较加线、跨表与八度的代价。拍内休止后、普通小节起点和真正乐句边界不是同一放置规则；乐句边界可优先于拍线，反复后与cue又有例外。`clefs`中的`CLEF_READING.md`用《lit》的必要局部换号和原创短例区分条件：只按音高阈值虽少加线，却可破坏轮廓；隐藏Clef虽同MIDI仍丢读法。预告、实际变化和新行表头分别看，不按可见字形数去重。谱号改写单列为记法提议，不把三条加线或2/3大小当用户阈值／全局预设。

<a id="octaves"></a>

`INTEGRATED_READING_WORLD_REASON.md`：Reason K首二分仍在8va，后sfz已原位；同表不同干向不自行分割8vb范围。

`INTEGRATED_READING_RUMBLING_AETHER.md`：m67–68全线尾晚于最后下干四分，另干／另p不终止同表8va；窄图缺线尾不能判断。

`INTEGRATED_READING_TABI_TAMASHII.md`：Tabi J八度仍罩后行q0慢和弦，loco在随后快8；Tamashii角端止最后上头，共同梁不扩到下表。

`INTEGRATED_READING_STYX_SUGAR.md`：Sugar21第8与9成员之间结束8va，共梁继续；STYX F前仅首和弦8va，L低8vb与高8va范围不同。

`INTEGRATED_READING_RESONANCE_RISING.md`：Resonance长8va从p5s4跨六系统至p6s3第三小节末，越过K／L；段号不截范围，续行括号保留。

`INTEGRATED_READING_MIIRO_MIXED.md`：Miiro末行8va到首16接收后结束，ff运行原区，别拖到最终和弦。

`INTEGRATED_READING_KAWAKI_JANE.md`的L连续高区给出整段8va候选：前三系统最多5条加线可降到1条，末尾下降最多2条下加线，不能凭下降直接否决。先保完整句，别只转同表慢旋律；这仅为谱位计算，仍须原生范围、实际音高、净空及M恢复检查。

`INTEGRATED_READING_HIKARU_HISTORY.md`用J的相邻小节作正反例：短8va断口内若有新原位和弦，合线会误包入；只有起音早于线的长保持、或主线已经换表时，可再考虑跨短休止。不得默认8va只管上声部。

`LEGATO_RAVEL_READING.md`的Borodine跨行八度实际覆盖m90二分和弦，末钩在之后四分休止前；整页初看估到m89的错误由系统／矢量纠正。先追目标音与终点，不按行尾取消或吸到下一小节。

`INTEGRATED_READING_GRAND_GREAT.md`两处竖折和一处斜升八度续线为高音／奏法留空间，Gould29有垂直预算条件。抬高不是结束钩或多升八度；与歌词稳定基线的条件分别调用。

## 八度的范围与原位材料

八度线的折角须结合通道判断：Gould p29在空间紧时允许随轮廓升降，仍要求避开其它记号；较长乐句线可在外侧。`octaves`中的Zen Zen Zense K例保留这种层序，优先指出过渡虚线穿弧；末尾避低头的折角与线尾体例另判，不按折角数或非水平外形批量报错。

结构标签和音区范围可以有不同起点。ninelie的C前已有mp、slur和8va，C位于随后小节线；I的第一颗快音又晚于小节起点。按当前音乐分别核引入、段号、状态及起音，不以标签位置“修齐”范围。整曲再现也不自动消除同表loco／ottava的旧歧义。

八度线先认目标谱表与音型、实际范围和loco，再选加线／转置与线尾。范围经过空段可能影响空表保留，改变范围后旧手工偏移未必仍适用；普通长音线尾不等于放键时点，颤音／省写另有例外。音高差12还要查字段层次与八度上下文，不能按XML方向名再转一次。`octaves`中的当前工程案例保留四表背景、处理后续空表，并拒绝提前收线版。

同表8va常规作用于各部，贴上干部的短线不自动等于voice专属。转置与原位材料同时出现时，先核意图与明确限定；孤立高音可保加线，持续叠层再考虑分表，同表偶发混写须说明范围。`overview`／`octaves`中的`INTEGRATED_READING_NINELIE.md`保留初判后回查规范的修正：官谱局部也可列记法疑问，不能以出版身份代替核查。原创控制原生pitch／音数未变的内层仍实际抬八度，故同时核实际音高与作用范围，不照外形加Ottava。

<a id="navigation"></a>

`INTEGRATED_READING_SNOW_SPARKLE.md`：Sparkle D.S.先回E Segno，再从To Coda到尾声，不能按相邻PDF页面直接进Coda。局部两bar反复另核返回的速度、谱号和八度状态；显示路线不证明播放展开。

`INTEGRATED_READING_SHINZOU_SHIRUSHI.md`：D.S.旁三降预告回E，物理相邻Coda为五降；L五降起点与后来三降第二起点各配自己的房子。按实际来路核调号／持续，不从相邻行继承。

`INTEGRATED_READING_MIIRO_MIXED.md`：Mixed D.S.三音回C、To Coda八度去Coda，纸面相邻DS→Coda没有音乐边；查每个真实来路及调号再配接收。

`INTEGRATED_READING_GURENGE_HACKING.md`：D.S.→D→To Coda→Coda→H逐段追，跳前／落点接收一起保；不能为对齐段首把fp移到旧音接收处。

`INTEGRATED_READING_FATE_FRIEREN.md`有房子层级清楚却缺局部起反复的I／Q。先澄清实际返回点，再谈紧凑和避碰；字母不自动提供跳转语义。

`navigation`／`octaves`的`INTEGRATED_READING_CATCH_CHANGE.md`把短8va的首音后终点、D.S.返回D、To Coda出口与另行Coda分读。线尾不吸到段号／行末；D.S.与Coda同页不消除回p2的翻纸路线。保留原断行，必要时另比落点留白。

`navigation`的`SKILL_TRANSFER_CONTINUITY.md`补实际D.S.：Little Busters!返回D恢复五升与6/4，随后4/4；再次到To Coda跳H，H重列四升。按每次真实来路读状态和提示，出口后的首遍预告不提前作用到出口小节；静态路径与工程展开播放分别验证。

## 反复路线与状态恢复

导航先分返回点、出口和落点，再读每次进入时的音区／调号／速度／动态／持续状态。相同Coda字形不是同角色，结尾房子的开尾也未必是漏线。行内断口与新系统各付宽／高预算，不能为填白抹掉谱线断口或省掉恢复表头；复杂路线可另议写出，不夹在美化里展开音乐。`navigation`中的原生例有两种同路线布局，以及同图、同写出音却回错地方的控制；需要时核内部连接及实际展开顺序，截图和音数相同不够。未测试的嵌套／多跳转或交换保留不借用该简单例的通过。
