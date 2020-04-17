class Term(object):
    """
    LR(1)产生式条目类，包括产生式左部，以及展望符
    """

    def __init__(self, left, right, lookahead):
        self.left = left
        self.right = right
        self.lookahead = lookahead

    def __eq__(self, other):
        if other == None:
            return False
        if len(self.left) != len(other.left) or len(self.right) != len(other.right):
            return False
        for i in range(len(self.left)):
            if self.left[i] != other.left[i]:
                return False
        for i in range(len(self.right)):
            if self.right[i] != other.right[i]:
                return False
        if self.lookahead != other.lookahead:
            return False
        return True

    def __hash__(self):
        hs = hash(self.lookahead)
        for st in self.left:
            hs += (hash(st) + hash(st))
        for st in self.right:
            hs += (hash(st) + hash(st) + hash(st))

        return hs

    def __str__(self):
        s = ""
        s = s + self.left[0] + " ==> "
        for r in self.right:
            s += (" " + r)
        s += ","
        s += self.lookahead
        return s

    def IsWaitingReduce(self):  # 判断是否是待约状态
        if self.right[0] == ".":
            return True
        else:
            return False

    def NextToDot(self):  # 返回beta串的第一个字符
        if self.right.index(".") < len(self.right) - 1:
            return self.right[self.right.index(".") + 1]
        else:
            return None

    def Beta(self):  # beta串

        if self.right.index(".") < len(self.right) - 2:
            return self.right[self.right.index(".") + 2:].copy()
        else:
            return []