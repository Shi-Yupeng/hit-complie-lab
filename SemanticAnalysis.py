from syntax.LRCFG import LRCFG
from syntax.LexicalUnit import Lexical_unit
from syntax.ParseTree import ParseTree
from syntax.ShiftReduce import ShiftReduce
from semantic.Board import Board


def main():
    analyzer = SemanticAnalysis()
    analyzer.event_get_CFGfile()
    analyzer.event_get_test_file()
    analyzer.get_parse_tree()

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
        self.root = None
        self.board = Board()

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


if __name__ == '__main__':
    main()