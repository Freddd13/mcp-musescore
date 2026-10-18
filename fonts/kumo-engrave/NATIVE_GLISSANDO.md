# 0.490：让专用滑音波形在谱面生效

2026-10-19。字体0.490与0.480的所有Music/Text轮廓、字宽、字框、垂直度量、字符映射及布局表逐项一致，仍处理112个码位、保留完整Leland底库。只在Study音乐JSON增加可选声明：

```json
{"kumoEngraving":{"wavyGlissandoGlyph":"wiggleGlissando"}}
```

此字形此前已制作，但MuseScore3的原生波浪滑音固定使用`wiggleTrill`，改专用字形不会影响实际对象。Evolution个人0.71接口允许外部字体声明所需字形，不按私人家族名硬编码。旧宿主忽略声明，仍用原波形；内置字体及未声明字体保持旧行为。普通颤音、直滑音不变，不需要MCP/skill。

## 实际验证

- 独立原生Release构建并完整安装；五组声明用例及初始化/清理共7项通过。检查缺省、未知名字、只在回退字体存在、空墨迹、有效声明和字体复制；用真实栅格墨迹检查水平、升降、反向、极短和零长外框。
- 自制八小节钢琴谱覆盖升降滑音、直线对照、密集32分、跨谱表、跨行和颤音对照。0.480与0.490用同一宿主渲染；Control全页逐像素一致，Study仅波浪滑音路径改变，直滑音与所有其它SVG元素一致。输出`dist/native-gliss-104-125/`、`native-gliss-114-125/`，核查`native-gliss-audit-127.json`。
- 五类实际尺寸：mf **2.4854sp**、8 **0.9649sp**、8va **0.9391sp**、Ped. **1.7738sp**、解除星号 **1.1391sp**，与0.480完全一致。用户谱两字体副本仍9页；原MSCZ SHA保持`4a62cc33723b1c19a207102f27425c983e9fd40d570a2ff65d7a818b82ac91ad`，只改两项字体字段，附件保留。十组力度组合/整字墨迹IoU均1。输出`dist/native-size-128/`、`native-size-audit-130/`。
- `audit_font_geometry.py`确认四套Music/Text全部轮廓与度量保持，结果`dist/font-geometry-129.json`。字体构建仅改变版本声明，19个Text尺寸校正继续保留。

首次隔离启动失败已查明缺少安装的workspaces数据，`cmake --install`补齐后测试与导出通过；没有修改用户安装目录来修复。原谱、PDF和全局设置保持。实际打印、更多屏幕缩放和所有少见角色尚未验收，不能由本接口通过推断整套目标完成。

随后合入原生0.70更新并重新构建、安装、验证，7项测试与谱面检查均通过。最终宿主SHA256 `be8c3894c01256fbe039085981dbd5ccd26da8e0a7b80f051e81b15be2878d8b`；最终滑音`dist/native-gliss-133/`，尺寸/用户谱`native-size-134/`与`native-size-audit-135/`，保护结果见`native-size-134/score-protection.json`。功能提交`MuseScore@4a4ef1a5e`，整合`3ff1a61d5`保留0.70的`d24539071`，版本定位`personal-v0.71.0`。

## 试用与更新

本机包为`dist/kumo-score-study-0.490-local.zip`。退出Evolution，将Study与Study Text两个完整文件夹成对更新到偏好设置的Score Fonts目录并重启；乐谱副本选两套家族，保持原字号和其它样式。无需重装MCP、skill或Windows字体。0.480已安装者只有想试专用滑音时才需要此次字体更新；效果需要个人0.71宿主。源码合入不等于用户正在运行的程序已替换。

接口源码、用户说明和测试存于MuseScore个人仓库；字体构建与诊断存于本项目。保留0.480包。参考曲线/字体包仅本机研究，不公开提交；公开脚本不含原PDF字体程序。后续仍需处理成员语义及其它图录，见[COVERAGE_RECONCILIATION](COVERAGE_RECONCILIATION.md)。
