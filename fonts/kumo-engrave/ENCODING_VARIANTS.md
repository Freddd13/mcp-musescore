# 编码不能代替字形：三项空白结案与八份谱的特殊对应

2026-10-19。继续制作官谱中出现的音乐符号，未处理部分保持Leland。本轮不改变0.500字体、字号或安装配置，完成两项会影响覆盖判断的核查。

## 三项空白已检查全部对应位置

选样图录中的Chaconne U+0003、U+0020及CIDFont+F1 U+F020此前均为空白，但抽样不足以证明其它PDF中相同键也为空。此次遍历清单中**全部117份使用这两套字体的PDF**，包括混排中没有进入旧索引的空格。

| 分类 | 数量 | 证据与处理 |
| --- | ---: | --- |
| Chaconne U+0003源字符位置 | 86 | 原对象字图对应区域均为纯白；均带Unicode映射错误标志，不凭提取码推断字形 |
| Chaconne U+0020源字符位置 | 241 | 239处对应字图区域纯白；另2个空格对象见下方独立检查 |
| CIDFont+F1 U+F020源字符位置 | 130 | 原对象字图对应区域均为纯白 |
| PDFium自动补出的间隔 | 298 | `FPDFText_IsGenerated`为真，不是应补入字体的源字形 |
| 合计 | 755 | 457个源字符位置，加298个生成间隔 |

旧索引记录235次，另有222个源混排空格未被旧索引计入；两套计数已逐PDF／字体／键核对。455处原对象字图在32倍尺度的指定区域最暗像素仍为255，没有用低阈值抹掉浅色墨迹。A130 p3 text obj649、651的单独字图接口返回空，**该返回值本身不足以结案**；另在内存停用其它对象，仅保留相应原对象，按带1pt边界的原页区域32倍、64倍渲染，两者均全白。恢复对象状态，不保存PDF。117份原件SHA保持。

同一字图／裁切方法用于三个可见对照：A003 p1 obj41的速度四分音符、A020 p3 obj727的mf、A021 p2 obj0的高音谱号，都保留可见墨迹。这里A020的提取字符是“(”，实际外观却是mf；不能按字符名称把对照称为括号。

生成间隔的行为由PDFium[官方接口说明](https://pdfium.googlesource.com/pdfium/+/refs/heads/main/public/fpdf_text.h)确认。部分空间／错误映射键经`FPDFFont_GetGlyphPath`反查仍得到10段路径，而原对象实际没有对应墨迹；反查结果没有用作无墨迹或实际字形的判据。没有读取／保存FontFile字体程序。

实现：[audit_catalog_empty_occurrences.py](audit_catalog_empty_occurrences.py)。本机结果`dist/catalog-empty-159/audit.json`及`dist/catalog-empty-controls-166/controls.json`；三项已接入[audit_catalog_coverage.py](audit_catalog_coverage.py)的全位置证明，结果`dist/catalog-coverage-167/`。这只关闭上述三项，不连带认证其它未解决的字体键。

## 八份同名字体，另有一套编码对应

从mf对照发现真实的同码异形后，单独展开A020、A024、A036、A055、A082、A087、A106、A142：共296个逐PDF字形键样本，290个成功显示，6个无墨迹的U+0003键已由上面的全位置检查覆盖。按同码外观分成65个代表组，**三张图板全部审视，并查看18处原页情境**。同码分组仅表示几何接近，不等于每个未展示成员的用途都独立确认。

几处会导致错误覆盖判断的差异：

| 键 | 此八份谱的可见代表 | 其它选样的常见对应 | 决定 |
| --- | --- | --- | --- |
| U+0023 | 两道斜杠震音，A106 p2 obj243 | 升号 | 已有tremolo2；实际引擎震音仍走几何路径 |
| U+0028 | mf，A020 p1 obj352 | 左括号 | 已有dynamicMF，保留Text尺寸校准 |
| U+0032 | mp，A020 p1 obj36 | 拍号2 | 已有dynamicMP |
| U+0034 | 十六分下符尾，A024 p4 obj985 | 拍号4 | 已有flag16thDown |
| U+0052 | 速度四分音符，A020 p1 obj34 | 十六分下符尾 | 已有metNoteQuarterUp，保留速度实际比例 |
| U+0066 | Ped.，A020 p3 obj628 | f | 已有keyboardPedalPed，保留Text尺寸校准 |
| U+006C | sfz，A024 p1 obj327 | 下方重音断音 | 已有dynamicSforzato |
| U+00B0 | 二分休止，A020 p2 obj1100 | Ped. | 原页确认休止立在中线上；已有restHalf |
| U+00BB | 上方重音断音，A082 p3 obj1115 | 等号 | 圆点在重音下、音符上；已有articAccentStaccatoAbove |

这些角色均已有对应字形，没有为编码别名新增重复的SMuFL码位。U+0030两种外框／粗细的括号还原号分成两组，但同属已有三个符号组合。需要进一步评价的历史字形变体不直接替换当前默认造型。

另外纠正旧选样图录中**Chaconne U+004B**的手工对应：其实际选样为八分上符尾，A020 p1 obj86原页为X符头的单旗音符。不能把单旗选样自动当内部旗尾／完整三十二分。此修正只作用于这套选样，不推广到同码的其它字体。当前0.500的八分、三十二分及内部上符尾分别来自已核查的A064、Daisy实例，本轮没有改变它们。

实现：[catalog_per_pdf_variants.py](catalog_per_pdf_variants.py)逐PDF渲染，[source/reviewed_encoding_variants.py](source/reviewed_encoding_variants.py)保存明确形状对应，[audit_encoding_variant_coverage.py](audit_encoding_variant_coverage.py)核对65组与最终Study Music/Text中的目标。图板`dist/encoding-variants-161/`，原页`dist/encoding-context-162/`，最终核查`dist/encoding-coverage-164/`。样本、上下文与原件都绑定SHA；没有把自动匹配名当作人工结论。

## 当前可用状态与下一步

仍使用[0.500包及成对安装方式](CATALOG_COVERAGE.md)，本轮无需重新安装字体、MCP或skill。112个处理码位、97个含三次曲线，大小继续按[TEXT_SIZING](TEXT_SIZING.md)保护。只在副本中换Music／Text字体，不覆盖原谱。

本轮完成全位置空白核查及上述八份谱的逐键样本对应，没有宣布整个目录每个对象均经语义校对。接着检查其它逐PDF键的编码冲突和隐藏字体未展示字符，并按真实需要补字形；普通文本、相同点／括号的不同音乐用途与宿主几何仍分开。A064路径代表的范围另见[PATH_ROLE_COVERAGE](PATH_ROLE_COVERAGE.md)。
