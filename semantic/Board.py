
def main():
    pass

class Board:
    '''
    记录中间代码生成结果的类
    '''
    def __init__(self):
        self.counter = 1 # 将会写入下一条中间代码的行的行号。从第一行开始写。
        self.content = {} # 保存各行中间代码的内容
                          # 格式：   行号:(操作符，运算分量1，运算分量2，结果变量)
                          # 如果运算分量缺省，用'-'表示

    def append(self, t1, t2, t3, t4):
        '''
        添加
        :param t1: 操作符
        :param t2: 运算分量1
        :param t3: 运算分量2
        :param t4: 结果变量
                    要求t1-t4都是字符串
        '''
        assert isinstance(t1, str)
        assert isinstance(t2, str)
        assert isinstance(t3, str)
        assert isinstance(t4, str)

        self.content[self.counter] = (t1, t2, t3, t4)

    def next_line_num(self):
        '''
        获取将会写入下一条中间代码的行的行号
        '''
        return self.counter

    def clear(self):
        '''
        清空之前存储的所有中间代码
        '''
        self.counter = 1
        self.clear()



if __name__ == '__main__':
    main()