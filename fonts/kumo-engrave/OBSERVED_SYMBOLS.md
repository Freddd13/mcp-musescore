# 官谱少见符号与显示路径：0.450

2026-10-18。继续用户的全目录目标；这是新增16码位的小样，不是完整 Chaconne 字体。目录仍为146份PDF、1,135页；清点和候选抽样不代表逐页所有角色已经复原。

## 本轮依据与实现

将此前1,179个待复核候选按轮廓归为156组，七张联系表均已浏览；随后回到原页确认用途。归一化图形相同，不代表符号角色相同。下列新角色已接入108码位小样；未改部分继续完整保留Leland。

| 新字形 | 原页依据与处理 | 实际显示路径 |
| --- | --- | --- |
| `wiggleGlissando` | A007《A Cruel Angel's Thesis》p3、文字对象445；G050短S形为滑音波形。A002/A043/A112的原页也确认同类用途；旋转还原后保存独立重复段 | Text可用；原生波浪滑音目前复用`wiggleTrill`，不会自动调用它 |
| `breathMarkComma` | A031 p1、对象180的逗号位于乐句间，是呼吸记号 | 原生Breath |
| `articMarcatoStaccatoAbove/Below` | A031 p6、对象24，为尖音＋断音组合；下方版本是明确的上下反射适配 | 原生Articulation；检查上下字形及谱表上下锚定 |
| `noteheadCircleX` | A101 p7、对象426，ff滑音起点的圈叉符头 | 原生`xcircle`头型；另校准两侧接杆点，避免照搬Leland旧接点 |
| `flagInternalUp`、`flag32ndUp` | A034 p3、对象664是内部短符尾；实际32分上符尾由对象663的16分旗尾与664共同构成，保留原相对位置 | 原生32分上符尾；下符尾未在本轮改造 |
| `tremolo2` | A106 p2、对象243的“#”实际显示两道震音，不是系统分隔符 | Text字形；原生Tremolo仍绘制几何，不受此字形替换影响 |
| `dynamicMezzo/Sforzando/Z` | A064 p1路径1079的mf、p5路径164的sfz；按已核查轮廓提取m/s/z，保留母字形基线关系 | 原生自定义力度/音乐Text；十组完整力度liga继续保留 |
| `repeatDot` | A064 p3、路径891，已在起始反复线右侧的上下两点原页确认；不是附点，也不是百分号形反复小节组件 | 原生反复小节线 |
| `brace/braceSmall/braceLarge/braceLarger` | A064 p1、路径19＋20，原页大括号由两半曲线组成。标准字形按两谱表横向倍率3.625补偿、4谱距字框高度适配；其余三个尺寸采用Leland原有宽度比例派生 | 原生大括号，已查看1/2/3/4/6谱表输出；并非恢复四套独立原字体光学尺寸 |

源码选择记录见 `source/observed_roles.json`。原页引用使用的是具体实例，不能据字体名称或Unicode编码将所有PDF统一映射。例如Chaconne图录选中的U+007E在A036实际是pp，G050的U+007E却是滑音段；保留前者已有pp样本，不将其别名整体改成滑音。

G107的“音符＋等号”实为同一文字对象中两个字符，并非新的预组合字形。G133的va、G139/G141/G142的m/s/z显示在Opus系对象里，只用于识别功能；本轮m/s/z的造型采用A064目标谱中的现成曲线，没有把Opus字形混入。大括号/反复点也没有拿普通附点或其它相似形状代替。

## 曲线、错误映射与保护

`source/pdf_glyph_geometry.py` 使用PDFium的`FPDFFont_GetGlyphPath`获取已显示字符的曲线，不读取/保存FontFile字体程序。该API接收Unicode，再由PDF字体映射到实际glyph；不能把返回非空视为取字正确。实现依据见[PDFium源码](https://pdfium.googlesource.com/pdfium/+/refs/heads/main/fpdfsdk/fpdf_edittext.cpp)。本机返回的是归一化EM坐标，按实际文字矩阵和字号投影，与原对象渲染对比，再按谱距适配。

五个直接曲线字符的原对象/投影墨迹IoU为0.96625–0.99567，尺寸差不超过1像素；32分旗尾的两个组成对象也各自通过。A106震音“#”的API却返回空框，IoU仅0.23198，已明确拒绝该路径；这一个字形采用实际字符高分辨率渲染轮廓，并记录失败原因。不能把这个空框计作曲线恢复成功。

本轮新增15个曲线字形及一个栅格轮廓字形。完整基底音乐493→502字、Text182→262字；构建回读核对未声明修改字形的轮廓、字宽以及GPOS/GDEF字节不变，新字形CFF/实际外框/字宽/曲线段数一致。三种brace尺寸是宿主支持的Leland备选名，从`glyphsWithAlternates`解析F400–F402，未当作未知SMuFL名或私有Unicode碰撞处理。

各来源PDF读前/读后SHA256保持；原MSCZ只读，副本只改两项字体字段，归档其它附件逐字节相同。不安装Windows字体，不改用户首选项，不改本体代码。参考轮廓与字体仍仅存于忽略目录，默认公开构建与旧原型不变。

## 本机文件与验证边界

- 字体：`dist/corpus-font-076/`；捕获：`dist/observed-capture-075/`，集成：`dist/observed-integrated-076/`。
- 全套固定宿主测试：`dist/corpus-native-078/`，新增谱例的最终上下锚定/力度文本修正：`dist/observed-native-081/`。
- 当前可用本机包：`dist/kumo-score-study-0.450-local.zip`。成对更新两个Study完整文件夹，重启后在谱子副本选择Study与Study Text；无需重装MCP或skill。
- 固定原生宿主0.21，SHA256 `7581cb761217c5c2ef6fc802cf7aafbbe8fe1133c8553967b07e22cc3e74f034`。常用谱、扩展谱、新角色谱、五种brace跨度、波线、108字图录、十组力度通过；十组力度像素IoU均1.0。用户谱Control/Study在此宿主均9页，不能与上轮不同宿主的8页直接比较字体优劣。
- 本轮当前`repair_current`宿主SHA256 `59e245e010029b8620e21d198cb540634539ec9ba7e7a8df497975ccb183466e`在导入阶段异常退出；用上一轮0.440字体、再用空私有字体目录与新独立配置也均复现，返回3221226356（0xC0000374），二进制SHA前后相同。证据`dist/current-host-import-079/`及`dist/current-host-import-082/`。尚未定位原因，**不宣称当前宿主验证通过**，也不据此归因于本轮字体。只向净书任务同步证据，未擅改本体。

复现顺序：`group_symbol_reviews.py` → `review_group_context.py` → `capture_observed_glyphs.py`（bundled Python）→ `integrate_observed_font.py` → `build_corpus_font.py`（fontTools Python）→ `prove_corpus_font.py` → `review_corpus_font.py` / `verify_score_copies.py`。输入保持前阶段本机数据，新输出目录不得覆盖旧记录。

仍需继续：156组的角色逐项结案、A064全路径和其它少见组合，32分下符尾/64分等真实来源，剩余栅格轮廓的曲线化；滑音和Tremolo的宿主路径是否需要插件或最小接口另行论证。不能用108码位或已浏览联系表代替全部出现符号的完成证明。参见[全目录研究](CORPUS_STUDY.md)、[字体计划](../../docs/FONT_PLAN.md)。
