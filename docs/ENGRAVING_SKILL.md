# 钢琴净书skill：使用、关联与更新

最新工作分支已补[三层连音归属](engraving/TUPLET_OWNERSHIP_STUDY.md)：可用`--topic cross-staff --query "换表点 连音 加线"`查外置与近梁的实际取舍。三种上下文已核，m97真实候选尚待迁移；固定0.21仍是此前快照，引用最新补充时记实际Git提交。

0.21之后的工作分支已补[跨表连音通道及旧候选修正](engraving/TUPLET_CHANNEL_STUDY.md)。可查`--topic notation --query "跨表 连音 穿干"`；m97仅伸长右端的采用倾向已撤回，须结合范围、连接及独立层继续判断。关联安装读取更新后的项目即可；固定0.21标签保留原研究快照，尚不含本补充。

0.21纳入[梁坡与实曲应用](engraving/BEAM_WIDTH_TRANSFER.md)、[共梁范围](engraving/BEAM_SCOPE_TRANSFER.md)和[交换机理／换号回查](engraving/BEAM_EXCHANGE_CLEF_STUDY.md)。可查`--topic beams --query "声部归属 第一音 干向"`或`--topic clefs --query "E4 G4 换号"`。新案例在音乐起音保持时仍暴露图面、轨道和释放变化，先读实际验证范围；XML诊断输入用于复现，不能当通用转换补丁。关联／复制更新方式沿用下文，无新增MCP配置步骤。

2026-10-31。最近发布的可用研究版为**[0.21.0／engraving-v0.21.0](ENGRAVING_RELEASES.md)**；工作目录可含之后的知识更新，引用时同时记录实际Git提交。学习未完也可直接试用，能力与已知限制随版记录。入口为[skills/piano-engraving/SKILL.md](../skills/piano-engraving/SKILL.md)，基础判断核查见[FOUNDATION_REVIEW](engraving/FOUNDATION_REVIEW.md)。它把当前PDF／工程的阅读问题与项目知识库连接，形成有依据的保留、建议或原生副本候选；没有新增MCP、MuseScore插件／本体接口，也不是一键全谱净书。

## 按具体问题定位来源

保留原专题清单，另可直接查相关段落：

    python <skill目录>/scripts/engraving_library.py --topic notation --query "6:3 等值" --limit 3
    python <skill目录>/scripts/engraving_library.py --topic piano --query "S.P. A八度" --limit 3

返回匹配文件、标题、行号和至多700字符的原文节选；默认最多5份，可用1–20调整。不带查询时仍返回完整专题清单。查询在当前专题与共同入口内进行，支持中文关键词、英文和比例；关键词间可加空格。作者定义仍先读，词语排序不代表规范或审美正确性，命中后继续读相关上下文及原例。未命中时换词或回到专题列表，不补写未读内容。

脚本使用Python标准库、按需读取项目Markdown，不建立索引或媒体缓存。已知五类问题的来源定位属于检索回归，未计新的净书迁移成绩；旧命令、20专题、比例全角形式、空结果、限制参数及输入只读均已测试。

## 怎样使用

将这个项目保留在可读位置。skill先读知识库入口与偏好，再按当前情境取判断指南、专题／案例；skill自身的详细提醒也由表格链接按问题读取，不默认整库加载。长书和教程只在需要具体依据时查。项目的教材、原谱及图片缓存没有打包进skill，不能在另一电脑冒称这些私有材料都已存在。

可在支持技能选择的输入框选择“钢琴净书”；Codex CLI／IDE可显式写`$piano-engraving`。尚未安装发现入口时，也可以直接提供本项目`skills/piano-engraving/SKILL.md`的完整路径，要求读取并按其执行。例子：

```text
使用 $piano-engraving 只读分析这份钢琴PDF，找出最影响跟读和归属的地方。
先解释为什么值得改，以及哪些排法应该保留；不要修改原件。
```

```text
使用 $piano-engraving 比较这两个原生排版候选。
不要只看是否等距，检查拍组、声部、标记层次和其它系统的连带效果。
```

分析不要求先启动MCP。需要生成原生候选时，使用本机确实可用的宿主／工具，先在副本完成音乐、记法和版面核查。打印／试奏未做时列明状态，不当作阅读分析的前置门槛。

## 本地发现与维护方式

OpenAI官方说明：本地技能从项目`.agents/skills`及用户`~/.agents/skills`等位置发现，支持符号链接技能目录。详见[官方Build skills](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)。以下只关联这个净书skill，不调用原项目MCP安装器或改动MCP配置。2026-10-24检查上述用户位置及旧`~/.codex/skills`同名位置均未发现安装；本次验证的是项目内入口可用，没有宣称当前App已发现此skill。

在Windows上可把用户技能目录中的一个目录联接指向本项目skill，避免复制后维护两份。以下命令在同名目标已存在时停止，不删除或覆盖任何内容：

```powershell
$engravingRepo = 'E:\programming\funcodes\mcp-musescore'
$engravingSource = Join-Path $engravingRepo 'skills\piano-engraving'
$engravingRoot = Join-Path $HOME '.agents\skills'
$engravingTarget = Join-Path $engravingRoot 'piano-engraving'
if (-not (Test-Path -LiteralPath (Join-Path $engravingSource 'SKILL.md'))) {
    throw 'Skill source missing; check the checkout path.'
}
if (Get-Item -LiteralPath $engravingTarget -Force -ErrorAction SilentlyContinue) {
    throw 'Target already exists; inspect it before changing its installation.'
}
New-Item -ItemType Directory -Path $engravingRoot -Force | Out-Null
New-Item -ItemType Junction -Path $engravingTarget -Target $engravingSource
```

也可在本机支持时使用`SymbolicLink`，或在其它系统按官方支持的符号链接关联同一文件夹。目录联接的文件访问和知识库定位可在项目隔离目录验证；本轮不把这种检查冒充已修改用户技能目录或在当前App中成功发现。本轮交付的是项目内skill及安装方法，没有自动执行上面的用户目录写入。

若选择复制安装，保留整个skill文件夹；知识库仍以此项目的`docs/engraving`为准。定位器可显式指定仓库，不必复制整套教材：

```text
python <skill目录>/scripts/engraving_library.py --repo <mcp-musescore项目路径> --topic spacing
```

定位器只输出实际文件路径，不读取／修改乐谱、不启动软件或网络；只需Python 3.10+标准库。源位置的关联安装会解析真实目录；复制后可用`--repo`、已有`MCP_MUSESCORE_DIR`或在本项目中运行来定位。错误的显式位置会报错，避免悄悄读另一份库。

## 以后更新需要重装吗

关联安装时，`git pull`更新这个项目即可同时更新skill正文和知识库，通常不需重装；App未重新显示时按官方说明刷新／重启。仓库搬家时才需更新关联位置。复制安装则需同步改变过的skill文件；知识库路径仍指向更新后的项目。

仅更新这些净书文档／skill，不需要重新注册或配置MCP。MCP代码、依赖、启动路径或宿主插件另有变更时，按那一组件的实际更新要求处理；技能安装与MCP连接是两件事。不要为了加载净书知识而重装软件环境。

## 验证范围

创建格式使用系统skill-creator校验；路径定位测试覆盖源码目录、复制目录、关联目录、显式／环境位置优先级、错误位置和专题引用。它们只证明技能包与定位器的结构／行为，不证明审美判断正确。实际任务使用与已知边界记录在[SKILL_REVIEW](engraving/SKILL_REVIEW.md)，机器可复查结果在[skill_validation.json](engraving/skill_validation.json)。

后续根据真实乐谱判断和用户反馈更新对应专题，不通过复制整本资料、追加无条件规则或改一组默认数值声称知识已经掌握。软件自动净书适配留到以后单独开展。
