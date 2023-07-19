from datetime import datetime, timedelta
from calendar import timegm


def rule_90_day(start_date: str, end_date: str) -> str:
    """90 day rule: Due to API coingecko limitations, if the start
    date and end date range is more than 90 days, data granularity
    will be daily, meaning one data point per day. To make life
    easier, we always will extract a minimum of 90 days of data
    regardless the input end_date. However, refined table with
    the moving average will just contain data until the input
     end_date

    Args:
        start_date (str): user input start date format YYYYMMMDD
        end_date (str): user input end date format YYYYMMMDD inclusive

    Returns:
        str: _description_
    """
    start_date_dt = datetime.strptime(start_date, "%Y%m%d")
    end_date_dt = datetime.strptime(end_date, "%Y%m%d")

    delta = end_date_dt - start_date_dt

    # Evaluate delta date to acquire end_date for coin data extraction
    if delta.days < 90:
        end_date = (start_date_dt + timedelta(days=90)).strftime("%Y%m%d")

    print(f"end_date for coin data extraction: {end_date}")

    return end_date


def date_to_epoch(date: str, is_start: bool) -> int:
    """Convert calendar date format to epoch time

    Args:
        date (str): calendar date in format YYYYMMDD
        is_start (bool): If True, set time to 00:00:00,
        if false, set time to 23:59:59 for conversion.

    Returns:
        int: returns date in epoch time
    """
    if is_start:
        date += " 00:00:00"
    else:
        date += " 23:59:59"

    formatted_date = datetime.strptime(date, "%Y%m%d %H:%M:%S")
    epochtime = timegm(formatted_date.timetuple())

    return epochtime
