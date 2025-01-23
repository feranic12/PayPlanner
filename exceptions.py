# исключение, возбуждаемое в методе application.show_sum_price, если начальная дата больше конечной
class WrongDatesError(Exception):
    pass


# исключение, возбуждаемое в методе add_form.check_form, если заполнены не все обязательные поля
class AddFormNotFilledError(Exception):
    pass
