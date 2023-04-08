import response

from flask import Blueprint, request, jsonify
import job
from log import logger

controller = Blueprint('main', __name__)


@controller.route('/')
def api():
    return response.success(msg='hello my lady')


@controller.route('/job/add', methods=['POST'])
def add_job():
    openid = request.form.get("openid")
    msg = request.form.get("msg")
    return jsonify(job.parse_job(openid, msg))


@controller.route('/job/update', methods=['POST'])
def update_job():
    job_id = request.form.get("job_id")
    openid = request.form.get("openid")
    title = request.form.get("title")
    msg = request.form.get("msg")
    return job.update_job(job_id, openid, title, msg)


@controller.route('/job/list', methods=['GET'])
def list_job():
    openid = request.args.get("openid")
    result = job.list_job(openid)
    logger.info(result)
    return result


@controller.route('/job/remove', methods=['POST'])
def remove_job():
    openid = request.args.get("openid")
    job_id = request.args.get("job_id")
    return job.remove_job(f'{openid}_{job_id}')
