import re

from werobot import WeRoBot

import config
import job
from db import UsersNotify, Users
from log import logger

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


@myRobot.text
def hello(message):
    logger.info(
        f'解析任务 openid={message.source}, message={message.content}, createTime={message.CreateTime}, msgId={message.MsgId}')
    parse_job = job.parse_job(message.source, message.content)
    logger.info(
        f'解析结果：[{parse_job}] openid={message.source}, message={message.content}, createTime={message.CreateTime}, msgId={message.MsgId}')
    return parse_job

#
# @myRobot.filter("图片")
# def send_custom_image(message):
#     # 从本地读取图片
#     with open('/Users/selier/Pictures/bg/iss067e302248.jpeg', 'rb') as f:
#         image_data = f.read()
#
#     return_json = Client.upload_media(media_type="image", media_file=image_data)
#     mediaid = return_json["media_id"]
#
#     # 创建 ImageMessage 对象
#     image_message = ImageMessage(media_id=None, media_file=image_data)
#     # 发送图片消息
#     return image_message
#
