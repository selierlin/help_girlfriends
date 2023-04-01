from log import logger


def sendNotify(openid, title, msg, create_time):
    logger.info(f'title={title},msg={msg},openid={openid},create_time={create_time}')


def pushDeer(title, msg):
    pass
