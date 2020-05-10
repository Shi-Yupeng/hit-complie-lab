'''
该模块定义了递归产生中间代码的各个产生式的SDT
'''
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

    def gen(self, t1, t2, t3, t4, sanyuanshi):
        '''
        生成一条中间代码
        :param 操作符，运算分量1，运算分量2，结果变量
                要求都是字符串
        '''
        self.board.append(t1, t2, t3, t4, sanyuanshi)

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
        S1.symbel_set_name = S.symbel_set_name
        S2.symbel_set_name = S.symbel_set_name
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
        D1.symbel_set_name = D.symbel_set_name
        D2.symbel_set_name = D.symbel_set_name
        func1 = self.get_func(D1)
        func2 = self.get_func(D2)
        func1(D1)
        func2(D2)
        D.type = '(' + D1.type + ')' + 'x' + '(' + D2.type + ')'
        D.width = D1.width + D2.width
        D.addr = D1.addr
        D.recordaddr = D1.recordaddr

    def g5_D(self, D):  # syp
        assert len(D.child) == 6
        D1 = D.child[3]
        S = D.child[4]
        id = D.child[1]
        idname = D.symbel_set_name + id.val.split(':')[1]
        D.symbel_set_name = idname + '_'
        D1.symbel_set_name = D.symbel_set_name
        S.symbel_set_name = D.symbel_set_name
        funD1 = self.get_func(D1)
        funD1(D1)
        funS = self.get_func(S)
        funS(S)  # todo 衔接位置
        D.addr = D1.addr
        D.type = 'function'
        D.width = 1
        offset = self.board.offset
        D.recordaddr = offset
        find = False

        for t in self.board.symble_set:
            if t.value == idname:
                id.addr = t.offset
                find = True
                break
        if find:
            linenumber = id.line_num
            # print('Error at Line {} :函数变量重复声明{}'.format(str(linenumber),idname))
            self.board.append_wrong(str(linenumber), '函数变量重复声明: ' + idname)
        self.board.enter(idname, 'function', offset)
        self.board.offset += 1

    def g6_D(self, D):  # syp
        assert len(D.child) == 3
        T = D.child[0]
        T.symbel_set_name = D.symbel_set_name
        id = D.child[1]
        func = self.get_func(T)
        func(T)
        value = D.symbel_set_name + id.val.split(':')[1]
        type_ = T.type
        offset = self.board.offset
        if 'record' in str(type_):
            find = False
            for t in self.board.symble_set:
                if t.value == value:
                    id.addr = t.offset
                    find = True
                    break
            if find:
                linenumber = id.line_num
                # print('Error at Line {} :变量重复声明{}'.format(str(linenumber), value))
                self.board.append_wrong(str(linenumber), '变量重复声明: ' + value)

            self.board.enter(value, type_, T.recordaddr)
        else:
            find = False

            for t in self.board.symble_set:
                if t.value == value:
                    id.addr = t.offset
                    find = True
                    break
            if find:
                linenumber = id.line_num
                # print('Error at Line {} :变量重复声明{}'.format(str(linenumber), value))
                self.board.append_wrong(str(linenumber), '变量重复声明: ' + value)
            self.board.enter(value, type_, offset)
            self.board.offset += T.width
        D.recordaddr = offset

        D.type = value + 'X' + str(type_)  # 确定了d类型
        D.width = T.width
        D.addr = offset

    def g7_T(self, T):  # syp
        assert len(T.child) == 2
        X = T.child[0]
        X.symbel_set_name = T.symbel_set_name
        funcX = self.get_func(X)
        funcX(X)
        self.board.t = X.type
        self.board.w = X.width
        C = T.child[1]
        C.symbel_set_name = T.symbel_set_name
        funcC = self.get_func(C)
        funcC(C)
        T.type = C.type
        T.width = C.width

    def g8_T(self, T):  # syp
        assert len(T.child) == 3
        D = T.child[1]
        D.symbel_set_name = T.symbel_set_name
        funcD = self.get_func(D)
        funcD(D)
        T.type = 'record' + '' + '(' + D.type + ')'
        T.width = D.width
        T.recordaddr = D.recordaddr  # TODO

        # print(T.recordaddr)

    def g9_X(self, X):  # syp
        assert len(X.child) == 1
        int_ = X.child[0]
        X.type = int_.val
        X.width = 4

    def g10_X(self, X):  # syp
        assert len(X.child) == 1
        real = X.child[0]
        X.type = real.val
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
        E.symbel_set_name = S.symbel_set_name
        func = self.get_func(E)
        func(E)

        # lookup函数
        id = S.child[0]
        find = False
        idname = S.symbel_set_name + id.val.split(':')[1]
        for t in self.board.symble_set:
            if t.value == idname:
                id.addr = t.value
                find = True
                break
        if not find:
            # raise Exception('函数变量未声明', idname)
            # print('函数变量未声明')
            self.board.append_wrong(id.line_num, '变量' + idname + '未声明')
        self.board.append('=', E.addr, '-', idname, idname + ' = ' + E.addr)

    # S==>L=E; 数组
    def g14_S(self, S):
        L = S.child[0]
        L.symbel_set_name = S.symbel_set_name
        func = self.get_func(L)
        func(L)

        E = S.child[2]
        E.symbel_set_name = S.symbel_set_name
        func = self.get_func(E)
        func(E)

        self.board.append('[]=', E.addr, L.name, L.offset,
                          L.name + '[' + L.offset + ']' + ' = ' + E.addr)

    # L==>id[E] 数组
    def g15_L(self, L):
        E = L.child[2]
        E.symbel_set_name = L.symbel_set_name
        func = self.get_func(E)
        func(E)

        tid = L.child[0]
        idname = L.symbel_set_name + tid.val.split(':')[1]
        line_num = tid.line_num
        find = False
        for t in self.board.symble_set:
            if t.type_ != str and t.value == idname:
                id = t
                L.array = t.type_
                L.array_base = t.offset
                L.name = idname
                find = True
                break
        if not find:
            # raise Exception('函数变量未声明', idname)
            # print('函数变量未声明')
            self.board.append_wrong(tid.line_num, '变量' + idname + '未声明')
        # 数组下标为float
        if E.type != 'int':
            # raise Exception('数组下标不能引用浮点数', E.addr)
            # print('数组下标不能引用浮点数')
            self.board.append_wrong(E.line_num, '数组下标不能为浮点数: ' + str(E.addr))
        # 非数组元素使用下标
        if id.type_ == 'int' or id.type_ == 'real':
            L.type = id.type_
            L.addr = id.value
            self.board.append_wrong(line_num, '对非数组元素使用下标访问: ' + idname)
            return

        type = L.array
        while True:
            if type == 'int':
                L.width = 4
                break
            elif type == 'real':
                L.width = 8
                break
            if type.elem == 'int' or type.elem == 'real':
                L.type = type
            type = type.elem

        L.offset = self.board.new_temp()
        L.addr = id.value
        self.board.append('*', E.addr, str(L.width), L.offset,
                          L.offset + ' = ' + E.addr + ' * ' + str(L.width))

    # L==>L1[E] 数组
    def g16_L(self, L):
        L1 = L.child[0]
        L1.symbel_set_name = L.symbel_set_name
        func = self.get_func(L1)
        func(L1)

        E = L.child[2]
        E.symbel_set_name = L.symbel_set_name
        func = self.get_func(E)
        func(E)

        # 非数组元素使用下标
        if L1.type == 'int' or L1.type == 'real':
            # self.board.append_wrong(L1.line_num, '对非数组元素使用下标访问: ' + L1.addr)
            L.addr = L1.addr
            L.type = L1.type
            L.name = L1.name
            return
        # 找到L1类型的外层类型
        t = L1.array

        while True:
            if t.elem == L1.type:
                L.type = t
                break
            t = t.elem
        L.array = L1.array
        L.addr = L1.addr
        L.array_base = L1.array_base
        L.name = L1.name
        t = self.board.new_temp()
        if E.type != 'int':
            # raise Exception('数组下标不能引用浮点数', E.addr)
            self.board.append_wrong(E.line_num, '数组下标不能为浮点数: ' + str(E.addr))

        self.board.append('*', E.addr, str(L1.type.get_length()), t,
                          t + ' = ' + E.addr + ' * ' + str(L1.type.get_length()))
        L.offset = self.board.new_temp()
        self.board.append('+', L1.offset, t, L.offset, L.offset + ' = ' + L1.offset + ' + ' + t)

    # E==>E1+E2
    def g17_E(self, E):
        E1 = E.child[0]
        E1.symbel_set_name = E.symbel_set_name
        func = self.get_func(E1)
        func(E1)

        E2 = E.child[2]
        E2.symbel_set_name = E.symbel_set_name
        func = self.get_func(E2)
        func(E2)

        E.addr = self.board.new_temp()
        if E1.type == E2.type:
            E.type = E1.type
            self.board.append('+', E1.addr, E2.addr, E.addr,
                              E.addr + ' = ' + E1.addr + ' + ' + E2.addr)
        # 类型不匹配
        elif E2.type == 'real':
            E.type = E2.type
            u = self.board.new_temp()
            self.board.append_wrong(E.line_num,
                                    '类型不匹配: ' + str(E1.addr) + ':' + str(E1.type) + ' ' + str(
                                        E2.addr) + ':' + str(E2.type))
            self.board.append('inttoreal', E1.addr, '-', u, u + ' = ' + '(inttoreal)' + E1.addr)
            self.board.append('+', u, E2.addr, E.addr, E.addr + ' = ' + u + ' + ' + E2.addr)
        else:
            E.type = E1.type
            u = self.board.new_temp()
            self.board.append_wrong(E.line_num,
                                    '类型不匹配: ' + str(E1.addr) + ':' + str(E1.type) + ' ' + str(
                                        E2.addr) + ':' + str(E2.type))
            self.board.append('inttoreal', E2.addr, '-', u, u + ' = ' + '(inttoreal)' + E2.addr)
            self.board.append('+', E1.addr, u, E.addr, E.addr + ' = ' + E1.addr + ' + ' + u)

    # E==>E1*E2
    def g18_E(self, E):
        E1 = E.child[0]
        E1.symbel_set_name = E.symbel_set_name
        func = self.get_func(E1)
        func(E1)

        E2 = E.child[2]
        E2.symbel_set_name = E.symbel_set_name
        func = self.get_func(E2)
        func(E2)

        E.addr = self.board.new_temp()
        if E1.type == E2.type:
            E.type = E1.type
            self.board.append('*', E1.addr, E2.addr, E.addr,
                              E.addr + ' = ' + E1.addr + ' * ' + E2.addr)
        # 类型不匹配
        elif E2.type == 'real':
            E.type = E2.type
            u = self.board.new_temp()
            self.board.append_wrong(E.line_num,
                                    '类型不匹配: ' + str(E1.addr) + ':' + str(E1.type) + ' ' + str(
                                        E2.addr) + ':' + str(E2.type))
            self.board.append('inttoreal', E1.addr, '-', u, u + ' = ' + '(inttoreal)' + E1.addr)
            self.board.append('*', u, E2.addr, E.addr, E.addr + ' = ' + u + ' * ' + E2.addr)
        else:
            E.type = E1.type
            u = self.board.new_temp()
            self.board.append_wrong(E.line_num,
                                    '类型不匹配: ' + str(E1.addr) + ':' + str(E1.type) + ' ' + str(
                                        E2.addr) + ':' + str(E2.type))
            self.board.append('inttoreal', E2.addr, '-', u, u + ' = ' + '(inttoreal)' + E2.addr)
            self.board.append('*', E1.addr, u, E.addr, E.addr + ' = ' + E1.addr + ' * ' + u)

    # E==>E1-E2
    def g19_E(self, E):
        E1 = E.child[0]
        E1.symbel_set_name = E.symbel_set_name
        func = self.get_func(E1)
        func(E1)

        E2 = E.child[2]
        E2.symbel_set_name = E.symbel_set_name
        func = self.get_func(E2)
        func(E2)

        E.addr = self.board.new_temp()
        if E1.type == E2.type:
            E.type = E1.type
            self.board.append('-', E1.addr, E2.addr, E.addr,
                              E.addr + ' = ' + E1.addr + ' - ' + E2.addr)
        # 类型不匹配
        elif E2.type == 'real':
            E.type = E2.type
            u = self.board.new_temp()
            self.board.append_wrong(E.line_num,
                                    '类型不匹配: ' + str(E1.addr) + ':' + str(E1.type) + ' ' + str(
                                        E2.addr) + ':' + str(E2.type))
            self.board.append('inttoreal', E1.addr, '-', u, u + ' = ' + '(inttoreal)' + E1.addr)
            self.board.append('-', u, E2.addr, E.addr, E.addr + ' = ' + u + ' - ' + E2.addr)
        else:
            E.type = E1.type
            u = self.board.new_temp()
            self.board.append_wrong(E.line_num,
                                    '类型不匹配: ' + str(E1.addr) + ':' + str(E1.type) + ' ' + str(
                                        E2.addr) + ':' + str(E2.type))
            self.board.append('inttoreal', E2.addr, '-', u, u + ' = ' + '(inttoreal)' + E2.addr)
            self.board.append('-', E1.addr, u, E.addr, E.addr + ' = ' + E1.addr + ' - ' + u)

    # E==>-E1
    def g20_E(self, E):
        E1 = E.child[1]
        E1.symbel_set_name = E.symbel_set_name
        func = self.get_func(E1)
        func(E1)

        E.addr = self.board.new_temp()
        E.type = E1.type
        self.board.append('-', E1.addr, '-', E.addr, E.addr + ' = ' + '-' + E1.addr)

    # E==>(E1)
    def g21_E(self, E):
        E1 = E.child[1]
        E1.symbel_set_name = E.symbel_set_name
        func = self.get_func(E1)
        func(E1)
        E.addr = E1.addr
        E.type = E1.type

    # E==>id
    def g22_E(self, E):
        id = E.child[0]
        find = False
        idname = E.symbel_set_name + id.val.split(':')[1]
        E.name = idname
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
            # print('函数变量未声明')
            self.board.append_wrong(id.line_num, '变量' + idname + '未声明')

    # E==>digit
    def g23_E(self, E):
        digit = E.child[0]
        digit.type = 'int'
        E.addr = digit.val.split(':')[1]
        E.type = digit.type

    # E==>float
    def g24_E(self, E):
        float = E.child[0]
        float.type = 'real'
        E.addr = float.val.split(':')[1]
        E.type = float.type

    # E==>L 数组
    def g25_E(self, E):
        L = E.child[0]
        L.symbel_set_name = E.symbel_set_name
        func = self.get_func(L)
        func(L)

        E.addr = self.board.new_temp()
        type = L.type
        while True:
            if type == 'int' or type == 'real':
                E.type = type
                break
            type = type.elem
        # 对非数组元素使用下标
        if L.type == 'int' or L.type == 'real':
            # self.board.append_wrong(L.line_num, '对非数组元素使用下标访问: ' + L.addr)
            return
        self.board.append('=[]', L.name, L.offset, E.addr,
                          E.addr + ' = ' + L.name + '[' + L.offset + ']')

    def g26_S(self, S):
        # S -> if B then S endif
        assert len(S.child) == 5

        B = S.child[1]
        B.symbel_set_name = S.symbel_set_name
        B.inh['true'] = self.board.new_label()
        B.inh['false'] = S.inh['next']

        func = self.get_func(B)
        func(B)

        S1 = S.child[3]
        S1.symbel_set_name = S.symbel_set_name
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
        B.symbel_set_name = S.symbel_set_name
        S1.symbel_set_name = S.symbel_set_name
        S2.symbel_set_name = S.symbel_set_name
        B.inh['true'] = self.board.new_label()
        B.inh['false'] = self.board.new_label()

        func = self.get_func(B)
        func(B)

        self.board.label(B.inh['true'])
        S1.inh['next'] = S.inh['next']

        func = self.get_func(S1)
        func(S1)

        self.gen('goto', '-', '-', S.inh['next'], 'goto ' + S.inh['next'])
        self.board.label(B.inh['false'])
        S2.inh['next'] = S.inh['next']

        func = self.get_func(S2)
        func(S2)

    def g28_S(self, S):
        # S -> while B do S1 endwhile
        assert len(S.child) == 5
        B = S.child[1]
        S1 = S.child[3]
        B.symbel_set_name = S.symbel_set_name
        S1.symbel_set_name = S.symbel_set_name
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

        self.gen('goto', '-', '-', S.inh['begin'], 'goto ' + S.inh['begin'])

    def g29_B(self, B):
        # B -> B || B
        assert len(B.child) == 3

        B1 = B.child[0]
        B1.symbel_set_name = B.symbel_set_name
        B1.inh['true'] = B.inh['true']
        B1.inh['false'] = self.board.new_label()

        func = self.get_func(B1)
        func(B1)

        self.board.label(B1.inh['false'])
        B2 = B.child[2]
        B2.symbel_set_name = B.symbel_set_name
        B2.inh['true'] = B.inh['true']
        B2.inh['false'] = B.inh['false']

        func = self.get_func(B2)
        func(B2)

    def g30_B(self, B):
        # B -> B && B
        assert len(B.child) == 3

        B1 = B.child[0]
        B1.symbel_set_name = B.symbel_set_name
        B1.inh['true'] = self.board.new_label()
        B1.inh['false'] = B.inh['false']

        func = self.get_func(B1)
        func(B1)

        self.board.label(B1.inh['true'])
        B2 = B.child[2]
        B2.symbel_set_name = B.symbel_set_name
        B2.inh['true'] = B.inh['true']
        B2.inh['false'] = B.inh['false']

        func = self.get_func(B2)
        func(B2)

    def g31_B(self, B):
        # B -> ! B
        assert len(B.child) == 2

        B1 = B.child[1]
        B1.symbel_set_name = B.symbel_set_name
        B1.inh['true'] = B.inh['false']
        B1.inh['false'] = B.inh['true']

        func = self.get_func(B1)
        func(B1)

    def g32_B(self, B):
        # B -> ( B )
        assert len(B.child) == 3

        B1 = B.child[1]
        B1.symbel_set_name = B.symbel_set_name
        B1.inh['true'] = B.inh['true']
        B1.inh['false'] = B.inh['false']

        func = self.get_func(B1)
        func(B1)

    def g33_B(self, B):
        # B -> E RE E
        assert len(B.child) == 3
        E1 = B.child[0]
        E1.symbel_set_name = B.symbel_set_name
        RE = B.child[1]
        E2 = B.child[2]
        E2.symbel_set_name = B.symbel_set_name

        func = self.get_func(E1)
        func(E1)

        func = self.get_func(RE)
        func(RE)

        func = self.get_func(E2)
        func(E2)

        self.gen(RE.syn['relop'], E1.addr, E2.addr, B.inh['true'],
                 'if ' + E1.addr + ' ' + RE.syn['relop'] + ' ' + E2.addr + ', goto ' + B.inh[
                     'true'])
        self.gen('goto', '-', '-', B.inh['false'], 'goto ' + B.inh['false'])

    def g34_B(self, B):
        # B -> true
        assert len(B.child) == 1
        self.gen('goto', '-', '-', B.inh['true'], 'goto ' + B.inh['true'])

    def g35_B(self, B):
        # B -> false
        assert len(B.child) == 1
        self.gen('goto', '-', '-', B.inh['false'], 'goto ' + B.inh['false'])

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
        Elist.symbel_set_name = S.symbel_set_name
        funElist = self.get_func(Elist)
        funElist(Elist)
        cnt = 0
        if self.board.Q != None:
            for t in self.board.Q:
                cnt += 1
                sanyuanshi = 'param  {}'.format(str(t))
                self.board.append('param', str(t), '_', '_', sanyuanshi)
        find = False
        idname = S.symbel_set_name + id.val.split(':')[1]
        for t in self.board.symble_set:
            if t.value == idname:
                id.addr = t.offset
                find = True
                break
        if not find:
            # raise Exception('函数变量未声明', idname)
            # print('函数变量未声明')
            self.board.append_wrong(id.line_num, '函数变量' + idname + '未声明')
        elif t.type_ != 'function':
            # print('对非函数变量进行调用:{}'.format(idname))
            self.board.append_wrong(id.line_num, '对非函数变量进行调用: ' + idname)
        sanyuanshi = 'call {},{}'.format(idname, str(cnt))
        self.board.append('call', str(id.addr), str(cnt), '_', sanyuanshi)

    def g43_ELIST(self, ELISTf):  # syp
        assert len(ELISTf.child) == 3
        ELIST = ELISTf.child[0]
        ELIST.symbel_set_name = ELISTf.symbel_set_name
        E = ELISTf.child[2]
        E.symbel_set_name = ELISTf.symbel_set_name
        funELIST = self.get_func(ELIST)
        funELIST(ELIST)

        funE = self.get_func(E)
        funE(E)
        self.board.Q.append(E.addr)

    def g44_ELIST(self, ELIST):  # syp
        child_nodes = ELIST.child
        assert len(child_nodes) == 1
        E = child_nodes[0]
        E.symbel_set_name = ELIST.symbel_set_name
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
