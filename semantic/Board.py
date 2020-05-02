
def main():
    pass

class Board:
    '''
    记录中间代码生成结果的类
    '''
    def __init__(self):
        self.line_cnt = 1 # 将会写入下一条中间代码的行的行号。从第一行开始写。
        self.content = {} # 保存各行中间代码的内容
                          # 格式：   行号:(操作符，运算分量1，运算分量2，结果变量)
                          # 如果运算分量缺省，用'-'表示
        self.label_cnt = 1 # 生成的下一个标号的编号
        self.label_dic = {} # 存放临时标号和行号的对应关系
                            # 格式：   'Lb_1': 3, 'Lb_2': 17, ...

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

        self.content[self.line_cnt] = [t1, t2, t3, t4]
        self.line_cnt += 1

    def next_line_num(self):
        '''
        获取将会写入下一条中间代码的行的行号
        '''
        return self.line_cnt

    def clear(self):
        '''
        清空之前存储的所有中间代码
        '''
        self.line_cnt = 1
        self.content.clear()
        self.label_cnt = 1
        self.label_dic.clear()


    def new_label(self):
        '''
        生成一个新标号  格式：Lb_1, Lb_2, Lb_3, ...
        :return: 生成的新标号
        '''
        ret = 'Lb_' + str(self.label_cnt)
        self.label_cnt += 1
        return ret

    def label(self, label):
        '''
        用下一行的行号来标记标号label，将对应关系放入self.label_dic
        '''
        self.label_dic[label] = self.line_cnt

    def label_scan(self):
        '''
        使用label和行号的对应关系，扫描中间代码，进行替换
        '''
        for i in self.content:
            if 'Lb' in self.content[i][3]:
                self.content[i][3] = self.label_dic[self.content[i][3]]


if __name__ == '__main__':
    main()