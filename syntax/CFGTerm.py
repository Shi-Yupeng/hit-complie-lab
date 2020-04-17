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

    def __str__(self):
        s = ""
        s = s + self.__left[0] + " ==> "
        for r in self.__right:
            s += (" " + r)
        return s