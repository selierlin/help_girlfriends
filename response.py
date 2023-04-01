from flask import jsonify


def success(code=200, msg='操作成功', data={}):
    return jsonify({'code': code, 'data': data, 'msg': msg})


def fail(code=404, msg='操作失败', data={}):
    return jsonify({'code': code, 'data': data, 'msg': msg})
