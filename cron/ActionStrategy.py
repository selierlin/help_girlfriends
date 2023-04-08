from log import logger


def parse(users_notify, action):
    logger.info(f'action={action}')
    result = []
    for user in users_notify:
        tags = user[3].split(',')
        for tag in tags:
            if action.startswith(tag):
                user['action'] = action.replace(tag, '')
                result.append(user)
                logger.info(f'user={user}')
                break
    return result
