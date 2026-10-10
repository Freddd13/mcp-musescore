# 规范来源与证据等级

核查日期：2026-10-09。这里列明**实际读到的范围**，不把软件默认值等同于普遍规范，也不声称已读完所列书籍。

## 来源索引

| ID | 原始来源 | 本批核查内容 | 用途与边界 |
| --- | --- | --- | --- |
| S01 | Elaine Gould, [Behind Bars 官方样页](https://behindbarsnotation.co.uk/contents/sample_pages.pdf) | 样页中印刷页 14–15、22、29、153、557–558；153 页另渲染核对拍号图 | 净书原则的出版教材依据；只核查样页，未读取整书。谱号/拍号是图形，不能仅依赖 PDF 抽取文字。 |
| S02 | Dorico 官方开发文章 [Development diary, part 10](https://blog.dorico.com/2015/03/development-diary-part-10/) | 梁的分组、坡度与谱线关系、规则存在分歧 | 2015 年设计说明；可解释梁几何问题，不代表当前所有默认行为。 |
| S03 | Dorico 6.2 [Beam grouping according to meters](https://www.steinberg.help/r/dorico-pro/6.2/en/dorico/topics/notation_reference/notation_reference_beaming/notation_reference_beaming_according_to_meter_c.html) | 连梁与拍子结构、自定义分组 | 拍子结构原则可借鉴；具体默认分组是 Dorico 的实现选择。 |
| S04 | Dorico 6.2 [Stem direction](https://www.steinberg.help/r/dorico-pro/6.2/en/dorico/topics/notation_reference/notation_reference_stems/notation_reference_stems_direction_c.html) | 单声部、多声部、和弦/梁/跨谱表的情境 | 支持“先看声部再按音高定符干”；不把其每条自动策略照搬到 Evolution。 |
| S05 | Dorico 6.2 [Slur endpoint positions](https://www.steinberg.help/r/dorico-pro/6.2/en/dorico/topics/notation_reference/notation_reference_slurs/notation_reference_slurs_position_endpoint_c.html) | 线间/线上、符头侧/干侧、发音法、延音和叠加弧线 | 学习情境分类；示例数值是软件默认值，不是必须采用的个人样式。 |
| S06 | Dorico 6.2 [Slur collision avoidance](https://www.steinberg.help/r/dorico-pro/6.2/en/dorico/topics/notation_reference/notation_reference_slurs/notation_reference_slurs_collision_avoidance_c.html) | 改形/移动端点的权衡、跨谱表复杂性、变音记号穿越例外 | 支持分层碰撞判断；不能据此证明 MuseScore 同样处理。 |
| S07 | Dorico 6.2 [Positions of dynamics](https://www.steinberg.help/r/dorico-pro/6.2/en/dorico/topics/notation_reference/notation_reference_dynamics/notation_reference_dynamics_positions_c.html) | 钢琴两谱表之间、独立力度例外、与弧线/踏板的层次 | 标记归属及放置惯例；不把谱表间中心线当固定坐标。 |
| S08 | Dorico 6.2 [Aligning dynamics](https://www.steinberg.help/r/dorico-pro/6.2/en/dorico/topics/notation_reference/notation_reference_dynamics/notation_reference_dynamics_aligning_t.html) | 图形对齐可与分组分开，布局作用域 | 对齐与音乐关系分开处理的实现参考。 |
| S09 | Dorico 6.2 [Voice-specific dynamics](https://www.steinberg.help/r/dorico-pro/6.2/en/dorico/topics/notation_reference/notation_reference_dynamics/notation_reference_dynamics_voice_specific_c.html) | 独立声部力度与默认整乐器范围 | 说明作用域需要明示；当前 MS3 范围模型另核源码，不能等同。 |
| S10 | Dorico 6.2 [Positions of octave lines](https://www.steinberg.help/r/dorico-pro/6.2/en/dorico/topics/notation_reference/notation_reference_octave_lines/notation_reference_octave_lines_positions_c.html) | 高/低八度线的上下位置、图形位移与时间范围分离 | 8va 外形优化不能改变实际作用音符。 |
| S11 | LilyPond [Optical spacing](https://lilypond.org/doc/v2.25/Documentation/essay/optical-spacing) | 音符/符干组合造成的视觉间距、小节线影响 | 官方设计解释；是候选评价依据，不是单一距离公式。核查的是 2.25 开发文档。 |
| S12 | Dorico 6.2 [Note spacing options](https://www.steinberg.help/r/dorico-pro/6.2/en/dorico/topics/engrave_mode/engrave_mode_note_spacing_page_layout_options_r.html) | 时值间距与实际占宽、跨谱表 optical spacing、末行伸展 | 说明理想时间网格与占宽约束可以分开；不照搬默认阈值。 |
| S13 | LilyPond 2.26 [Page breaking](https://lilypond.org/doc/v2.26/Documentation/notation/page-breaking) | 普通最优分页与翻页优化不同、允许翻页位置、扫描无音区段 | 实现思路；钢琴是否腾得出手还需演奏条件，不直接套声部休止长度。 |
| S14 | LilyPond [Beauty contests](https://lilypond.org/doc/v2.25/Documentation/essay/beauty-contests) | 多候选布局评分 | 自动净书架构参考，评分权重必须用本项目案例验证。 |
| S15 | 本机 Evolution 源码 `libmscore/beam.cpp`、`dynamic.cpp`、`dynamic.h`、`bracket.cpp` | 梁生成、力度范围读入/默认、Leland名称触发的括号几何分支 | 本机实现事实，位置见 IMPLEMENTATION；不推断上游所有版本。只读核查，软件仓库并发变更可能改变行号。 |
| S16 | 本项目 QML 桥及 `src/tools/connection.py` | 当前读谱字段与已注册能力 | 能力缺口依据；“Plugin API 可读”与“已有 MCP 工具返回”分开。 |
| S17 | 用户OneDrive本地 *Behind Bars* (2011)，696页PDF | Keyboard及连音、装饰音/震音、重复、间距、翻页等定向正文；20个图页 | 本次读取范围/页码/未读处见 [BEHIND_BARS_NOTES.md](BEHIND_BARS_NOTES.md)；没有通读全书，正文不提交。 |

## 本批从教材取用的原则

连梁让拍子结构容易辨认，具体分组要看拍号和上下文；3/4、6/8 不能只因总时值相等就同排。4/4 的半小节分界有阅读作用，但须识别有意的节奏表达，不能把所有跨界梁当待自动修复错误。长跨度标记要体现层级。谱表尺寸需考虑使用距离和场景，不能把某一种演出材料的尺寸建议直接套给钢琴谱。[S01](https://behindbarsnotation.co.uk/contents/sample_pages.pdf)

## 本项目的判断等级

1. **语义保护**：音高/拼写、书面和实际时值、发音起点、延音链、声部、跨度标记范围、力度作用域等。优化外观不能悄悄改变这些内容。
2. **情境规范**：支持拍子辨认、声部跟踪、标记归属的排法；必须先满足触发条件，保留例外。
3. **出版/个人偏好**：符头黑度、弧线厚度、整体紧凑程度、文字字号等。偏好可以有目标区间，不能冒充唯一正确排法。
4. **本例假说**：根据版面提出的阅读解释或候选改法；未做同曲对照/读谱验证前，不声称已经改善阅读速度。

PDF 观察标为“可见事实”，工程 XML 标为“结构事实”，原生同曲试验标为“受控对照”。出版者为何如此排版没有直接访谈资料，本库提供有规范支持的解释，并记录其他可能原因。统计外观不能反推出作者一定手动调整过某个参数。

## 下一批学习缺口

扩大研究已定向核查声部休止、连音数字/括号、装饰音、指法/手分配、踏板和跳转；见S17与 [覆盖矩阵](EXPANDED_RESEARCH.md)。下一步补切分时值拆写、变音重复提示/跨小节与跳转后的记忆、附点/二度几何、嵌套比例和跨页tie/Slur。教材条件已核不代表工程实现或打印通过；新条目必须附可查来源与正反例。

## 2026-10-10 横向专题增补来源

Gould主文件新增完整图页p39–43、87–88、489–490；5份官谱为Again、Black Catcher、Cry Baby、unravel、Kaikai Kitan，本次近读页与定位见 [SPACING_STUDY](SPACING_STUDY.md) 和 [spacing_evidence.json](spacing_evidence.json)。不反推PDF的编辑声部或出版者操作。用户PDF第2页测量结合release5只读结构核查，但不证明二者逐对象一致。

再次核查[Dorico part nine](https://blog.dorico.com/2014/12/development-diary-part-nine/)、[part 11](https://blog.dorico.com/2015/06/development-diary-part-11/)、[6.2间距层次](https://www.steinberg.help/r/dorico-pro/6.2/en/dorico/topics/engrave_mode/engrave_mode_note_spacing_c.html)、[跨谱表符干光学选项](https://www.steinberg.help/r/dorico-pro/6.2/en/dorico/topics/notation_reference/notation_reference_beaming/notation_reference_beaming_cross_staff_optical_changing_to_t.html)（检索正文可读，直接打开cache miss）与[LilyPond光学间距](https://lilypond.org/doc/v2.25/Documentation/essay/optical-spacing)。旧设计/竞争比较与当前文档区分，本次未运行Dorico作同曲测试。

只读本机 `libmscore/measure.cpp`、`segment.cpp`、`shape.cpp`、`layout.cpp`、`style.cpp`，源码定位见专题；自制fixture在 [fixtures](fixtures/README.md)，原生SVG标记MuseScore 3.7.0。源码HEAD与安装二进制的精确对应未确认，不将其称为该源码提交的完整构建回归。原始文件保护和无改善候选状态均有记录。
