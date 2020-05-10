import sys
import traceback

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem

from UI.MainWindow import Ui_Form
from UI.SymbleTable import Ui_Form as UiSymbleTable
from syntax.LRCFG import LRCFG
from syntax.LexicalUnit import Lexical_unit
from syntax.ParseTree import ParseTree
from syntax.ShiftReduce import ShiftReduce
from semantic.Board import Board
from semantic.CodeGenerator import Generator


def main():
    app = QApplication(sys.argv)
    m = Main()
    m.show()
    sys.exit(app.exec_())


class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__()
        self.main_window = Ui_Form()
        self.main_window.setupUi(self)

        self.analyzer = SemanticAnalysis()
        self.analyzer.get_CFGfile()

        self.bind_button()

    def bind_button(self):
        self.main_window.semantic_lb_import.clicked.connect(self.import_source_file)
        self.main_window.semantic_lb_generate.clicked.connect(self.generate_code)
        self.main_window.semantic_lb_symble.clicked.connect(self.event_show_symble_table)
        self.main_window.semantic_lb_3addr.clicked.connect(self.event_show_3addr)

    def import_source_file(self):
        fname = QFileDialog.getOpenFileName(self, caption='Open file', directory='.')
        try:
            if fname[0]:
                self.source_file = fname[0]
                with open(fname[0], 'r', encoding='utf8') as f:
                    strings = f.read()
                strings = strings.split('\n')
                self.main_window.semantic_table_source.setRowCount(len(strings))
                self.main_window.semantic_table_source.clear()
                for i in range(len(strings)):
                    self.main_window.semantic_table_source.setItem(i, 0,
                                                                   QTableWidgetItem(strings[i]))

                self.analyzer.set_test_file(self.source_file)
                self.analyzer.get_parse_tree()
        except Exception as e:
            pass

    def generate_code(self):
        try:
            self.analyzer.board.clear()
            # 生成中间代码
            self.analyzer.generate()

            # 获取结果并输出
            ans = self.analyzer.board.get_result()
            lines = ans.split('\n')
            self.main_window.semantic_table_out.setRowCount(len(lines))
            self.main_window.semantic_table_out.clear()
            for i in range(len(lines)):
                self.main_window.semantic_table_out.setItem(i, 0, QTableWidgetItem(lines[i]))

            # 获取错误并输出
            err_list = self.analyzer.board.get_wrong()
            self.main_window.semantic_text_error.clear()
            for err in err_list:
                self.main_window.semantic_text_error.append(err)
        except Exception:
            exstr = traceback.format_exc()
            self.main_window.semantic_text_error.append(exstr)
            print(exstr)

    def event_show_3addr(self):
        ans = self.analyzer.board.get_3addr()
        lines = ans.split('\n')
        self.main_window.semantic_table_out.clear()
        self.main_window.semantic_table_out.setRowCount(len(lines))
        for i in range(len(lines)):
            self.main_window.semantic_table_out.setItem(i, 0, QTableWidgetItem(lines[i]))

    def event_show_symble_table(self):
        try:
            self.symble_table_window = QMainWindow()
            ui = UiSymbleTable()
            ui.setupUi(self.symble_table_window)
            ui.text1.setText(self.analyzer.board.get_table())
            self.symble_table_window.show()
        except Exception:
            exstr = traceback.format_exc()
            print(exstr)


class SemanticAnalysis:
    '''
    语义分析+中间代码生成
    '''

    def __init__(self):
        # 语法分析器需要的变量
        self.CFGfile = None
        self.cfg = None
        self.LRtable = None
        self.cfgterms = None
        self.Testfile = None
        self.token_list = None

        # 语义分析器相关变量
        self.root = None  # 分析树的根节点
        self.board = Board()  # 保存生成的中间代码
        self.generator = Generator(self.board)

    def generate(self):
        '''
        生成中间代码，保存在self.board中
        '''
        func = self.get_func(self.root)
        func(self.root)
        self.board.label_scan()
        self.board.show_result()
        # self.board.show_wrong()
        print('中间代码生成完成！')

    def get_parse_tree(self):
        '''
        使用LR(1)语法分析技术构造分析树
        '''
        input, wrong_reduce = ShiftReduce(self.cfgterms, self.cfg.cluster, self.LRtable,
                                          self.token_list).main()
        root = ParseTree.create_tree(input, self.cfgterms)
        pre_str = root.pre_order_str(root, 0)
        print(pre_str)
        self.root = root

    def get_CFGfile(self):
        '''
        读CFG文件，生成cfg项、LR表、LR项集族
        '''
        self.CFGfile = 'source/syntax/cfg/cfg_file_full.txt'
        self.cfg = LRCFG(self.CFGfile)
        self.LRtable = self.cfg.table
        self.cfgterms = self.cfg.cfgTerms

    def set_test_file(self, path):
        '''
        读测试文件，生成TOKEN列表
        '''
        # self.Testfile = 'source/semantic/test/wrong_test.txt' #syp更改测试文件路径
        self.Testfile = path
        self.token_list = Lexical_unit(self.Testfile).getTokenList()

    def get_func(self, node):
        '''
        获取一个节点对应的SDT函数
        :param: node 节点
        :return: node对应SDT的函数
        '''
        func_name = 'g' + str(node.cfg_index) + '_' + node.val
        func = getattr(self.generator, func_name)
        return func


if __name__ == '__main__':
    main()
