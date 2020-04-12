# from token import Token
import re
from lexicalanalyzer import LexicalAnalyzer



class Term(object):
    """
    LR(1)产生式条目类，包括产生式左部，以及展望符
    """
    def __init__(self, left, right, lookahead):
        self.left = left
        self.right = right
        self.lookahead = lookahead

    def __eq__(self, other):
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
    def IsWaitingReduce(self):#判断是否是待约状态
        if self.right[0] == ".":
            return True
        else:
            return False
    def NextToDot(self): #返回beta串的第一个字符
        if self.right.index(".") < len(self.right) - 1:
            return self.right[self.right.index(".") + 1]
        else:
            return None

    def Beta(self): #beta串

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

class LRCFG(object):

    def __init__(self, cfg_file): #通过文件加载文法
        self.terms = [] #所有LR(1)条目
        self.cfgTerms = []
        dot = "."
        self.Symbels = []
        with open(cfg_file, "r") as f:
            lines = f.readlines()
            for line in lines:
                left = re.findall(r"\((.*?)\)", line.split("==>")[0]) #CFG条目左部，字符列表
                right = re.findall(r"\((.*?)\)", line.split("==>")[1]) #CFG条目右部，字符列表
                for l in left:
                    self.Symbels.append(l)
                for r in right:
                    self.Symbels.append(r)
                self.cfgTerms.append(CFGTerm(left, right))
        self.Items()

    def FirstForSingle(self, ALPHA): #单个字符的first集
        """
        求解单个字符的first集
        :param ALPHA:
        :return:
        """
        firstSet = set({})
        if ALPHA.islower():#小写的为终结符
            firstSet.add(ALPHA)
            return firstSet
        elif ALPHA.isupper():#大写的为非终结符
            for cfgterm in self.cfgTerms:
                if cfgterm.left()[0] == ALPHA and cfgterm.left()[0] != cfgterm.right()[0]: #跳过左递归
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

    def First(self,string_lst): #一个串的first集
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
    def Closure(self, term_set): #项目集闭包
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
                                    right_set.insert(0,".")
                                    newterm = Term([B], right_set,syb)
                                    if not newterm in SET:
                                        SET.add(newterm)
                                        self.terms.append(newterm)


            if len(TEMSET) != len(SET):
                TEMSET = SET.copy()
                add = True
        return SET

    def Goto(self, setI, X):
        """
        输入 项目集闭包，文法符号X
        输出 后继项目集闭包
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
        initTerm = Term(["SA"],[".","S"],"dollar")
        s.add(initTerm)
        initSet = self.Closure(s)
        self.cluster.append(initSet)
        add = True
        temcluster = self.cluster.copy()
        while add:
            add = False
            for I in temcluster:
                for X in self.Symbels:
                    goto = self.Goto(I,X)
                    if goto and not (goto in self.cluster):
                        self.cluster.append(goto)
            if len(temcluster) != len(self.cluster.copy()):
                temcluster = self.cluster.copy()
                add = True



    def LRtable(self):
        #todo 欧龙燊
        return None

    def ErrorHandle(self):
        # todo 王程
        pass



class SyntacticAnalyzer(object):

    def __init__(self):
        lst = LexicalAnalyzer.main()
        self.token_list = []
        for token in lst:
            if token.illegal == False:
                self.token_list.append(token) #从词法分析其中获取token list




if __name__ == "__main__":

    cfg = LRCFG("source/cfg_file.txt")
    #cfg_file暂定格式：cfg的每个符号用括号括起来，中间的大写代表非终结符，小写代表终结符

    # for t in cfg.Closure({Term(["SA"],[".","S"],"dollar")}):
    #     print(t)
    # print('------------------------------')
    # c = cfg.Closure({Term(["SA"],[".","S"],"dollar")})
    # for i in cfg.Goto(c,"mul"):
    #     print(i)


    cnt = 0
    for c in cfg.cluster:
        print(cnt, '-----------------------------------')
        cnt += 1
        for t in c:
            print(t)
