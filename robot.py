import re

from werobot import WeRoBot
from werobot.replies import ImageReply

from utils import config, media, job
from db import UsersNotify, Users
from utils.job import format_key
from utils.log_utils import log
from utils.media import get_img_media_id

myRobot = WeRoBot(token=config.get('we_token'))
myRobot.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{config.get("db_path")}'
myRobot.config["APP_ID"] = config.get("APP_ID")
myRobot.config["APP_SECRET"] = config.get("APP_SECRET")


@myRobot.subscribe
def subscribe(message):
    log.info(f'subscribe openid={message.source}')
    Users.add(message.source)
    return '''Hello My Friend!
    回复【帮助】获取更多功能哦
    '''


@myRobot.unsubscribe
def unsubscribe(message):
    log.info(f'unsubscribe openid={message.source}')
    return 'Goodbye My Friend!'


@myRobot.filter("帮助")
def show_help(message):
    log.info(
        f'openid={message.source}, message={message.content}')
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
【8】回复：删除key <key id>
PS：多个标签需要用","隔开
目前仅支持 PushDeer
"""


@myRobot.filter(re.compile("绑定\s.*"))
def bind(message):
    log.info(
        f'message={message.content}, openid={message.source}')
    words = message.content.split()
    if len(words) != 3:
        return "格式不规范，正确格式：绑定 key 标签"
    words[2] = words[2].replace('，', ',')
    log.info(f'message={message.content}, openid={message.source}, 绑定={words}')
    result = UsersNotify.add(message.source, 1, words[1], words[2])
    if result:
        log.info(
            f'message={message.content}, 绑定成功 openid={message.source}')
        return "绑定成功"
    log.info(
        f'message={message.content}, 绑定失败 openid={message.source}')
    return "绑定失败，可能原因：重复绑定"


@myRobot.filter(re.compile("解绑.*"))
def unbind(message):
    log.info(
        f'message={message.content}, openid={message.source}')
    words = message.content.split()
    if len(words) != 2:
        return "格式不规范"
    log.info(words)
    result = UsersNotify.delete(message.source, 1, words[1])
    if result > 0:
        log.info(
            f'message={message.content}, 解绑成功 openid={message.source}')
        return "解绑成功"
    log.info(
        f'message={message.content}, 解绑失败 openid={message.source}')
    return "解绑失败，可能原因：未绑定该key"


@myRobot.filter(re.compile("删除任务.*"))
def my_task_list(message):
    log.info(
        f'message={message.content}, openid={message.source}')
    # 使用正则表达式匹配数字
    num_list = re.findall(r'\d+', message.content)
    if num_list:
        # 输出所有匹配到的数字
        for num in num_list:
            jobid = f'{message.source}_{num}'
            log.info(
                f'删除任务 openid={message.source}, 任务id={jobid}')
            job.remove_job(jobid)
        return "操作完成"
    return "未匹配到任务"


@myRobot.filter(re.compile("清空任务"))
def my_task_list(message):
    log.info(
        f'message={message.content}, openid={message.source}')
    list_job = job.list_job(message.source)
    if list_job.get('data'):
        # 输出所有匹配到的数字
        for my_job in list_job.get('data'):
            jobid = f'{message.source}_{my_job["任务ID"]}'
            log.info(
                f'删除任务 openid={message.source}, 任务id={jobid}')
            job.remove_job(jobid)
        return "清空任务完成"
    return "未匹配到任务"


@myRobot.filter(re.compile("我的任务"))
def my_task_list(message):
    log.info(
        f'message={message.content}, openid={message.source}')
    job_list = job.list_job(message.source)
    log.info(
        f'message={message.content}, 我的任务 openid={message.source}, job_list={job_list}')
    if job_list.get('data'):
        img_file_name = f'./job_{message.source}.png'

        # 定义表头和列宽
        header = ['任务ID', '发送对象', '发送方式', '下一次触发时间', '创建时间', '发送内容']
        header_width = [100, 100, 100, 200, 200, 300]
        media.dict_to_table(job_list['data'], img_file_name, header, header_width)
        id = get_img_media_id(myRobot, img_file_name)
        reply = ImageReply(message=message, media_id=id)
        return reply
    return "当前没有任务"


@myRobot.filter(re.compile("我的\s?key"))
def my_key_list(message):
    log.info(
        f'message={message.content}, openid={message.source}')
    key_list = UsersNotify.list_key(message.source)
    log.info(
        f'message={message.content}, 我的key openid={message.source}, key_list={key_list}')
    if key_list:
        format_keys = format_key(key_list)
        img_file_name = f'./temp/key_{message.source}.png'
        # 定义表头和列宽
        header = ['ID', '名称', '发送方式', '是否启用', '创建时间', 'key']
        header_width = [80, 200, 100, 80, 200, 500]
        media.dict_to_table(format_keys, img_file_name, header, header_width)
        id = get_img_media_id(myRobot, img_file_name)
        reply = ImageReply(message=message, media_id=id)
        return reply
    return "当前没有任务"


@myRobot.filter(re.compile("禁用\s?key.*"))
def my_task_list(message):
    log.info(
        f'message={message.content}, openid={message.source}')
    # 使用正则表达式匹配数字
    num_list = re.findall(r'\d+', message.content)
    if num_list:
        # 输出所有匹配到的数字
        for num in num_list:
            log.info(
                f'禁用Key openid={message.source}, key id={num}')
            UsersNotify.update_by_openid(message.source, num, 0)
        return "操作完成"
    return "未匹配到Key"


@myRobot.filter(re.compile("启用\s?key.*"))
def my_task_list(message):
    log.info(
        f'message={message.content}, openid={message.source}')
    # 使用正则表达式匹配数字
    num_list = re.findall(r'\d+', message.content)
    if num_list:
        # 输出所有匹配到的数字
        for num in num_list:
            log.info(
                f'启用Key openid={message.source}, key id={num}')
            UsersNotify.update_by_openid(message.source, num, 1)
        return "操作完成"
    return "未匹配到Key"


@myRobot.filter(re.compile("删除\s?key.*"))
def my_task_list(message):
    log.info(
        f'message={message.content}, openid={message.source}')
    # 使用正则表达式匹配数字
    num_list = re.findall(r'\d+', message.content)
    if num_list:
        # 输出所有匹配到的数字
        for num in num_list:
            log.info(
                f'删除Key openid={message.source}, key id={num}')
            UsersNotify.delete_by_openid(message.source, num)
        return "操作完成"
    return "未匹配到Key"


# @myRobot.filter(re.compile("1"))
# def test(message):
#     img_url = 'https://www.baidu.com/img/flexible/logo/pc/result@2.png'
#     img_file_name = 'img_media.jpg'
#     media_id = get_img_media_id_by_url(img_url, img_file_name)
#     reply = ImageReply(message=message, media_id=media_id)
#     return reply


@myRobot.text
def hello(message):
    log.info(
        f'message={message.content}, 解析任务 openid={message.source}')
    parse_job = job.parse_job(message.source, message.content)
    log.info(
        f'message={message.content}, 解析结果=[{parse_job}], openid={message.source}')
    return parse_job
