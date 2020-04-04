# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LexicalDefinition.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LexicalDefinition(object):
    def setupUi(self, LexicalDefinition):
        LexicalDefinition.setObjectName("LexicalDefinition")
        LexicalDefinition.resize(699, 520)
        self.textBrowser = QtWidgets.QTextBrowser(LexicalDefinition)
        self.textBrowser.setGeometry(QtCore.QRect(10, 10, 671, 491))
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(LexicalDefinition)
        QtCore.QMetaObject.connectSlotsByName(LexicalDefinition)

    def retranslateUi(self, LexicalDefinition):
        _translate = QtCore.QCoreApplication.translate
        LexicalDefinition.setWindowTitle(_translate("LexicalDefinition", "词法定义"))
        self.textBrowser.setHtml(_translate("LexicalDefinition", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'宋体\';\">1. 标识符：</span>[A-Za-z_][0-9 A-Za-z_]* </p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'宋体\';\">2. 关键字：由于关键字有限，因此使用集合保存直接判断，无需构造自动机。</span> </p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'宋体\';\">3. 运算符：</span> </p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">  a. <span style=\" font-family:\'宋体\';\">算术运算符</span>: ([+][+=]?)|([-][-=]?)|([*/][=]?)|([%=]) </p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">  b. <span style=\" font-family:\'宋体\';\">关系运算符</span>: ([&gt;&lt;][=]?)|([=!][=]) </p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">  c. <span style=\" font-family:\'宋体\';\">逻辑运算符</span>: (&amp;&amp;)|(\\|\\|)|(!) </p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'宋体\';\">4. 界符：</span>[\\{\\}\\[\\]\\(\\),;\\?.:] </p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    （记</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    digit = 0-9 </p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    letter = a-f | A-F ）</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'宋体\';\">5. 无符号整数</span> </p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'宋体\';\">  a. 十进制数：</span><img src=\"file:///C:/Users/龙桑/AppData/Local/Temp/msohtmlclip1/01/clip_image002.gif\" width=\"100\" height=\"16\" /> </p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'宋体\';\">  b. 八进制数：</span><img src=\"file:///C:/Users/龙桑/AppData/Local/Temp/msohtmlclip1/01/clip_image004.gif\" width=\"104\" height=\"16\" /> </p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'宋体\';\">  c. 十六进制数：</span><img src=\"file:///C:/Users/龙桑/AppData/Local/Temp/msohtmlclip1/01/clip_image006.gif\" width=\"359\" height=\"21\" /> </p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'宋体\';\">6. 浮点数</span> </p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'宋体\';\">  a. 普通浮点数：</span><img src=\"file:///C:/Users/龙桑/AppData/Local/Temp/msohtmlclip1/01/clip_image008.gif\" width=\"153\" height=\"16\" /> </p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'宋体\';\">  b. 科学计数法：</span><img src=\"file:///C:/Users/龙桑/AppData/Local/Temp/msohtmlclip1/01/clip_image010.gif\" width=\"420\" height=\"25\" /> </p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'宋体\';\">7. 字符常数：</span>’(letter | <span style=\" font-family:\'宋体\';\">运算符</span> | digit | _ | <span style=\" font-family:\'宋体\';\">界符</span>)’ </p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'宋体\';\">8. 字符串常数：</span>”(letter | digit | _ | <span style=\" font-family:\'宋体\';\">运算符</span> | <span style=\" font-family:\'宋体\';\">界符</span>)” </p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'宋体\';\">      （记</span>a<span style=\" font-family:\'宋体\';\">为</span>*<span style=\" font-family:\'宋体\';\">以外的字符，</span>b<span style=\" font-family:\'宋体\';\">为</span>/<span style=\" font-family:\'宋体\';\">以外的字符</span> ）</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'宋体\';\">9. 注释：</span><img src=\"file:///C:/Users/龙桑/AppData/Local/Temp/msohtmlclip1/01/clip_image012.gif\" width=\"125\" height=\"16\" /> </p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
