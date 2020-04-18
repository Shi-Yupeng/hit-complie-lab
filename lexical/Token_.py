unique = ['if', 'else', 'do', 'while', 'printf',
          'real', "int", 'switch', 'case', 'default',
          'for', 'endrecord', 'return', 'def', 'enddef',
          'char', 'call', 'record', 'then', 'endif',
          'endwhile', 'true', 'false']


class Token(object):
    def __init__(self, string, kindline, rownumber):
        self.rownumber = rownumber
        self.string = string
        self.kind = "illegal"
        self.value = None
        self.illegal = False
        self.attribute = None
        if kindline == None:
            self.illegal = True
            self.attribute = "_"
        else:
            self.kind = kindline.split(":")[1]
            self.value = string
            if kindline.split(":")[2] == "False":  # 代表属性非关键字
                self.attribute = self.value

            else:
                self.attribute = kindline.split(":")[2]
        if string in unique:
            self.kind = str(self.string).upper()
            self.attribute = self.kind.lower()

    def __str__(self):
        if self.value is None:
            return "{:15}".format(self.string) + \
                   "<" + "{:15}".format(self.kind) + \
                   "," + "{:15}".format("_") + "{:15}".format(self.attribute) + ">" + self.error()
        if not self.value is None:
            t = self.value
            s = "{:15}".format(self.string)
            if self.kind == "CMT":
                if len(self.value) > 8:
                    t = self.value[:3] + "..." + self.value[-3:]
                s = self.string + '\n' + "{:15}".format('')
            return s + \
                   "<" + "{:15}".format(self.kind) + \
                   "," + "{:15}".format(t) + "{:15}".format(self.attribute) + ">" + self.error()

    def error(self):
        if self.illegal == True:
            return "illegal string at row " + str(self.rownumber) + ":" + self.string
        else:
            return ""
