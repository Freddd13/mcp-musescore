# 本机研究材料的位置

2026-10-30 MOLA英文补读：本批约2.71MiB，总净书缓存约2.723GiB（最终小记录前）。25视图中10复用、15新图；复用已有英文／中文PDF与运行时，无原谱副本或删除，低于100MiB／3GiB检查线。[时点与字节](mola_english_reading_evidence.json)。

2026-10-26 Butter-Fly／Call of Silence批次清点：本批5,707,013字节（约5.44MiB），全部研究缓存2,457,560,654字节（约2.289GiB逻辑长度）；Windows按路径报告存储长度2,316,271,427字节，不能当卷空间净变化。复用14张官谱整页与13张教材页，新增19处完整系统细图及10张教材页，无原PDF／运行时副本、删除或扫描错误。均低于既定检查线；时点及完整范围见[本批证据](butterfly_silence_closeout_evidence.json)。

2026-10-26占位批次复用冻结宿主及前批原创输入，新目录初次汇总2,008,713字节（约1.92MiB），全部净书缓存2,451,896,869字节（约2.284GiB逻辑长度）；计量时点见[证据](twenty_to_six_occupancy_evidence.json)，后续笔记脚本有小幅增长。均低于100MiB／3GiB检查线，无原PDF／运行时副本及删除。新增文件主要为10个原生条件的导出与校验记录，不复制官谱整页。

2026-10-18按用户要求，将本对话旧临时目录迁到E盘项目内。原谱和书籍仍从用户提供的OneDrive位置只读，不迁移原件。

| 材料 | 当前位置 |
| --- | --- |
| 2026-10-08至10-10的渲染、试验、教材图页、脚本 | `E:\programming\funcodes\mcp-musescore\tmp\engraving\legacy-2026-10-08` |
| 146份官谱的页面渲染和阅读辅助文本 | `E:\programming\funcodes\mcp-musescore\tmp\engraving\corpus\A编号` |
| 迁移逐文件记录 | `tmp/engraving/cache-migration.json` |

旧路径前缀 `C:\Users\Fred\.codex\visualizations\2026\10\08\01a11a5f-d840-7eb3-84c2-39e9d493a830` 对应上表的legacy目录。历史JSON、命令日志、旧脚本保留当时路径作为证据；查找旧图时替换此前缀即可，不重新执行会写C盘的旧脚本。当前文档中的图集入口已改为E盘。

迁移核查：685个文件、133,438,772字节，逐文件SHA-256一致，原C盘任务目录已不存在。本机完整清单保留在迁移记录中。此结论仅覆盖本对话该目录；其它任务和运行时公共依赖不属于本次缓存。

新临时数据统一使用`tmp/engraving/`，该目录被Git忽略，避免把书页和参考谱渲染提交到仓库。Python使用`-B`并将TEMP/TMP指向这里。跨电脑复查可用[只读准备脚本](../../tools/engraving/corpus.py)重新渲染；生成图不等于完成阅读。

## 2026-10-23清点与无损减量

本次操作只涉及项目忽略缓存，原PDF／MSCZ、字体任务和软件源码均不在范围内。清点时9,775个文件，共2,323,686,224字节逻辑数据，约2.16GiB；其中官谱缓存约1.14GiB，已经用于多次复读，不因属于tmp就视为无用。

两份已有实验宿主目录采用NTFS透明压缩：

| 缓存目录 | Windows报告存储长度减少 |
| --- | ---: |
| `leading-reserve-2026-10-21/runtime-with-assets` | 84,775,082字节 |
| `seconds-ownership-2026-10-19/frozen-host-7b4e6fbf` | 56,514,145字节 |
| 合计 | **141,289,227字节，约135MiB** |

压缩前后2,346个文件的路径集合与逐文件SHA-256一致，没有删除、移动或替换文件内容。清点后缓存整体约2.03GiB存储长度，新增的小型清点／哈希记录另计。该值来自Windows `GetCompressedFileSizeW`按路径求和，未按硬链接去重，不等于卷空闲量净增长；其它任务也可能同时使用磁盘。[摘要证据](cache_maintenance_evidence.json)保留实际范围，完整哈希及compact输出留在`tmp/engraving/status-report-2026-10-23/`。

只读复查命令，在项目根目录运行：

```text
python -B tools/engraving/cache_inventory.py
```

工具只清点本项目净书缓存，不跟随子目录链接／重解析点，不扫描OneDrive原件，不压缩或删除数据；输出逻辑体积、Windows存储长度、逐批占用与读取错误。只清点不产生新的谱面图。

## 后续缓存预算与保留

- 每批开始复用已有原页、谱例和宿主。源哈希／页码／渲染条件相符才复用；需要其它倍率或去批注时只补所需页，不再整套重渲染。
- **单批新增100MiB、总逻辑体积3GiB作为检查线**。接近时先清点增长原因、复用率及必要性；确需超出则记录具体材料与预算，不把检查线当自动删除阈值。
- 宿主按实际二进制与资产指纹复用；新研究不另复制同版本运行时。每批独立的是输入副本、配置和结果，不能为省空间让实验共写用户配置或GUI当前谱。
- 长期保留知识、证据摘要、可重建的原创输入／配方、关键对照及原生重载结果。私有参考图留本机；源PDF本身不再复制一套进研究目录。
- 失败试排优先保留小输入、原因和必要对照，避免每次都输出全谱所有格式。已经完整验证的批次不为汇报再导出一遍；发布直接打Git标签，不另复制整套缓存做发布包。
- 当前遵守AGENTS的“不在未得到同意的基础上删除任何文件”。本次通过复用规则和无损压缩减量；已有大目录若需删除，先形成明确文件范围及可重建／保留依据，再按用户授权处理，不用年龄或tmp名称推定可删。

2026-10-26本批团子大家族／Hanezeve缓存约4.78MiB；总净书缓存约2.293GiB逻辑长度。复用18张图，新存17处系统、八张新教材及两张页码纠正后的旧页；没有原PDF／运行时副本或删除。低于100MiB／3GiB检查线，清点先于最终验证小记录；完整尺寸见[本批证据](dango_hanezeve_closeout_evidence.json)。

2026-10-26手册／Spacing批次缓存约0.53MiB，总净书缓存约2.294GiB逻辑长度。复用1936文件运行时，无新宿主或原谱副本；仅五份原创小输入、30次导出／重载及必要记录，未删除文件。14官方图请求失败只存小型状态记录；清点先于最终验证记录，仍低于100MiB／3GiB检查线，见[证据](musescore3_layout_reading_evidence.json)。

2026-10-26 Catch／Change批次清点：本批约7.69MiB，全部净书缓存约2.302GiB逻辑长度；复用13张整页，新增27张系统／扩大上下文图及20张教材图（8新、12复读）。无原PDF／运行时副本、删除或扫描错误，低于100MiB／3GiB检查线；时点和精确字节见[本批证据](catch_change_closeout_evidence.json)，清点先于最后小记录。

2026-10-27 COLORS／crossing批次清点：本批约9.43MiB，总净书缓存约2.311GiB逻辑长度。复用19张图，新增19张系统、27张教材整页和六张复杂图放大；无原PDF／运行时副本、删除或扫描错误，低于既定100MiB／3GiB检查线。完整字节与时点见[证据](colors_crossing_closeout_evidence.json)，清点先于最后小记录。

2026-10-27 Cry／Daisy批次缓存约8.21MiB，总净书缓存约2.319GiB逻辑长度；复用18张图，新增50张（23系统、25教材整页、两放大图）。无原PDF／运行时副本、删除或扫描错误，低于100MiB／3GiB检查线；[时点和精确字节](cry_daisy_closeout_evidence.json)先于最后小记录。

2026-10-27 Departures批次缓存约7.56MiB，总净书缓存约2.326GiB逻辑长度；复用22张图，新增48张（29系统、17教材整页、两处梁端）。无原PDF／运行时副本、删除或清点错误；低于100MiB／3GiB检查线，[精确字节及时间](departures_closeout_evidence.json)先于最终小记录。

2026-10-27 Lazy／Eien批次缓存约8.12MiB，总净书缓存约2.334GiB逻辑长度；复用23张图，新增51张。74张实际查看图含32系统及一处两行连读；旧book-142实为p122，本批另读真正p142，未删除／重计覆盖。无原PDF／运行时副本或清点错误；低于100MiB／3GiB检查线，[精确字节和时点](lazy_eien_closeout_evidence.json)先于最终小记录。

2026-10-27 EONIAN／Euterpe批次缓存约10.67MiB，总净书缓存约2.345GiB逻辑长度；复用23张，新增63张。86张实际查看图含39系统、两局部、34教材页；旧194／195名实为174／175已更正记录并另读实际页。无原PDF／运行时副本、删除或清点错误；低于100MiB／3GiB检查线，[字节和时点](eonian_euterpe_closeout_evidence.json)先于最终小记录。

2026-10-27 Everyday／Extra批次缓存约9.64MiB，总净书缓存约2.354GiB逻辑长度；79张实际阅读图复用24张、新增55张。无原PDF／运行时副本、删除或清点错误，低于100MiB／3GiB检查线；[字节和时点](everyday_extra_closeout_evidence.json)先于最终小记录。

2026-10-27 Fate／Frieren批次缓存约17.07MiB，总净书缓存约2.371GiB逻辑长度；120张实际阅读图复用32张、新增88张。原PDF／运行时没有副本、删除或清点错误，低于100MiB／3GiB检查线；[精确字节与时点](fate_frieren_closeout_evidence.json)先于最终小记录。

2026-10-27吹雪／无限城批次缓存约13.21MiB，总净书缓存约2.384GiB逻辑长度；99张实际阅读图复用27张、新增72张。无原PDF／运行时副本、删除或清点错误，低于100MiB／3GiB检查线；[精确字节与时点](fubuki_castle_closeout_evidence.json)先于最终小记录。

2026-10-27 God knows／宝可梦批次缓存约12.92MiB，总净书缓存约2.396GiB逻辑长度；108张实际阅读图复用30张、新增78张。无原PDF／运行时副本、删除或清点错误，低于100MiB／3GiB检查线；[精确字节与时点](god_pokemon_closeout_evidence.json)先于最终小记录。

2026-10-27 Grand Escape／Great Days批次缓存约13.37MiB，总净书缓存约2.409GiB逻辑长度；87张实际阅读图复用23张、新增64张。无原PDF／运行时副本、删除或清点错误，低于100MiB／3GiB检查线；[精确字节与时点](grand_great_closeout_evidence.json)先于最终小记录。

2026-10-27 Gurenge／Hacking批次缓存约12.75MiB，总净书缓存约2.422GiB逻辑长度；88张记录图复用23张、新增65张。无原PDF／运行时副本、删除或清点错误，低于100MiB／3GiB检查线；[精确字节及单页复渲说明](gurenge_hacking_closeout_evidence.json)先于最终小记录。

2026-10-27拉威尔资源批次缓存约9.16MiB，总净书缓存约2.431GiB逻辑长度；46张新图、15张旧教材图复用，另新增两份公开参考PDF共289860字节。用户原PDF／MSCZ／教材及运行时无副本或改写，无删除或清点错误，低于100MiB／3GiB检查线；[精确时点](legato_ravel_reading_evidence.json)先于最终小记录。

2026-10-27光るなら／History Maker批次约11.60MiB，总净书缓存约2.442GiB逻辑长度；99图记录复用28张、新增71张。无原PDF／运行时副本、删除或扫描错误，低于100MiB／3GiB检查线；[精确时点与复渲说明](hikaru_history_closeout_evidence.json)先于最终小记录。

2026-10-27 Homura／Hyori批次约15.01MiB，总净书缓存约2.457GiB逻辑长度；127图记录复用33张、新增94张。无原PDF／运行时副本、删除或清点错误，低于100MiB／3GiB检查线；[精确时点及四处页码纠正](homura_hyori_closeout_evidence.json)先于最终小记录。

2026-10-27 Ichiban／Idol批次约12.88MiB，总净书缓存约2.470GiB逻辑长度；100图记录复用26张、新增74张。无原PDF／运行时副本、删除或清点错误，低于100MiB／3GiB检查线；[精确时点及三页复渲说明](ichiban_idol_closeout_evidence.json)先于最终小记录。

2026-10-28 Imagination／pool批次约11.76MiB，总净书缓存约2.481GiB逻辑长度；99图记录复用30张、新增69张。无原PDF／运行时副本、删除或清点错误，低于100MiB／3GiB检查线；[精确时点](imagination_pool_closeout_evidence.json)先于最终小记录。

2026-10-28 IRIS／Kaibutsu批次约12.40MiB，总净书缓存约2.493GiB逻辑长度；实际阅读62图，另50张预制但未读，不计成果。后续按需裁图，避免预制闲置；本批无原PDF／运行时副本、删除或清点错误，低于检查线。[精确时点](iris_kaibutsu_closeout_evidence.json)先于最终小记录。

2026-10-28炭治郎／舰队批次约11.59MiB，总净书缓存约2.505GiB逻辑长度。只渲染18处需要的系统；39页辅助内容用7拼页核查，5页序言另直接读，共52张实际显示图。无原PDF／运行时副本、删除或清点错误，低于检查线。[精确时点](tanjiro_kantai_closeout_evidence.json)先于最终小记录。

2026-10-29内梁批次缓存约2.67MiB，总净书缓存约2.507GiB逻辑体积。复用既有1936文件运行时及两张Gould旧页；原生输出按三条件及保存／交换核查生成，没有新原PDF／运行时副本或删除，低于检查线。[精确时点与字节](inner_beam_hierarchy_evidence.json)先于最后小记录；发布仅三份原创谱及两张同框图。

2026-10-29 Kawaki／JANE批次缓存约2.86MiB，总净书缓存约2.510GiB逻辑长度。39张实际显示图中22张复用、17张新图（15系统及2教材复读），无原PDF／运行时副本或删除，低于检查线。[精确时点与字节](kawaki_jane_closeout_evidence.json)先于最后小记录。

2026-10-29 Key／KICK批次约3.70MiB，总净书缓存约2.514GiB逻辑长度；58张已看图中36张复用、22张新系统图。无原PDF／运行时副本或删除，低于100MiB／3GiB检查线。[字节与时点](key_kick_closeout_evidence.json)先于最后小记录。

2026-10-29 Kigeki／Killy批次约5.24MiB，总净书缓存约2.519GiB逻辑长度；51张已看图中25张复用、26张新系统图。无原PDF／运行时副本或删除，低于100MiB／3GiB检查线。[字节与时点](kigeki_killy_closeout_evidence.json)先于最后小记录。

2026-10-29 Kimi／Kizuna批次约4.79MiB，总净书缓存约2.524GiB逻辑长度；60张已看图中32张复用、28张新系统图。无原PDF／运行时副本或删除，低于100MiB／3GiB检查线。[字节与时点](kimi_kizuna_closeout_evidence.json)先于最后小记录。

2026-10-29 KonoSuba／Kuchizuke批次约5.96MiB，总净书缓存约2.530GiB逻辑长度；67张已看图中33张复用、34张新图（33系统及1必要末小节）。无原PDF／运行时副本或删除，低于100MiB／3GiB检查线。[字节与时点](konosuba_kuchizuke_closeout_evidence.json)先于最后小记录。

2026-10-29 Kura／Kuusou批次约6.23MiB，总净书缓存约2.536GiB逻辑长度；68张已看图中33张复用、35张新图（34系统＋一张旧覆盖教材页212重渲染）。无原PDF／运行时副本或删除，低于100MiB／3GiB检查线。[字节与时点](kura_kuusou_closeout_evidence.json)先于最后小记录。

2026-10-29 Kyouran／Conan批次约5.34MiB，总净书缓存约2.541GiB逻辑长度；58张已看图中27张复用、31张新系统图。无原PDF／运行时副本或删除，低于100MiB／3GiB检查线。[字节与时点](kyouran_conan_closeout_evidence.json)先于最后小记录。

2026-10-29部分梁短括号批次约0.83MiB，总净书缓存约2.542GiB逻辑长度；复用1936文件固定运行时，22次CLI按两候选及自动探针核查。新增原创输入／导出与两张同框图，无原PDF／MSCZ／运行时副本、删除或清点错误，低于100MiB／3GiB检查线。[精确字节与时点](partial_tuplet_brackets_evidence.json)先于最后小记录；发布三份原创谱及两图。

2026-10-29 Melissa／Merry批次约6.34MiB，总净书缓存约2.548GiB逻辑长度；65张实际看图中32张复用、33张新系统图。无原PDF／运行时副本、删除或清点错误，低于检查线。[精确字节与时点](melissa_merry_closeout_evidence.json)先于最后小记录。

2026-10-29 Miiro／Mixed批次约5.23MiB，总净书缓存约2.553GiB；58张实际看图中31张复用、27张新系统细节。无原PDF／运行时副本、删除或清点错误，低于检查线。[精确字节与时点](miiro_mixed_closeout_evidence.json)先于最后小记录。

2026-10-29 Dearest／Hero批次约7.93MiB，总净书缓存约2.561GiB；73张不同实际视图中31复用、42新图。无原PDF／运行时副本、删除或清点错误，低于检查线；两处误选书页未计19页且旧图保留。[精确字节与时点](dearest_hero_closeout_evidence.json)先于最后小记录。

2026-10-29 Soul／My War批次约6.90MiB，总净书缓存约2.568GiB；66张不同实际视图中28复用、38新图。无原PDF／运行时副本、删除或清点错误，低于检查线；书页按明确印刷／物理映射及可见页脚核选。[精确字节与时点](soul_war_closeout_evidence.json)先于最后小记录。

2026-10-29 Nagi／NieR批次约9.01MiB，总净书缓存约2.577GiB；89张不同实际视图中41复用、48新图。无原PDF／运行时副本、删除或清点错误，低于检查线；书页按明确印刷／物理映射及可见页脚核选。[精确字节与时点](nagi_nier_closeout_evidence.json)先于最后小记录。

2026-10-29 Kiss／Chance与嵌套连音两批缓存分别约7.47MiB／1.35MiB，总净书缓存约2.585GiB；62张官谱／书页视图26复用36新图，另看原创原生对照。没有原PDF／运行时副本或删除，低于检查线；初次次梁指令错误探针保私有不发布。[精确字节和时点](kiss_chance_closeout_evidence.json)先于最后小记录。

2026-10-29 Railgun／Pierce本批约8.46MiB，总净书缓存约2.593GiB；76张本地实际视图33复用43新图，R22两图及封面仅浏览器查看未下载。无原PDF／运行时副本或删除，低于100MiB／3GiB检查线；[精确字节与时点](railgun_pierce_closeout_evidence.json)先于最后小记录。

2026-10-29 Resonance／Rising本批约9.62MiB，总净书缓存约2.603GiB；87张本地视图34复用53新图，R20十四图仅浏览器查看。无原PDF／运行时副本或删除，低于100MiB／3GiB检查线；[精确字节与时点](resonance_rising_closeout_evidence.json)先于最后小记录。

2026-10-30 Sakayume／Sayonara本批约14.22MiB，总净书缓存约2.617GiB；105张不同本地视图38复用67新图。无原PDF／字体／运行时副本或删除，浏览器视频未下载；低于100MiB／3GiB检查线。[精确字节与时点](sakayume_sayonara_closeout_evidence.json)先于最后小记录。

2026-10-30 Shinzou／Shirushi本批约12.39MiB，总净书缓存约2.629GiB；101张不同本地视图36复用65新图。无原PDF／字体／运行时副本或删除，低于100MiB／3GiB检查线。[精确字节与时点](shinzou_shirushi_closeout_evidence.json)先于最后小记录。

2026-10-30 Silhouette／Sirius本批约14.36MiB，总净书缓存约2.643GiB；114张不同本地视图35复用79新图。无原PDF／字体／运行时副本或删除，低于100MiB／3GiB检查线。[精确字节与时点](silhouette_sirius_closeout_evidence.json)先于最后小记录。

2026-10-30 Snow／Sparkle本批约15.52MiB，总净书缓存约2.658GiB；108张不同本地视图32复用76新图。无原PDF／字体／运行时副本或删除，低于100MiB／3GiB检查线。[精确字节与时点](snow_sparkle_closeout_evidence.json)先于最后小记录。

2026-10-30 SPECIALZ／Ghibli本批约16.27MiB，总净书缓存约2.674GiB；126张不同视图41复用85新图。无原PDF／字体／运行时副本或删除，低于100MiB／3GiB检查线。[精确字节与时点](specialz_ghibli_closeout_evidence.json)先于最后小记录。

2026-10-30 STYX／Sugar本批约16.86MiB，总净书缓存约2.691GiB；126张不同视图37复用89新图。无原PDF／字体／运行时副本或删除，低于100MiB／3GiB检查线。[精确字节与时点](styx_sugar_closeout_evidence.json)先于最后小记录。

2026-10-30 Suzume／Swordland本批约15.60MiB，总净书缓存约2.706GiB；114张不同视图33复用81新图，含补全范围的一处放大。无原PDF／字体／运行时副本或删除，低于100MiB／3GiB检查线。[精确字节与时点](suzume_swordland_closeout_evidence.json)先于最后小记录。

2026-10-30 Tabi／Tamashii本批约14.62MiB，总净书缓存约2.720GiB；112视图33复用79新图，含完整M范围补图。无原PDF／字体／运行时副本或删除，低于100MiB／3GiB检查线。[字节与时点](tabi_tamashii_closeout_evidence.json)先于最终小记录。

2026-10-30 Everlasting／Heroes本批约10.26MiB，总净书缓存约2.733GiB；84视图30复用54新图，原PDF与运行时复用，未删文件。低于100MiB／3GiB检查线，[字节与时点](everlasting_heroes_closeout_evidence.json)在最终小记录前。

2026-10-30 Rumbling／Aether本批约9.02MiB，总净书缓存约2.742GiB；67视图19复用48新图，原PDF与运行时复用，未删文件。低于100MiB／3GiB检查线，[字节与时点](rumbling_aether_closeout_evidence.json)在最终小记录前。

2026-10-30 WORLD／Reason本批约12.70MiB，总净书缓存约2.754GiB；94个不同视图33复用61新图，原PDF与运行时复用，未删文件。低于100MiB／3GiB检查线，[字节与时点](world_reason_closeout_evidence.json)在最终小记录前。

2026-10-30 This Game两版本批约13.57MiB，总净书缓存约2.767GiB；101个不同视图32复用69新图，原PDF与运行时复用，未删文件。低于100MiB／3GiB检查线，[字节与时点](this_game_closeout_evidence.json)在最终小记录前。

2026-10-30 Beginning／To You本批约11.61MiB，总净书缓存约2.779GiB；91个不同视图30复用61新图，原PDF与运行时复用，未删文件。低于100MiB／3GiB检查线，[字节与时点](beginning_to_you_closeout_evidence.json)在最终小记录前。

2026-10-30 Tokimeki／Uchiage本批约10.95MiB，总净书缓存约2.789GiB；89不同视图33复用56新图，原PDF／运行时复用，未删文件。低于100MiB／3GiB检查线，[字节与时点](tokimeki_uchiage_closeout_evidence.json)在最终小记录前。

2026-10-30 unlasting／unravel本批约13.94MiB，总净书缓存约2.803GiB；107不同视图35复用72新图，原PDF／运行时复用，未删文件。低于100MiB／3GiB检查线，[字节与时点](unlasting_unravel_closeout_evidence.json)在最终小记录前。

2026-10-30 Uragirimono／Vogel本批约13.68MiB，总净书缓存约2.816GiB；118不同视图43复用75新图，原PDF／运行时复用，未删文件。低于100MiB／3GiB检查线，[字节与时点](uragiri_vogel_closeout_evidence.json)在最终小记录前。

2026-10-30 We Are!／Weight本批约16.01MiB，总净书缓存约2.832GiB；127不同视图44复用83新图，原PDF／运行时复用，未删文件。低于100MiB／3GiB检查线，[字节与时点](weare_weight_closeout_evidence.json)在最终小记录前。

2026-10-30 WILL／BIGGIRL本批约15.39MiB，总净书缓存约2.847GiB；125不同视图42复用83新图，原PDF／运行时复用，未删文件。低于100MiB／3GiB检查线，[字节与时点](will_biggirl_closeout_evidence.json)在最终小记录前。

2026-10-30 残响／红莲本批约19.07MiB，总净书缓存约2.866GiB；148不同视图40复用108新图，原PDF／运行时复用，未删文件。低于100MiB／3GiB检查线，[字节与时点](zankyou_guren_closeout_evidence.json)在最终小记录前。

2026-10-30 廻廻奇譚／残酷天使本批约18.38MiB，总净书缓存约2.884GiB；125不同视图39复用86新图，原PDF／运行时复用，未删文件。低于100MiB／3GiB检查线，[字节与时点](kaikai_cruel_closeout_evidence.json)在最终小记录前。

2026-10-30 Again／Akuma本批约16.92MiB，总净书缓存约2.900GiB；121不同视图38复用83新图，原PDF／运行时复用，未删文件。低于100MiB／3GiB检查线，[字节与时点](again_akuma_closeout_evidence.json)在最终小记录前。
