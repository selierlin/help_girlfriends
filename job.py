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
            actions = ActionStrategy.parse(users_notify, action)
            for action in actions:
                print(f"{deal_data} {action} {message}")
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
        kwargs = {'openid': openid, 'title': action_content, 'msg': action_content, 'create_time': current,
                  'notify_type': notify_type,
                  'notify_key': notify_key, }
        my_trigger = None
        if deal_data['trigger'] == 'cron' or deal_data['trigger'] == 'date':
            my_trigger = CronTrigger(year=deal_data['year'], month=deal_data['month'], day=deal_data['day'],
                                     hour=deal_data['hour'], minute=deal_data.get('minute'),
                                     second=deal_data.get('second'))
        elif deal_data['trigger'] == 'interval':
            my_trigger = IntervalTrigger(days=deal_data['day'], hours=deal_data['hour'],
                                         minutes=deal_data.get('minute'), seconds=deal_data.get('second'))
        else:
            pass

        job_id = f'{openid}_{random.randrange(100, 1000)}'
        scheduler.add_job(id=job_id, func=send_notify, trigger=my_trigger,
                          name=action_content,
                          kwargs=kwargs)
        logger.info(f'添加任务成功 openid={openid}, job_id={job_id}, kwargs={kwargs}')
        return response.success()
    except Exception as e:
        logger.error(e)
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


def remove_job(jobId):
    if jobId is None:
        return response.fail(msg='缺少参数')
    try:
        scheduler = current_app.config['scheduler']
        scheduler.remove_job(jobId)
    except Exception:
        return response.fail(msg='系统异常')


def list_job(openid):
    if openid is None:
        return response.fail(msg='缺少参数')
    scheduler = current_app.config['scheduler']
    jobs = scheduler.get_jobs()
    job_data = format_job(jobs)
    return response.success(data=job_data)


def format_job(jobs):
    if jobs is None:
        return None
    array = []
    for job in jobs:
        obj = {}
        obj['id'] = job.id
        obj['next_run_time'] = job.next_run_time.strftime('%Y-%m-%d %H:%M:%S')
        obj['trigger'] = str(job.trigger)
        obj['name'] = job.name
        obj['args'] = job.args
        obj['kwargs'] = job.kwargs
        array.append(obj)
    return array


if __name__ == '__main__':
    parse_job(openid='oOy0J6Fbp9gSC8Np6PG8auZ5g3Jg', message="明天15点提醒本人记得及时出门哦，然后注意看一下有没有下雨")
