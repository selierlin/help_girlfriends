from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ProcessPoolExecutor
import config
from controller import bp
from pytz import timezone
from db import Db

# 创建Flask
app = Flask(__name__)
app.debug = True
# 加载配置
config.load_config()
jobstores = {
    # 可以配置多个存储
    # 'mongo': {'type': 'mongodb'},
    # 'default': MyJobStore(url='sqlite:///jobs.sqlite')  # SQLAlchemyJobStore指定存储链接
    'default': SQLAlchemyJobStore(url=f'sqlite:///{config.conf().get("db_path")}')  # SQLAlchemyJobStore指定存储链接
}
executors = {
    'default': {'type': 'threadpool', 'max_workers': 20},  # 最大工作线程数20
    'processpool': ProcessPoolExecutor(max_workers=500)  # 最大工作进程数为5
}
job_defaults = {
    'coalesce': False,  # 关闭新job的合并，当job延误或者异常原因未执行时
    'max_instances': 10  # 并发运行新job默认最大实例多少
}


def createAPP():
    app.config['JSON_AS_ASCII'] = False
    scheduler = BackgroundScheduler()
    # 创建带有时区信息的 pytz.timezone 对象
    beijing_tz = timezone('Asia/Shanghai')
    # 创建后台调度器对象，并将时区设置为北京时间
    scheduler.configure(jobstores=jobstores, executors=executors, job_defaults=job_defaults,
                        timezone=beijing_tz)  # utc作为调度程序的时区
    # 启动调度器
    scheduler.start()
    app.config['scheduler'] = scheduler
    app.register_blueprint(bp)
    return app


createAPP()
Db.initTable()
if __name__ == '__main__':
    app.run()
