import logging
import re
from datetime import timedelta, datetime

day_key = '((?P<day>\d+)(天|日))?\s*'
hour_key = '((?P<hour>\d+)(小时|个小时|点))?\s*'
minute_key = '((?P<minute>\d+)(分钟|分))?\s*'
second_key = '((?P<second>\d+)(秒|s))?\s*'
action_key = '(?P<action>.+)'
tip_key = '(拿|叫|提醒|告诉)'


class ExtractStrategy:
    @staticmethod
    def extract(input_str, nickname):
        delta_minute = None
        action = ''
        try:
            # 每隔、每小时、每分钟关键字，使用 interval 执行处理
            pattern = fr'(每隔|每)\s*{day_key}{hour_key}{minute_key}{tip_key}({nickname})?{action_key}'
            match = re.match(pattern, input_str)
            if match:
                day = int(match.group('day') or 0)
                hour = int(match.group('hour') or 0)
                minute = int(match.group('minute') or 0)
                delta_minute = {'day': day, 'hour': hour, 'minute': minute, 'trigger': 'interval'}
                action = match.group('action')
                return (delta_minute, action)
            # 每天X点，使用 cron 表达式执行处理
            pattern = fr'(每天|每)\s*{day_key}{hour_key}{minute_key}{tip_key}({nickname})?{action_key}'
            match = re.match(pattern, input_str)
            if match:
                day = int(match.group('day') or 0)
                hour = int(match.group('hour') or 9)
                minute = int(match.group('minute') or 0)
                delta_minute = {'day': day, 'hour': hour, 'minute': minute, 'trigger': 'cron'}
                action = match.group('action')
                return (delta_minute, action)
            # 今天、明天、后天、一个小时后、5分钟后的关键字，使用 date 执行处理
            pattern = fr'((?P<day>.+?天|日))?\s*{hour_key}{minute_key}{tip_key}({nickname})?{action_key}'
            match = re.match(pattern, input_str)
            if match:
                hour = int(match.group('hour') or 9)
                minute = int(match.group('minute') or 0)
                delta_minute = {'hour': hour, 'minute': minute, 'trigger': 'date'}
                ParseStrategy.parseDay(delta_minute, match)
                action = match.group('action')
                return (delta_minute, action)
            # 一天后、一个小时后、5分钟后的关键字，使用 date 执行处理
            pattern = fr'{day_key}{hour_key}{minute_key}{second_key}(后|前)?\s*{tip_key}({nickname})?{action_key}'
            match = re.match(pattern, input_str)
            if match:
                day = int(match.group('day') or 0)
                hour = int(match.group('hour') or 0)
                minute = int(match.group('minute') or 0)
                second = int(match.group('second') or 0)
                delta_minute = {'hour': hour, 'minute': minute, 'second': second, 'trigger': 'date', 'day': day}
                ParseStrategy.parseTime(delta_minute)
                action = match.group('action')
                return (delta_minute, action)

        except Exception as e:
            logging.error(e)
        finally:
            if delta_minute is not None:
                ParseStrategy.fill_delta(delta_minute)
        return None

class ParseStrategy:
    @staticmethod
    def parseDay(delta_minute, match):
        day = match.group('day')
        today = datetime.now()
        target = today
        if day == '明天':
            target = today + timedelta(days=1)
        elif day == '后天':
            target = today + timedelta(days=2)
        elif day == '大后天':
            target = today + timedelta(days=3)
        pass

        delta_minute['day'] = target.day
        delta_minute['month'] = target.month
        delta_minute['year'] = target.year

    @staticmethod
    def parseTime(delta_minute):
        today = datetime.now()
        target = today
        target += timedelta(days=delta_minute['day'])
        target += timedelta(hours=delta_minute['hour'])
        target += timedelta(minutes=delta_minute['minute'])
        target += timedelta(seconds=delta_minute['second'])

        delta_minute['day'] = target.day
        delta_minute['month'] = target.month
        delta_minute['year'] = target.year
        delta_minute['hour'] = target.hour
        delta_minute['minute'] = target.minute
        delta_minute['second'] = target.second

    @staticmethod
    def fill_delta(delta_minute):
        if delta_minute['trigger'] == 'date':
            pass


class ConvertStrategy:
    @staticmethod
    def convert(delta_minute):
        month = delta_minute.get('month') if delta_minute.get('month') else -1
        day = delta_minute.get('day') if delta_minute.get('day') else -1
        hour = delta_minute.get('hour') if delta_minute.get('hour') else -1
        minute = delta_minute.get('minute') if delta_minute.get('minute') else -1
        return f"{minute} {hour} {day} {month} * * *"


# 每隔、每小时、每分钟关键字，可以使用 interval 执行处理
# 每天X点，可以使用 cron 表达式执行处理
# 今天、明天、后天、一个小时后、5分钟后的关键字，可以使用 date 执行处理
#
if __name__ == '__main__':
    input_strs = [
        "明天19点15分提醒我约会",
        "后天提醒我出门带伞",
        "后天叫我出门带钥匙",
        "明天9点拿快递",
        "3个小时后叫我睡觉",
        "30分钟后告诉我敷面膜",
        "每隔3天提醒我浇水",
        "每天7点提醒我起床"
    ]

    # convert_strategy = ConvertStrategy()

    for input_str in input_strs:
        extracted_data = ExtractStrategy.extract(input_str, "我")
        if extracted_data:
            delta_minute, action = extracted_data
            # cron_expression = convert_strategy.convert(delta_minute)
            print(f"{delta_minute} {input_str}")
        else:
            print("无法识别任务信息")
