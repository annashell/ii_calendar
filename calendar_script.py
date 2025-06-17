import datetime
import time


def date_to_rus(date):
    months = "января февраля марта апреля мая июня июля августа сентября октября ноября декабря".split()
    return f"{date.day} {months[date.month - 1]}"


def get_today_request():
    with open("holidays.txt", "r", encoding='utf-8') as f:
        text = f.read()

    holidays = {(i := line.split(" - "))[0].strip(): i[1].strip() for line in text.split("   ")}
    realtime = datetime.datetime.fromtimestamp(time.time())
    return holidays[date_to_rus(realtime)]


get_today_request()