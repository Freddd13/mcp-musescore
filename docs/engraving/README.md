# 钢琴净书研究：规范、案例与实现依据

本库用于解释出版谱为什么这样排，并据此对当前钢琴谱作出保留、建议或副本候选。关注拍组、声部、手、持续、标记归属与导航的阅读收益；整齐不能单由等距、统一线高或固定小节数定义。

更新：2026-10-22。所属计划：[ENGRAVING_PLAN](../ENGRAVING_PLAN.md)；字体线：[FONT_PLAN](../FONT_PLAN.md)。当前可用于只读诊断及少量有依据的原生副本比较；尚未完成全谱自动净书、全部规范的掌握或个人细微审美的确认。本阶段不开发 MuseScore／MCP／插件适配。

## 阅读入口

先读[个人方向与作者说明](PREFERENCES.md)，再按当前问题选[判断指南](JUDGMENT_GUIDE.md)中的相关情境和下表专题，追到实际页／系统／小节。无需先读全部材料。后续任务可使用[净书skill](../../skills/piano-engraving/SKILL.md)；[使用与更新](../ENGRAVING_SKILL.md)说明知识库关联方式。

| 当前要判断什么 | 从这里进入 |
| --- | --- |
| 整页里哪些值得改、哪些该保留 | [用户整谱](WHOLE_SCORE_REVIEW.md)、[综合应用](INTEGRATED_REVIEW.md)、[ninelie](INTEGRATED_READING_NINELIE.md)、[Kakyoin’s Theme独立试读](INTEGRATED_READING_KAKYOIN.md)、[Kaikai Kitan整首](INTEGRATED_READING_KAIKAI.md) |
| 同值音忽宽忽窄、左右手与变音占位 | [间距取舍](SPACING_DECISIONS.md)、[变音列](ACCIDENTAL_SPACING.md)、[实曲迁移](SPACING_TRANSFER.md)；其它原生比较见[用户应用](USER_SPACING_APPLICATION.md)与[候选](SPACING_CANDIDATES.md) |
| 拍组、切分、梁层级与干长 | [节拍阅读](RHYTHM_READING.md)、[梁干](BEAM_STEM_STUDY.md)、[跨表梁与休止](CROSS_STAFF_STUDY.md) |
| 快慢层、手与谱表不一致 | [钢琴织体](PIANO_TEXTURE_STUDY.md)、[Akuma no Ko整首](INTEGRATED_READING_AKUMA.md)、[同音附点](UNISON_DOTS_STUDY.md)、[二度归属](SECONDS_OWNERSHIP.md) |
| tie／slur与持续、续行或疑似断口 | [弧线](CURVES_STUDY.md)、[持续与休止](SUSTAIN_AND_RESTS.md)、[持音提示](SUSTAIN_CONTINUATION.md)、[输出核查](OUTPUT_READING.md) |
| 力度、奏法、文字与指法归属 | [力度与奏法](DYNAMICS_ARTICULATION.md)、[Connect的省写与分层](INTEGRATED_READING_CONNECT.md)、[指法](FINGERING_STUDY.md) |
| 符头、休止、附点、连音与装饰 | [符号阅读](SYMBOL_READING.md)、[记谱细节](NOTATION_DETAILS.md)、[连音](TUPLET_READING.md)、[颤音](TRILL_READING.md) |
| 滑奏与跨表动作 | [滑奏](GLISSANDO_READING.md)、[跨表琶音／共同梁](CROSS_STAFF_STUDY.md) |
| 换拍、变速、延长和自由等待 | [拍与速度](METRE_TEMPO_READING.md)、[自由段](FREE_PASSAGE_READING.md) |
| 谱号、八度、加线、范围与空表 | [换谱号](CLEF_READING.md)、[八度阅读](OCTAVE_READING.md)、[同表原位材料的反例](INTEGRATED_READING_NINELIE.md) |
| 反复、跳转、变音拼写与状态恢复 | [导航](REPEAT_NAVIGATION.md)、[变音实际来路](ACCIDENTAL_CONTEXT.md)、[拼写与等音](ACCIDENTAL_SPELLING.md) |
| 分行、页面密度与翻页 | [行页](PAGE_FLOW_STUDY.md)、[空间层级](PAGE_HIERARCHY.md)、[外部实践](EXTERNAL_PRACTICE.md) |
| 查规范、原谱和历史案例 | [来源](SOURCES.md)、[Gould已核章节](BEHIND_BARS_NOTES.md)、[MPA图版复核](MPA_READING.md)、[资源落实](RESOURCE_PLAN_MAPPING.md)、[官谱索引](corpus/INDEX.md)、[E案例](CASES.md)及[扩大案例](CASES_EXPANDED.md) |
| 查当前能力、输入与验证边界 | [实现研究](IMPLEMENTATION.md)、[输入历史](INPUT_HISTORY.md)、[skill试用记录](SKILL_REVIEW.md)、[原创原生例](fixtures/README.md) |

## 最近形成的可迁移判断

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
