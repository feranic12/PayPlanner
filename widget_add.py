# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_add.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(351, 272)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 10, 131, 21))
        self.label.setObjectName("label")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(20, 40, 311, 31))
        self.textEdit.setObjectName("textEdit")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(20, 150, 121, 21))
        self.label_2.setObjectName("label_2")
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(20, 180, 201, 31))
        self.comboBox.setObjectName("comboBox")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(20, 80, 111, 21))
        self.label_3.setObjectName("label_3")
        self.dateEdit = QtWidgets.QDateEdit(Form)
        self.dateEdit.setGeometry(QtCore.QRect(240, 110, 91, 31))
        self.dateEdit.setDate(QtCore.QDate(2020, 1, 1))
        self.dateEdit.setObjectName("dateEdit")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(230, 150, 111, 21))
        self.label_4.setObjectName("label_4")
        self.textEdit_2 = QtWidgets.QTextEdit(Form)
        self.textEdit_2.setGeometry(QtCore.QRect(240, 180, 91, 31))
        self.textEdit_2.setObjectName("textEdit_2")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(230, 80, 111, 21))
        self.label_5.setObjectName("label_5")
        self.comboBox_2 = QtWidgets.QComboBox(Form)
        self.comboBox_2.setGeometry(QtCore.QRect(20, 110, 201, 31))
        self.comboBox_2.setObjectName("comboBox_2")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(260, 230, 75, 31))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Добавить подписку"))
        self.label.setText(_translate("Form", "Название подписки:"))
        self.label_2.setText(_translate("Form", "Банковская карта:"))
        self.label_3.setText(_translate("Form", " Срок продления"))
        self.label_4.setText(_translate("Form", "Сумма списания:"))
        self.label_5.setText(_translate("Form", " Срок окончания:"))
        self.pushButton.setText(_translate("Form", "Сохранить"))

