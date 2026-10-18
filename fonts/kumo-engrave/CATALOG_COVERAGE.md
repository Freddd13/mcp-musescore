# 0.500：跨字体图录核查与两枚曲线改善

2026-10-19。本轮继续“所有出现过的符号，没做过的保持Leland或相似适配”。**目标仍在进行**：图录选样、字体存在、原生效果与整个PDF目录逐对象覆盖分开记录。

## 这轮实际核查了什么

逐项查看7套音乐图录的21张图板：

| 选样图录 | 编码项 | 有墨迹的选样 |
| --- | ---: | ---: |
| Chaconne | 136 | 134 |
| CIDFont+F1 | 122 | 121 |
| 隐去名字的控制码字体 | 35 | 35 |
| Pavane | 76 | 76 |
| OpusStd | 17 | 17 |
| OpusTextStd | 6 | 6 |
| OpusSpecialStd | 7 | 7 |
| 合计 | 399 | 396 |

每个实际选样明确对应已制作的字形或组合，所有指定目标在最终Study Music与Text中存在。不是399种不同的符号，也不把同名字体在另一PDF里的同一编码自动当作相同符号。手工决定固定到原图录SHA，见[source/reviewed_catalog_roles.py](source/reviewed_catalog_roles.py)，核查脚本[audit_catalog_coverage.py](audit_catalog_coverage.py)，最终结果`dist/catalog-coverage-147/catalog-coverage.json`。三项无墨迹选样另列，尚不能由抽样断言所有对应对象均为空。

另看完269个隐藏字体组的12张整对象联系表，并回原页看13个音乐组的16处情境。分类为243个普通文字/数字组的选样、13个音乐组的选样和13个此前已穷举所有对象而确认无墨迹的组。普通文字包括标题、版权、速度表情术语、排练字母与连音/指法数字；其字面和字号仍走宿主对应文本样式，不能用替换音乐码位冒充。**前两类只确认所展示的样本，不宣称每个未展示的字符都经过独立核查。** 13个无墨迹组的全对象证据继续引用`pending-empty-052/audit.json`。

几个容易误判的例子：

- CIDFont+F1的U+007E、U+F07E及Pavane的U+007E都是滑音波形部件，不是内部旗尾。A083 p3、A043 p1、A010 p3原页连续波线与gliss文字确认，见`dist/catalog-context-137/`。Chaconne的U+007E选样却是pp，不能跨字体套低字节映射。
- H010的方括号是标题「lit」的引号；H053的星号在Madoka☆Magica副标题；H251的单音符在歌曲标题里。均不当作新钢琴记号。
- H111包含16分休止、pp及全休止，不能按第一个符号推断整组用途；H193/H196含二分符头与下方重音断音的组成字母。原页核查`dist/hidden-context-139/`。
- H157数字8属于八度线，H269括号括住音符，已有对应字形；其实际Music/Text大小继续由专门回归保护。

本轮没有发现需要另加默认码位的新音乐角色；这只针对上述明确范围，不是“整个目录没有遗漏”的证明。已制作的Chaconne造型仍作为默认方向，不因历史Pavane/Opus变体重复增加互相冲突的默认字形。

## 0.500改善的两枚字形

此前某些PDF的Unicode逆映射会返回另一枚形状，旧候选因此被拒绝。本轮换用**另一个已回原页确认的实例**，不是放宽检查：

| 字形 | 新来源 | 来源轮廓/原图IoU | 最终OTF/原图IoU |
| --- | --- | ---: | ---: |
| Coda | A084 p3，CIDFont+F1 U+F0DE | 0.9823 | 0.9893 |
| 下方重音断音 | A046 p3，CIDFont+F1 U+F0DF | 0.9786 | 0.9767 |

两枚原先的栅格描边改为实际字符曲线；Coda保留30段三次曲线，重音断音保留8段。最终OTF按声明的物理尺度与原图对比，外框差≤1像素，未通过自由缩放掩盖尺寸差。第三枚caesura候选仅0.9379，未达既定门槛，保留旧的已核查形状。PDFium接口从Unicode反查字符，其行为可见[官方实现](https://pdfium.googlesource.com/pdfium/+/refs/heads/chromium/6905/fpdfsdk/fpdf_edittext.cpp)；非空路径不能证明字形对应正确。

当前仍112处理码位，97个字形含三次曲线。与0.490逐字比较，Study Music/Text只改变这两枚轮廓及下方重音断音的字宽；其余轮廓和度量、字符映射、垂直度量与布局表保持，Control两家族完全保持。滑音声明与19枚Text大小校准保留。源、选择与验证：`source/alternate_curve_choices.json`、`prepare_alternate_curves.py`、`dist/alternate-capture-138/`、`alternate-integrated-141/`、`alternate-verify-141/`、`font-geometry-144.json`。参考轮廓/字库仅本机研究，原PDF未修改。

## 放回实际谱面

同一隔离0.71宿主完成常用/扩展/新增角色、五种大括号跨度、波线、112字图录、十组力度及用户谱副本的SVG/PNG。十组力度墨迹IoU均1.0。mf、8、8va、Ped.与解除星号实际谱距比例和0.490完全一致，原MSCZ哈希/音乐内容/附件保持，用户谱两副本仍9页。输出`dist/corpus-native-142/`和`native-size-audit-145/`。

另用真实Coda Marker与上下重音断音对象生成钢琴谱，确认两枚Coda及20个Articulation实际绘制，见`dist/refinement-native-146/`。第一次自制fixture把Marker放在voice中，宿主忽略了它；修正为measure子元素并使用codab标签后才验收，不把未出现的对象算作通过。没有因此改本体。

本机包`dist/kumo-score-study-0.500-local.zip`；字库`dist/corpus-font-141/`。退出Evolution，成对更新Study/Study Text完整文件夹并重启；无需重装MCP/skill。保留原字号及排版样式，旧包保留。专用滑音仍需个人0.71，见[NATIVE_GLISSANDO](NATIVE_GLISSANDO.md)。

后续补记：A064全路径的864个代表已有明确角色决定、65处原页情境与完整成员归属核对，10项空白已证明是反向边填充抵消，见[PATH_ROLE_COVERAGE](PATH_ROLE_COVERAGE.md)。这不等于逐个成员语义认证。接下来继续同名字体的跨PDF编码冲突及未展示成员、未渲染项的全对象检查、尚未验收的宿主路径/缩放和纸面打印。不能以399个选样或112码位替代这些任务。
