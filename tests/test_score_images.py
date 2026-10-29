"""Native PNG content and note references travel together through MCP."""
import asyncio,base64
import pytest
from fastmcp import Client,FastMCP
from fastmcp.exceptions import ToolError
from src.context.service import ContextService
from src.tools.viewer import setup_viewer_tools

PNG='iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aZ1kAAAAASUVORK5CYII='
class Images:
    def __init__(self):self.calls=[];self.stale=False
    async def send_command(self,action,params=None):
        self.calls.append((action,params))
        assert action=='arrangementImage'
        if self.stale:return {'status':'success','result':{'error':'乐谱已经更新，请重新读取这一段后取图。'}}
        return {'status':'success','result':{'schemaVersion':'score-image/1','snapshotId':'score:1','geometryVersion':'geometry:1',
            'identity':{'displayTitle':'谱面标题'},'scope':params['scope'],'imageIndex':params['imageIndex'],'imageCount':2,'nextImage':1,
            'measures':[{'firstMeasure':9,'lastMeasure':12}],'notes':[{'ref':{'snapshotId':'score:1','id':'0:0:0'},'pixelRect':{'x':0,'y':0,'width':1,'height':1}}],
            'mimeType':'image/png','pngBase64':PNG,'width':1,'height':1}}
def setup():
    score=Images();service=ContextService(score)
    service.contexts['task-1']={'contextId':'task-1','snapshotId':'score:1','scope':{'start':0,'end':480,'firstTrack':0,'endTrack':4}}
    mcp=FastMCP('images-check');setup_viewer_tools(mcp,score,service)
    return score,mcp
def test_native_png_and_structured_refs_share_context():
    async def check():
        score,mcp=setup()
        async with Client(mcp) as client:
            result=await client.call_tool('get_score_image',{'context_id':'task-1'})
            image=next(v for v in result.content if v.type=='image')
            assert base64.b64decode(image.data).startswith(b'\x89PNG\r\n\x1a\n')
            assert result.data['contextId']=='task-1' and result.data['snapshotId']=='score:1'
            assert result.data['notes'][0]['ref']=={'snapshotId':'score:1','id':'0:0:0'}
            assert 'pngBase64' not in result.data
            assert '9—12' in result.content[0].text
        assert score.calls==[('arrangementImage',{'snapshotId':'score:1','scope':{'start':0,'end':480,'firstTrack':0,'endTrack':4},'imageIndex':0})]
    asyncio.run(check())
def test_next_image_uses_same_read_version():
    async def check():
        score,mcp=setup()
        async with Client(mcp) as client:
            result=await client.call_tool('get_score_image',{'context_id':'task-1','image_index':1})
            assert result.data['imageIndex']==1 and score.calls[-1][1]['snapshotId']=='score:1'
    asyncio.run(check())
def test_stale_read_returns_current_action():
    async def check():
        score,mcp=setup();score.stale=True
        async with Client(mcp) as client:
            with pytest.raises(ToolError,match='重新读取'):
                await client.call_tool('get_score_image',{'context_id':'task-1'})
    asyncio.run(check())
def test_unknown_context_keeps_native_score_untouched():
    async def check():
        score,mcp=setup()
        async with Client(mcp) as client:
            with pytest.raises(ToolError):await client.call_tool('get_score_image',{'context_id':'missing'})
        assert score.calls==[]
    asyncio.run(check())
def test_redo_forwards_one_native_action():
    from src.tools.notes_measures import setup_notes_measures_tools
    class Edit:
        calls=[]
        async def send_command(self,action,params=None):self.calls.append(action);return {'success':True}
    async def check():
        score=Edit();mcp=FastMCP('redo-check');setup_notes_measures_tools(mcp,score)
        async with Client(mcp) as client:
            assert (await client.call_tool('redo')).data['success']
        assert score.calls==['redo']
    asyncio.run(check())
