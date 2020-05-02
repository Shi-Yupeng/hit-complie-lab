'''
该模块定义了递归产生中间代码的各个产生式的SDT
'''
def main():
    pass

class Generator:
    def __init__(self, board):
        self.board = board # 记录中间代码生成结果

    def get_func_name(self, node):
        '''
        获取一个节点对应的SDT函数
        :param: node 节点
        :return: node对应SDT的函数
        '''
        func_name = 'g' + str(node.cfg_index) + '_' + node.val
        func = getattr(self, func_name)
        return func

    def g0_SA(self):
        print('rua!')
        pass

    def g1_P(self):
        pass

    def g2_P(self, child):
        print('执行g2_P')
        assert len(child) == 1
        print('rua')

        S_next = self.board.new_label()
        next_node = child[0]
        func = self.get_func_name(next_node)
        func(S_next)
        self.board.label(S_next)

        pass

    def g3_S(self):
        pass

    def g4_D(self):
        pass

    def g5_D(self):
        pass

    def g6_D(self):
        pass

    def g7_T(self):
        pass

    def g8_T(self):
        pass

    def g9_X(self):
        pass

    def g10_X(self):
        pass

    def g11_C(self):
        pass

    def g12_C(self):
        pass

    def g13_S(self):
        pass

    def g14_S(self):
        pass

    def g15_L(self):
        pass

    def g16_L(self):
        pass

    def g17_E(self):
        pass

    def g18_E(self):
        pass

    def g19_E(self):
        pass

    def g20_E(self):
        pass

    def g21_E(self):
        pass

    def g22_E(self):
        pass

    def g23_E(self):
        pass

    def g24_E(self):
        pass

    def g25_E(self):
        pass

    def g26_S(self, S_next):
        print('jump suc')
        self.board.append('goto', '-', '-', '2')
        self.board.append('goto', '-', '-', S_next)
        pass

    def g27_S(self):
        pass

    def g28_S(self):
        pass

    def g29_B(self):
        pass

    def g30_B(self):
        pass

    def g31_B(self):
        pass

    def g32_B(self):
        pass

    def g33_B(self):
        pass

    def g34_B(self):
        pass

    def g35_B(self):
        pass

    def g36_RE(self):
        pass

    def g37_RE(self):
        pass

    def g38_RE(self):
        pass

    def g39_RE(self):
        pass

    def g40_RE(self):
        pass

    def g41_RE(self):
        pass

    def g42_S(self):
        pass

    def g43_ELIST(self):
        pass

    def g44_ELIST(self):
        pass

    def g45_ELIST(self):
        pass



if __name__ == '__main__':
    main()
