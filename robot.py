import json
import re

from werobot import WeRoBot, client
from werobot.replies import ImageReply, TextReply

import config
import job
from db import UsersNotify, Users
from log import logger
import media
import urllib

myRobot = WeRoBot(token=config.conf().get('we_token'))
myRobot.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{config.conf().get("db_path")}'
myRobot.config["APP_ID"] = config.conf().get("APP_ID")
myRobot.config["APP_SECRET"] = config.conf().get("APP_SECRET")


@myRobot.subscribe
def subscribe(message):
    logger.info(f'subscribe openid={message.source}, createTime={message.CreateTime}')
    Users.add(message.source)
    return 'Hello My Friend!'


@myRobot.unsubscribe
def unsubscribe(message):
    logger.info(f'unsubscribe openid={message.source}, createTime={message.CreateTime}')
    return 'Good My Friend!'


@myRobot.filter("帮助")
def show_help(message):
    logger.info(
        f'openid={message.source}, message={message.content}, createTime={message.CreateTime}, msgId={message.MsgId}')
    return """【1】回复：绑定 key 标签。即可添加接收人
示例：绑定 abcabcabc 我,本人
【2】回复：解绑 key。即可删除接收人
示例：解绑 abcabcabc
【3】回复：提醒内容即可触发定时推送
示例：明天15点提醒我出门
效果：明天15点就会推送消息给标签为"我"的手机上
【4】回复：获取key
效果：将会发送你一张图片
【5】回复：我的任务
【6】回复：删除任务 <任务id> <任务id>
示例：删除任务 595。多个任务用空格分割
【7】回复：清空任务
PS：多个标签需要用","隔开
目前仅支持 PushDeer
"""


@myRobot.filter(re.compile("绑定.*"))
def bind(message):
    logger.info(
        f'openid={message.source}, message=【{message.content}】, createTime={message.CreateTime}, msgId={message.MsgId}')
    words = message.content.split()
    if len(words) != 3:
        return "格式不规范"
    words[2] = words[2].replace('，', ',')
    logger.info(words)
    result = UsersNotify.add(message.source, 1, words[1], words[2])
    if result:
        logger.info(
            f'绑定成功 openid={message.source}, message=【{message.content}】, createTime={message.CreateTime}, msgId={message.MsgId}')
        return "绑定成功"
    logger.info(
        f'绑定失败 openid={message.source}, message=【{message.content}】, createTime={message.CreateTime}, msgId={message.MsgId}')
    return "绑定失败，可能原因：重复绑定"


@myRobot.filter(re.compile("解绑.*"))
def unbind(message):
    logger.info(
        f'openid={message.source}, message={message.content}, createTime={message.CreateTime}, msgId={message.MsgId}')
    words = message.content.split()
    if len(words) != 2:
        return "格式不规范"
    logger.info(words)
    result = UsersNotify.delete(message.source, 1, words[1])
    if result > 0:
        logger.info(
            f'解绑成功 openid={message.source}, message={message.content}, createTime={message.CreateTime}, msgId={message.MsgId}')
        return "解绑成功"
    logger.info(
        f'解绑失败 openid={message.source}, message={message.content}, createTime={message.CreateTime}, msgId={message.MsgId}')
    return "解绑失败，可能原因：未绑定该key"


@myRobot.filter(re.compile("删除任务.*"))
def my_task_list(message):
    logger.info(
        f'openid={message.source}, message={message.content}, createTime={message.CreateTime}, msgId={message.MsgId}')
    # 使用正则表达式匹配数字
    num_list = re.findall(r'\d+', message.content)
    if num_list:
        # 输出所有匹配到的数字
        for num in num_list:
            jobid = f'{message.source}_{num}'
            logger.info(
                f'删除任务 openid={message.source}, 任务id={jobid}')
            job.remove_job(jobid)
        return "操作完成"
    return "未匹配到任务"


@myRobot.filter(re.compile("清空任务"))
def my_task_list(message):
    logger.info(
        f'openid={message.source}, message={message.content}, createTime={message.CreateTime}, msgId={message.MsgId}')
    list_job = job.list_job(message.source)
    if list_job.get('data'):
        # 输出所有匹配到的数字
        for my_job in list_job.get('data'):
            jobid = f'{message.source}_{my_job["任务ID"]}'
            logger.info(
                f'删除任务 openid={message.source}, 任务id={jobid}')
            job.remove_job(jobid)
        return "清空任务完成"
    return "未匹配到任务"


@myRobot.filter(re.compile("我的任务"))
def my_task_list(message):
    logger.info(
        f'openid={message.source}, message={message.content}, createTime={message.CreateTime}, msgId={message.MsgId}')
    list_job = job.list_job(message.source)
    logger.info(
        f'我的任务 openid={message.source}, message={message.content}, createTime={message.CreateTime}, list_job={list_job}')
    if list_job.get('data'):
        img_file_name = f'./{message.source}.png'
        media.dict_to_table(list_job['data'], img_file_name)
        id = get_img_media_id(img_file_name)
        reply = ImageReply(message=message, media_id=id)
        return reply
        # return json.dumps(list_job['data']).encode('utf-8').decode('unicode_escape')

    return "当前没有任务"


# @myRobot.filter(re.compile("1"))
# def test(message):
#     img_url = 'https://www.baidu.com/img/flexible/logo/pc/result@2.png'
#     img_file_name = 'img_media.jpg'
#     media_id = get_img_media_id_by_url(img_url, img_file_name)
#     reply = ImageReply(message=message, media_id=media_id)
#     return reply


@myRobot.text
def hello(message):
    logger.info(
        f'解析任务 openid={message.source}, message={message.content}, createTime={message.CreateTime}, msgId={message.MsgId}')
    parse_job = job.parse_job(message.source, message.content)
    logger.info(
        f'解析结果：[{parse_job}] openid={message.source}, message={message.content}, createTime={message.CreateTime}, msgId={message.MsgId}')
    return parse_job


def get_img_media_id_by_url(img_url, img_file_name):
    """
    * 上传临时素菜
    * 1、临时素材media_id是可复用的。
    * 2、媒体文件在微信后台保存时间为3天，即3天后media_id失效。
    * 3、上传临时素材的格式、大小限制与公众平台官网一致。
    """
    resource = urllib.request.urlopen(img_url)
    f_name = img_file_name
    with open(f_name, 'wb') as f:
        f.write(resource.read())
    return get_img_media_id(r"./img_media.jpg")


def get_img_media_id(img_file_name):
    media_json = myRobot.client.upload_media("image", open(img_file_name, "rb"))  ## 临时素材
    # media_json = myRobot.client.upload_permanent_media("image", open(r"./img_media.jpg", "rb")) ##永久素材
    media_id = media_json['media_id']
    # media_url = media_json['url']
    print('微信素材id:', media_id)
    return media_id
