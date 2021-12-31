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