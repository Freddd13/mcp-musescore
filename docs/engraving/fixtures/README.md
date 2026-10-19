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
