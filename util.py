from datetime import datetime


class WrongDatesException(Exception):
    pass


def get_last_day_of_month(month, year):
    if month in (1, 3, 5, 7, 8, 10, 12):
        return 31
    elif month in (4, 6, 9, 11):
        return 30
    elif month == 2:
        if year % 4 == 0:
            return 29
        else:
            return 28