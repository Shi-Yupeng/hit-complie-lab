import re

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

class ParseTree:
    def __init__(self, val, child_list, line_num):
        '''
        构造方法
        :param child_list: 装着子节点的列表。规定子节点排序从左向右。
                    如果没有子节点，那么child_list应该等于[]
        '''
        self.val = val
        self.child = child_list
        self.line_num = line_num
        self.str = ''

    def __str__(self):
        return self.val

    @staticmethod
    def create_tree(input, cfg_list):
        '''
        构建语法分析树
        :param input: 读入的终结符和使用的各个产生式的标号
        :param cfg_list: 文法产生式列表
        :return: 语法分析树根节点
        '''
        ans = []
        for i in input:
            if not i.isdigit():
                tmp = i.strip().split(' ')
                line_num = int(tmp[1].replace('(', '').replace(')', ''))
                t = ParseTree(tmp[0], [], line_num)
                ans.append(t)
            else:
                cfg_index = int(i)
                cfg = cfg_list[cfg_index]
                child_num = len(cfg.right())
                child = []
                for i in cfg.right():
                    if i == 'epsilon':
                        t1 = ParseTree('epsilon', [], -1)
                        child.insert(0, t1)
                    else:
                        child.insert(0, ans.pop())
                line_num = -1
                for i in child:
                    if i.line_num > line_num:
                        line_num = i.line_num
                        break
                t = ParseTree(cfg.left()[0], child, line_num)
                ans.append(t)

        assert len(ans) == 1
        root = ans[0]
        return root

    def __pre_order(self, node, depth):
        '''
        ParseTree先根遍历，内部方法
        :param node: 子树的根节点
        :param depth: 该节点的深度 规定根节点深度为0
        '''
        for i in range(depth):
            self.str += '\t'
        self.str += node.val + ' (' + str(node.line_num) + ')' + '\n'
        for i in node.child:
            self.__pre_order(i, depth + 1)

    def pre_order_str(self, node, depth):
        '''
        ParseTree先根遍历
        :param node:
        :param depth:
        :return: ParseTree先根遍历对应字符串
        '''
        if self.str != '':
            return self.str
        else:
            self.__pre_order(node, depth)
            return self.str


l = []
terminals = set()
nonterminals = set()



def main():
    # 输入是读入的终结符和使用的各个产生式的标号
    # 输出是语法分析树
    cfg_list = []
    global terminals, nonterminals
    # with open('ParseTreeTest.txt', 'r') as f:
    #     lines = f.readlines()
    #     for line in lines:
    #         line = line.strip().split('\t')[1]
    #         tmp = line.split(' -> ')
    with open('ParseTreeTest.txt', "r") as f:
        lines = f.readlines()
        for line in lines:
            left = re.findall(r"\((.*?)\)", line.split("==>")[0])  # CFG条目左部，字符列表
            right = re.findall(r"\((.*?)\)", line.split("==>")[1])  # CFG条目右部，字符列表
            for l in left:
                nonterminals.add(l)
            for r in right:
                if r.islower():
                    terminals.add(r)
                elif r.isupper():
                    nonterminals.add(r)
                else:
                    raise Exception('大写字母和小写字母混用，无法判别符号类型')
            cfg_list.append(CFGTerm(left, right))
    pass

    input = [
        'proc (1)', 'id:inc (1)', 'sc (1)', 'int (2)', '6',
        '7', '5', 'id:i (2)', 'sc (2)', '3',
        'id:i (3)', 'eq (3)', 'id:i (3)', '9', 'add (3)',
        'digit:1 (3)', '10', '8', 'sc (3)', '4',
        '2', '1'
    ]

    root = ParseTree.create_tree(input, cfg_list)
    pre_str = root.pre_order_str(root, 0)
    print(pre_str)


if __name__ == '__main__':
    main()