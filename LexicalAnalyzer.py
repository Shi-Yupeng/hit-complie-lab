# -*- coding: utf-8 -*-

import csv
import re
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QWidget

from UI.MainWindow import Ui_Form
from UI.LexicalDefinition import Ui_LexicalDefinition
from UI.DfaForm import Ui_DfaForm
from lexical.Token_ import Token


##DFA, NFA的相互转换
class State():
    def __init__(self, contant):
        """

        :param contant: 列表，nfa状态集合的子集
        """
        self.tag = False  # 子集构造法中需要加上的标记
        self.contant = contant  # 因为这是nfa合并之后的状态，所以dfa中的每个状态时nfa状态集合的子集，contant的内容是一个列表，存放的是nfa的状态集合的子集
        self.is_final = False  # 是否是终态，默认false
        for ctt in contant:  # 如果合并后的dfa状态中，含有nfa的终态，那么这个dfa状态就是终态
            if "t_" in ctt:
                self.is_final = True
                break

    def __hash__(self):
        hs = hash(self.contant[0])
        for c in self.contant[1:]:
            hs += hash(c)
        return hs

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.contant == other.contant

    def __str__(self):
        discribe = ""
        for s in self.contant:
            discribe += ("," + s)
        return "(" + discribe[1:] + ")"


class DFA(object):

    def __init__(self, Dstart, Dtran):
        self.start_state = State(Dstart)  # 存放的是合并状态之后dfa的起始状态
        self.trans_table = {}  # 将dfa转换条目存储成字典形式，方便下边状态转换的查询
        self.states = [self.start_state]  # 存放dfa的所有状态
        self.conditions = []  # 转换条件，也就是字符
        for trans_term in Dtran:  # tran_term的数据形式（（s,a），t）,s代表状态，a代表遇到的字符，也就是转移条件，t代表转换之后的状态
            condition = trans_term[0][1]
            if not condition in self.conditions:  # 将转换条件存储
                self.conditions.append(condition)
            current_state = State(trans_term[0][0])
            next_state = State(trans_term[1])
            if not current_state in self.states:
                self.states.append(current_state)  # 将状态存储
            if not next_state in self.states:
                self.states.append(next_state)
            self.trans_table[(current_state, condition)] = next_state

    def printDfa(self, set_form=False):
        """
        以两种形式展示dfa
        :param set_form: 如果form是true，那么展示表，否则展示条目
        :return:
        """
        if set_form:
            lst = self.trans_table.items()
            for itm in lst:
                print(str(itm[0][0]) + " if " + itm[0][1] + " => " + str(itm[1]))
            return
        head = "condition\states  "
        for state in self.states:
            head += "{:21}".format(str(state))
        print(head)
        for c in self.conditions:
            print("{:17}".format(c), end=" ")
            for i in range(len(self.states)):
                if (self.states[i], c) in self.trans_table.keys():
                    s = self.trans_table[(self.states[i], c)]
                else:
                    s = ""
                print("{:20}".format(str(s)), end=" ")
            print()

    def move(self, s, c):
        """
        状态s遇到条件c的转移
        :param s:
        :param c:
        :return: 如果状态机有对应的转移，那么返回转移后的状态，否则返回空
        """
        if (s, c) in self.trans_table.keys():
            return self.trans_table[(s, c)]
        else:
            return None

    def firstStringAccept(self, string):
        """
        返回：
        :param string:
        :return: dfa接收的串，dfa所处终态，剩下的串；如果某次没有成功处理字符串，返回："",None,string.其中，String是输入的串
        """

        s = self.start_state

        acpt = 0  # 记录上一次识别成功接受的位置
        s_pre = None  # 记录上一次识别成功接收时的终态

        for i in range(len(string)):
            c = string[i]
            if u'\u4e00' <= c <= u'\u9fa5' or c == "，" or c == '；' or c == '。' or c == '、':
                c = "中"
            if s.is_final:
                acpt = i
                s_pre = s
            s = self.move(s, c)
            if s == None:
                return string[:acpt], s_pre, string[acpt:]
            if i == len(string) - 1:
                if s.is_final:
                    return string, s, ""
                else:
                    return string[:acpt], s_pre, string[acpt:]


class FA(object):
    def __init__(self, FA_file):
        self.trans_table = {}  # 状态转换表
        self.start_state = []  # 存放起始状态
        # self.terminal_state = {}
        self.states = []
        self.symbles = []
        self.new_start = None
        with open(FA_file, "r", encoding='utf-8') as f:
            file = csv.reader(f)
            f_csv = []
            for line in file:
                f_csv.append(line)
            headers = f_csv[0]
            inputs = headers[1:]  # csv文件第一行，从序号1开始存放的都是输入字符
            self.symbles = inputs  # 初始化输入字符
            f_csv = f_csv[1:]  # 此时f_csv存放的是状态，以及状态后边遇到字符后的转移状态
            for row in f_csv:
                state = row[0]
                self.states.append(state)  # 状态集合中存放状态
                if "s_" in state:  # 判断是否是起始状态，如果是，将s_后边的串存放在起始状态和状态列表中
                    state = state[2:]
                    self.start_state.append(state)
                    # self.start_state=[state]
                # if "t_" in state:
                #     state = state[2:]
                #     self.terminal_state.get(state)
                for i in range(len(row) - 1):
                    term = (inputs[i], state)  # 转移条件：状态 + 字符
                    next_states = row[i + 1]
                    states = re.match(r"{(.*?)}", next_states) \
                        .group(1).replace(" ", "").split(",")  # 转移的状态
                    if len(states[0]) != 0:
                        self.trans_table[term] = states  # 将此条状态转移条目加到自动机转换表中
        if len(self.start_state) > 1:  # 如果起始状态中有多个，说明有多个自动机，此时要设置一个新的、共同的起点，和所有原来自动机的起始状态用空边相连接
            self.new_start = "new_start"
            term = ("null", self.new_start)
            self.trans_table[term] = self.start_state
        else:
            self.new_start = self.start_state[0]

    def dfa(self):  # 子集构造法 得到DFA
        init_state = State(self.epsilon_closure([self.new_start]))
        Dset = [init_state]
        Dtran = []  # dfa转换状态条目
        for state in Dset:

            if state.tag == False:
                state.tag = True
                for smp in self.symbles:
                    if len(self.move(state.contant, smp)) == 0 or smp == "null":
                        continue
                    U = State(self.epsilon_closure(self.move(state.contant, smp)))
                    if not U in Dset:
                        Dset.append(U)
                    k = (state.contant, smp)  # 得到的dfa转移状态和转移条件
                    v = U.contant  # 得到的dfa的转换状态
                    Dtran.append((k, v))
        Dstart = self.epsilon_closure([self.new_start])  # 起始状态的epsilon集合作为dfa起始状态
        dfa = DFA(Dstart, Dtran)
        return dfa

    def move(self, T, a):
        lst = []
        for t in T:
            if (a, t) in self.trans_table.keys():
                lst.extend(self.trans_table[(a, t)])
        return lst

    def epsilon_closure(self, T):

        out = list(T)

        stack = []
        for sp in out:
            stack.append(sp)
        while len(stack) != 0:
            t = stack.pop()
            if ('null', t) in self.trans_table.keys():
                for u in self.trans_table[('null', t)]:
                    if not u in out:
                        out.append(u)
                        stack.append(u)
        return out


class TokenMaker(object):
    """
    根据token定义文件，将终态和对应种别码读入
    """

    def __init__(self, Tokenfile):
        self.token_list = []
        with open(Tokenfile, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                self.token_list.append(line.rstrip())

    def __call__(self, state, string, rownumber):  # 根据终态、被接受的字符串new出一个Token
        if state != None:
            for tk in self.token_list:
                if tk.split(":")[0] in state.contant:
                    token = Token(string, tk, rownumber)
                    return token
        else:
            return Token(string, None, rownumber)


class LexicalAnalyzer(object):

    @staticmethod
    def main(FAtable, string):
        # string = re.sub(r'[\u4e00-\u9fa5]','a',string)
        dfa = FA(FAtable).dfa()
        dfa.printDfa()
        tkn = TokenMaker("source/token.txt")
        token_list = []
        string_lines = string.split("\n")
        for rownumber in range(len(string_lines)):
            line = string_lines[rownumber]
            string = line
            string = string.lstrip()

            error_str = ""
            while string != "":

                acept_string, state, left = dfa.firstStringAccept(string)
                # if left != "":
                #     if left[0] == " " or  left[0] == "\t":  # 去掉串首空格

                left = left.lstrip()
                # string = left
                # continue
                err = False
                if acept_string == "":  # 如果某次处理之后，剩下的串长度没变，说明此时的串没有被识别，条过并记录该字符继续处理
                    err = True
                    # print("===========",left)
                    error_str += left[0]
                    left = left[1:]
                if left == "" and err == True:  # 条过字符一直到最终也没遇到可以接受的合法字符
                    token_list.append(tkn(None, error_str, rownumber + 1))
                if err == False:
                    if len(error_str) != 0:
                        token_list.append(tkn(None, error_str, rownumber + 1))
                        error_str = ""
                    token_list.append(tkn(state, acept_string, rownumber + 1))
                string = left
        return token_list


class LexDef(QWidget, Ui_LexicalDefinition):
    def __init__(self):
        super(LexDef, self).__init__()
        self.setupUi(self)


class DfaShow(QWidget, Ui_DfaForm):
    def __init__(self):
        super(DfaShow, self).__init__()
        self.setupUi(self)
        import show_dfa
        self.textBrowser.setText(show_dfa.get_dfa_str())


class Main(QMainWindow):
    FAtable = "source/FA_INPUT.csv"
    Testfile = 'source/test.txt'

    # 初始化
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.Main_Ui = Ui_Form()
        self.Main_Ui.setupUi(self)
        self.bindbutton()

    # 绑定按钮
    def bindbutton(self):
        self.Main_Ui.importFAtablepushButton.clicked.connect(self.openfatable)
        self.Main_Ui.importtestfilepushButton.clicked.connect(self.opentestfile)
        self.Main_Ui.begintestpushButton.clicked.connect(self.beginTest)
        self.Main_Ui.savecontentpushButton.clicked.connect(self.savetestcontent)
        self.Main_Ui.showlexicalrulespushButton.clicked.connect(self.event_show_lex_def)
        self.Main_Ui.showDFAtablepushButton.clicked.connect(self.event_show_dfa)

    # 导入FA表
    def openfatable(self):
        fname = QFileDialog.getOpenFileName(self, caption='Open file', directory='.')
        if fname[0]:
            self.FAtable = fname[0]

    # 导入测试文件
    def opentestfile(self):
        fname = QFileDialog.getOpenFileName(self, caption='Open file', directory='.')
        try:
            if fname[0]:
                self.Testfile = fname[0]
                # print(self.Testfile)
                with open(fname[0], 'r', encoding='utf8') as f:
                    strings = f.read()

                strings = strings.split('\n')
                self.Main_Ui.tableWidget.setRowCount(len(strings))
                self.Main_Ui.tableWidget.clear()
                for i in range(len(strings)):
                    self.Main_Ui.tableWidget.setItem(i, 0, QTableWidgetItem(strings[i]))
        except Exception as e:
            pass
            # print(e)

    # 开始测试
    def beginTest(self):
        strs = ""
        self.token_lst = LexicalAnalyzer.main(self.FAtable, self.gettablecontent())
        self.Main_Ui.textBrowser.clear()
        self.Main_Ui.textBrowser_2.clear()
        for t in self.token_lst:
            strs += t.error() + ";"  # TODO 添加输出信息
            self.Main_Ui.textBrowser.insertPlainText(str(t) + '\n')
            if t.error() != '':
                self.Main_Ui.textBrowser_2.insertPlainText(str(t.error()) + '\n')

    # 保存内容
    def savetestcontent(self):
        with open(self.Testfile, 'w', encoding='utf8') as f:
            f.write(self.gettablecontent())
        self.Main_Ui.textBrowser.clear()
        self.Main_Ui.textBrowser_2.clear()
        self.Main_Ui.textBrowser.insertPlainText('保存成功！')

    # 获取表格内容
    def gettablecontent(self):
        count = self.Main_Ui.tableWidget.rowCount()
        string = ""
        for i in range(count):
            string += self.Main_Ui.tableWidget.item(i, 0).text() + '\n'
        return string[:-1]

    # 查看词法规则
    def event_show_lex_def(self):
        self.lexdef_win = LexDef()
        self.lexdef_win.show()

    # 查看DFA转换表
    def event_show_dfa(self):
        self.dfa_win = DfaShow()
        self.dfa_win.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    m = Main()
    m.show()
    sys.exit(app.exec_())

    # fa = FA("转换表.csv")
    # dfa = fa.dfa()
    # dfa.printDfa(set_form=False)
    # token_lst = LexicalAnalyzer.main()
    # for t in token_lst:
    #     print(t)
