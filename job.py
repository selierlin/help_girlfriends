from flask import jsonify
import json
def jobFunction(args):
    print("执行定时任务..."+args)


def formatJob(jobs):
    if jobs is None:
        return None
    array = []
    for job in jobs:
        print(job)
        obj = {}
        obj['id'] = job.id
        obj['next_run_time'] = job.next_run_time.strftime('%Y-%m-%d %H:%M:%S')
        obj['trigger'] = str(job.trigger)
        obj['name'] = job.name
        obj['args'] = job.args
        array.append(obj)
    return array