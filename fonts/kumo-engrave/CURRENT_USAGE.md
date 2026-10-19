# 使用 Kumo Score Study 0.500

本机个人音乐字体，以所给 Animenz 官谱为参考，处理112个码位，保留完整Leland底库及未改字形。音乐字体502字形、配套Text字体266字形。全目录覆盖说明见 [FONT_DELIVERY](FONT_DELIVERY.md)；独立于MCP和skill安装。

## 安装和选择

1. 取得本机 `dist/kumo-score-study-0.500-complete-local.zip`。这是资料补全包；两个字体家族与原0.500包逐字节相同，已经安装0.500者不用重复安装。
2. 在Evolution偏好设置查看 **Score Fonts／乐谱字体** 目录，然后退出Evolution。解压后，将 **Kumo Score Study** 和 **Kumo Score Study Text** 两个完整文件夹复制进该目录。每个文件夹内的OTF、JSON及文件夹名称应相同；不要把两者的文件混放在目录根部。
3. 重新打开Evolution，使用乐谱**独立副本**。在 **格式 → 样式 → 乐谱** 同时选择音乐符号字体 **Kumo Score Study**、音乐Text字体 **Kumo Score Study Text**。
4. 第一轮取消“使用所选字体的推荐样式／自动优化样式”，保持原谱距、字号及其他样式。mf、八度、踏板的Text尺寸已经在字体侧校准，详见 [TEXT_SIZING](TEXT_SIZING.md)。

专用波浪滑音需要 **Evolution个人0.71或后续包含该接口的版本**。较旧程序可加载字体，但会使用原来的滑音波形。源码的版本号不能证明当前运行的EXE已更新，见 [NATIVE_GLISSANDO](NATIVE_GLISSANDO.md)。普通音符、力度等已分别用原生程序验证。

本机已经备好独立0.71试用构建：`dist/Evolution-0.71-font-study/`。**先退出正在运行的Evolution，再在此目录双击 `Start-Font-Study.cmd`**。它使用独立设置，已预置两套字体，直接从上面第3步选择家族；现有安装程序和原配置保持。该构建的实际预配置与专用滑音已验证，版本细节见 [FONT_DELIVERY](FONT_DELIVERY.md)。

普通8va、sf等使用原生元素。额外的swing、特殊组合及Unicode入口见 [TEXT_EXTRAS](TEXT_EXTRAS.md)。字库不负责决定连梁分组、弧线、系统断行和页面布局；这部分由净书线继续处理。

## 以后怎样更新

退出Evolution，先把现有两个家族文件夹复制到Score Fonts搜索路径之外的备份目录，再成对更新完整文件夹并重启。同一家族无需重新选择；换家族名才需在副本中重新选择。**不用重装或重新配置MCP、skill，也不用安装到Windows系统字体目录。**

字体和参考派生资产保留本机使用，旧包与旧原型均保留。源PDF／MSCZ未修改；本包不包含原厂字体程序。完整验证范围、使用边界和源文件保护见 [FONT_DELIVERY](FONT_DELIVERY.md)。
