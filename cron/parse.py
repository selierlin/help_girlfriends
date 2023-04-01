from abc import ABC
from datetime import datetime, timedelta
class CronExpression:
    def __init__(self, minute, hour, day, month, weekday):
        self.minute = minute
        self.hour = hour
        self.day = day
        self.month = month
        self.weekday = weekday

    def __str__(self):
        return f"{self.minute} {self.hour} {self.day} {self.month} {self.weekday}"
class EveryDayFactory(CronFactory):
    def getCron(self):
        pass
class EveryAtFactory:

    @classmethod
    def getCron(cls, msg):
        pass


class CronFactory:
    @staticmethod
    def every_day():
        return CronExpression("0", "0", "*", "*", "?")

    @staticmethod
    def every_n_days(n):
        return CronExpression("0", "0", f"*/{n}", "*", "?")

    @staticmethod
    def every_day_at_n_hour(n):
        return CronExpression("0", str(n), "*", "*", "?")

    @staticmethod
    def tomorrow_at_n_hour_minute(n, m):
        tomorrow = datetime.now() + timedelta(days=1)
        return CronExpression(str(m), str(n), str(tomorrow.day), str(tomorrow.month), "?")

    @staticmethod
    def after_n_hours(n):
        return CronExpression("0", f"*/{n}", "*", "*", "?")

    @staticmethod
    def after_n_minutes(n):
        return CronExpression(f"*/{n}", "*", "*", "*", "?")

def getCron(msg: str) -> str:
    if "每天" in msg:
        cron_exp = EveryDayFactory.getCron(msg)
    elif "每隔" in msg:
        cron_exp = EveryAtFactory.getCron(msg)
    elif "明天" in msg:
        n = int(''.join(filter(str.isdigit, msg)))
        m = int(''.join(filter(lambda x: x.isdigit(), msg.split("明天")[1].split("点")[1].split("分")[0])))
        cron_exp = CronFactory.tomorrow_at_n_hour_minute(n, m)
    elif "后天" in msg:
        n = int(''.join(filter(str.isdigit, msg)))
        m = int(''.join(filter(lambda x: x.isdigit(), msg.split("后天")[1].split("点")[1].split("分")[0])))
        day_after_tomorrow = datetime.now() + timedelta(days=2)
        cron_exp = CronExpression(str(m), str(n), str(day_after_tomorrow.day), str(day_after_tomorrow.month), "?")
    elif "小时后" in msg:
        n = int(''.join(filter(str.isdigit, msg)))
        cron_exp = CronFactory.after_n_hours(n)
    elif "分钟后提醒" in msg:
        n = int(''.join(filter(str.isdigit, msg)))
        cron_exp = CronFactory.after_n_minutes(n)
    else:
        raise ValueError("Invalid message format")

    return str(cron_exp)

if __name__ == '__main__':
    cron_exp = getCron("每天提醒我")
    print(cron_exp)  # 0 0 * * ? (每天0点0分)

    cron_exp = getCron("每隔3天提醒我浇水")
    print(cron_exp)  # 0 0 */3 * ? (每隔3天0点0分)

    cron_exp = getCron("每天7点提醒我起床")
    print(cron_exp)  # 0 7 * * ? (每天7点0分)

    cron_exp = getCron("明天9点30分提醒我起床充电")
    print(cron_exp)  # 30 9 2 4 ? (明天4月2日9点30分)

    cron_exp = getCron("后天18点20分提醒我参加聚会")
    print(cron_exp)  # 20 18 3 4 ? (后天4月3日18点20分)
    getCron("4个小时后提醒我晒衣服")
    print(cron_exp)  # 0 */4 * * ? (每隔4小时0分)

    cron_exp = getCron("30分钟后提醒我敷面膜")
    print(cron_exp)  # */30 * * * ? (每隔30分钟)