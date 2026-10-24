# 钢琴净书研究：规范、案例与实现依据

2026-10-24补[Secret Base六页整曲](INTEGRATED_READING_SECRET_BASE.md)：区分旧长短组与E的新四分单位3组、F空表的手分配未知、H六次局部8vb及完整收束。深化20/24首、132/164页，回查12/146；新增Gould p563–566四个实质图页，累计315/696（311实质＋4标题／目录），资料10/25、迁移2/8保持。没有新原生候选或适配。

2026-10-24补[Michishirube六页整曲](INTEGRATED_READING_MICHISHIRUBE.md)：C的层内稳定、D的一个休止加五音、I的手分配提示与末尾不同持续线分判；核31系统／123小节及PDF边界。深化19/24首、126/164页，回查11/146；19个教材页均复读，Gould311/696、资料10/25及迁移2/8保持，无新原生候选或适配。

2026-10-24补齐[LilyPond净书原理](AUTOMATED_ENGRAVING_JUDGMENT.md)：21/21正文／书目网页、55/55不同图及32份片段，另核一个共用include。结合既有定向间距阅读，R19范围闭合，资料10/25；官谱18/24、Gould311/696、迁移2/8保持。新补候选评分的证据限制、出版变体及无碰撞仍难读的判断，已接skill；没有新原生候选或软件适配。

上一批续学[Madoka组曲十页](INTEGRATED_READING_MADOKA.md)：独立休止与突出旋律的附加干分判；段前准备、跨换拍tie和两手延迟进入各有位置，行容量随拍号及活动密度变化。累计18/24首、120/164页，回查10/146；14个教材页均复读，Gould311/696、迁移2/8保持。已接现有skill，0.3.0标签保持。

前一批补入[Giorno五页整曲](INTEGRATED_READING_GIORNO.md)：对照主题加厚、切分、梁弧分工与密度变化，复核行中入口／跨页返回，并区分末尾交接与双滑奏。该批后累计17/24首、110/164页，回查9/146；17个教材页均复读，Gould311/696、迁移2/8保持。0.3.0发布快照及证据不改写。

本库用于解释出版谱为什么这样排，并据此对当前钢琴谱作出保留、建议或副本候选。关注拍组、声部、手、持续、标记归属与导航的阅读收益；整齐不能单由等距、统一线高或固定小节数定义。

更新：2026-10-24。所属计划：[ENGRAVING_PLAN](../ENGRAVING_PLAN.md)；字体线：[FONT_PLAN](../FONT_PLAN.md)。当前可用于只读诊断及少量有依据的原生副本比较；尚未完成全谱自动净书、全部规范的掌握或个人细微审美的确认。本阶段不开发 MuseScore／MCP／插件适配。

## 阅读入口

查看[当前进度与后续完整计划](STATUS_AND_ROADMAP.md)，区分已形成的能力、本阶段继续学习／候选验证和以后才启动的软件适配。

**现在可用：[0.3.0发布记录与直接试用](../ENGRAVING_RELEASES.md)。** 工作分支持续积累，较大更新保留净书版本标签；[进度账本](progress.json)固定各阶段分母。首轮146/146份，下一轮整曲深化20/24首（132/164页）；数量表示覆盖，不表示已完全掌握。

先读[个人方向与作者说明](PREFERENCES.md)，再按当前问题选[判断指南](JUDGMENT_GUIDE.md)中的相关情境和下表专题，追到实际页／系统／小节。无需先读全部材料。后续任务可使用[净书skill](../../skills/piano-engraving/SKILL.md)；[使用与更新](../ENGRAVING_SKILL.md)说明知识库关联方式。

| 当前要判断什么 | 从这里进入 |
| --- | --- |
| 整页里哪些值得改、哪些该保留 | [用户整谱](WHOLE_SCORE_REVIEW.md)、[综合应用](INTEGRATED_REVIEW.md)、[ninelie](INTEGRATED_READING_NINELIE.md)、[Kakyoin’s Theme整曲与历史试读](INTEGRATED_READING_KAKYOIN.md)、[Kaikai Kitan整首](INTEGRATED_READING_KAIKAI.md) |
| 同值音忽宽忽窄、左右手与变音占位 | [候选判断](AUTOMATED_ENGRAVING_JUDGMENT.md)、[间距取舍](SPACING_DECISIONS.md)、[变音列](ACCIDENTAL_SPACING.md)、[实曲迁移](SPACING_TRANSFER.md)；其它原生比较见[用户应用](USER_SPACING_APPLICATION.md)与[候选](SPACING_CANDIDATES.md) |
| 拍组、切分、梁层级与干长 | [节拍阅读](RHYTHM_READING.md)、[梁干](BEAM_STEM_STUDY.md)、[跨表梁与休止](CROSS_STAFF_STUDY.md) |
| 快慢层、手与谱表不一致 | [钢琴织体](PIANO_TEXTURE_STUDY.md)、[Akuma no Ko整首](INTEGRATED_READING_AKUMA.md)、[同音附点](UNISON_DOTS_STUDY.md)、[二度归属](SECONDS_OWNERSHIP.md) |
| tie／slur与持续、续行或疑似断口 | [弧线](CURVES_STUDY.md)、[持续与休止](SUSTAIN_AND_RESTS.md)、[持音提示](SUSTAIN_CONTINUATION.md)、[输出核查](OUTPUT_READING.md) |
| 力度、奏法、文字与指法归属 | [力度与奏法](DYNAMICS_ARTICULATION.md)、[Connect的省写与分层](INTEGRATED_READING_CONNECT.md)、[指法](FINGERING_STUDY.md) |
| 符头、休止、附点、连音与装饰 | [符号阅读](SYMBOL_READING.md)、[记谱细节](NOTATION_DETAILS.md)、[连音](TUPLET_READING.md)、[颤音](TRILL_READING.md) |
| 滑奏与跨表动作 | [滑奏](GLISSANDO_READING.md)、[跨表琶音／共同梁](CROSS_STAFF_STUDY.md) |
| 换拍、变速、延长和自由等待 | [拍与速度](METRE_TEMPO_READING.md)、[自由段](FREE_PASSAGE_READING.md) |
| 谱号、八度、加线、范围与空表 | [换谱号](CLEF_READING.md)、[八度阅读](OCTAVE_READING.md)、[同表原位材料的反例](INTEGRATED_READING_NINELIE.md) |
| 反复、跳转、变音拼写与状态恢复 | [导航](REPEAT_NAVIGATION.md)、[变音实际来路](ACCIDENTAL_CONTEXT.md)、[拼写与等音](ACCIDENTAL_SPELLING.md)、[特殊调号／变音边界](ACCIDENTAL_EDGE_CASES.md) |
| 分行、页面密度与翻页 | [行页](PAGE_FLOW_STUDY.md)、[空间层级](PAGE_HIERARCHY.md)、[外部实践](EXTERNAL_PRACTICE.md) |
| 查规范、原谱和历史案例 | [来源](SOURCES.md)、[Gould已核章节](BEHIND_BARS_NOTES.md)、[MPA图版复核](MPA_READING.md)、[MOLA全文／译文复核](MOLA_READING.md)、[资源落实](RESOURCE_PLAN_MAPPING.md)、[官谱索引](corpus/INDEX.md)、[E案例](CASES.md)及[扩大案例](CASES_EXPANDED.md) |
| 查当前能力、输入与验证边界 | [实现研究](IMPLEMENTATION.md)、[输入历史](INPUT_HISTORY.md)、[skill试用记录](SKILL_REVIEW.md)、[原创原生例](fixtures/README.md) |

## 最近形成的可迁移判断

[T02预选后间距应用](SKILL_TRANSFER_SPACING.md)核五个快组及28个共同书面列；保留多数组织，将行中谱号占位与最低必要宽度的证明分开。迁移覆盖现2/8，其中本例为主agent预选后只读应用，非独立盲测；没有新增全曲深化或原生候选。

[时间—空间与独立反复](TIME_SPACE_AND_REPETITION.md)补Gould19个新实质页：同速独立／同步子组不抹掉对应，立即退出／完成当前循环后退出不混用；普通稳定间距与距离直接计时也不是一回事。回看三个已知自由段保留原读法，不借新式记法强换无干、平梁或循环框；Gould现311/696，迁移试用不增。

[Link组曲九页](INTEGRATED_READING_LINK_MEDLEY.md)区分结构标签、提前引入、伴奏准备、旋律进入与真实物理翻页；上表四小节休止不证明当前页末可翻。[Adabana七页](INTEGRATED_READING_ADABANA.md)补一个4/4拆成两行的2＋2拍及八度真实终点：出版实例与Gould例外条件分开，末角不吸到G段。

[Here九页](INTEGRATED_READING_HERE.md)核完整tie、开放留声弧、中间换踏板和末端双星；双层控制应保留，简称、范围和各次释放归属仍可澄清。[Last Stardust六页](INTEGRATED_READING_LAST_STARDUST.md)区分局部a tempo与后来Tempo I，未tie相连的长和弦不自动并音，non Ped结尾也不能靠假定踏板删持续。这四首是已知材料综合复读，不增加独立skill评测或教材首次覆盖。

[五连间距原生比较](FIVE_FOUR_SPACING_STUDY.md)有三档宽度及一个局部候选：共同时间本来正确，另一表的中间进入仍可使一格变宽；保住两组边界及两手关系，候选更稳。120mm版原生保存重载保持，但offset依赖当次布局，窄版仍换行，不作全谱预设。

[Owari八页](INTEGRATED_READING_OWARI.md)补第二次fp拆小节、三连到普通十六分的参照改变与6对3真实共同点；[lit五页](INTEGRATED_READING_LIT.md)解释变奏间不同密度／路线、末7组的五头加长休止，并保留非显式比例的记法疑问。

[Kokecola准备／输入全文与22处图](KOKE_COLA_WORKFLOW.md)补内容、计量／路线及空间预算的依赖，通用工具示意不当作品数据。[Dorico条件补记](DORICO_EDITORIAL_PRACTICE.md)仍缺原图；时值比与同值组内不匀分判，不把个人设置当规范。

[Kakyoin四页整曲](INTEGRATED_READING_KAKYOIN.md)补梁的4+4计数与tenuto位置3+3+2分工、条件性踏板省写、必要长干及3／8小节行容量；F的二分重奏不并成长音，G的先后力度不拉齐。本轮是全曲回查，不是第二次独立skill评测。

[MOLA完整16页](MOLA_READING.md)核中英文的页码、每行状态和纸幅译文，并解释提示、等待、恢复定位及最终渲染的用处。乐团分谱尺寸不是独奏钢琴硬阈值。[变音边界](ACCIDENTAL_EDGE_CASES.md)补特殊调号、符号定义与取消，避免把必要音高修饰移成似指法的上方数字；不为普通钢琴制造微分音。

[ninelie六页整曲](INTEGRATED_READING_NINELIE.md#8-2026-10-23把局部放回整首)补A／I的休止频率、J的真实单位与近稳定局部间距、C的预先进入和K的指示。保留组形与不同锚点，八度旧疑问未被再现自动消除；没有新增原生候选。

[十二对十一原生研究](POLYRHYTHM_SPACING_STUDY.md)保住默认共同起止，并区分换号占位与联合事件轴的非线性弹性／最低宽度。隐藏谱号诊断的内部间距可按该机制重建；两列简单加留白未解决首尾紧缩，移头又破坏可见汇合，当前保留默认。公开四份CC0输入与原生对照，未改软件或原谱。

[My Dearest整曲复读](INTEGRATED_READING_MY_DEAREST.md)将装饰约定、P段12／11异分及S的不同进入分判。七处运行内部不应逐头吸齐，真正共同末点另核；首处同型二分头约错开0.83sp，后六处对齐，记录为局部候选而非制作软件缺陷。旧装饰结论复核，不重复算成新规则；本轮没有原生替代。

[Mixed Nuts整首续读](INTEGRATED_READING_MIXED_NUTS.md)把D／H简明长值与B／F第三拍接收分开：完整拍位、熟悉型和计数收益共同决定，不能全拆或全并。末尾两个5组及局部8va已核清并校正旧记，原谱仍只读；此批没有新增原生候选。

[跨表弧原生续验](CROSS_STAFF_SLUR_ROUTING.md)在原创两部短谱保留头到头外绕：保护原连接、其它墨迹和完整MIDI，并实际保存重载。避梁仍须看归属；关闭局部自动避碰也不冻结原形。是一个已验证构型，没有替官谱或用户工程改谱。

[unlasting整首复读](INTEGRATED_READING_UNLASTING.md)先保留mf／ff、p sub.／pp的独立层及进入时间，再指出H前实际弧穿梁和L跨行渐弱短语的不同候选。规范、参考风格和本线建议分开，未从PDF补播放scope或宣称替代版已改善。

[间距目标与模型](SPACING_MODELS.md)补传统借长音空白与严格比例的取舍，并区分均匀伸缩、光学补偿和撑满行。官方图也须查源码：最挤的比例例主动取消音头占宽，概述一组还改变音区。回看A102后，先选阅读任务再提候选；本轮没有同输入双引擎或新增MuseScore优化结论。

[The Rumbling／unravel整曲阅读](INTEGRATED_READING_RUMBLING_UNRAVEL.md)将组形、实际时间与稳定再现连起来：F的首5组只有三个快音头，八分休止占两份；括号说明梁外休止的范围，延伸梁已覆盖全组时又可另判。对应再现行保持分布，不代表整页排格线；震音缩写与写出的变化也须分读。本轮是PDF与规范判断，没有新的原生优化或用户审美选择。

[行首留白](LEADING_RESERVE.md)区分谱头后与行中小节的空间预算：单个还原号可在原创例中使用已有空白，三个强求头位不变则挤到拍号而拒绝。共同列保持并非唯一目标；还需读实际前沿、符号分隔和整行重分。两局部控制已原生重载，40音及完整MIDI保持；[导出环境复核](NATIVE_EXPORT_ENVIRONMENT.md)同时限定了部分旧记录的配置隔离说法。

[符号阅读](SYMBOL_READING.md)把符头、线重、加线与休止的形状／谱位连起来：书中同拍休止局部同高的图文曾被文字提取漏掉，现已核实。原创两小节仅将二分休止上移半sp，实际两拍与完整MIDI保持，却看似全休止；反例原生重载也保持。因此可优化留白的前提还包括识谱参照，不按无碰撞／数据不变即采用，也不把整数offset当全谱规则。

[换谱号研究](CLEF_READING.md)解释了保持音程轮廓与减少加线的冲突：休止后新材料、乐句、拍线和小节起点各有放置条件；《lit》的叠层使局部频繁换号有理由。原创四小节保留边界换号，拒绝按单音阈值频繁切换、组中延后和隐藏谱号；四版同35次起音，读法仍不同。已核独立音乐配方和保留版原生重载，不为用户工程改谱或开发适配。

[Kakyoin’s Theme整页试读](INTEGRATED_READING_KAKYOIN.md)在未提供预期答案的独立分析中，调用已有知识解释了慢声部跨表、双手接替、行中段首和不同层的八度范围。主agent回看原页与Gould后保留主要判断；没有为整齐给叠层上部随手加8va。这是当前skill的只读行为样本，不是用户审美认可、原生优化完成或全面能力证明。

[共同梁原生比较](CROSS_STAFF_STUDY.md#8-续读中部梁不是把所有东西放在中间)说明同距平梁与稍宽斜梁有不同空间代价，拍内休止可靠近后续音，但不能切进梁；同MIDI的错误排法仍须拒绝。候选经过原生重载，适用条件限于该短例，不能给全曲套全局平梁。

## 本批最重要的认识

出版观感来自不同信息有清楚、稳定的视觉线索，让读者一次识别一组、一层或一种动作。必要变音、异分同步与密集和弦会合理改变局部空间；稳定轮廓和完整时间对齐需要一起判断。段落标记可在行中，空白也可能承担导航或进入准备。[Kaikai Kitan整首对照](INTEGRATED_READING_KAIKAI.md)将相似材料、H的分层、行中B／I／J及首尾不同拍数组连起来；E的十六分长短说明和F恢复又表明，不能把swing演奏比例直接变成横距比例或真实变速。

音乐字体影响字形、重量、字宽和连接；梁坡、弧线、标记通道、时间分配和分页还由记谱与布局决定。当前固定字体研究布局，不以换字体代替诊断。参考谱的排法提供可讨论的阅读效果，不证明出版者亲自采用了某种设计推理，也不能免除规范核查。

用户已确认《如果有来生》m132的S.P.保持A八度，两条长弧表示持续，详见[PREFERENCES](PREFERENCES.md#作者已确认的音乐含义)。它不自动指定精确释放时点，也不是已采用某个线形候选。极简6/8两图的“暂时看不出差别”不构成等距偏好。

## 证据边界与材料保护

原PDF、MSCZ和教材只读，试验用独立副本或原创fixture。PDF是可见版面的证据，不能独自确定内部voice、播放和对象范围；用户PDF与release5工程也未证明逐对象完全对应。参考原图／教材不加入Git，原生候选的音乐、记法、几何与行页连带影响分别核对。使用方法和输出陷阱见[原生比较参考](../../skills/piano-engraving/references/native-review.md)。

清点时146份官谱、1,135页均有全页审视记录，历史近读379页；这是[目录覆盖批次](corpus/reviews.json)，不是逐音校对或“全材料吃透”。其后的定向重读和新增近读保留在各专题，不改写旧批次数。Gould为定向章节学习，受限的视频／课程不算已读。

本次整理完整保存了此前入口的批次说明、原有链接与旧下一步，见[整理前入口快照](READING_LOG_2026-10-20.md)。旧日期结论、旧验证结果不能冒充当前实测；缓存位置见[CACHE_LOCATIONS](CACHE_LOCATIONS.md)。

## 下一步

继续用实际谱面问题检验判断和skill的调用效果，优先处理影响跟读、归属和范围的情境。当前知识已有少量有效原生候选与拒绝反例，下一步应用仍需重新读取输入和上下文；不把旧数值拼成全谱预设。

用户无需逐条审核规则或反复辨认微差。技术核查由agent完成；在有明确阅读取舍的候选时再取得少量反馈，积累真实偏好。准备采用时才补实际尺寸、打印或试奏验收。软件优化先保存具体复现与条件，开发留到后续授权的任务。
