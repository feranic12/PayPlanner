from datetime import datetime, date, timedelta

# вспомогательные методы и классы


# исключение, возбуждаемое в методе application.show_sum_price, если начальная дата больше конечной
class WrongDatesException(Exception):
    pass


# исключение, возбуждаемое в методе add_form.check_form, если заполнены не все обязательные поля
class AddFormNotFilledException(Exception):
    pass


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
        if (date_from.day == 31)\
            or ((date_from.day == 30) and (date_from.month == 1))\
            or ((date_from.day == 29) and (date_from.month == 1) and (get_last_day_of_month(2, date_from.year)) == 28):
                date_to = date(date_from.year, date_from.month + duration + 1, 1)
        else:
                date_to = date(date_from.year, date_from.month + duration, date_from.day)
    else:
        if (date_from.day == 31)\
            or ((date_from.day == 30) and (date_from.month == 1))\
            or ((date_from.day == 29) and (date_from.month == 1) and (get_last_day_of_month(2, date_from.year)) == 28):
                date_to = date(date_from.year + 1, date_from.month + duration - 12 + 1, 1)
        else:
                date_to = date(date_from.year + 1, date_from.month + duration - 12, date_from.day)
    return date_to
