from log import logger


def parse(users_notify, action):
    result = []
    for user in users_notify:
        tags = user[4].split(',')
        for tag in tags:
            if action.startswith(tag):
                temp = {'openid': user[1], 'notify_type': user[2], 'notify_key': user[3], 'tags': user[4],
                        'action': action.replace(tag, '')}
                result.append(temp)
                break
    logger.info(f'解析用户指令 user result={result}')
    return result
