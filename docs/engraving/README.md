# 钢琴净书研究：规范、案例与实现依据

更新：2026-10-19。所属计划：[ENGRAVING_PLAN.md](../ENGRAVING_PLAN.md)；字体线：[FONT_PLAN.md](../FONT_PLAN.md)。

**当前继续深学，尚未达到“吃透并可稳定应用”的目标。** 下文“本轮完成”指上一轮覆盖与整理。用户新目标是先掌握材料和问题处理，再设计净书skill；软件适配另期进行。[间距取舍](SPACING_DECISIONS.md)新增A102五/七对三的实测解释、同拍错列条件、Kokecola七张实际对照图与当前宿主四种参数条件的原生实验。

最新应用见[用户实曲副本](USER_SPACING_APPLICATION.md)：m50／52整小节疏密与m51内部波动分别形成A、B候选，三版同为8页，其它7页几何相同，所查共同起点与音乐内容保持。它验证一个片段可调，尚未证明阅读或审美更好。此前[原创间距候选](SPACING_CANDIDATES.md)虽在技术上更均匀，用户反馈“暂时看不出差别”；没有据此确定等距偏好，相同参数在变音/密集反例也不能照搬。

随后[弧线专题](CURVES_STUDY.md)增加实曲m113–114线宽候选：保留长弧和文字，单独减轻密集和弦Tie黑度。音乐、音符／梁／Slur及8页结构保持，第8页两个标记有极小位置连动；它说明应先查有效样式与层次，不必先换字体或搬文字。数值仍未获用户／打印认可。

本轮新增[节拍阅读](RHYTHM_READING.md)，实际看过Gould p153–173全部21页图文，补内梁、休止、切分与速度关系；放大复核纠正A128 m29起音数。[梁干专题](BEAM_STEM_STUDY.md)新增原生自动／全局平梁对照和第四层断点导入丢失的具体复现。前者保护已有合理自动处理，后者记录软件限制供以后适配；本次不开发接口／本体。

持续任务：[全目录学习与资源整理](CONTINUOUS_STUDY.md)。已清点并渲染全部146份PDF、1,135页；本轮已审视全部146份谱1,135页，近读379页，见[逐谱一](corpus/READING_001.md)、[逐谱二](corpus/READING_002.md)、[逐谱三](corpus/READING_003.md)、[逐谱四](corpus/READING_004.md)、[逐谱五](corpus/READING_005.md)、[逐谱六](corpus/READING_006.md)、[逐谱七](corpus/READING_007.md)、[逐谱八](corpus/READING_008.md)、[逐谱九](corpus/READING_009.md)、[逐谱十](corpus/READING_010.md)、[逐谱十一](corpus/READING_011.md)、[逐谱十二](corpus/READING_012.md)、[逐谱十三](corpus/READING_013.md)、[逐谱十四](corpus/READING_014.md)、[逐谱十五](corpus/READING_015.md)、[逐谱十六](corpus/READING_016.md)、[逐谱十七](corpus/READING_017.md)、[逐谱十八](corpus/READING_018.md)、[逐谱十九](corpus/READING_019.md)、[逐谱二十](corpus/READING_020.md)、[逐谱二十一](corpus/READING_021.md)、[逐谱二十二](corpus/READING_022.md)、[逐谱二十三](corpus/READING_023.md)、[逐谱二十四](corpus/READING_024.md)、[逐谱二十五](corpus/READING_025.md)、[154页串烧的13章](corpus/READING_MEDLEY_200.md)及[覆盖记录](corpus/reviews.json)。新增[附点、变音与连音的判断](NOTATION_DETAILS.md)、[资源核实目录](RESOURCE_RESEARCH.md)与[规划落实](RESOURCE_PLAN_MAPPING.md)。本轮全目录阅读完成；全页审视与近读分别记录，不等于逐音校对。综合判断和后续应用见[JUDGMENT_GUIDE](JUDGMENT_GUIDE.md)，范围与限制见[完成核查](COMPLETION_REVIEW.md)。缓存已迁E盘，位置见[CACHE_LOCATIONS](CACHE_LOCATIONS.md)。

当前优先阅读：[具体情境的净书判断](JUDGMENT_GUIDE.md)、[个人偏好与应用方法](PREFERENCES.md)、[横向间距专题](SPACING_STUDY.md)。用户进一步明确：需要持续学习并形成具体的审美判断、建议与后续自动净书能力，不以规则数量/技术检查替代。横向专题最初增加5份官谱、8个定位观察和一个自制原生复现，后续候选见上；HS编号与以下35个正式E案例分开记录。

早期阶段 A 累计 **35 个案例、26 张规则卡**：首批14例/14规则，扩大研究新增21例/12规则。该批新增12份官谱、229页发现材料，19页近读；《Behind Bars》定向正文阅读与20个图页核查。这些历史批次与本轮全目录记录分开。这是后续诊断的依据库，尚未实现自动修改；全部钢琴记谱规范的学习、逐音校对、实际打印与演奏验收尚未完成。先解释阅读问题，再决定是否需要参数、插件或本体开发。

## 阅读入口

- [RHYTHM_READING.md](RHYTHM_READING.md)：主／内梁、短副梁、普通与整小节休止、跨拍持续、切分例外及换拍关系；解释为什么有时保留、有时才建议改记法。
- [USER_SPACING_APPLICATION.md](USER_SPACING_APPLICATION.md)：《如果有来生》m49–52实际副本的两类调整、失败尝试、共同时间轴与整页连带效果；技术成功与阅读收益分开。
- [SPACING_CANDIDATES.md](SPACING_CANDIDATES.md)：同版心原生间距候选、含变音的拒绝案例及密集谱2+2分行备选；解释收益、空间代价和控制范围。
- [PIANO_TEXTURE_STUDY.md](PIANO_TEXTURE_STUDY.md)：手／声部／谱表的区别、可省与不可省的休止、用户四谱表的阅读理由、指法与踏板的条件反例；含“数据不变但视觉提示变差”的原创原生对照。
- [CURVES_STUDY.md](CURVES_STUDY.md)：tie与slur的读法、端点与层次、允许交叉和跨行续接；含官谱／用户PDF分析及自制原生谱的连接保护验证。
- [JUDGMENT_GUIDE.md](JUDGMENT_GUIDE.md)：八类音乐情境的正面判断、间距的五种原因、怎样应用到用户工程及开发先后。
- [COMPLETION_REVIEW.md](COMPLETION_REVIEW.md)：本轮完成范围、来源访问限制、原件保护和后续任务边界。

- [CROSS_STAFF_STUDY.md](CROSS_STAFF_STUDY.md)：副梁、休止、括号、slur与八度范围为何需要联合判断，含教材条件与官谱定位。
- [EXTERNAL_PRACTICE.md](EXTERNAL_PRACTICE.md)：星出和宏6/7mm同曲对照、MOLA适用范围、Dorico控制层次，以及LilyPond光学间距/加线/尺寸的实际图与源码核查；区分观察、实现机制和未做的对照。
- [PREFERENCES.md](PREFERENCES.md)：明确偏好、未确认取舍、怎样让用户验收少量候选，以及跨任务怎样读取/应用知识。
- [BEAM_STEM_STUDY.md](BEAM_STEM_STUDY.md)：梁坡、干长、梁与谱线/加线的黑白关系；结合新官谱与Gould p17–26解释出版观感，并区分现可调项和待验证开发方案。
- [SPACING_STUDY.md](SPACING_STUDY.md)：横向间距的规范、更多谱例、用户m50–52测量、原生25%变幅复现与开发假说；[spacing_evidence.json](spacing_evidence.json)保存证据，[fixtures](fixtures/README.md)保存自制谱与复现方法。
- [EXPANDED_RESEARCH.md](EXPANDED_RESEARCH.md)：本轮新增情境、为什么这样排更易读、覆盖矩阵与路线调整。
- [CASES_EXPANDED.md](CASES_EXPANDED.md)：E15–E35与替代方案代价；[RULES_EXPANDED.md](RULES_EXPANDED.md)：R15–R26的适用条件与例外。
- [BEHIND_BARS_NOTES.md](BEHIND_BARS_NOTES.md)：本地全文的定向阅读记录、印刷/PDF页码与已解决疑问。
- [expanded_cases.json](expanded_cases.json)、[expanded_verification.json](expanded_verification.json)：新增材料/近读页/坐标和原文件保护核验；图页保留本机。
- [CASES.md](CASES.md)：具体位置、音乐上下文、为什么这样排、替代方案的代价、例外、验收条件。
- [RULES.md](RULES.md)：触发条件、数据需求、保护约束和候选动作，区分语义约束、情境规范与风格偏好。
- [SOURCES.md](SOURCES.md)：规范来源、核查范围、软件惯例与出版规范的区别。
- [IMPLEMENTATION.md](IMPLEMENTATION.md)：当前可以调什么、诊断先做什么、插件/MCP/本体各自承担什么。
- [cases.json](cases.json)：与案例编号对应的源文件、PDF 页/系统定位、裁图坐标和规则关联；不含原谱文件。
- [verification.json](verification.json)：本批原文件哈希与历史基线的核验，以及文档/案例完整性检查。

## 本批最重要的认识

官谱的秩序感来自几种信息使用不同的视觉通道：连梁揭示节拍，符干揭示声部，弧线揭示持续或分句，文字与跨度线揭示作用范围，系统与页面帮助寻找结构。读者可以一次辨认一个组，而不必逐个数音符、猜文字归属。这是本研究对阅读收益的解释，并非出版者亲述设计过程。

“漂亮”不等于所有间距相等、符梁水平、每行四小节或每段另起一行。重复音型需要稳定轮廓；变化、分层和密集处需要额外空间；全局统一应保留有理由的局部例外。IRIS OUT 的 D/E 在行中，而 Sincerely 的 B/C 在行首，两者均有可解释的用途。

你的谱子与官谱的差距，不能全部归到音乐字体。字体影响符头形状、重量、字宽和连接；梁的分组/坡度、弧线曲率、标记层次、时间间距和分页主要由音乐结构与布局共同决定。本地 `libmscore/beam.cpp` 使用 `beamWidth` 等样式值生成梁几何，核查位置见 [IMPLEMENTATION.md](IMPLEMENTATION.md)。

值得优先排查的不是全谱重新换字体，而是：相同类型的弧线是否一致；长文字与长弧线是否争用通道；多声部和跨谱表是否读得明白；局部距离是否因手动偏移或布局策略而被放大。你的第 2 页 m41 的 mf、pp 分别在小节开始和一个四分音符后，不能按视觉接近就合并；第 8 页 m148–149 实际出现四谱表，不能给全曲强套双谱表规则。

## 证据边界与材料保护

PDF 是版面事实，不提供完整的编辑对象和音乐作用域。`如果有来生-release5.mscz` 是独立提供的工程，对应摘录可补充结构证据；尚未证明它与 `arr_by_kumo.pdf` 的每个对象一一相同。官谱未获得工程，因此其声部、断行是否手动、出版者真实意图均不作确定性推断。

本批仅只读原 PDF、MSCZ 和软件代码。使用既有页面渲染生成本机裁图/HTML；没有修改原谱、字体、MCP、插件或 MuseScore 本体，也未操作当前 GUI 乐谱。参考谱图不入 Git，保留在隔离目录，`cases.json` 记录复查路径。仓库中的文字分析与索引可跨对话使用；本机图集不保证在其他电脑可用。

本机图集：`E:\programming\funcodes\mcp-musescore\tmp\engraving\legacy-2026-10-08\engraving_stage_a\atlas.html`。浏览器可以按案例选择片段和查看坐标。裁图用于分析，不是新的排版成品；保持原渲染的比例，未作为印刷尺寸示范。

## 下一步

先继续按视觉问题学习与解释，交付可定位、可反驳的谱例批注。当前横向优先点是共同时间列、持续脉冲、真实避碰与光学补偿，而不是先扩MCP。自制与实际副本已有受控候选，但尚未证明最佳替代、获得实曲用户选择或做打印验收；不为微小差异反复要求用户选图，优先研究阅读影响明确的归属、碰撞与结构情境。

先围绕 E08/E09/E13 建立只读工程审计：标记时间/范围、局部偏移、有效样式和实际页面几何。输出“事实—可能问题—候选—未确定项”，随后在独立副本中分别测试文字通道、弧线和垂直间距。先保持字体固定；字体线的原型另做对照，再结合两边验证过的参数。

阶段 A 已补自由/严格声部与休止、同音共头、连音数字、装饰音/震音、swing、力度归属、踏板、跳转与coda片段的条件规则。下一批优先补变音提示、附点/二度几何、嵌套连音、跨页tie/Slur；严格对位、指法/替指与三踏板需补自制和真实工程。没有证据与副本验收例的规则，不进入自动写入阶段。
