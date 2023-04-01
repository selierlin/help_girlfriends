from flask import current_app
from notify import sendNotify
from datetime import datetime
import response
import random


def addJob(openid, title, msg):
    if not all([openid, title, msg]):
        # 如果任意一个为空，则执行相应的操作
        return response.fail(msg='缺少参数')
    try:
        scheduler = current_app.config['scheduler']
        current = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        kwargs = {'openid': openid, 'title': title, 'msg': msg, 'create_time': current}
        scheduler.add_job(id=f'{openid}_{random.randrange(100, 1000)}', func=sendNotify, trigger='interval', name=title,
                          seconds=5,
                          kwargs=kwargs)
        return response.success()
    except Exception:
        return response.fail(msg='系统异常')


def removeJob(jobId):
    if jobId is None:
        return response.fail(msg='缺少参数')
    try:
        scheduler = current_app.config['scheduler']
        scheduler.remove_job(jobId)
    except Exception:
        return response.fail(msg='系统异常')


def listJob(openid):
    if openid is None:
        return response.fail(msg='缺少参数')
    scheduler = current_app.config['scheduler']
    jobs = scheduler._get_jobs()
    jobData = formatJob(jobs)
    return response.success(data=jobData)


def formatJob(jobs):
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
