import time
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
    def shift_in(self, next_state, insymbol):
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
            time.sleep(1)
            for item in self.LRtable['goto'].keys():
                if self.state_stack[-1] in item:
                    si = self.state_stack[-1]
                    nonterminal_symbol = item[1]
                    flag = True
            if flag:  # 寻找到则跳出
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
        self.state_stack.append(
            int(self.LRtable['goto'][(self.state_stack[-1], self.symbol_stack[-1])]))
        return nonterminal_symbol, reduce_formula  # 返回A，用于丢弃输入符

    # LR分析表 格式：table{'action':{(i, a):sj}, 'goto':{(i, B): j} }
    def main(self):
        # 规约用的式子
        reduce_formula = []
        # 错误的式子
        wrong_reduce = []
        i = 0
        for token in self.tokenlist:
            print(token)
        while True:
            token = self.tokenlist[i]

            # 判断是否接受
            if token == 'dollar' and self.LRtable['action'][
                self.state_stack[-1], 'dollar'] == 'acc':
                print('源程序正确接受')
                break

            if token != 'dollar' and token.kind == 'CMT':  # 跳过注释
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
                reduce_formula.append(
                    attribute + ':' + token.value + ' (' + str(token.rownumber) + ')')
                i += 1
            # 规约
            elif next_operate[0] == 'r':
                reduce_number = int(next_operate[1:])
                self.reduce(reduce_number)
                self.state_stack.append(
                    int(self.LRtable['goto'][(self.state_stack[-1], self.symbol_stack[-1])]))
                reduce_formula.append(str(reduce_number))
            # 错误处理
            else:
                print('发生错误, 将使用恐慌模式处理！')
                nonterminal_symbol, reduce_formula = self.ErrorHandle(reduce_formula)  # 找到出错的规约式
                print(reduce_formula)

                # 找到A推导的产生式, 并用它规约
                for i in range(len(self.terms)):
                    if self.terms[i].left()[0] == nonterminal_symbol:
                        for right in self.terms[i].right():
                            reduce_formula.append(right + ' (' + str(token.rownumber) + ')')
                        reduce_formula.append(str(i))
                        # 记录错误，格式：Error at Line [token.rownumber]：错误规约：规约式
                        wrong_reduce.append('Error at Line [' + str(token.rownumber) + ']：错误规约：' +
                                            self.terms[i].left()[0] + '-->' + ' '.join(
                            self.terms[i].right()))
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
