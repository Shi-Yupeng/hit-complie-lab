# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1013, 768)
        self.lexicalanalys = QtWidgets.QTabWidget(Form)
        self.lexicalanalys.setGeometry(QtCore.QRect(0, 0, 1011, 761))
        font = QtGui.QFont()
        font.setItalic(False)
        self.lexicalanalys.setFont(font)
        self.lexicalanalys.setMouseTracking(True)
        self.lexicalanalys.setObjectName("lexicalanalys")
        self.tab = QtWidgets.QWidget()
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tab.setFont(font)
        self.tab.setObjectName("tab")
        self.layoutWidget = QtWidgets.QWidget(self.tab)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 1021, 741))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.importFAtablepushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.importFAtablepushButton.setObjectName("importFAtablepushButton")
        self.horizontalLayout.addWidget(self.importFAtablepushButton)
        self.importtestfilepushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.importtestfilepushButton.setObjectName("importtestfilepushButton")
        self.horizontalLayout.addWidget(self.importtestfilepushButton)
        self.showlexicalrulespushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.showlexicalrulespushButton.setObjectName("showlexicalrulespushButton")
        self.horizontalLayout.addWidget(self.showlexicalrulespushButton)
        self.showDFAtablepushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.showDFAtablepushButton.setObjectName("showDFAtablepushButton")
        self.horizontalLayout.addWidget(self.showDFAtablepushButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.tableWidget = QtWidgets.QTableWidget(self.layoutWidget)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setObjectName("tableWidget")
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.tableWidget)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.begintestpushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.begintestpushButton.setObjectName("begintestpushButton")
        self.horizontalLayout_2.addWidget(self.begintestpushButton)
        self.savecontentpushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.savecontentpushButton.setObjectName("savecontentpushButton")
        self.horizontalLayout_2.addWidget(self.savecontentpushButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.textBrowser = QtWidgets.QTextBrowser(self.layoutWidget)
        self.textBrowser.setObjectName("textBrowser")
        self.horizontalLayout_3.addWidget(self.textBrowser)
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.layoutWidget)
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.horizontalLayout_3.addWidget(self.textBrowser_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.lexicalanalys.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.layoutWidget1 = QtWidgets.QWidget(self.tab_2)
        self.layoutWidget1.setGeometry(QtCore.QRect(0, 0, 1021, 741))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.import_cfg_pushButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.import_cfg_pushButton.setObjectName("import_cfg_pushButton")
        self.horizontalLayout_5.addWidget(self.import_cfg_pushButton)
        self.import_test_pushButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.import_test_pushButton.setObjectName("import_test_pushButton")
        self.horizontalLayout_5.addWidget(self.import_test_pushButton)
        self.show_cfg_pushButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.show_cfg_pushButton.setObjectName("show_cfg_pushButton")
        self.horizontalLayout_5.addWidget(self.show_cfg_pushButton)
        self.show_LRtable_pushButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.show_LRtable_pushButton.setObjectName("show_LRtable_pushButton")
        self.horizontalLayout_5.addWidget(self.show_LRtable_pushButton)
        self.bt_view_first = QtWidgets.QPushButton(self.layoutWidget1)
        self.bt_view_first.setObjectName("bt_view_first")
        self.horizontalLayout_5.addWidget(self.bt_view_first)
        self.verticalLayout_7.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_4.addWidget(self.label_4)
        self.tableWidget_2 = QtWidgets.QTableWidget(self.layoutWidget1)
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.setColumnCount(1)
        self.tableWidget_2.setObjectName("tableWidget_2")
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        self.tableWidget_2.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_2.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_4.addWidget(self.tableWidget_2)
        self.horizontalLayout_6.addLayout(self.verticalLayout_4)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_5 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_5.addWidget(self.label_5)
        self.wrong_textBrowser = QtWidgets.QTextBrowser(self.layoutWidget1)
        self.wrong_textBrowser.setObjectName("wrong_textBrowser")
        self.verticalLayout_5.addWidget(self.wrong_textBrowser)
        self.horizontalLayout_6.addLayout(self.verticalLayout_5)
        self.verticalLayout_7.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.begin_test_pushButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.begin_test_pushButton.setObjectName("begin_test_pushButton")
        self.horizontalLayout_7.addWidget(self.begin_test_pushButton)
        self.save_pushButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.save_pushButton.setObjectName("save_pushButton")
        self.horizontalLayout_7.addWidget(self.save_pushButton)
        self.verticalLayout_7.addLayout(self.horizontalLayout_7)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_6 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_6.addWidget(self.label_6)
        self.result_textBrowser = QtWidgets.QTextBrowser(self.layoutWidget1)
        self.result_textBrowser.setObjectName("result_textBrowser")
        self.verticalLayout_6.addWidget(self.result_textBrowser)
        self.verticalLayout_7.addLayout(self.verticalLayout_6)
        self.lexicalanalys.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.splitter_4 = QtWidgets.QSplitter(self.tab_3)
        self.splitter_4.setGeometry(QtCore.QRect(10, 532, 991, 199))
        self.splitter_4.setOrientation(QtCore.Qt.Vertical)
        self.splitter_4.setObjectName("splitter_4")
        self.label_9 = QtWidgets.QLabel(self.splitter_4)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.semantic_text_error = QtWidgets.QTextBrowser(self.splitter_4)
        self.semantic_text_error.setObjectName("semantic_text_error")
        self.splitter = QtWidgets.QSplitter(self.tab_3)
        self.splitter.setGeometry(QtCore.QRect(10, 20, 251, 501))
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.semantic_lb_import = QtWidgets.QPushButton(self.splitter)
        self.semantic_lb_import.setObjectName("semantic_lb_import")
        self.label_7 = QtWidgets.QLabel(self.splitter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.semantic_table_source = QtWidgets.QTableWidget(self.splitter)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.semantic_table_source.setFont(font)
        self.semantic_table_source.setColumnCount(1)
        self.semantic_table_source.setObjectName("semantic_table_source")
        self.semantic_table_source.setRowCount(0)
        self.semantic_table_source.horizontalHeader().setVisible(False)
        self.semantic_table_source.horizontalHeader().setMinimumSectionSize(25)
        self.semantic_table_source.horizontalHeader().setStretchLastSection(True)
        self.semantic_table_source.verticalHeader().setDefaultSectionSize(20)
        self.semantic_table_source.verticalHeader().setMinimumSectionSize(20)
        self.splitter_2 = QtWidgets.QSplitter(self.tab_3)
        self.splitter_2.setGeometry(QtCore.QRect(264, 20, 731, 501))
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName("splitter_2")
        self.semantic_lb_generate = QtWidgets.QPushButton(self.splitter_2)
        self.semantic_lb_generate.setObjectName("semantic_lb_generate")
        self.label_8 = QtWidgets.QLabel(self.splitter_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.semantic_table_out = QtWidgets.QTableWidget(self.splitter_2)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.semantic_table_out.setFont(font)
        self.semantic_table_out.setColumnCount(1)
        self.semantic_table_out.setObjectName("semantic_table_out")
        self.semantic_table_out.setRowCount(0)
        self.semantic_table_out.horizontalHeader().setVisible(False)
        self.semantic_table_out.horizontalHeader().setStretchLastSection(True)
        self.semantic_table_out.verticalHeader().setDefaultSectionSize(9)
        self.semantic_table_out.verticalHeader().setMinimumSectionSize(9)
        self.semantic_lb_symble = QtWidgets.QPushButton(self.splitter_2)
        self.semantic_lb_symble.setObjectName("semantic_lb_symble")
        self.lexicalanalys.addTab(self.tab_3, "")

        self.retranslateUi(Form)
        self.lexicalanalys.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.importFAtablepushButton.setText(_translate("Form", "导入FA表"))
        self.importtestfilepushButton.setText(_translate("Form", "导入测试文件"))
        self.showlexicalrulespushButton.setText(_translate("Form", "查看词法规则"))
        self.showDFAtablepushButton.setText(_translate("Form", "查看DFA转换表"))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">测试内容：</span></p></body></html>"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "源程序"))
        self.begintestpushButton.setText(_translate("Form", "开始测试"))
        self.savecontentpushButton.setText(_translate("Form", "保存内容"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">测试结果：</span></p></body></html>"))
        self.label_3.setText(_translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">错误报告：</span></p></body></html>"))
        self.lexicalanalys.setTabText(self.lexicalanalys.indexOf(self.tab), _translate("Form", "词法分析"))
        self.import_cfg_pushButton.setText(_translate("Form", "导入文法文件"))
        self.import_test_pushButton.setText(_translate("Form", "导入测试文件"))
        self.show_cfg_pushButton.setText(_translate("Form", "查看文法定义"))
        self.show_LRtable_pushButton.setText(_translate("Form", "查看LR表"))
        self.bt_view_first.setText(_translate("Form", "查看FIRST集"))
        self.label_4.setText(_translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">测试内容：</span></p></body></html>"))
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("Form", "源程序"))
        self.label_5.setText(_translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">错误报告：</span></p></body></html>"))
        self.begin_test_pushButton.setText(_translate("Form", "开始测试"))
        self.save_pushButton.setText(_translate("Form", "保存内容"))
        self.label_6.setText(_translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">测试结果：</span></p></body></html>"))
        self.lexicalanalys.setTabText(self.lexicalanalys.indexOf(self.tab_2), _translate("Form", "语法分析"))
        self.label_9.setText(_translate("Form", "错误报告"))
        self.semantic_lb_import.setText(_translate("Form", "导入源程序"))
        self.label_7.setText(_translate("Form", "源程序"))
        self.semantic_lb_generate.setText(_translate("Form", "生成！"))
        self.label_8.setText(_translate("Form", "中间代码"))
        self.semantic_lb_symble.setText(_translate("Form", "查看符号表"))
        self.lexicalanalys.setTabText(self.lexicalanalys.indexOf(self.tab_3), _translate("Form", "语义分析"))
