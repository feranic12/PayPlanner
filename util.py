from datetime import datetime, date, timedelta


# вычислить последний день текущего месяца, с учетом високосного года для февраля.
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


# промотать дату на один шаг вперёд
def date_forward(date_from, duration):
    if duration + date_from.month <= 12:
        # ловим исключение ValueError, которое возникает, если день "выпадает" из месяца
        try:
            date_to = date(date_from.year, date_from.month + duration, date_from.day)
        except ValueError:
            # и в этом случае выставляем следующую дату 1 числа следующего месяца.
            date_to = date(date_from.year, date_from.month + duration + 1, 1)
    else:
        try:
            date_to = date(date_from.year + 1, date_from.month + duration - 12, date_from.day)
        except ValueError:
            date_to = date(date_from.year + 1, date_from.month + duration - 12 + 1, 1)
    return date_to
