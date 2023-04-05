from datetime import timedelta, datetime


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

def fill_delta(delta_minute):
    if delta_minute['trigger'] == 'date':
        pass
