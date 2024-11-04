import json
import requests
import os
import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import Message


test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))
_log = logging.get_logger()

class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_at_message_create(self, message: GroupMessage):
        _log.info(message.author.avatar)
        if "/请求音乐" in message.content:
            _log.info(message.author.avatar)
            name = message.content.split("-")[0]
            page = message.content.split("-")[1]
            _log.info(f"name:{name},page:{page}")
            params={
                'input':name,
                'filter':'name',
                'type':"netease",
                'page':int(page),
            }
            headers={
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',}
            url='https://www.at38.cn/'
            response=requests.post(url,data=params,headers=headers)
            datas=json.loads(response.text)
            songs = {}
            print(datas)
            title = datas['data'][0]['title']
            songurl = datas['data'][0]['url']
            songs[str(title)] = str(url)
        _log.info(message.author.username)
        file_url = songurl  # 这里需要填写上传的资源Url
        uploadMedia = await message._api.post_group_file(
            group_openid=message.group_openid, 
            file_type=1, # 文件类型要对应上，具体支持的类型见方法说明
            url=file_url # 文件Url
        )

        # 资源上传后，会得到Media，用于发送消息
        await message._api.post_group_message(
            group_openid=message.group_openid,
            msg_type=7,  # 7表示富媒体类型
            msg_id=message.id, 
            media=uploadMedia
        )
        
if __name__ == '__main__':
    intents = botpy.Intents(public_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], secret=test_config["secret"])
