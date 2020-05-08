#syp array 类型表达式，递归创建type
class Array:
    def __init__(self, number, type):
        self.number = number
        self.elem = type
    def __str__(self):
        return 'array' + '('+str(self.number)+',' + str(self.elem) + ')'

    def get_length(self):
        if self.elem == 'int':
            return 4 * self.number
        elif self.elem == 'real':
            return 8 * self.number
        return self.number * self.elem.get_length()