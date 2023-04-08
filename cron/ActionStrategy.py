from log import logger


def parse(users_notify, action):
    result = []
    for user in users_notify:
        tags = user[4].split(',')
        for tag in tags:
            if action.startswith(tag):
                temp = {}
                temp['openid'] = user[1]
                temp['notify_type'] = user[2]
                temp['notify_key'] = user[3]
                temp['tags'] = user[4]
                temp['action'] = action.replace(tag, '')
                result.append(temp)
                break
    logger.info(f'解析用户指令 user result={result}')
    return result
