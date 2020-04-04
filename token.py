

unique = ['if','else','do','while','printf']
class Token(object):
    def __init__(self,string, kindline,rownumber):
        self.rownumber = rownumber
        self.string = string
        self.kind = "illegal"
        self.value = None
        self.illegal = False
        if kindline == None:
            self.illegal = True
        else:
            self.kind = kindline.split(":")[1]
            if kindline.split(":")[2] == "False": #代表属性非关键字
                self.value = string
        if string in unique:
            self.kind = str(self.string).upper()
    def __str__(self):
        if self.value is None:
            return "{:20}".format(self.string) + \
                   "<" + "{:20}".format(self.kind) + \
                   "," + "{:20}".format("_") + ">" + self.error()
        if not self.value is None:
            return "{:20}".format(self.string) + \
                   "<" + "{:20}".format(self.kind) + \
                   "," + "{:20}".format(self.value) + ">" + self.error()
    def error(self):
        if self.illegal == True:
            return "illegal string at row " + str(self.rownumber) + ":" + self.string
        else:
            return ""
