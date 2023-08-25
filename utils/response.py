SUCCESS_CODE = 200


def success(code=SUCCESS_CODE, msg='操作成功', data=None):
    if data is None:
        data = {}
    return {'code': code, 'data': data, 'msg': msg}


def fail(code=404, msg='操作失败', data=None):
    if data is None:
        data = {}
    return {'code': code, 'data': data, 'msg': msg}


def is_success(self):
    return self['code'] == SUCCESS_CODE


def is_fail(self):
    return self['code'] != SUCCESS_CODE
