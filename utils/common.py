from datetime import datetime


def get_today():
    current_date = datetime.now()
    day_of_week = current_date.weekday()
    weekdays = ["一", "二", "三", "四", "五", "六", "日"]
    weekday_name = weekdays[day_of_week]
    return current_date.strftime("%Y-%m-%d") + " 星期" + weekday_name
