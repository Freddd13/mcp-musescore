"""Append only this font release to native guide and stage only its HEAD diff.

Other chats' unstaged guide edits are preserved byte-for-byte. Does not commit
or push; caller inspects staged patch and commits it separately.
"""
import argparse,difflib,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent
REPO=Path(r'E:\programming\funcodes\muse3_dev\MuseScore')
GIT=r'E:\Git\cmd\git.exe'
PATH='personal/USER_GUIDE.md'
TITLE='## Kumo Piano 字体草案 0.2（2026-10-10）'

def git(*args):
    return subprocess.check_output([GIT,'-C',str(REPO),*args])

def run(commit,appendix=None,title=None):
    title=title or TITLE
    assert not git('diff','--cached','--name-only').strip(),'Native index contains other work; preserve it'
    old_ref=git('rev-parse','HEAD').strip()
    base=git('show','HEAD:'+PATH)
    working=(REPO/PATH).read_bytes()
    assert title not in base.decode('utf-8') and title not in working.decode('utf-8'),'Already documented'
    text=f'''

{title}

用户改选 Leland 底库，新增独立字体 **Kumo Piano**，以 Animenz 官谱为观察目标，重画38个常用字形（符头、G/F谱号、休止、变音、8/16分旗尾、方向琶音、发音符号和延长号）。其余字形沿用Leland；旧Maestro原型保留。本次是可安装评审的造型草案，未完成审美认可和纸面打印。

取得 [字体项目及安装说明](../../../mcp-musescore/fonts/kumo-engrave/README.md) 的 `dist/kumo-engrave-0.2.0-prototypes.zip`，将 `piano/Kumo Piano` 整个文件夹放进偏好设置的 Score Fonts 目录，重启。在乐谱独立副本的 **格式 → 样式 → 乐谱** 选择音乐符号字体 `Kumo Piano`、音乐Text保留内置 `Leland Text`，第一轮关闭自动优化／推荐样式。无需重装MCP、skill或Windows字体；不覆盖内置字体和原谱。更新时成对更换OTF/JSON并重启，原字体可随时在副本中选回。

包内 `Kumo Piano Text` 暂留作兼容试验：常用测试谱一致，但用户谱的八度线等混排仍有差异，当前不推荐为默认搭配。踏板、力度、数字、装饰及组合发音等尚未独立重画。字体不会替你决定符杠、圆滑线、换行和翻页，后续净书另线实施。

原生0.17固定宿主测试、原PDF/MSCZ哈希与重建检查见 [验证记录](../../../mcp-musescore/fonts/kumo-engrave/VERIFICATION.md)。发现现有大括号对精确名称Leland有特殊处理：6谱表工程只改字体名称也可能改分页；反事实副本验证确认本工程该差异由括号跨度分支触发。新字形与同样处于私人家族分支的Control对照；不建议为此修改原谱span。

字体独立版本为0.2.0，源码提交 `Freddd13/mcp-musescore@{commit}`（`codex/musescore-evolution`）。本次只更新本体仓库用户说明，不改原生代码、个人软件版本或字体引擎。
'''
    if appendix:
        text=appendix.read_text(encoding='utf-8').replace('{{FONT_COMMIT}}',commit)
        assert title in text,'Appendix title mismatch'
    addition=text.encode('utf-8')
    desired=base+addition
    patch=''.join(difflib.unified_diff(base.decode('utf-8').splitlines(True),desired.decode('utf-8').splitlines(True),fromfile='a/'+PATH,tofile='b/'+PATH))
    assert git('rev-parse','HEAD').strip()==old_ref
    (REPO/PATH).write_bytes(working+addition)
    patch_file=ROOT/'dist/native-font-guide.patch';patch_file.write_bytes(patch.encode('utf-8'))
    subprocess.check_call([GIT,'-C',str(REPO),'apply','--cached','--',str(patch_file)])
    assert git('show',':'+PATH)==desired,'Unexpected staged contents'
    assert (REPO/PATH).read_bytes()==working+addition
    assert git('diff','--cached','--name-only').decode().strip()==PATH
    print('Staged only the font appendix; all previous guide edits retained.')
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('font_commit')
    p.add_argument('--appendix',type=Path);p.add_argument('--title')
    a=p.parse_args();run(a.font_commit,a.appendix,a.title)
