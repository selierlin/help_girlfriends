from utils.log_utils import log
from pypushdeer import PushDeer


def send_notify(openid, title, msg, create_time, notify_type, notify_key, tags):
    try:
        log.info(
            f'接收发送通知 title=openid={openid}, title={title}, msg={msg}, create_time={create_time}, notify_type={notify_type}'
            f', notify_key={notify_key}')
        push_deer(notify_key, title, msg)
        log.info(f'发送完成 openid={openid}, title={title}, msg={msg}')
    except Exception as e:
        log.error(f'发送失败 openid={openid}, title={title}, msg={msg}')


def push_deer(push_key, title, msg):
    try:
        pd = PushDeer(pushkey=push_key)
        a = pd.send_markdown(title, desp=
        f'''
            ### {msg}
        ''')
        log.info(f'发送通知结果={a}, title={title}, msg={msg}')
    except Exception as e:
        log.error(f'发送通知异常 key[{push_key}]失效')


if __name__ == '__main__':
    push_deer('PDU21071TYLVoILnbAoQLIAmiiXZxKfmvrVCLScck', '记得给车充电🔋', '明天约会记得醒来后给小电炉充电呀宝💗')
