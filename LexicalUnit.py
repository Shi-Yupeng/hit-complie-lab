from lexicalanalyzer import LexicalAnalyzer

# 获取词法单元
class Lexical_unit(object):
    def __init__(self, Testfile):
        with open(Testfile, 'r', encoding='utf8') as f:
            string = f.read()
        lst = LexicalAnalyzer.main('source/FA_INPUT.csv', string)
        self.token_list = []
        for token in lst:
            if token.illegal == False:
                self.token_list.append(token)  # 从词法分析其中获取token list
        self.token_list.append('dollar') # 末尾添加$符

    def getTokenList(self):
        return self.token_list