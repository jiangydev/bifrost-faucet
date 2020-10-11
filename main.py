import asyncio
import logging
import random
import re
import time
from threading import Thread

import schedule as schedule
from telethon import TelegramClient, events
from telethon.network import connection

# Use your own values from my.telegram.org
api_id = 0
api_hash = 'api_hash'

proxy_custom = ('1.2.3.4', 443, 'secret')

client = TelegramClient('anon', api_id, api_hash
                        # , connection=connection.ConnectionTcpMTProxyRandomizedIntermediate
                        # , proxy=proxy_custom
                        )

# 日志输出
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

handling_bnc = []

bot_reply_time = 0


# Bifrost Faucet has ID -1001352638541
# @bifrost_faucet2_bot: 1173124754
@client.on(events.NewMessage(chats=[-1001352638541], from_users=[1173124754]))
async def my_event_handler(event):
    global bot_reply_time
    bot_reply_time = 0
    print(f'[消息监听] 待处理的bnc地址列表: {handling_bnc}')
    msg = event.message.message
    # 正则查找bnc地址
    bnc_obj = re.search('(5\\w{47})|([a-h]\\w{46})', msg)
    if bnc_obj:
        # 如果能找到bnc地址
        bnc = bnc_obj.group()
        print(f'[消息监听] 正则匹配到的bnc地址: {bnc}')
        if bnc in handling_bnc:
            if 'successful' in msg:
                print(f'[消息监听] 已成功: {bnc}')
            if 'has already dripped' in msg:
                print(f'[消息监听] 已发放: {bnc}')
            print(f'[消息监听] 移除备选bnc地址: {bnc}')
            # 无论成功与否，移除bnc地址
            handling_bnc.remove(bnc)


# 发送tl消息
async def send_msg(user, bnc_address):
    async with TelegramClient('tmp', api_id, api_hash
                              # , connection=connection.ConnectionTcpMTProxyRandomizedIntermediate
                              # , proxy=proxy_custom
                              ) as tmp_client:
        await tmp_client.send_message(user, f'/want {bnc_address}')
        client.run_until_disconnected()
    print(f'[定时任务] 发送消息完成, user: {user}, bnc_address: {bnc_address}')


# 先从文件中读取地址，放入集合；
def load_bnc_job():
    print(f'[定时任务] 开始执行')
    with open('./bnc_waiting.txt', 'r', encoding='UTF-8') as lines:
        # 读取到的每一行末尾有换行符\n, 需要剔除
        array = lines.readlines()
        for i in array:
            i = i.strip('\n')
            i = i.strip('!')
            # 跳过空行和注释行; 如果地址已存在, 也不加入备选
            if len(i) > 0 and not i.startswith('#') and i not in handling_bnc:
                handling_bnc.append(i)
        print(f'[定时任务] 读取文件完成: {handling_bnc}')
    print(f'[定时任务] 执行结束')


# 任务初始化：先从文件中读取地址，放入集合；
def load_bnc_init():
    print(f'[任务初始化] 开始执行')
    with open('./bnc_waiting.txt', 'r', encoding='UTF-8') as lines:
        # 读取到的每一行末尾有换行符\n, 需要剔除
        array = lines.readlines()
        for i in array:
            i = i.strip('\n')
            # 跳过空行和注释行; 如果地址已存在, 也不加入备选
            if len(i) > 0 and not i.startswith('#') and not i.startswith('!') and i not in handling_bnc:
                handling_bnc.append(i)
        print(f'[任务初始化] 读取文件完成: {handling_bnc}')
    print(f'[任务初始化] 执行结束')


# 判断集合元素个数，并一直取第0个，发送 /want bnc 的 message；
def send_msg_job():
    global bot_reply_time
    if bot_reply_time > 180:
        print('[定时任务-消息发送] 机器人响应超时, 不发送消息')
        return None
    print('[定时任务-消息发送] 机器人正常')
    sleep_seconds = random.randint(1, 10)
    print(f'[定时任务-消息发送] 开始随机休眠{sleep_seconds}s')
    time.sleep(sleep_seconds)
    print(f'[定时任务-消息发送] 结束随机休眠')
    if len(handling_bnc) > 0:
        current_bnc = handling_bnc[0]
        print(f'[定时任务-消息发送] 开始执行: {current_bnc}')
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(send_msg(-1001352638541, current_bnc))
        loop.close()
    print(f'[定时任务-消息发送] 执行结束')


# 定时任务1:加载bnc地址(每24h)
schedule.every(24).hours.do(load_bnc_job)
# 定时任务2:发送tl消息(每60s)
schedule.every(60).seconds.do(send_msg_job)


def job_start():
    while True:
        schedule.run_pending()
        time.sleep(1)


def time_start():
    global bot_reply_time
    while True:
        time.sleep(1)
        bot_reply_time = bot_reply_time + 1


if __name__ == '__main__':
    # 先初始化一次bnc地址
    load_bnc_init()
    # 开启定时任务线程
    Thread(target=job_start).start()
    Thread(target=time_start).start()
    # 运行tl
    client.start()
    client.run_until_disconnected()
