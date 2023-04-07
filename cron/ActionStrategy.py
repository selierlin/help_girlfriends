def parse(users_notify, action):
    result = []
    for user in users_notify:
        tags = user['tags'].split(',')
        for tag in tags:
            if action.startswith(tag):
                user['action'] = action.replace(tag, '')
                result.append(user)
                break
    return result
