# 钢琴净书1.0：使用、安装与更新

当前首版：**1.0.0／engraving-v1.0.0**。包含已有知识库、20个专题入口、案例与原创正反例；可分析PDF／MuseScore工程，提出有依据的保留、改进建议或原生副本候选。软件自动净书适配待试用认可后开展。[能力与差距](engraving/STATUS_AND_ROADMAP.md) · [固定清单](engraving/release_1_0_0_evidence.json) · [示范](engraving/V1_TRIAL.md)。

## 怎样使用

本机安装后，在下一回合选择“钢琴净书”或写`$piano-engraving`，附PDF／MSCZ完整路径和任务范围。可以先用这句：

```text
使用 $piano-engraving 只读审查这份钢琴谱：<完整路径>。
先看完整曲谱，找最影响跟读、间距或声部归属的3–5处。
先给保留／改进判断，再解释为什么、可行改法与代价；不要修改原件。
```

试已有谱时可提供`C:\Users\Fred\OneDrive - yunzd\arr\如果有来生\如果有来生_arr_by_kumo.pdf`，并提醒参考同目录的`如果有来生-release5.mscz`。想测新情境可换另一首完整谱。

未安装也能直接写：

```text
读取 E:\programming\funcodes\mcp-musescore\skills\piano-engraving\SKILL.md，按它只读审查我提供的钢琴谱。
```

需要候选时再要求“在独立副本给少量MuseScore原生对照，保音乐并说明整行连带”；只读分析不要求先连MCP或启动MuseScore。发布包不含你的原谱、教材原图、字体或运行时。

## 本地发现与维护方式

本项目提供一次关联安装脚本，在用户`~/.agents/skills/piano-engraving`建立指向当前项目的目录联接，不复制知识库、不改MCP配置。目标已正确关联则返回成功；其它同名目录存在时停止，保留全部原内容。

```powershell
pwsh -NoProfile -File E:\programming\funcodes\mcp-musescore\tools\engraving\install_skill.ps1
```

也可解压首版包后执行其中的同一路径脚本，知识库和skill保留同一包结构。Codex官方支持本地`.agents/skills`发现与符号链接目录，见[Build skills](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)。安装后下一回合读取；若技能列表仍未刷新，再重开会话／应用。

其它系统可以将`skills/piano-engraving`符号链接到用户`.agents/skills`，或复制整个skill目录并向定位器提供知识库所在包的`--repo`路径。

## 按具体问题定位来源

```text
python skills/piano-engraving/scripts/engraving_library.py --topic spacing --query "共同起音 变音" --limit 5
python skills/piano-engraving/scripts/engraving_library.py --topic piano --query "S.P. A八度" --limit 3
```

脚本使用Python3.10+标准库，无网络／索引缓存，返回匹配文件、标题、行号与简短原文。命中后继续读上下文；排序不代表规范或审美优先级。可用`--list-topics`列20入口，省略`--query`取完整专题清单。复制安装或异地运行用`--repo <知识库包路径>`明确指定；错误位置会报错，不悄悄用另一份库。

## 以后更新需要重装吗

关联安装只需更新项目的同一分支，skill和知识库一起更新，通常无需重装。项目搬家时再调整关联；脚本遇到旧关联会停止，不自动删除。复制安装需要同步skill与知识库所在版本。

只更新净书知识／skill无需重配MCP。MCP、宿主插件或启动路径本身变更时，按那些组件单独更新。

## 怎样看效果

主要看它是否发现真正有价值的问题，能否解释为什么、保住合理排法，以及候选是否更易读。可以直接指出“这处不用改”“方向喜欢原来那样”“这里仍挤”或提供反例；不需要逐项审规则。实际打印／试奏在准备采用时检查。

外部资料16/25，余9项已按用户要求暂缓；未知音乐含义与技术缺口见[迭代清单](engraving/ITERATION_BACKLOG.md)。已核知识现在即可使用，不把未读内容写成结论。格式／检索／打包检查也不证明个人审美已完全掌握。

逐轮安装／更新历史保存在[0.34历史说明](ENGRAVING_SKILL_HISTORY_0_34.md)，研究版旧标签保持。
