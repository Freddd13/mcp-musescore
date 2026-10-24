# 键盘与多声部谱例：连接、占位和可见范围

2026-10-24。R24规定的定向范围补齐：**9/9例、9/9官方谱图、9/9配套完整.ly文件**。键盘五例、多声部四例；强制移位与附点移位分列，保留此前涉及的情境。它们来自2.24.4文档，片段声明版本为2.23.13；不称整个LSR、两个完整专题或当前版本已研究完。[证据与图源](lilypond_keyboard_cases_evidence.json)记录固定清单、哈希及实际查看；原图和源码留忽略缓存。本批未编译LilyPond或运行MuseScore。

**最有用的经验：先辨认图形在说明哪种关系，再决定如何调整。** 跨声部的动作弧、同音持续、同手跨表和弦、交替震音和踏板范围需要不同的连接。用隐藏对象或局部移位实现外观时，还要查它保留的占位、归属与实际事件。

## 1. 跨声部弧线：可见的一条动作不一定落在一个容器里

**LS01 Creating slurs across voices**：[正文](https://lilypond.org/doc/v2.24/Documentation/snippets/keyboards#keyboards-creating-slurs-across-voices)／[图](https://lilypond.org/doc/v2.24/Documentation/96/lily-b71fc3ff.png)。图中较低音依次趋向上方重复的a，短弧让每次动作一眼成组；梁仍交代各层的节奏。例子注明BWV1004 m235，是小提琴实例，不能据键盘标签推定左右手。

源码在低部插入隐藏a作弧端，上部相同时点已有可见a。由此得到的外观适合说明跨层连接；实现却包含额外的音符事件。不能把这些隐藏音逐项加入MuseScore后，仅凭图像相近宣布音乐保持，也不能为消除容器跨越而重分原声部。后续候选应优先保留实际音符和连接对象，确需辅助对象时逐项核查其事件、占位和输出；本例未验证播放。

**LS07 Making an object invisible with the ’transparent property**：[正文](https://lilypond.org/doc/v2.24/Documentation/snippets/simultaneous-notes#simultaneous-notes-making-an-object-invisible-with-the-_0027transparent-property)／[图](https://lilypond.org/doc/v2.24/Documentation/55/lily-8152ed4f.png)。本例隐藏的是两处起始**Stem**，音头仍可见。上部b→b、g→g各有tie，下层b–g–g–e继续成梁；同位起音处可共用可见头，接收端保留上干音。这样能同时追踪保持音和运动，若把tie换成普通分句弧，持续含义会丢。

这里的透明对象仍参与原布局与连接；删除对象、隐藏整颗音和只隐藏干是三种不同操作。不要从标题猜整颗音被删掉，也不要把一个可见头计成只有一个音乐角色。与[同音附点](UNISON_DOTS_STUDY.md)、[持续与休止](SUSTAIN_AND_RESTS.md)共同使用。

## 2. 跨表：保持同一动作，还要给其它层留下通道

**LS02 Cross-staff chords – beaming problems workaround**：[正文](https://lilypond.org/doc/v2.24/Documentation/snippets/keyboards#keyboards-cross_002dstaff-chords-_002d-beaming-problems-workaround)／[图](https://lilypond.org/doc/v2.24/Documentation/49/lily-d9a038c1.png)。三个长干把上表音与下表低音连成四分和弦；下表另有连续八分伴奏。共享干让跨表的同时性直接可见，伴奏梁则维持自己的阅读路线。只把各表分别压紧，会忽略两种连接所需的共同空间。

源码选择上表的干向下延伸，并对移到下表的列局部忽略碰撞；作者另说明从下表构造可能需要限制梁的碰撞检测。**这是一种对象组织与避碰相互影响的绕行例，不能推广成关闭全曲自动避碰。** `Stem.length=19`注释明确采用半谱间距，即9.5sp；`Y-offset=-6`配合其延长方向。数值依赖本图音区和表距，不能移植为默认干长。参照[跨表研究](CROSS_STAFF_STUDY.md)已有原生短干、休止和表距正反例。

**LS03 Cross-staff tremolos**：[正文](https://lilypond.org/doc/v2.24/Documentation/snippets/keyboards#keyboards-cross_002dstaff-tremolos)／[图](https://lilypond.org/doc/v2.24/Documentation/08/lily-7631fc1e.png)。图中两组附点四分和弦分布两表，三条震音斜杠在中间连接；它表示两组交替，不把上下头逐一对应或读成普通六连音。

源码把换表命令与第二和弦包在同一音乐参数中，使`repeat tremolo`获得两个交替对象。六次两颗三十二分的循环，总量为12/32＝3/8，与拍号及图中覆盖时长对应。这里说明构造方法和读法，没有提供“比普通写出音更漂亮”的比较。实际运行需要变化、重音或手交接时，仍可能需要写出，见[Sadness整曲](INTEGRATED_READING_SADNESS.md)。

**LS05 Indicating cross-staff chords with arpeggio bracket**：[正文](https://lilypond.org/doc/v2.24/Documentation/snippets/keyboards#keyboards-indicating-cross_002dstaff-chords-with-arpeggio-bracket)／[图](https://lilypond.org/doc/v2.24/Documentation/96/lily-04b4b8a6.png)。以Debussy《Les collines d’Anacapri》m65说明同手跨表。括形连接上表首个八分音符与下表上层三音和弦，下面另一个三音和弦不在连接成员内；上表后续八分运动另由梁和弧组织。

这里用Arpeggio对象绘制括形，意图是手分配。不能因对象名含arpeggio，就将它解释成从低到高滚奏；也不能按整条下表的外框延长括形，把未参加连接的低和弦包进去。后续对工程须查实际成员与播放属性，对PDF先依据本谱定义和可见端点判断。此图没有标l.h./r.h.，本库不补指定哪只手。

## 3. 踏板线：外形改变会影响人看见的时点

**LS04 Fine-tuning pedal brackets**：[正文](https://lilypond.org/doc/v2.24/Documentation/snippets/keyboards#keyboards-fine_002dtuning-pedal-brackets)／[图](https://lilypond.org/doc/v2.24/Documentation/af/lily-99c0703c.png)。六小节分成三次相同的踩下／释放配方：每次第一小节起点On，下一小节起点Off。第一组为通常形态；第二组的线向两端延长，左段穿入文字下方，释放竖钩也越过原对应音；第三组右钩更高，整条线在本图也较低。

源码第二组只设`shorten-pair=(-7 . -2)`，第三组只设`edge-height=(0 . 3)`。同版本[属性参考](https://lilypond.org/doc/v2.24/Documentation/internals/piano_002dpedal_002dbracket_002dinterface)说明负值延长、边高左右分别控制。图形越长不意味着实际控制持续越久；这类变化也可能让人误读释放拍位，不能只验MIDI后称无损净书。第三组的较低位置是本图观察，未做单变量重编译，不断言全部下降机制。

**本例保留第一组作为普通清晰范围的参照；另两组用于认识控制与反例，不推荐全曲套用。** 用户S.P.已有作者定义，先保护A八度持续和未知边界，再比较线形，不能从这个外部例补上用户未说明的释放时点。

## 4. 列内错位：同时起音可以有不同横坐标

**LS06 Forcing horizontal shift of notes**：[正文](https://lilypond.org/doc/v2.24/Documentation/snippets/simultaneous-notes#simultaneous-notes-forcing-horizontal-shift-of-notes)／[图](https://lilypond.org/doc/v2.24/Documentation/db/lily-32ded791.png)。两次都是上部d–g、下部b–f二分和弦；第二次只给下部列设`force-hshift=1.7`。图中下部从左侧换到右侧，解决一种交叠方向，也改变干与头的组合轮廓。图形展示控制能力，没有证明第二次就是应采用的净书方案。应把同时性、声部连续和必要分隔一起比较，不能把这种列内错头诊断成起音迟到。

**教程的单位在这里有错误风险。** snippet正文写staff spaces，但同版本[NoteColumn属性参考](https://lilypond.org/doc/v2.24/Documentation/internals/note_002dcolumn_002dinterface)写符头宽度；本次再核官方[v2.24.4实现](https://gitlab.com/lilypond/lilypond/-/blob/v2.24.4/lily/note-collision.cc)，`forced_shift`取该属性，`calc_positioning_done`将其乘以选定音头外框宽度。源码相应段支持后者，不能把1.7当作1.7sp复制。它也说明字体／头型变化会影响这种单位的实际距离；不等于MuseScore的offset使用相同单位。

**LS08 Moving dotted notes in polyphony**：[正文](https://lilypond.org/doc/v2.24/Documentation/snippets/simultaneous-notes#simultaneous-notes-moving-dotted-notes-in-polyphony)／[图](https://lilypond.org/doc/v2.24/Documentation/f9/lily-3464d6ed.png)。同样的f附点二分＋四分，与下面四个e四分重复三次。通常与显式true两次，带点f在右；中间false让f到左，点列也随构型变化。同一音乐需要的额外空间可以换一种分配，不能只统计头距后判哪版更稳。

本图为普通高低关系的二度：保留带点部在右有归属依据，避免点像另一部的奏法，见Gould条件已核的[二度专题](SECONDS_OWNERSHIP.md)。声部交叠时判断又可能改变；该原生专题m2让带点部到左，条件不同，不能用统一的prefer-dotted-right类开关处理全部钢琴织体。

**LS09 Suppressing warnings for clashing note columns**：[正文](https://lilypond.org/doc/v2.24/Documentation/snippets/simultaneous-notes#simultaneous-notes-suppressing-warnings-for-clashing-note-columns)／[图](https://lilypond.org/doc/v2.24/Documentation/46/lily-0f83d345.png)。第一部f2–g2设置忽略碰撞，另一部c2后转为下干c；第二组包含同向干的列。源码对这一部持续设置ignore-collision，正文明确其还会停止列的碰撞处理。图中没有报警文字，无法据此断言本轮编译无警告或结构正确。

自动诊断遇这种覆盖，应先记录受影响列、保留理由和旁边实际冲突。若要恢复自动处理，必须在副本看结果；“清掉警告”“清理隐藏对象”“删除手动偏移”都不能直接当作美化策略。

## 5. 怎样接入本线的实际判断

| 触发情境 | 先核什么 | 可考虑的动作与反例 |
| --- | --- | --- |
| 一条弧似乎跨voice | slur／tie角色、可见成员、隐藏头或干、起音与接收 | 优先保实际连接；LS01隐藏音与LS07隐藏干不可混用 |
| 跨表干长或空间奇怪 | 同一和弦／动作与独立伴奏，表距、干起点及局部避碰 | 比较连接和纵向预算；LS02数值不能当模板 |
| 看似琶音、震音或手括号 | 形状定义、连接成员、时长与展开 | 保留功能；LS05对象名称不决定滚奏，LS03两组不逐头吸齐 |
| 踏板长短／末钩待美化 | 实际On／Off与视觉端点分别核 | 小量比较；LS04外观延长可增加范围歧义 |
| 二度和附点挤或错列 | 干向、高低／交叠、点归谁、单位和局部覆盖 | 按条件移位；LS08与既有m2是条件不同的两例 |

这些例子补足的是连接与空间的判断依据。今后可用可编辑输入做控制和回归；本轮没有新增原生候选、播放／打印验收、官谱整曲回查、教材页或独立skill迁移成绩。

R24阅读范围闭合，公开资料**11/25项，余14项**。目录最终问题回查20/146、固定深化24/24首／164/164页、Gould372/696（359实质＋13辅助）、迁移5/8保持。下一步T06符号／拼写／装饰应用，再交替补剩余目录与规范。
