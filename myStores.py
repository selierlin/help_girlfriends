
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, PickleType, MetaData
from sqlalchemy.orm import sessionmaker
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


class MyJobStore(SQLAlchemyJobStore):
    def __init__(self, url, tablename='apscheduler_jobs1', metadata=None, **options):
        # 创建数据库引擎，连接到 SQLite 数据库
        engine = create_engine(url)

        # 创建元数据对象
        if not metadata:
            metadata = MetaData()

        # 定义新的数据表字段
        my_new_field = Column('my_new_field', String(255), nullable=True)

        # 创建新的数据表模型
        Table(tablename, metadata,
              Column('id', Integer, primary_key=True),
              Column('next_run_time', Float),
              Column('job_state', PickleType),
              my_new_field,
              extend_existing=True
              )

        # 调用父类的构造函数
        super().__init__(url, tablename=tablename,
                         metadata=metadata, **options)

    def _lookup_job(self, job_id):
        # 从数据库中读取新列的值
        row = self.session.query(self.JobModel).filter_by(id=job_id).first()
        if row:
            return self._reconstitute_job(row, self.misfire_grace_time)
        else:
            return None

    def update_job(self, job):
        # 更新已存在的任务信息，并加入自定义字段
        job_meta = self._get_jobs([job.id])[0]
        job_meta.func_ref = job.func_ref
        job_meta.trigger = job.trigger
        job_meta.args = job.args
        job_meta.kwargs = job.kwargs
        job_meta.name = job.name
        job_meta.misfire_grace_time = job.misfire_grace_time
        job_meta.coalesce = job.coalesce
        job_meta.max_instances = job.max_instances
        job_meta.next_run_time = job.next_run_time
        job_meta.my_new_field = 'my_custom_value'
        return job_meta