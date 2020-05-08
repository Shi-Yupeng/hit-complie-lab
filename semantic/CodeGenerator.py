'''
该模块定义了递归产生中间代码的各个产生式的SDT
'''
from lexical import Token_
from .array_ import Array


def main():
    pass


class Generator:
    def __init__(self, board):
        self.board = board  # 记录中间代码生成结果

    def get_func(self, node):
        '''
        获取一个节点对应的SDT函数
        :param: node 节点
        :return: node对应SDT的函数
        '''
        func_name = 'g' + str(node.cfg_index) + '_' + node.val
        func = getattr(self, func_name)
        return func

    def gen(self, t1, t2, t3, t4):
        '''
        生成一条中间代码
        :param 操作符，运算分量1，运算分量2，结果变量
                要求都是字符串
        '''
        self.board.append(t1, t2, t3, t4)

    def g0_SA(self, SA):
        pass

    def g1_P(self, P):
        assert len(P.child) == 1
        D = P.child[0]

        self.board.offset = 0

        func = self.get_func(D)
        func(D)

    def g2_P(self, P):
        assert len(P.child) == 1

        S = P.child[0]
        S.inh['next'] = self.board.new_label()

        func = self.get_func(S)
        func(S)

        self.board.label(S.inh['next'])

    def g3_S(self, S):
        # S==>S1 S2
        assert len(S.child) == 2
        S1 = S.child[0]
        S2 = S.child[1]

        S1.inh['next'] = self.board.new_label()

        func1 = self.get_func(S1)
        func1(S1)

        self.board.label(S1.inh['next'])
        S2.inh['next'] = S.inh['next']

        func2 = self.get_func(S2)
        func2(S2)

    def g4_D(self, D):  # syp
        assert len(D.child) == 2
        D1 = D.child[0]
        D2 = D.child[1]
        func1 = self.get_func(D1)
        func2 = self.get_func(D2)
        func1(D1)
        func2(D2)
        D.type = '(' + D1.type + ')' + 'x' + '(' + D2.type + ')'
        D.width = D1.width + D2.width
        D.addr = D1.addr

    def g5_D(self, D):  # syp
        assert len(D.child) == 6
        D1 = D.child[3]
        S = D.child[4]
        id = D.child[1]
        idname = id.val.split(':')[1]
        funD1 = self.get_func(D1)
        funD1(D1)
        funS = self.get_func(S)
        funS(S)  # todo 衔接位置
        D.addr = D1.addr
        D.type = 'function'
        D.width = 1
        offset = self.board.offset
        self.board.enter(idname, 'function', offset)
        self.board.offset += 1

    def g6_D(self, D):  # syp
        assert len(D.child) == 3
        T = D.child[0]
        id = D.child[1]
        func = self.get_func(T)
        func(T)
        value = id.val.split(':')[1]
        type_ = T.type
        offset = self.board.offset

        self.board.enter(value, type_, offset)
        self.board.offset += T.width
        D.type = value + 'X' + str(type_)  # 确定了d类型
        D.width = T.width
        D.addr = offset

    def g7_T(self, T):  # syp
        assert len(T.child) == 2
        X = T.child[0]
        funcX = self.get_func(X)
        funcX(X)
        self.board.t = X.type
        self.board.w = X.width
        C = T.child[1]
        funcC = self.get_func(C)
        funcC(C)
        T.type = C.type
        T.width = C.width

    def g8_T(self, T):  # syp
        assert len(T.child) == 3
        D = T.child[1]
        funcD = self.get_func(D)
        funcD(D)
        T.type = 'record' + '' + '(' + D.type + ')'
        T.width = D.width

    def g9_X(self, X):  # syp
        assert len(X.child) == 1
        int_ = X.child[0]
        X.type = int_.val
        X.width = 4

    def g10_X(self, X):  # syp
        assert len(X.child) == 1
        real = X.child[0]
        X.type = real
        X.width = 8

    def g11_C(self, C):  # syp
        assert len(C.child) == 4
        digit = C.child[1]
        value = int(digit.val.split(':')[1])
        C1 = C.child[3]
        funcC1 = self.get_func(C1)
        funcC1(C1)
        C.type = Array(value, C1.type)
        C.width = value * C1.width

    def g12_C(self, C):  # syp
        assert len(C.child) == 0
        C.width = self.board.w
        C.type = self.board.t

    # S==>id=E;
    def g13_S(self, S):
        E = S.child[2]
        func = self.get_func(E)
        func(E)

        # lookup函数
        id = S.child[0]
        find = False
        idname = id.val.split(':')[1]
        for t in self.board.symble_set:
            if t.value == idname:
                id.addr = t.value
                find = True
                break
        if not find:
            # raise Exception('函数变量未声明', idname)
            print('函数变量未声明')
        self.board.append('=', E.addr, '-', idname)

    # S==>L=E; 数组
    def g14_S(self, S):
        L = S.child[0]
        func = self.get_func(L)
        func(L)

        E = S.child[2]
        func = self.get_func(E)
        func(E)

        self.board.append('[]=', E.addr, str(L.array_base), L.offset)

    # L==>id[E] 数组
    def g15_L(self, L):
        E = L.child[2]
        func = self.get_func(E)
        func(E)

        id = L.child[0]
        idname = id.val.split(':')[1]
        find = False
        for t in self.board.symble_set:
            if t.type_ != str and t.value == idname:
                L.array = t.type_
                L.array_base = t.offset
                find = True
                break
        if not find:
            # raise Exception('函数变量未声明', idname)
            print('函数变量未声明')
        if E.type != 'int':
            # raise Exception('数组下标不能引用浮点数', E.addr)
            print('数组下标不能引用浮点数')
        L.type = L.array.elem

        if L.array.elem == 'int':
            L.width = 4
        elif L.array.elem == 'real':
            L.width = 8
        L.offset = self.board.new_temp()
        self.board.append('*', E.addr, str(L.width), L.offset)

    # L==>L1[E] 数组
    def g16_L(self, L):
        L1 = L.child[0]
        func = self.get_func(L1)
        func(L1)

        E = L.child[2]
        func = self.get_func(E)
        func(E)
        L.type = L1.type.elem
        L.array = L1.array
        L.array_base = L1.array_base
        t = self.board.new_temp()
        if E.type != 'int':
            # raise Exception('数组下标不能引用浮点数', E.addr)
            print('数组下标不能引用浮点数')
        self.board.append('*', E.addr, str(L.array.elem.get_length()), t)
        L.offset = self.board.new_temp()
        self.board.append('+', L1.offset, t, L.offset)

    # E==>E1+E2
    def g17_E(self, E):
        E1 = E.child[0]
        func = self.get_func(E1)
        func(E1)

        E2 = E.child[2]
        func = self.get_func(E2)
        func(E2)

        E.addr = self.board.new_temp()
        if E1.type == E2.type:
            E.type = E1.type
            self.board.append('+', E1.addr, E2.addr, E.addr)
        # 类型不匹配
        elif E2.type == 'real':
            E.type = E2.type
            u = self.board.new_temp()
            self.board.append('inttoreal', E1.addr, '-', u)
            self.board.append('+', u, E2.addr, E.addr)
        else:
            E.type = E1.type
            u = self.board.new_temp()
            self.board.append('inttoreal', E2.addr, '-', u)
            self.board.append('+', E1.addr, u, E.addr)

    # E==>E1*E2
    def g18_E(self, E):
        E1 = E.child[0]
        func = self.get_func(E1)
        func(E1)

        E2 = E.child[2]
        func = self.get_func(E2)
        func(E2)

        E.addr = self.board.new_temp()
        if E1.type == E2.type:
            E.type = E1.type
            self.board.append('*', E1.addr, E2.addr, E.addr)
        # 类型不匹配
        elif E2.type == 'real':
            E.type = E2.type
            u = self.board.new_temp()
            self.board.append('inttoreal', E1.addr, '-', u)
            self.board.append('*', u, E2.addr, E.addr)
        else:
            E.type = E1.type
            u = self.board.new_temp()
            self.board.append('inttoreal', E2.addr, '-', u)
            self.board.append('*', E1.addr, u, E.addr)

    # E==>E1-E2
    def g19_E(self, E):
        E1 = E.child[0]
        func = self.get_func(E1)
        func(E1)

        E2 = E.child[2]
        func = self.get_func(E2)
        func(E2)

        E.addr = self.board.new_temp()
        if E1.type == E2.type:
            E.type = E1.type
            self.board.append('-', E1.addr, E2.addr, E.addr)
        # 类型不匹配
        elif E2.type == 'real':
            E.type = E2.type
            u = self.board.new_temp()
            self.board.append('inttoreal', E1.addr, '-', u)
            self.board.append('-', u, E2.addr, E.addr)
        else:
            E.type = E1.type
            u = self.board.new_temp()
            self.board.append('inttoreal', E2.addr, '-', u)
            self.board.append('-', E1.addr, u, E.addr)

    # E==>-E1
    def g20_E(self, E):
        E1 = E.child[1]
        func = self.get_func(E1)
        func(E1)

        E.addr = self.board.new_temp()
        E.type = E1.type
        self.board.append('-', E1.addr, '-', E.addr)

    # E==>(E1)
    def g21_E(self, E):
        E1 = E.child[1]
        func = self.get_func(E1)
        func(E1)
        E.addr = E1.addr
        E.type = E1.type

    # E==>id
    def g22_E(self, E):
        id = E.child[0]
        find = False
        idname = id.val.split(':')[1]
        for t in self.board.symble_set:
            if t.value == idname:
                id.addr = t.value
                find = True
                E.addr = t.value
                E.type = t.type_
                break
        if not find:
            E.addr = 'unkonwn'
            E.type = 'unkonwn'
            # raise Exception('函数变量未声明', idname)
            print('函数变量未声明')

    # E==>digit
    def g23_E(self, E):
        digit = E.child[0]
        E.addr = digit.val.split(':')[1]
        E.type = digit.type

    # E==>float
    def g24_E(self, E):
        float = E.child[0]
        E.addr = float.val.split(':')[1]
        E.type = float.type

    # E==>L 数组
    def g25_E(self, E):
        L = E.child[0]
        func = self.get_func(L)
        func(L)

        E.addr = self.board.new_temp()
        self.board.append('=[]', str(L.array_base), L.offset, E.addr)

    def g26_S(self, S):
        # S -> if B then S endif
        assert len(S.child) == 5

        B = S.child[1]
        B.inh['true'] = self.board.new_label()
        B.inh['false'] = S.inh['next']

        func = self.get_func(B)
        func(B)

        S1 = S.child[3]
        self.board.label(B.inh['true'])
        S1.inh['next'] = S.inh['next']

        func = self.get_func(S1)
        func(S1)

    def g27_S(self, S):
        # S -> if B then S1 else S2 endif
        assert len(S.child) == 7
        B = S.child[1]
        S1 = S.child[3]
        S2 = S.child[5]

        B.inh['true'] = self.board.new_label()
        B.inh['false'] = self.board.new_label()

        func = self.get_func(B)
        func(B)

        self.board.label(B.inh['true'])
        S1.inh['next'] = S.inh['next']

        func = self.get_func(S1)
        func(S1)

        self.gen('goto', '-', '-', S.inh['next'])
        self.board.label(B.inh['false'])
        S2.inh['next'] = S.inh['next']

        func = self.get_func(S2)
        func(S2)

    def g28_S(self, S):
        # S -> while B do S1 endwhile
        assert len(S.child) == 5
        B = S.child[1]
        S1 = S.child[3]

        S.inh['begin'] = self.board.new_label()
        self.board.label(S.inh['begin'])
        B.inh['true'] = self.board.new_label()
        B.inh['false'] = S.inh['next']

        func = self.get_func(B)
        func(B)

        self.board.label(B.inh['true'])
        S1.inh['next'] = S.inh['begin']

        func = self.get_func(S1)
        func(S1)

        self.gen('goto', '-', '-', S.inh['begin'])

    def g29_B(self, B):
        # B -> B || B
        assert len(B.child) == 3

        B1 = B.child[0]
        B1.inh['true'] = B.inh['true']
        B1.inh['false'] = self.board.new_label()

        func = self.get_func(B1)
        func(B1)

        self.board.label(B1.inh['false'])
        B2 = B.child[2]
        B2.inh['true'] = B.inh['true']
        B2.inh['false'] = B.inh['false']

        func = self.get_func(B2)
        func(B2)

    def g30_B(self, B):
        # B -> B && B
        assert len(B.child) == 3

        B1 = B.child[0]
        B1.inh['true'] = self.board.new_label()
        B1.inh['false'] = B.inh['false']

        func = self.get_func(B1)
        func(B1)

        self.board.label(B1.inh['true'])
        B2 = B.child[2]
        B2.inh['true'] = B.inh['true']
        B2.inh['false'] = B.inh['false']

        func = self.get_func(B2)
        func(B2)

    def g31_B(self, B):
        # B -> ! B
        assert len(B.child) == 2

        B1 = B.child[1]
        B1.inh['true'] = B.inh['false']
        B1.inh['false'] = B.inh['true']

        func = self.get_func(B1)
        func(B1)

    def g32_B(self, B):
        # B -> ( B )
        assert len(B.child) == 3

        B1 = B.child[1]
        B1.inh['true'] = B.inh['true']
        B1.inh['false'] = B.inh['false']

        func = self.get_func(B1)
        func(B1)

    def g33_B(self, B):
        # B -> E RE E
        assert len(B.child) == 3
        E1 = B.child[0]
        RE = B.child[1]
        E2 = B.child[2]

        func = self.get_func(E1)
        func(E1)

        func = self.get_func(RE)
        func(RE)

        func = self.get_func(E2)
        func(E2)

        self.gen(RE.syn['relop'], E1.addr, E2.addr, B.inh['true'])
        self.gen('goto', '-', '-', B.inh['false'])

    def g34_B(self, B):
        # B -> true
        assert len(B.child) == 1
        self.gen('goto', '-', '-', B.inh['true'])

    def g35_B(self, B):
        # B -> false
        assert len(B.child) == 1
        self.gen('goto', '-', '-', B.inh['false'])

    def g36_RE(self, RE):
        # RE -> <
        assert len(RE.child) == 1
        RE.syn['relop'] = RE.child[0].val

    def g37_RE(self, RE):
        # RE -> <=
        assert len(RE.child) == 1
        RE.syn['relop'] = RE.child[0].val

    def g38_RE(self, RE):
        # RE -> ==
        assert len(RE.child) == 1
        RE.syn['relop'] = RE.child[0].val

    def g39_RE(self, RE):
        # RE -> !=
        assert len(RE.child) == 1
        RE.syn['relop'] = RE.child[0].val

    def g40_RE(self, RE):
        # RE -> >
        assert len(RE.child) == 1
        RE.syn['relop'] = RE.child[0].val

    def g41_RE(self, RE):
        # RE -> >=
        assert len(RE.child) == 1
        RE.syn['relop'] = RE.child[0].val

    def g42_S(self, S):  # syp
        assert len(S.child) == 6
        id = S.child[1]
        Elist = S.child[3]
        funElist = self.get_func(Elist)
        funElist(Elist)
        cnt = 0
        if self.board.Q != None:
            for t in self.board.Q:
                cnt += 1
                self.board.append('param', str(t), '_', '_')
        find = False
        idname = id.val.split(':')[1]
        for t in self.board.symble_set:
            if t.value == idname:
                id.addr = t.offset
                find = True
                break
        if not find:
            # raise Exception('函数变量未声明', idname)
            print('函数变量未声明')
        self.board.append('call', str(id.addr), str(cnt), '_')

    def g43_ELIST(self, ELIST):  # syp
        assert len(ELIST.child) == 3
        ELIST = ELIST.child[0]
        E = ELIST.child[2]

        funELIST = self.get_func(ELIST)
        funELIST(ELIST)

        funE = self.get_func(E)
        funE(E)
        self.board.Q.append(E.addr)

    def g44_ELIST(self, ELIST):  # syp
        child_nodes = ELIST.child
        assert len(child_nodes) == 1
        E = child_nodes[0]
        funE = self.get_func(E)
        funE(E)  # TODO 衔接位置
        self.board.Q = [E.addr]

    def g45_ELIST(self, ELIST):  # syp
        pass

    def g46_P(self, P):  # syp
        # P -> D S
        assert len(P.child) == 2
        D = P.child[0]
        S = P.child[1]

        self.board.offset = 0

        funcD = self.get_func(D)
        funcD(D)

        S.inh['next'] = self.board.new_label()

        funcS = self.get_func(S)
        funcS(S)

        self.board.label(S.inh['next'])


if __name__ == '__main__':
    main()
