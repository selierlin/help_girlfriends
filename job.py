from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from flask import current_app

from cron import ActionStrategy
from db import UsersNotify
from log import logger
from notify import send_notify
from datetime import datetime
import response
import random
from cron.ChineseParse import ExtractStrategy


def parse_job(openid, message):
    users_notify = UsersNotify.find(openid)
    if users_notify is None or len(users_notify) == 0:
        return '你还没有绑定的key，请回复"帮助"进行绑定'
    extracted_data = ExtractStrategy.extract(message)
    if extracted_data:
        try:
            deal_data, action = extracted_data
            if action and len(message) > len(action):
                actions = ActionStrategy.parse(users_notify, action)
                if actions is None or len(actions) == 0:
                    return "没有找到通知对象🙅"
                for action in actions:
                    logger.info(
                        f"准备添加任务 openid={openid}, message={message}, deal_data={deal_data}, action={action} ")
                    res = add_job(openid, deal_data, action)
                    if response.is_fail(res):
                        return "任务处理失败"
                return "收到🫡"
        except Exception as e:
            logger.error(f'解析任务失败 {e}')
    return "无法识别任务信息"


def add_job(openid, deal_data, action):
    # 如果任意一个为空，则执行相应的操作
    if not all([openid, deal_data, action]):
        return response.fail(msg='缺少参数')
    try:
        scheduler = current_app.config['scheduler']
        current = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        action_content = action['action']
        notify_type = action['notify_type']
        notify_key = action['notify_key']
        tags = action['tags']

        kwargs = {'openid': openid, 'title': action_content, 'msg': action_content, 'create_time': current,
                  'notify_type': notify_type,
                  'notify_key': notify_key, 'tags': tags}
        my_trigger = None
        if deal_data['trigger'] == 'cron' or deal_data['trigger'] == 'date':
            my_trigger = CronTrigger(year=deal_data.get('year'), month=deal_data.get('month'), day=deal_data.get('day'),
                                     hour=deal_data.get('hour'), minute=deal_data.get('minute'),
                                     second=deal_data.get('second'))
        elif deal_data['trigger'] == 'interval':
            my_trigger = IntervalTrigger(days=deal_data.get('day'), hours=deal_data.get('hour'),
                                         minutes=deal_data.get('minute'), seconds=deal_data.get('second'))
        else:
            pass

        job_id = f'{openid}_{random.randrange(100, 999)}'
        scheduler.add_job(id=job_id, func=send_notify, trigger=my_trigger,
                          name=action_content,
                          kwargs=kwargs)
        logger.info(f'添加任务成功 openid={openid}, job_id={job_id}, kwargs={kwargs}')
        return response.success()
    except Exception as e:
        logger.error(f'添加任务失败 {e}')
        return response.fail(msg='添加任务失败')


def update_job(job_id, openid, title, msg):
    if not all([job_id, title, msg]):
        # 如果任意一个为空，则执行相应的操作
        return response.fail(msg='缺少参数')
    try:
        scheduler = current_app.config['scheduler']
        current = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        kwargs = {'openid': openid, 'title': title, 'msg': msg, 'create_time': current}
        scheduler.add_job(id=job_id, func=send_notify, trigger='interval', name=title,
                          seconds=5,
                          kwargs=kwargs, replace_existing=True)
        return response.success()
    except Exception:
        return response.fail(msg='系统异常')


def remove_job(job_id):
    if job_id is None:
        return response.fail(msg='缺少参数')
    try:
        scheduler = current_app.config['scheduler']
        scheduler.remove_job(job_id)
    except Exception:
        return response.fail(msg='系统异常')


def list_job(openid):
    if openid is None:
        return response.fail(msg='缺少参数')
    scheduler = current_app.config['scheduler']
    jobs = scheduler.get_jobs()
    job_data = format_job(jobs, openid)
    return response.success(data=job_data)


def format_job(jobs, openid):
    if jobs is None:
        return None
    array = []
    for job_obj in jobs:
        # header = ['任务ID', '发送内容', '发送对象', '发送方式', '下一次触发时间', '创建时间']
        # 找到下划线的位置
        if not job_obj.id.startswith(f'{openid}_'):
            continue
        idx = job_obj.id.find('_')
        notify_type = "PushDeer" if job_obj.kwargs.get('notify_type') == 1 else "其他"
        next_time = job_obj.next_run_time.strftime('%Y-%m-%d %H:%M:%S') if job_obj.next_run_time else ""
        obj = {'任务ID': job_obj.id[idx + 1:], '下一次触发时间': next_time,
               'trigger': str(job_obj.trigger), '发送内容': job_obj.name, 'args': job_obj.args,
               '创建时间': job_obj.kwargs.get('create_time'),
               '发送对象': job_obj.kwargs.get('tags'),
               '发送方式': notify_type}
        array.append(obj)
    return array


# 每隔、每小时、每分钟关键字，可以使用 interval 执行处理
# 每天X点，可以使用 cron 表达式执行处理
# 今天、明天、后天、一个小时后、5分钟后的关键字，可以使用 date 执行处理
#
if __name__ == '__main__':
    input_strs = [
        # "明天19点15分提醒我约会",
        # "后天提醒我出门带伞",
        # "后天叫我出门带钥匙",
        # "明天9点叫我拿快递",
        # "3秒后提醒我我吃饭",
        # "3个小时后叫我睡觉",
        # "30分钟后告诉我敷面膜",
        # "每隔3天提醒我浇水",
        "每隔3天9点15分提醒我浇水",
        # "每天7点提醒我起床"
    ]

    for input_str in input_strs:
        job = parse_job(openid='oOy0J6Fbp9gSC8Np6PG8auZ5g3Jg', message=input_str)
        print(job)
