from syntax.LRCFG import LRCFG
from syntax.LexicalUnit import Lexical_unit
from syntax.ParseTree import ParseTree
from syntax.ShiftReduce import ShiftReduce
from semantic.Board import Board
from semantic.CodeGenerator import Generator


def main():
    analyzer = SemanticAnalysis()
    analyzer.event_get_CFGfile()
    analyzer.event_get_test_file()
    analyzer.get_parse_tree()
    analyzer.generate()

class SemanticAnalysis:
    '''
    语义分析+中间代码生成
    '''
    def __init__(self):
        # 语法分析器需要的变量
        self.CFGfile = None
        self.cfg = None
        self.LRtable = None
        self.cfgterms = None
        self.Testfile = None
        self.token_list = None

        # 语义分析器相关变量
        self.root = None # 分析树的根节点
        self.board = Board() # 保存生成的中间代码
        self.generator = Generator(self.board)

    def generate(self):
        '''
        生成中间代码，保存在self.board中
        '''
        func = self.get_func(self.root)
        func(self.root.child)
        self.board.label_scan()
        print('中间代码生成完成！')

    def get_parse_tree(self):
        '''
        使用LR(1)语法分析技术构造分析树
        '''
        input, wrong_reduce = ShiftReduce(self.cfgterms, self.cfg.cluster, self.LRtable,
                                          self.token_list).main()
        root = ParseTree.create_tree(input, self.cfgterms)
        pre_str = root.pre_order_str(root, 0)
        print(pre_str)
        self.root = root

    def event_get_CFGfile(self):
        '''
        读CFG文件，生成cfg项、LR表、LR项集族
        '''
        self.CFGfile = 'source/syntax/cfg/cfg_file_full.txt'
        self.cfg = LRCFG(self.CFGfile)
        self.LRtable = self.cfg.table
        self.cfgterms = self.cfg.cfgTerms

    def event_get_test_file(self):
        '''
        读测试文件，生成TOKEN列表
        '''
        self.Testfile = 'source/semantic/test/bool.txt'
        self.token_list = Lexical_unit(self.Testfile).getTokenList()

    def get_func(self, node):
        '''
        获取一个节点对应的SDT函数
        :param: node 节点
        :return: node对应SDT的函数
        '''
        func_name = 'g' + str(node.cfg_index) + '_' + node.val
        func = getattr(self.generator, func_name)
        return func

if __name__ == '__main__':
    main()