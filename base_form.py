# базовый класс для классов EditForm и AddForm
class BaseForm:
    # инициализация выпадающих списков значениями из БД
    def advanced_setup(self, app):
        states = app.db_driver.get_all_states()
        for s in states:
            self.comboBox_3.addItem(s[1])

        durations = app.db_driver.get_all_durations()
        for d in durations:
            self.comboBox_2.addItem(str(d[1]) + ' мес')

        bank_cards = app.db_driver.get_all_bank_cards()
        for bc in bank_cards:
            self.comboBox.addItem(bc[3] + ' ' + bc[1][-4:])
