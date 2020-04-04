# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DfaForm.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DfaForm(object):
    def setupUi(self, DfaForm):
        DfaForm.setObjectName("DfaForm")
        DfaForm.resize(700, 414)
        self.textBrowser = QtWidgets.QTextBrowser(DfaForm)
        self.textBrowser.setGeometry(QtCore.QRect(10, 10, 681, 391))
        self.textBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.textBrowser.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.textBrowser.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(DfaForm)
        QtCore.QMetaObject.connectSlotsByName(DfaForm)

    def retranslateUi(self, DfaForm):
        _translate = QtCore.QCoreApplication.translate
        DfaForm.setWindowTitle(_translate("DfaForm", "DFA转换表"))
        self.textBrowser.setHtml(_translate("DfaForm", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
