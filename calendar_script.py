import datetime
import time
import urllib.request
from bs4 import BeautifulSoup
import ssl


def date_to_rus(date):
    months = "января февраля марта апреля мая июня июля августа сентября октября ноября декабря".split()
    return f"{date.day} {months[date.month - 1]}"


def get_today_request():
    with open("holidays.txt", "r", encoding='utf-8') as f:
        text = f.read()

    holidays = {(i := line.split(" - "))[0].strip(): i[1].strip() for line in text.split("   ")}
    realtime = datetime.datetime.fromtimestamp(time.time())
    return holidays[date_to_rus(realtime)]


def get_today_holidays():
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    HOLIDAYS_URL = "https://kakoyprazdnik.com/"
    req = urllib.request.Request(HOLIDAYS_URL, headers={"User-Agent": useragent, "authorization": ""})
    try:
        with urllib.request.urlopen(req, context=ctx) as f:
            data = f.read().decode("utf-8")
    except Exception as e:
        return "Ошибочка вышла"

    soup = BeautifulSoup(data, features="html.parser")
    holidays = soup.find_all("h4")

    if len(holidays) == 0:
        return "Ошибочка вышла"
    else:
        return '\n\n'.join(['\U0001F389' + name.getText().strip() for name in holidays])
