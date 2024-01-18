import erniebot
erniebot.api_type = "aistudio"
erniebot.access_token = "2d6865cfdda39adae11465125df14705060899e6"
		
class BaiduApi():
    def __init__(self):
    	pass
    async def _aask( self , prompt , stream=False, model="ernie-4.0" ,top_p=0.95):
        messages = [{'role': 'user', 'content': prompt}]
        response = erniebot.ChatCompletion.create(
            model= model,
            messages = messages,
            top_p = top_p,  # 改
            stream = stream
        )
        return response.result

#baidu_api = BaiduApi()
#result = baidu_api._aask("你好啊")
#print("result",result)