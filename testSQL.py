from pytz import utc

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ProcessPoolExecutor


jobstores = {
    # 可以配置多个存储
    # 'mongo': {'type': 'mongodb'},
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')  # SQLAlchemyJobStore指定存储链接
}
executors = {
    'default': {'type': 'threadpool', 'max_workers': 20},     # 最大工作线程数20
    'processpool': ProcessPoolExecutor(max_workers=5)         # 最大工作进程数为5
}
job_defaults = {
    'coalesce': False,   # 关闭新job的合并，当job延误或者异常原因未执行时
    'max_instances': 3   # 并发运行新job默认最大实例多少
}
scheduler = BackgroundScheduler()

# .. do something else here, maybe add jobs etc.

scheduler.configure(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc) # utc作为调度程序的时区