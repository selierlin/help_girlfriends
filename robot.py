from werobot import WeRoBot

import config
import notify
from log import logger

myRobot = WeRoBot(token=config.conf().get('we_token'))
myRobot.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{config.conf().get("db_path")}'


@myRobot.subscribe
def subscribe(message):
    logger.info(f'subscribe openid={message.source}, createTime={message.CreateTime}')
    return 'Hello My Friend!'


@myRobot.unsubscribe
def unsubscribe(message):
    logger.info(f'unsubscribe openid={message.source}, createTime={message.CreateTime}')
    return 'Good My Friend!'


@myRobot.filter("帮助")
def show_help(message):
    logger.info(
        f'openid={message.source}, message={message.content}, createTime={message.CreateTime}, msgId={message.MsgId}')
    return """
    帮助
    XXXXX
    """


@myRobot.text
def hello(message):
    logger.info(f'openid={message.source}, message={message.content}, createTime={message.CreateTime}, msgId={message.MsgId}')

    return 'Hello World!'
