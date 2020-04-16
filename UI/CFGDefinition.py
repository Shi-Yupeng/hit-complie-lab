# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PYTHON\hit-complie-lab-todo\UI\CFGDefinition.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class CFG_Ui_Form(object):
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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
