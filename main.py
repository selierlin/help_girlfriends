from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ProcessPoolExecutor
from controller import bp
from pytz import utc

from myStores import MyJobStore

jobstores = {
    # 可以配置多个存储
    # 'mongo': {'type': 'mongodb'},
    # 'default': MyJobStore(url='sqlite:///jobs.sqlite')  # SQLAlchemyJobStore指定存储链接
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')  # SQLAlchemyJobStore指定存储链接
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
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    scheduler = BackgroundScheduler()
    scheduler.configure(jobstores=jobstores, executors=executors, job_defaults=job_defaults,
                        timezone=utc)  # utc作为调度程序的时区
    # 启动调度器
    scheduler.start()
    app.config['scheduler'] = scheduler
    app.register_blueprint(bp)
    return app


if __name__ == '__main__':
    app = createAPP()
    app.run(debug=True)
