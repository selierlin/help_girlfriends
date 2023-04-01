from datetime import datetime

from flask import Blueprint, jsonify, request, current_app
import job

bp = Blueprint('main', __name__)


@bp.route('/api')
def api():
    data = {'name': 'John', 'age': 30}
    return jsonify(data)


@bp.route('/job/add', methods=['POST', 'GET'])
def addJob():
    scheduler = current_app.config['scheduler']
    args = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    scheduler.add_job(func=job.jobFunction, trigger='interval', name='name_'+args, seconds=5, args=[args])
    data = {'code': 200, 'data': '', 'msg': '添加成功'}
    return jsonify(data)


@bp.route('/job/list', methods=['POST', 'GET'])
def listJob():
    scheduler = current_app.config['scheduler']
    jobs = scheduler.get_jobs()
    data = {'code': 200, 'data': job.formatJob(jobs), 'msg': '成功'}
    return jsonify(data)


@bp.route('/job/remove', methods=['POST'])
def removeJob():
    scheduler = current_app.config['scheduler']
    jobId = request.args.get("jobId")
    try:
        scheduler.remove_job(jobId)
        data = {'code': 200, 'data': [], 'msg': '成功'}
        return jsonify(data)
    except Exception:
        data = {'code': 404, 'data': [], 'msg': '无任务'}
        return jsonify(data)

