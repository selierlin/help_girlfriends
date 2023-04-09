from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from sqlalchemy import (
    select)


class MyJobStore(SQLAlchemyJobStore):
    def _get_jobs(self, *conditions):
        jobs = []
        selectable = select(self.jobs_t.c.id, self.jobs_t.c.job_state)
        if conditions is not None:
            selectable.filter(self.jobs_t.c.id.like(f'{conditions}_%'))
        selectable.order_by(self.jobs_t.c.next_run_time)
        failed_job_ids = set()
        with self.engine.begin() as connection:
            for row in connection.execute(selectable):
                try:
                    jobs.append(self._reconstitute_job(row.job_state))
                except BaseException:
                    self._logger.exception('Unable to restore job "%s" -- removing it', row.id)
                    failed_job_ids.add(row.id)

            # Remove all the jobs we failed to restore
            if failed_job_ids:
                delete = self.jobs_t.delete().where(self.jobs_t.c.id.in_(failed_job_ids))
                connection.execute(delete)

        return jobs
