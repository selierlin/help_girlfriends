import logging
import re

from cron import ParseStrategy

day_key = '((?P<day>\d+)(天|日))?\s*'
hour_key = '((?P<hour>\d+)(小时|个小时|点))?\s*'
minute_key = '((?P<minute>\d+)(分钟|分))?\s*'
second_key = '((?P<second>\d+)(秒|秒钟|s))?\s*'
tip_key = '(拿|叫|提醒|告诉|)'
action_key = '(?P<action>.+)'


class ExtractStrategy:
    @staticmethod
    def extract(message):
        deal_data = None
        try:
            # 每隔、每小时、每分钟关键字，使用 interval 执行处理
            pattern = fr'(每隔)\s*{day_key}{hour_key}{minute_key}{second_key}{tip_key}{action_key}'
            match = re.match(pattern, message)
            if match:
                day = int(match.group('day') or 0)
                hour = int(match.group('hour') or 0)
                minute = int(match.group('minute') or 0)
                second = int(match.group('second') or 0)
                deal_data = {'day': day, 'hour': hour, 'minute': minute, 'second': second, 'trigger': 'interval'}
                action = match.group('action')
                return deal_data, action
            # 每天X点，使用 cron 表达式执行处理
            pattern = fr'(每天|每)\s*{day_key}{hour_key}{minute_key}{second_key}{tip_key}{action_key}'
            match = re.match(pattern, message)
            if match:
                day = int(match.group('day') or 0)
                hour = int(match.group('hour') or 9)
                minute = int(match.group('minute') or 0)
                deal_data = {'day': day, 'hour': hour, 'minute': minute, 'trigger': 'cron'}
                action = match.group('action')
                return deal_data, action
            # 一个小时后、5分钟后、10秒中的关键字，使用 date 执行处理
            pattern = fr'{hour_key}{minute_key}{second_key}(后|前)\s*{tip_key}{action_key}'
            match = re.match(pattern, message)
            if match:
                # day = int(match.group('day') or 0)
                hour = int(match.group('hour') or 0)
                minute = int(match.group('minute') or 0)
                second = int(match.group('second') or 0)
                deal_data = {'hour': hour, 'minute': minute, 'second': second, 'trigger': 'date', 'day': 0}
                ParseStrategy.parse_time(deal_data)
                action = match.group('action')
                return deal_data, action

            # 今天、明天、后天、大后天的关键字，使用 date 执行处理
            pattern = fr'((?P<day>.+?天|日))?\s*{hour_key}{minute_key}{second_key}{tip_key}{action_key}'
            match = re.match(pattern, message)
            if match:
                hour = int(match.group('hour') or 9)
                minute = int(match.group('minute') or 0)
                deal_data = {'hour': hour, 'minute': minute, 'trigger': 'date'}
                ParseStrategy.parse_day(deal_data, match)
                action = match.group('action')
                return deal_data, action

        except Exception as e:
            logging.error(e)
        finally:
            if deal_data is not None:
                ParseStrategy.fill_delta(deal_data)
