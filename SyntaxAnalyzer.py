import os
import sys
import traceback
import pickle as pk
from syntax.ParseTree import ParseTree
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem

from UI.MainWindow import Ui_Form
from UI.CFGDefinition import Ui_Form as CFG_Ui_Form
from UI.LRtable import Ui_Form as Ui_LRForm
from UI.FirstForm import Ui_Form as First_Ui_Form

from syntax.LexicalUnit import Lexical_unit
from syntax.LRCFG import LRCFG
from syntax.ShiftReduce import ShiftReduce


class Main(QMainWindow):
    # 初始化
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.Main_Ui = Ui_Form()
        self.Main_Ui.setupUi(self)
        self.bindbutton()

        self.CFGfile = None
        self.LRtable = None
        self.Testfile = None
        self.cfg = None
        self.cfgform = None
        self.cfgterms = None
        self.lrform = None
        self.token_list = None

    # 绑定按钮
    def bindbutton(self):
        self.Main_Ui.import_cfg_pushButton.clicked.connect(self.openCFG)
        self.Main_Ui.import_test_pushButton.clicked.connect(self.opentestfile)
        self.Main_Ui.show_cfg_pushButton.clicked.connect(self.event_show_CFG)
        self.Main_Ui.show_LRtable_pushButton.clicked.connect(self.event_show_LRtable)
        self.Main_Ui.save_pushButton.clicked.connect(self.savetestcontent)
        self.Main_Ui.begin_test_pushButton.clicked.connect(self.beginTest)
        self.Main_Ui.bt_view_first.clicked.connect(self.event_show_first)

    # 导入CFG
    def openCFG(self):
        try:
            # 选择文件
            fname = QFileDialog.getOpenFileName(self, caption='Open file', directory='.')
            if fname[0]:
                self.CFGfile = fname[0]
            else:
                return

            self.cfg = LRCFG(self.CFGfile)
            self.LRtable = self.cfg.table
            self.cfgterms = self.cfg.cfgTerms
        except Exception:
            exstr = traceback.format_exc()
            print(exstr)

    # 导入测试文件
    def opentestfile(self):
        fname = QFileDialog.getOpenFileName(self, caption='Open file', directory='.')
        try:
            if fname[0]:
                self.Testfile = fname[0]
                self.token_list = Lexical_unit(self.Testfile).getTokenList()
                with open(fname[0], 'r', encoding='utf8') as f:
                    strings = f.read()

                strings = strings.split('\n')
                self.Main_Ui.tableWidget_2.setRowCount(len(strings))
                self.Main_Ui.tableWidget_2.clear()
                for i in range(len(strings)):
                    self.Main_Ui.tableWidget_2.setItem(i, 0, QTableWidgetItem(strings[i]))
        except Exception as e:
            pass

    # 开始测试
    def beginTest(self):
        try:
            self.Main_Ui.result_textBrowser.clear()
            self.Main_Ui.wrong_textBrowser.clear()
            input, wrong_reduce = ShiftReduce(self.cfgterms, self.cfg.cluster, self.LRtable,
                                              self.token_list).main()
            try:
                root = ParseTree.create_tree(input, self.cfgterms)
                pre_str = root.pre_order_str(root, 0)
                self.Main_Ui.result_textBrowser.setText(pre_str)
            except:
                self.Main_Ui.result_textBrowser.setText('猜测错产生式，无法正常分析，构建语法树失败！')
            self.Main_Ui.wrong_textBrowser.setText('\n'.join(wrong_reduce))
        except Exception as e:
            exstr = traceback.format_exc()
            print(exstr)

    # 保存内容
    def savetestcontent(self):
        with open(self.Testfile, 'w', encoding='utf8') as f:
            f.write(self.gettablecontent())
        self.Main_Ui.result_textBrowser.clear()
        self.Main_Ui.wrong_textBrowser.clear()
        self.Main_Ui.result_textBrowser.insertPlainText('保存成功！')

    # 获取表格内容
    def gettablecontent(self):
        count = self.Main_Ui.tableWidget_2.rowCount()
        string = ""
        for i in range(count):
            string += self.Main_Ui.tableWidget_2.item(i, 0).text() + '\n'
        return string[:-1]

    # 查看CFG
    def event_show_CFG(self):
        cfg_string = ''
        for cfgterm in self.cfgterms:
            cfg_string += ' '.join(cfgterm.left())
            cfg_string += '\t-->\t'
            cfg_string += ' '.join(cfgterm.right())
            cfg_string += '\n'
        self.cfgform = QMainWindow()
        cfgui = CFG_Ui_Form()
        cfgui.setupUi(self.cfgform)
        cfgui.CFG_textBrowser.setText(cfg_string)
        self.cfgform.show()

    # 查看LR表
    def event_show_LRtable(self):
        try:
            lrtable = self.cfg.PrintLRtable()
            self.lrform = QMainWindow()
            lrui = Ui_LRForm()
            lrui.setupUi(self.lrform)
            lrui.textBrowser.setText(lrtable)
            self.lrform.show()
        except Exception:
            exstr = traceback.format_exc()
            print(exstr)

    def event_show_first(self):
        first_form = First_Ui_Form()
        self.first_win = QMainWindow()
        first_form.setupUi(self.first_win)

        if self.cfg == None:
            return
        ans = ''
        for i in self.cfg.nonterminals:
            ans += i + '\t' + str(self.cfg.FirstForSingle(i)) + '\n'

        first_form.textBrowser.setText(ans)
        self.first_win.show()


def main():
    app = QApplication(sys.argv)
    m = Main()
    m.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
