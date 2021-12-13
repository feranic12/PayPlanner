# базовый класс для классов EditForm и AddForm
class AdvancedSetup:
    # инициализация выпадающих списков значениями из БД
    def advanced_setup(self, app):
        states = app.db_driver.get_all_states()
        for s in states:
            self.comboBox_3.addItem(s[1])

        durations = app.db_driver.get_all_durations()
        for d in durations:
            self.comboBox_2.addItem(str(d[1]) + ' мес')
