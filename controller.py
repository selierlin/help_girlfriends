import response

from flask import Blueprint, request
import job
from log import logger

bp = Blueprint('main', __name__)


@bp.route('/')
def api():
    return response.success(msg='hello my lady')


@bp.route('/job/add', methods=['POST'])
def addJob():
    openid = request.form.get("openid")
    title = request.form.get("title")
    msg = request.form.get("msg")
    return job.addJob(openid, title, msg)


@bp.route('/job/update', methods=['POST'])
def updateJob():
    jobId = request.form.get("jobId")
    openid = request.form.get("openid")
    title = request.form.get("title")
    msg = request.form.get("msg")
    return job.updateJob(jobId, openid, title, msg)


@bp.route('/job/list', methods=['GET'])
def listJob():
    openid = request.args.get("openid")
    result = job.listJob(openid)
    logger.info(result)
    return result


@bp.route('/job/remove', methods=['POST'])
def removeJob():
    openid = request.args.get("openid")
    jobId = request.args.get("jobId")
    return job.removeJob(f'{openid}_{jobId}')
