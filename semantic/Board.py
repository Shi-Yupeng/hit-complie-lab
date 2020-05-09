import re


def main():
    pass


class SymbleTerm():  # syp 符号表中的一项
    # 暴露用户，应用时注意不能修改值
    def __init__(self, value, type_, offset):
        self.value = value  # 值
        self.type_ = type_  # 类型
        self.offset = offset  # 内存偏移量

    def __str__(self):
        ret = 'value: {:>10} | type: {:>30} | offset: {:>10}'.format(str(self.value), str(self.type_), str(self.offset))
        # ret = 'value: ' + str(self.value) + 'type: ' + str(self.type_) + 'offset: ' + str(self.offset)
        return ret


class Board:
    '''
    记录中间代码生成结果的类
    '''

    def __init__(self):
        self.line_cnt = 1  # 将会写入下一条中间代码的行的行号。从第一行开始写。
        self.content = {}  # 保存各行中间代码的内容
        # 格式：   行号:(操作符，运算分量1，运算分量2，结果变量)
        # 如果运算分量缺省，用'-'表示
        self.label_cnt = 1  # 生成的下一个标号的编号
        self.label_dic = {}  # 存放临时标号和行号的对应关系
        # 格式：   'Lb_1': 3, 'Lb_2': 17, ...
        self.temp_cnt = 0  # 下一个临时变量名下标
        self.offset = None  # syp 用于SDT设计时的临时变量
        self.t = None  # syp 用于SDT设计时的临时变量
        self.w = None  # syp 用于SDT设计时的临时变量
        self.Q = None  # syp 用于SDT设计时的临时变量
        self.symble_set = []  # syp符号表，中间数据是SymbleTerm类型
        self.wrong_list = [] # wc 错误列表
        self.string = None # 存放打印用字符串

    def enter(self, value, type_, offset):  # syp 在符号表中添加条目，并且添加到四元式代码中
        ST = SymbleTerm(value, type_, offset)
        self.symble_set.append(ST)
        sanyuanshi = 'enter({},{},{})'.format(value, str(type_), str(offset))
        self.append('enter', value, str(type_), str(offset),sanyuanshi)

    def show_result(self):
        '''
        输出中间代码生成结果
        '''
        for i in self.content:
            print(
                '{:3}: {:>10}, {:>25}, {:>25}, {:>20},      {}'.format(i, self.content[i][0], self.content[i][1],
                                                          self.content[i][2], self.content[i][3], self.content[i][4]))
        print('{:3}:'.format(self.line_cnt))

    def get_result(self):
        '''
        获得中间代码生成结果的字符串
        '''
        if self.string != None:
            return self.string
        else:
            self.string = ''
            for i in self.content:
                self.string += '{:>10}, {:>15}, {:>20}, {:>10}, {:>25}\n'.format(
                    self.content[i][0], self.content[i][1], self.content[i][2], self.content[i][3],
                    self.content[i][4])
            return self.string

    def get_table(self):
        '''
        获得表示符号表的自妇产
        '''
        ret = ''
        for i in self.symble_set:
            ret += str(i) + '\n'
        return ret

    def append(self, t1, t2, t3, t4, sanyuanshi):
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
        assert isinstance(sanyuanshi, str)

        self.content[self.line_cnt] = [t1, t2, t3, t4, sanyuanshi]
        self.line_cnt += 1

    def append_wrong(self, line_number, massage):
        '''
        添加报错
        :param line_number: 行号
        :param massage: 错误说明
        '''
        string = 'Error at Line [' + str(line_number) + ']：[' + str(massage) + ']'
        self.wrong_list.append(string)

    def show_wrong(self):
        '''
        输出错误记录
        '''
        for i in self.wrong_list:
            print(i)

    def get_wrong(self):
        return self.wrong_list

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
        self.string = None

    def new_temp(self):
        '''
        生成一个新标号  格式：t1, t2, t3, ...
        :return: 生成的新标号
        '''
        ret = 't' + str(self.temp_cnt)
        self.temp_cnt += 1
        return ret

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
            pat = '.*goto (Lb_\d+).*'
            m = re.match(pat, self.content[i][4])
            if m != None:
                lb = m.group(1)
                self.content[i][4] = self.content[i][4].replace(lb, str(self.label_dic[lb]))
            # if 'Lb' in self.content[i][4]:
            #     self.content[i][4] = self.content[i][4].replace('')


if __name__ == '__main__':
    main()
