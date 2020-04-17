from syntactical.CFGTerm import CFGTerm
from syntactical.Term import Term
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