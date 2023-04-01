import re
from datetime import timedelta, datetime


class ExtractStrategy:
    def extract(input_str, nickname):
        # 每隔、每小时、每分钟关键字，使用 interval 执行处理
        pattern = r'(每隔|每)\s*((?P<day>\d+)(天|日))?\s*((?P<hour>\d+)(小时|个小时|点))?\s*((?P<minute>\d+)(分钟|分))?\s*(叫|提醒|告诉)' + nickname + '(?P<action>.+)'
        match = re.match(pattern, input_str)
        if match:
            day = int(match.group('day') or 0)
            hour = int(match.group('hour') or 0)
            minute = int(match.group('minute') or 0)
            delta_minute = {'day': day, 'hour': hour, 'minute': minute, 'trigger': 'interval'}
            action = match.group('action')
            return (delta_minute, action)
        # 每天X点，使用 cron 表达式执行处理
        pattern = r'(每天|每)\s*((?P<day>\d+)(天|日))?\s*((?P<hour>\d+)(小时|个小时|点))?\s*((?P<minute>\d+)(分钟|分))?\s*(叫|提醒|告诉)' + nickname + '(?P<action>.+)'
        match = re.match(pattern, input_str)
        if match:
            day = int(match.group('day') or -1)
            hour = int(match.group('hour') or -1)
            minute = int(match.group('minute') or -1)
            delta_minute = {'day': day, 'hour': hour, 'minute': minute, 'trigger': 'cron'}
            action = match.group('action')
            return (delta_minute, action)
        # 今天、明天、后天、一个小时后、5分钟后的关键字，使用 date 执行处理
        pattern = r'(今天|明天|后天|大后天)\s*((?P<day>\d+)(天|日))?\s*(叫|提醒|告诉)' + nickname + '(?P<action>.+)'
        match = re.match(pattern, input_str)
        if match:
            day = int(match.group('day') or -1)
            hour = int(match.group('hour') or -1)
            minute = int(match.group('minute') or -1)
            delta_minute = {'day': day, 'hour': hour, 'minute': minute, 'trigger': 'date'}
            action = match.group('action')
            return (delta_minute, action)
        # 一天后、一个小时后、5分钟后的关键字，使用 date 执行处理
        pattern = r'((?P<day>\d+)(天|日))?\s*((?P<hour>\d+)(小时|个小时|点))?\s*((?P<minute>\d+)(分钟|分))?(后|前)?\s*(叫|提醒|告诉)' + nickname + '(?P<action>.+)'
        match = re.match(pattern, input_str)
        if match:
            day = int(match.group('day') or -1)
            hour = int(match.group('hour') or -1)
            minute = int(match.group('minute') or -1)
            delta_minute = {'day': day, 'hour': hour, 'minute': minute, 'trigger': 'date'}
            action = match.group('action')
            return (delta_minute, action)

        return None


class ConvertStrategy:
    def convert(self, delta_minute):
        month = delta_minute.get('month') if delta_minute.get('month') else -1
        day = delta_minute.get('day') if delta_minute.get('day') else -1
        hour = delta_minute.get('hour') if delta_minute.get('hour') else -1
        minute = delta_minute.get('minute') if delta_minute.get('minute') else -1
        return f"{minute} {hour} {day} {month} * * *"


# 每隔、每小时、每分钟关键字，可以使用 interval 执行处理
# 每天X点，可以使用 cron 表达式执行处理
# 今天、明天、后天、一个小时后、5分钟后的关键字，可以使用 date 执行处理
#
# if __name__ == '__main__':
#     input_strs = [
#         # "明天19点15分提醒我约会",
#         # "后天提醒我出门带伞",
#         # "后天叫我出门带钥匙",
#         # "提醒我明天9点拿快递",
#         # "3个小时后叫我睡觉",
#         "30分钟后告诉我敷面膜",
#         # "每隔3天提醒我浇水",
#         # "每天7点提醒我起床"
#     ]
#
#     extract_strategy = ExtractStrategy()
#     # convert_strategy = ConvertStrategy()
#
#     for input_str in input_strs:
#         extracted_data = extract_strategy.extract(input_str, '我')
#         if extracted_data:
#             delta_minute, action = extracted_data
#             # cron_expression = convert_strategy.convert(delta_minute)
#             print(f"{delta_minute} {action}")
#         else:
#             print("无法识别任务信息")
