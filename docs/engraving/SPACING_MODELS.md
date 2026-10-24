# 间距的目标：读得稳，不等于把谱变成时间尺

2026-10-22。本轮补看LilyPond 2.26官方间距文档的18张谱例及18份配套片段，复核Dorico Pro 6.2的间距选项，复看A102《Owari no Sekai Kara》p6–8。来源、缓存和实际读取范围见[证据](spacing_models_evidence.json)。没有安装／运行这两套软件作同输入比较，也没有修改MuseScore、MCP、插件、字体或原谱。

## 1. 先问这段谱要让人看清什么

演奏者需要认出拍组、配合点和动作，不是从每个毫米重新计算时长。长音已有头型、符干、附点或连接提示，未必需要与持续时间成正比的空白；密集短音却需要足够的形状分隔。另一种任务是精确比较复杂异分或配时间图，此时更严格的时间比例可能值得占用额外宽度。

因此，至少要分开四个问题：哪些书面时位必须对应；符号需要多少清楚可认的空间；有余宽时希望各区间怎样分配；选定整行内容后怎样撑满。一个“松一点”参数不一定同时改变这四件事。相同页数、较小的头距波动，也不是全部问题已经解决的证明。

## 2. 两套软件文档提供了什么思路

[LilyPond水平间距概述](https://lilypond.org/doc/v2.26/Documentation/notation/horizontal-spacing-overview)以可伸缩距离处理时值；在常规基准及以上，倍长音值增加一档理想空间，并非简单把距离翻倍，比基准更短者另按相对时值缩放。基准取各小节最短值的常见者，而不是全谱绝对最短音或总数最多的音值。这个政策避免少量极短音把全谱一同拉宽；它不是本机MuseScore已采用相同政策的证据。

[比例排版](https://lilypond.org/doc/v2.26/Documentation/notation/proportional-notation)另把距离直接联系时长；示例又分别处理均匀伸缩、谱号等无持续时值的占位及表头前置空间。严格比例通常要付出宽度，不作为一般钢琴谱的默认审美目标。文档中的“non-musical”是布局分类：变音、谱号没有持续时值，仍然决定音高／读法，不能据此删除。

[Dorico 6.2选项](https://www.steinberg.help/r/dorico-pro/6.2/en/dorico/topics/engrave_mode/engrave_mode_note_spacing_page_layout_options_r.html)把四分基础空间、时值比率和短音最低空间分开；另有撑满行时计实际／理想宽度的选择，以及跨表梁按干或头获得均匀感的光学校正。这里只证明手册描述了这些控制，不能从选项名称推断全部碰撞约束、默认成品优劣或本项目现有可调用能力。

这几种思路对应不同读者任务，不应合成“开启严格／理想间距就自动出版级”。前述文档的数字也不直接变成MuseScore参数。

## 3. 读图还须核对比较条件

以下编号按本机缓存中的页面顺序；官方图片和完整片段仅存在忽略目录，未加入Git。不是本机编译结果。

| 图例及实际来源 | 核实到的条件 | 可以怎样使用 |
| --- | --- | --- |
| 概述1／2：[源码1](https://lilypond.org/doc/v2.26/Documentation/5c/lily-6eb020b7.ly)、[源码2](https://lilypond.org/doc/v2.26/Documentation/2e/lily-c3f6ecc5.ly) | 一处八分拆为十六分，同时起始音区上移八度 | 可读机制说明；不能将图的全部间距变化归给最短值基准，干向／加线也随音区变化 |
| 概述3：[源码](https://lilypond.org/doc/v2.26/Documentation/74/lily-5fca4134.ly) | 重复材料后同时改变NoteSpacing与StaffSpacing的干向补偿，显式ragged-right | 展示光学构型影响，不是单改一个补偿量、相同撑满预算的比较 |
| 比例1／2：[源码1](https://lilypond.org/doc/v2.26/Documentation/e4/lily-2f451700.ly)、[源码2](https://lilypond.org/doc/v2.26/Documentation/4e/lily-3e7b6bf3.ly) | 同一二分＋四个十六分＋五连组；第二版加比例参照，均ragged-right | 长音借出空白与保留线性时间的差别清楚；较宽图片不是固定行宽下已经更好的证明 |
| 比例3：[源码](https://lilypond.org/doc/v2.26/Documentation/f5/lily-36a0ffef.ly) | 最挤的一行除了改比例参照，还把NoteHead的extra-spacing-width设为反向无穷区间，明确允许头重叠 | 重叠是有意构造的演示，不能指控为正常默认输出；也不复制这个关闭占宽保护的控制 |
| 比例4→5→6：[4](https://lilypond.org/doc/v2.26/Documentation/88/lily-30fabe36.ly)、[5](https://lilypond.org/doc/v2.26/Documentation/db/lily-8ca44fcd.ly)、[6](https://lilypond.org/doc/v2.26/Documentation/35/lily-f99ad919.ly) | 两表音乐相同；逐步增加比例参照、uniform-stretching，均ragged-right | 下部九连组从明显波动变为更规则；比例参照与均匀伸缩不是同一个开关，仍未做同宽替代比较 |
| 比例7／8：[7](https://lilypond.org/doc/v2.26/Documentation/ae/lily-811a73a4.ly)、[8](https://lilypond.org/doc/v2.26/Documentation/55/lily-e0f583de.ly) | 两行全音符，仅第二份移除Separating_line_group_engraver；两份都未设置比例参照 | 这是前置空间的独立演示，不是“完整比例模式”的两版；零时值不意味着普通出版谱应该零留白 |
| 比例9：[源码](https://lilypond.org/doc/v2.26/Documentation/e1/lily-92353a59.ly) | 相同节奏／中途换谱号，第二份加strict-note-spacing | 谱号占位可以与严格时间分配分开处理；图上这一处可容纳，不证明复杂变音／grace都可忽略其空间 |
| 全局1／2：[1](https://lilypond.org/doc/v2.26/Documentation/4a/lily-469250c9.ly)、[2](https://lilypond.org/doc/v2.26/Documentation/4a/lily-5ee23cbf.ly) | 同一16小节、同12cm名义行宽；第二份改基准为十六分，图从3系统变5系统 | 全曲松紧可能改变分行；不能只比较某两个头的距离，省略后续行页代价 |
| 新段2：[源码](https://lilypond.org/doc/v2.26/Documentation/72/lily-9b0bcd34.ly) | 同一短型重复，创建新SpacingSpanner后改变spacing-increment，再在新段恢复 | 局部参数有对象／段落边界，不是任意时间改值即作用于已有整行的证明 |

配套片段是lilypond-book生成文本，普通片段没有version指令，fragment又采用不同标记；缺少某个包装字段不能直接判成无效音乐。运行版本仍以明确文档／实际宿主另查，不由生成文件名补出。

## 4. 用A102的实际排法检验目标

p6末系统，上部保持后进入三连材料，下部重复三连背景；p7首系统第二小节，上部二分和弦后接五连、七连，下部继续三连。前批[间距取舍](SPACING_DECISIONS.md)已量到：七连对应下部三连的两个步长约18.72、22.80pt，插入时点与上部局部区间相符。本轮复看完整页／系统，原PDF哈希仍与该输入一致，没有将旧数值说成本轮重测。

这里“读得稳”靠数字、连梁、重复轮廓及配合点共同建立。下部步长不同，不自动等于低部难读或软件错误；但如果波动超过实际构型所需，仍值得做同内容候选，不能由出版身份免除检查。

**为什么不直接套严格比例：** 上部前半保持已经容易识别，后半五／七连却需要较多形状空间。若要求前半在可用的音乐时间区间内占一半，后半在相同区间预算下就更紧；要维持辨识净空，可能得改变小节宽度或整行安排。这是预算推理，尚未画出替代版，不能宣称其一定变丑或原版已最优。

p8前两系统又把三个小节分成各一小节半；半音密集部分分担到两行，而不是把所有六连组压成相同步长。原图、实际时值和规范条件已在[旧案例](SPACING_DECISIONS.md#p8把三小节分到两行各一小节半)详述。它说明音乐时间仍须保留，空间却可按复杂度分配；当前没有把这个拆行办法变为已实现的MuseScore操作。

同样，[unravel的混合休止连音](INTEGRATED_READING_RUMBLING_UNRAVEL.md)不能只数头来判等距，[行首留白](LEADING_RESERVE.md)也证明无持续时值的符号仍须有清楚分隔。时间尺、形状可读和稳定跟读是相关但不同的目标。

## 5. 自主诊断时怎样选择动作

看到连续八分忽宽忽窄，先核其实际时值、另一手的细分、tie／休止和正常侧音头；再区分表头前沿、拍间隔及跨小节边界。不能把错头、跨表干向光学效应或不同实际时值统一判成时间分配错误。

如果限制来自必要构型，先判断能否利用局部白空间而保持归属；空间不足时应比较少放小节等安排。若构型已有余地，问题在余宽如何分配，才比较更稳定的拍组／伴奏参照或更严格的局部时间分配。对复杂同步，比例更清楚可能值得；对普通慢线，过大的长音空白可能只让阅读跳得更远。

候选要用实际宿主、相同字体和明确预算，保住两手共同位置并读回整行及后续行页。这里没有形成全谱默认值，没有以均匀度排序软件，也不把LilyPond属性逐一映射成当前MCP命令。本阶段继续学习与验证，适配开发留待后续任务。

## 6. 数字默认值的一个未决点

概述文字称基础最短值的常规上限为八分；同版本[SpacingSpanner内部参考](https://lilypond.org/doc/v2.26/Documentation/internals/spacingspanner)却将base-shortest-duration列为3/16。本轮未运行LilyPond或追溯其确切构建代码，保留这项资料差异；不能将概述文字、内部文档数字或另一软件的比率直接当成用户工程应设的值。

[新间距段说明](https://lilypond.org/doc/v2.26/Documentation/notation/new-spacing-section)明确要求相应覆盖与新对象创建在同一音乐时刻。当前图例证明的是其所示spacing-increment情境，未验证所有属性在所有局部位置的切换行为。

## 2026-10-23：时间—空间记谱不是普通谱的“更匀”开关

[Gould后续图文](TIME_SPACE_AND_REPETITION.md)的p630把完整时值／梁组与按秒排列的黑头并置：少墨迹未必更易读，因为读者失去部分熟悉组形，要从距离估时。p638又将1秒密集区与8秒稀疏区分配不同尺度，前提是各段时间明确、内部仍按比例；不是全谱可任意错位的许可。

因此将软件的比例间距选项、普通同值稳定感和整套时间—空间记法分开。用户要改善变音／两手造成的局部波动，不因此接受删干／改音值或全页秒尺；先按实际阅读目标及空间原因诊断。p636–637的时标避碰另有声明音在标后仍从单位起点发声的体例，不能仅凭X差判晚进入。本轮未运行新引擎或把这些体例当MuseScore接口。

## 2026-10-24：从局部候选到可解释判断

[LilyPond完整essay复核](AUTOMATED_ENGRAVING_JUDGMENT.md)补出版变体、弧线端点与净空的取舍。教学例的分数是源码文字标签，未运行当前评分器；无碰撞、几何更匀与可读归属分别核，不能用一个综合数自动通过。此前原生案例仍沿用原验证，本批没有重跑或新增候选。
