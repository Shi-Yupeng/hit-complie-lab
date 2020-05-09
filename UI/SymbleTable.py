# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SymbleTable.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(620, 419)
        self.text1 = QtWidgets.QTextBrowser(Form)
        self.text1.setGeometry(QtCore.QRect(10, 10, 601, 401))
        self.text1.setObjectName("text1")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
