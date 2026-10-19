# 独立净书复现谱例

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

## 同音异时值与附点：按情境共头

以下是独立原创四小节3/4练习，CC0，无用户／官谱摘录；同一Leland／Leland Text和版心。上表两voice，下表一voice，31个音符、8个逻辑附点：

- [分头基线](unison-dots-separate.mscx)／[图](unison-dots-separate.png)：自动头型，四处异时值同音各自分头。
- [选择性共头](unison-dots-selective.mscx)／[图](unison-dots-selective.png)：只给m2／3上部首音加`headType=quarter`；用于反复梁组中可考虑的共头候选，未获用户选择。
- [全部共头](unison-dots-all-shared.mscx)／[图](unison-dots-all-shared.png)：再覆盖m1／4。本例不推荐将孤立交会也合头，不是所有共头的错误模板。

三版原生XML仅差上述headType节点；事件、附点、voice／谱表等与当前MusicXML对应，预期的显式normal／filled头型标签单独核对，其余非布局内容相同。MIDI逐字节相同，31条SVG Note绘制命令对应31／29／27个独立墨迹位置；选择性版保存重载保持。PNG只合白底、同裁框保留完整两手。原生导出方式同本页命令，使用独立配置及输出；这些检查不证明三版一样易读。完整理由和范围见[同音附点专题](../UNISON_DOTS_STUDY.md)及[证据](../unison_dots_evidence.json)。
