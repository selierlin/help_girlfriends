from log import logger
from pypushdeer import PushDeer


def sendNotify(openid, title, msg, create_time):
    logger.info(f'title={title},msg={msg},openid={openid},create_time={create_time}')


def pushDeer(pushkey, title, msg):
    pushdeer = PushDeer(pushkey=pushkey)
    pushdeer.send_markdown(title, desp=
    f'''
        ### {msg}
    ''')


if __name__ == '__main__':
    pushDeer('PDU21071TYLVoILnbAoQLIAmiiXZxKfmvrVCLScck', '记得给车充电🔋', '明天约会记得醒来后给小电炉充电呀宝💗')
