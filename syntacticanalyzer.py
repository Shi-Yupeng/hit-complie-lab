# from token import Token
import re
from lexicalanalyzer import LexicalAnalyzer



class Term(object):

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
            hs += hash(st)
        for st in self.right:
            hs += hash(st)

        return hs


    def __str__(self):
        s = ""
        s = s + self.left[0] + " ==> "
        for r in self.right:
            s += (" " + r)
        s += ","
        s += self.lookahead
        return s
    def IsWaitingReduce(self):
        if self.right[0] == ".":
            return True
        else:
            return False
    def NextToDot(self):
        if self.right.index(".") < len(self.right) - 1:
            return self.right[self.right.index(".") + 1]
        else:
            return None

    def Beta(self):
        if self.right.index(".") < len(self.right) - 3:
            return self.right[self.right.index(".") + 2:]
        else:
            return []


class CFGTerm(object):
    def __init__(self, left, right):
        self.__left = left
        self.__right = right

    def left(self):
        return self.__left.copy()

    def right(self):
        return self.__right.copy()

class LRCFG(object):

    def __init__(self, cfg_file):
        self.terms = []
        self.cfgTerms = []
        dot = "."
        with open(cfg_file, "r") as f:
            lines = f.readlines()
            for line in lines:
                left = re.findall(r"\((.*?)\)", line.split("==>")[0])
                right = re.findall(r"\((.*?)\)", line.split("==>")[1])
                self.cfgTerms.append(CFGTerm(left, right))

    def FirstForSingle(self, ALPHA):
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

    def First(self,string_lst):
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
    def Closure(self, term_set):
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
                                    if not Term(B, right_set,syb) in SET:
                                        SET.add(Term(B, right_set,syb))


            if len(TEMSET) != len(SET):
                TEMSET = SET.copy()
                add = True
        return SET





class SyntacticAnalyzer(object):

    def __init__(self):
        lst = LexicalAnalyzer.main()
        self.token_list = []
        for token in lst:
            if token.illegal == False:
                self.token_list.append(token)


if __name__ == "__main__":
    cfg = LRCFG("cfg_file.txt")

    for t in cfg.Closure({Term(["SA"],[".","S"],"dollar")}):
        print(t)
