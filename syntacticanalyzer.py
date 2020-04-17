# from token import Token
import sys
import traceback
from lexicalanalyzer import LexicalAnalyzer
from ParseTree import ParseTree
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QWidget
from UI.MainWindow import Ui_Form
from UI.CFGDefinition import CFG_Ui_Form
from UI.LRtable import Ui_LRForm

class Term(object):
    """
    LR(1)产生式条目类，包括产生式左部，以及展望符
    """

    def __init__(self, left, right, lookahead):
        self.left = left
        self.right = right
        self.lookahead = lookahead

    def __eq__(self, other):
        if other == None:
            return False
        for i in range(len(self.left)):
            if self.left[i] != other.left[i]:
                return False
        for i in range(len(self.right)):
            if self.right[i] != other.right[i]:
                return False
        if self.lookahead != other.lookahead:
            return False
        return True

    def __hash__(self):
        hs = hash(self.lookahead)
        for st in self.left:
            hs += (hash(st) + hash(st))
        for st in self.right:
            hs += (hash(st) + hash(st) + hash(st))

        return hs

    def __str__(self):
        s = ""
        s = s + self.left[0] + " ==> "
        for r in self.right:
            s += (" " + r)
        s += ","
        s += self.lookahead
        return s

    def IsWaitingReduce(self):  # 判断是否是待约状态
        if self.right[0] == ".":
            return True
        else:
            return False

    def NextToDot(self):  # 返回beta串的第一个字符
        if self.right.index(".") < len(self.right) - 1:
            return self.right[self.right.index(".") + 1]
        else:
            return None

    def Beta(self):  # beta串

        if self.right.index(".") < len(self.right) - 2:
            return self.right[self.right.index(".") + 2:].copy()
        else:
            return []

class CFGTerm(object):
    """
    CFG条目，包含产生式的左部和右部
    """

    def __init__(self, left, right):
        self.__left = left
        self.__right = right

    def left(self):
        return self.__left.copy()

    def right(self):
        return self.__right.copy()

    def __eq__(self, other):
        # print(self, other)
        if other == None:
            return False
        for i in range(len(self.__left)):
            if self.__left[i] != other.__left[i]:
                return False
        for i in range(len(self.__right)):
            if self.__right[i] != other.__right[i]:
                return False
        return True

    def __str__(self):
        s = ""
        s = s + self.__left[0] + " ==> "
        for r in self.__right:
            s += (" " + r)
        return s

class LRCFG(object):
    # 使用LR(1)分析法进行语法分析

    def __init__(self, cfg_file):  # 通过文件加载文法
        self.cfgTerms = [] # 文法产生式，元素格式为CFGTerm
        self.Symbels = []  # 所有产生式中终结符和非终结符
        self.terminals = set() # 文法用到的非终结符，包含dollar符号
        self.nonterminals = set() # 文法用到的终结符
        self.terms = []  # 所有LR(1)条目，格式：Term
        self.cluster = None # 项集族
        self.table = None # LR分析表 格式：table{'action':{(i, a):sj}, 'goto':{(i, B): j} }

        dot = "."

        # 收集终结符和非终结符
        with open(cfg_file, "r") as f:
            lines = f.readlines()
            for line in lines:
                left = [line.split("==>")[0]]  # CFG条目左部，字符列表
                right = line.split("==>")[1].split()  # CFG条目右部，字符列表
                for l in left:
                    self.Symbels.append(l)
                    self.nonterminals.add(l)
                for r in right:
                    self.Symbels.append(r)
                    if r.isupper(): # 大写视为非终极符
                        self.nonterminals.add(r)
                    else: # 非大写视为终结符
                        self.terminals.add(r)
                self.cfgTerms.append(CFGTerm(left, right))
        self.terminals.add('dollar')

        # 构造LR项集族
        self.Items()

        # 构造LR分析表
        self.LRtable()
        self.PrintLRtable()

    def FirstForSingle(self, ALPHA):  # 单个字符的first集
        """
        求解单个字符的first集
        :param ALPHA:
        :return:
        """
        firstSet = set({})
        if ALPHA.islower():  # 小写的为终结符
            firstSet.add(ALPHA)
            return firstSet
        elif ALPHA.isupper():  # 大写的为非终结符
            for cfgterm in self.cfgTerms:
                if cfgterm.left()[0] == ALPHA and cfgterm.left()[0] != cfgterm.right()[0]:  # 跳过左递归
                    right = cfgterm.right()
                    if right[0] == "0":
                        firstSet.add("0")
                        continue
                    cnt = 0
                    while cnt < len(right) and "0" in self.FirstForSingle(right[cnt]):
                        firstSet = firstSet.union(self.FirstForSingle(right[cnt]))
                        cnt += 1
                    if cnt < len(right):
                        if not "0" in self.FirstForSingle(right[cnt]):
                            firstSet.discard("0")
                            firstSet = firstSet.union(self.FirstForSingle(right[cnt]))
        return firstSet

    def First(self, string_lst):  # 一个串的first集
        """
        返回串的FIRST集
        :param string_lst:
        :return:
        """
        cnt = 0
        SET = set({})
        while cnt < len(string_lst) and "0" in self.FirstForSingle(string_lst[cnt]):
            SET = SET.union(self.FirstForSingle(string_lst[cnt]))
            cnt += 1
        if cnt < len(string_lst):
            if not "0" in self.FirstForSingle(string_lst[cnt]):
                SET.discard("0")
                SET = SET.union(self.FirstForSingle(string_lst[cnt]))

        return SET

    def Closure(self, term_set):  # 项目集闭包
        SET = term_set.copy()
        TEMSET = SET.copy()
        add = True
        while add:
            add = False
            for term in TEMSET:
                B = term.NextToDot()
                beta = term.Beta()
                if B != None:
                    if B.isupper():
                        for cfgTerm in self.cfgTerms:
                            if cfgTerm.left()[0] == B:
                                beta.append(term.lookahead)
                                s = beta
                                for syb in self.First(s):
                                    right_set = cfgTerm.right()
                                    right_set.insert(0, ".")
                                    newterm = Term([B], right_set, syb)
                                    if not newterm in SET:
                                        SET.add(newterm)
                                        self.terms.append(newterm)

            if len(TEMSET) != len(SET):
                TEMSET = SET.copy()
                add = True
        return SET

    def Goto(self, setI, X):
        """
        输入 项目集闭包setI，文法符号X
        输出 I的后继项目集闭包
        """
        setJ = set({})
        for item in setI:
            if item.NextToDot() == X:
                newleft = item.left
                right = item.right.copy()
                right = right[:right.index(".")]
                right.append(X)
                right.append(".")
                right.extend(item.Beta())
                newlookahead = item.lookahead
                new_item = Term(newleft, right, newlookahead)
                self.terms.append(new_item)
                setJ.add(new_item)
        return self.Closure(setJ)

    def Items(self):
        """
        构造项集族
        """
        self.cluster = []  # 项集族
        s = set({})
        initTerm = Term(["SA"], [".", "S"], "dollar")
        s.add(initTerm)
        initSet = self.Closure(s)
        self.cluster.append(initSet)
        add = True
        temcluster = self.cluster.copy()
        while add:
            add = False
            for I in temcluster:
                for X in self.Symbels:
                    goto = self.Goto(I, X)
                    if goto and not (goto in self.cluster):
                        self.cluster.append(goto)
            if len(temcluster) != len(self.cluster.copy()):
                temcluster = self.cluster.copy()
                add = True

    def LRtable(self):
        '''
        Author: 欧龙燊
        使用规范LR(1)项集族，构造LR分析表
        约定：使用SA表示开始符号
        '''
        table = {'action':{}, 'goto':{}}

        for term_set in self.cluster: # 对于每个项集族，构建对应状态
            # 获得项集族index
            index_i = self.cluster.index(term_set)
            for term in term_set: # 对于项集族中每个项
                term_len = len(term.right)
                dot_index = term.right.index('.')
                # print(dot_index)

                # 计算Goto下一个符号的项集族
                if dot_index != term_len - 1:
                    goto = self.Goto(term_set, term.right[dot_index+1])
                else:
                    goto = set()
                # 找到对应的index，如果没有就是-1
                if len(goto) != 0:
                    index_j = self.cluster.index(goto)
                else:
                    index_j = -1

                # print(index_i, term, 'goto index', index_j)

                # 如果点点后面是合法终结符
                if (dot_index != term_len - 1 and term.right[dot_index+1].islower()
                        and index_j != -1):
                    a = term.right[dot_index+1]
                    table['action'][(index_i, a)] = 's' + str(index_j)
                # 如果点点后面是合法非终结符
                elif (dot_index != term_len - 1 and term.right[dot_index+1].isupper()
                        and index_j != -1):
                    B = term.right[dot_index+1]
                    table['goto'][(index_i, B)] = str(index_j)
                # 如果是规约项
                elif (dot_index == term_len - 1 and term.left != ['SA']):
                    right = term.right[:]
                    right.remove('.')
                    cfg_term = CFGTerm(term.left, right)
                    # print(cfg_term)
                    cfg_index = self.cfgTerms.index(cfg_term)
                    a = term.lookahead
                    table['action'][(index_i, a)] = 'r' + str(cfg_index)
                # 如果是接收项
                elif (dot_index == term_len - 1 and term.left == ['SA'] and term.lookahead == 'dollar'):
                    table['action'][(index_i, 'dollar')] = 'acc'

        # 用错误项填充剩余内容
        for i in range(len(self.cluster)):
            for symbol in self.terminals:
                if (i, symbol) not in table['action']:
                    table['action'][(i, symbol)] = 'err'

        self.table = table

    def PrintLRtable(self, type='get'):
        '''
        打印LR分析表内容或者获取对应字符串
        :type 可以取值'print'或'get'
        '''
        if self.table == None:
            print('LR分析表还未生成')
            return

        terminals = list(self.terminals)
        nonterminals = list(self.nonterminals)
        # nonterminals.remove('SA')
        terminals.sort()
        nonterminals.sort()

        # 表头
        res = ' '
        for i in terminals:
            if i == 'dollar':
                res += '\t$'
            else:
                res += '\t' + i
        for i in nonterminals:
            res += '\t' + i
        res += '\n'

        for line in range(len(self.cluster)):
            res += str(line)
            for i in terminals:
                res += '\t' + self.table['action'][(line, i)]
            for i in nonterminals:
                if (line, i) in self.table['goto']:
                    res += '\t' + self.table['goto'][(line, i)]
                else:
                    res += '\t '
            res += '\n'

        if type == 'print':
            print(res)
        elif type == 'get':
            return res

# 获取词法单元
class Lexical_unit(object):
    def __init__(self, Testfile):
        with open(Testfile, 'r', encoding='utf8') as f:
            string = f.read()
        lst = LexicalAnalyzer.main('source/FA_INPUT.csv', string)
        self.token_list = []
        for token in lst:
            if token.illegal == False:
                self.token_list.append(token)  # 从词法分析其中获取token list
        self.token_list.append('dollar') # 末尾添加$符

    def getTokenList(self):
        return self.token_list

# 移入规约驱动程序
class ShiftReduce(object):
    terms = None
    LRtable = None
    tokenlist = None

    def __init__(self, clusters, terms, LRtable, token_list):
        self.symbol_stack = []  # 符号栈
        self.state_stack = [0]  # 状态栈
        self.clusters = clusters
        self.terms = terms
        self.LRtable = LRtable
        self.tokenlist = token_list
        self.symbol_stack.append(terms[0].left()[0])

    # 移入操作
    def shift_in(self,next_state, insymbol):
        self.state_stack.append(next_state)
        self.symbol_stack.append(insymbol)

    # 规约操作
    def reduce(self, reduce_number):
        term = self.terms[reduce_number]
        left = term.left()
        right = term.right()
        # 弹出产生式右部符号
        for i in range(len(right)):
            self.state_stack.pop()
            self.symbol_stack.pop()
        # 压入
        self.symbol_stack.append(left[0])

    # 错误处理(恐慌模式)
    def ErrorHandle(self, reduce_formula):
        si = None
        nonterminal_symbol = None
        # 寻找存在goto项的状态及对应非终结符
        flag = False
        while True:
            for item in self.LRtable['goto'].keys():
                if self.state_stack[-1] in item:
                    si = self.state_stack[-1]
                    nonterminal_symbol = item[1]
                    flag = True
            if flag: # 寻找到则跳出
                break

            # # 如果弹出的是终结符，需要在reduce_formula对应弹出
            # symbol = self.symbol_stack[-1]
            # if not symbol.isupper():
            #     while reduce_formula[-1].isdigit():
            #         reduce_formula.pop()

            self.state_stack.pop()
            self.symbol_stack.pop()
            reduce_formula.pop()

        # 将A压栈(相当于用A规约)
        self.symbol_stack.append(nonterminal_symbol)
        self.state_stack.append(int(self.LRtable['goto'][(self.state_stack[-1], self.symbol_stack[-1])]))
        return nonterminal_symbol, reduce_formula # 返回A，用于丢弃输入符

    # LR分析表 格式：table{'action':{(i, a):sj}, 'goto':{(i, B): j} }
    def main(self):
        # 规约用的式子
        reduce_formula = []
        # 错误的式子
        wrong_reduce = []
        i = 0
        while True:
            token = self.tokenlist[i]

            # 判断是否接受
            if token == 'dollar' and self.LRtable['action'][self.state_stack[-1], 'dollar'] == 'acc':
                print('源程序正确接受')
                break

            if token != 'dollar' and token.kind == 'CMT': # 跳过注释
                i += 1
                continue

            # dollar的kind就为dollar
            if token == 'dollar':
                attribute = 'dollar'
            else:
                attribute = token.attribute
            print(attribute)
            print(self.state_stack)
            print(self.symbol_stack)
            print()

            # 遇到非法字符直接跳过
            try:
                next_operate = self.LRtable['action'][(self.state_stack[-1], attribute)]
                print(next_operate)
            except:
                i += 1
                continue
            # 移入
            if next_operate[0] == 's':
                # print(token.value)
                next_state = int(next_operate[1:])
                self.shift_in(next_state, attribute)
                reduce_formula.append(attribute + ':' + token.value + ' (' + str(token.rownumber) + ')')
                i += 1
            # 规约
            elif next_operate[0] == 'r':
                reduce_number = int(next_operate[1:])
                self.reduce(reduce_number)
                self.state_stack.append(int(self.LRtable['goto'][(self.state_stack[-1], self.symbol_stack[-1])]))
                reduce_formula.append(str(reduce_number))
            # 错误处理
            else:
                print('发生错误, 将使用恐慌模式处理！')
                nonterminal_symbol, reduce_formula = self.ErrorHandle(reduce_formula) # 找到出错的规约式
                print(reduce_formula)

                # 找到A推导的产生式, 并用它规约
                for i in range(len(self.terms)):
                    if self.terms[i].left()[0] == nonterminal_symbol:
                        for right in self.terms[i].right():
                            reduce_formula.append(right + ' (' + str(token.rownumber) + ')')
                        reduce_formula.append(str(i))
                        # 记录错误，格式：Error at Line [token.rownumber]：错误规约：规约式
                        wrong_reduce.append('Error at Line [' + str(token.rownumber) + ']：错误规约：' + self.terms[i].left()[0] + '-->' + ' '.join(self.terms[i].right()))
                        break

                # 寻找合法跟在A后面的符号
                legal_symbol = None
                for c in self.clusters[self.state_stack[-2]]:
                    if c.left[0] == nonterminal_symbol:
                        # print(self.termswithlookahead[i])
                        legal_symbol = c.lookahead
                        break

                # 丢弃不可能跟着的输入
                print(nonterminal_symbol, legal_symbol)
                while token != 'dollar' and token.attribute != legal_symbol:
                    i += 1
                    token = self.tokenlist[i]
        print(reduce_formula)
        return reduce_formula, wrong_reduce
# L, dollar, ['id (0)', '4', 'eq (0)', 'id (0)', '3', '5', '1']
# R, dollar, ['id (0)', '4', 'eq (0)', 'id (0)', '5', '1']

class Main(QMainWindow):
    CFGfile = "source/syntactical/cfg_file.txt"
    Testfile = 'source/syntactical/test.txt'
    token_list = Lexical_unit(Testfile).getTokenList()
    cfg = LRCFG(CFGfile)
    LRtable = cfg.table
    cfgterms = cfg.cfgTerms

    # 初始化
    def __init__(self, parent = None):
        super(Main, self).__init__(parent)
        self.Main_Ui = Ui_Form()
        self.Main_Ui.setupUi(self)
        self.bindbutton()

    # 绑定按钮
    def bindbutton(self):
        self.Main_Ui.import_cfg_pushButton.clicked.connect(self.openCFG)
        self.Main_Ui.import_test_pushButton.clicked.connect(self.opentestfile)
        self.Main_Ui.show_cfg_pushButton.clicked.connect(self.event_show_CFG)
        self.Main_Ui.show_LRtable_pushButton.clicked.connect(self.event_show_LRtable)
        self.Main_Ui.save_pushButton.clicked.connect(self.savetestcontent)
        self.Main_Ui.begin_test_pushButton.clicked.connect(self.beginTest)

    # 导入CFG
    def openCFG(self):
        fname = QFileDialog.getOpenFileName(self, caption='Open file', directory='.')
        if fname[0]:
            self.CFGfile = fname[0]
        self.cfg = LRCFG(self.CFGfile)
        self.LRtable = self.cfg.table
        self.cfgterms = self.cfg.cfgTerms

    # 导入测试文件
    def opentestfile(self):
        fname = QFileDialog.getOpenFileName(self, caption='Open file', directory='.')
        try:
            if fname[0]:
                self.Testfile = fname[0]
                self.token_list = Lexical_unit(self.Testfile).getTokenList()
                # print(self.Testfile)
                with open(fname[0], 'r', encoding='utf8') as f:
                    strings = f.read()

                strings = strings.split('\n')
                self.Main_Ui.tableWidget_2.setRowCount(len(strings))
                self.Main_Ui.tableWidget_2.clear()
                for i in range(len(strings)):
                    self.Main_Ui.tableWidget_2.setItem(i, 0, QTableWidgetItem(strings[i]))
        except Exception as e:
            pass
            # print(e)

    # 开始测试
    def beginTest(self):
        self.Main_Ui.result_textBrowser.clear()
        self.Main_Ui.wrong_textBrowser.clear()
        input, wrong_reduce = ShiftReduce(self.cfg.cluster, self.cfgterms, self.LRtable, self.token_list).main()
        try:
            root = ParseTree.create_tree(input, self.cfgterms)
            pre_str = root.pre_order_str(root, 0)
            self.Main_Ui.result_textBrowser.setText(pre_str)
        except:
            self.Main_Ui.result_textBrowser.setText('猜测错产生式，无法正常分析，构建语法树失败！')
        self.Main_Ui.wrong_textBrowser.setText('\n'.join(wrong_reduce))

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
            cfg_string += '-->'
            cfg_string += ' '.join(cfgterm.right())
            cfg_string += '\n'
        self.cfgform = QMainWindow()
        cfgui = CFG_Ui_Form()
        cfgui.setupUi(self.cfgform)
        cfgui.CFG_textBrowser.setText(cfg_string)
        self.cfgform.show()

    # 查看LR表
    def event_show_LRtable(self):
        lrtable = self.cfg.PrintLRtable()
        self.lrform = QMainWindow()
        lrui = Ui_LRForm()
        lrui.setupUi(self.lrform)
        lrui.textBrowser.setText(lrtable)
        self.lrform.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    m = Main()
    m.show()
    sys.exit(app.exec_())
    # token_list = Lexical_unit().getTokenList()
    # for token in token_list:
    #     print(token.string, token.kind)
    # cfg = LRCFG("source/cfg_file.txt")
    # SR = ShiftReduce(cfg.cfgTerms, cfg.table, token_list)
    # SR.main()
    # print(cfg.cfgTerms[0].left())
