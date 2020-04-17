# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CFGDefinition.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(460, 421)
        self.CFG_textBrowser = QtWidgets.QTextBrowser(Form)
        self.CFG_textBrowser.setGeometry(QtCore.QRect(0, 0, 461, 421))
        self.CFG_textBrowser.setObjectName("CFG_textBrowser")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "CFGDefinition"))
