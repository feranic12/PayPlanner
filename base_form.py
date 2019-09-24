from PyQt5 import QtCore, QtWidgets


class BaseForm:
    def advanced_setup(self):
        states = self.app.db_driver.get_all_states()
        for s in states:
            self.comboBox_3.addItem(s[1])

        durations = self.app.db_driver.get_all_durations()
        for d in durations:
            self.comboBox_2.addItem(d[1])

        bank_cards = self.app.db_driver.get_all_bank_cards()
        for bc in bank_cards:
            self.comboBox.addItem(bc[3] + ' ' + bc[1][-4:])
