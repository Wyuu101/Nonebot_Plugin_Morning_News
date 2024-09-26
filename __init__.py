import nonebot
from nonebot import get_driver
from nonebot.plugin import PluginMetadata
from .config import Config
import asyncio
import parsel
__plugin_meta__ = PluginMetadata(
    name="plugin_moringnews",
    description="",
    usage="",
    config=Config,
)

global_config = get_driver().config
config = Config.parse_obj(global_config)
#
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.39'}
url = 'https://60s.viki.moe'


from nonebot import require
import requests
from nonebot_plugin_apscheduler import scheduler
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
def getBingImageURL():
    respond=requests.get(url='https://cn.bing.com',headers=header)
    respond.encoding = respond.apparent_encoding
    selector = parsel.Selector(respond.text, base_url=url)
    url1=str(selector.css('#preloadBg::attr(href)').extract_first())
    url1=confirmURL(url1)
    return url1

def confirmURL(url):
    url_head=str(url)
    result=""
    if(url_head[0:6]=="/th?id"):
        result="https://s.cn.bing.net"+url_head
        return result
    else:
        return str(url)

async def run_every_day():
    global url,header,group_id
    news_combine=''
    weiyu=''
    response = requests.get(url=url, headers=header)
    if response.status_code == 200:
        news_list = response.json()['data']
        for news in news_list:
            if '微语' in news:
                weiyu=news
                pass
            else:
                news_combine=news_combine+news+'\n'

        img_url=getBingImageURL()
        bot = nonebot.get_bot()
        await asyncio.sleep(5)

        await bot.send_group_msg(group_id=786016014, message=Message(f'--------☀每日新闻☀--------\n{news_combine}\n-----------生活愉快-----------\n{weiyu}')+Message('\n')+Message(MessageSegment.image(img_url)))
        await bot.send_group_msg(group_id=424744365, message=Message(f'--------☀每日新闻☀--------\n{news_combine}\n-----------生活愉快-----------\n{weiyu}')+Message('\n')+Message(MessageSegment.image(img_url)))

        #await bot.send_private_msg(user_id=2644489337, message=Message(f'--------☀每日早报☀--------\n{news_combine}\n-----------生活愉快-----------\n{weiyu}')+Message('\n')+Message(MessageSegment.image(img_url)))

        # await asyncio.sleep(5)
        # await bot.send_group_msg(group_id=750814641, message=Message(f'--------☀每日早报☀--------\n{news_combine}\n-----------生活愉快-----------\n{weiyu}')+Message('\n')+Message(MessageSegment.image(img_url)))
    #     await asyncio.sleep(5)
    #     await bot.send_private_msg(user_id=2644489337,
    #         message=Message(f'--------☀每日早报☀--------\n{news_combine}\n-----------生活愉快-----------\n{weiyu}')+Message('\n')+Message(MessageSegment.image(img_url)))
    else:
        bot = nonebot.get_bot()
        await asyncio.sleep(5)
        await bot.send_group_msg(group_id=786016014, message='获取新闻失败[plugin_news]')
        await bot.send_group_msg(group_id=424744365, message='获取新闻失败[plugin_news]')
        #await asyncio.sleep(5)
        # await bot.send_group_msg(group_id=750814641, message='获取新闻失败')
        # await asyncio.sleep(5)
        # await bot.send_private_msg(user_id=2644489337,message='获取新闻失败')

scheduler.add_job(run_every_day, "cron", hour=12, minute=0, second=0)
