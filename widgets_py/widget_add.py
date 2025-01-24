from PyQt5.QtWidgets import QWidget, QMessageBox

from widgets_py.widget_add_edit_from_ui import Ui_Form
from advanced_setup import AdvancedSetup
import exceptions


# класс, представляющий форму добавления новой записи, наследующий,
#  в т.ч. от класса, полученного в визуальном редакторе
class AddForm(QWidget, Ui_Form, AdvancedSetup):
    def __init__(self, app):
        QWidget.__init__(self)
        self.setupUi(self)
        self.setFixedSize(356, 277)
        self.pushButton.clicked.connect(app.save_new_subscription)
        self.advanced_setup(app)

    # проверка на заполненность обязательных полей
    def check_form(self):
        # если одно из полей ввода не заполнено, возбуждается исключение
        if self.textEdit.toPlainText() == "" \
                or self.textEdit_2.toPlainText() == "":
            raise exceptions.AddFormNotFilledError
