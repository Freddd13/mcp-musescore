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
