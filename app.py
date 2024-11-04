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

    async def on_at_message_create(self, message: Message):
        _log.info(message.author.avatar)
        if "请求音乐：" in message.content:
            params={
                'input':message.split("-")[1],
                'filter':'name',
                'type':"netease",
                'page':int(message.split("-")[2]),
            }
            headers={
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',}
            url='https://www.at38.cn/'
            response=requests.post(url,data=params,headers=headers)
            datas=response.json()
            songs = {}
            for data in datas['data']:
                songs[data[0]['title']] = data[0]['url']
            _log.info(message.author.username)
        await message.reply(content=f"已经帮您查询到相关歌曲：{songs}")

if __name__ == '__main__':
    intents = botpy.Intents(public_guild_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], secret=test_config["secret"])