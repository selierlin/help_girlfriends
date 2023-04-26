from log import logger
from pypushdeer import PushDeer


def send_notify(openid, title, msg, create_time, notify_type, notify_key, tags):
    try:
        logger.info(
            f'接收发送通知 title=openid={openid}, title={title}, msg={msg}, create_time={create_time}, notify_type={notify_type}'
            f', notify_key={notify_key}')
        push_deer(notify_key, title, msg)
        logger.info(f'发送成功 openid={openid}, title={title}, msg={msg}')
    except Exception as e:
        logger.error(f'发送失败 openid={openid}, title={title}, msg={msg}')


def push_deer(push_key, title, msg):
    try:
        pd = PushDeer(pushkey=push_key)
        pd.send_markdown(title, desp=
        f'''
            ### {msg}
        ''')
    except Exception as e:
        logger.error(f'key[{push_key}] is valid')


if __name__ == '__main__':
    push_deer('PDU21071TYLVoILnbAoQLIAmiiXZxKfmvrVCLScck', '记得给车充电🔋', '明天约会记得醒来后给小电炉充电呀宝💗')
