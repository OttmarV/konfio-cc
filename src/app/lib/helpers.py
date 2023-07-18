from datetime import datetime, timedelta
from calendar import timegm


def rule_90_day(start_date, end_date):
    start_date_dt = datetime.strptime(start_date, "%Y%m%d")
    end_date_dt = datetime.strptime(end_date, "%Y%m%d")

    delta = end_date_dt - start_date_dt

    if delta.days < 90:
        end_date = (start_date_dt + timedelta(days=90)).strftime("%Y%m%d")

    print(f"El end_date final es: {end_date}")

    return end_date


def date_to_epoch(date, is_start):
    if is_start:
        date += " 00:00:00"
    else:
        date += " 23:59:59"

    formatted_date = datetime.strptime(date, "%Y%m%d %H:%M:%S")
    epochtime = timegm(formatted_date.timetuple())

    return epochtime
