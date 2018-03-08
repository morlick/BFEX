class Stack:
    """ Simple stack class used to store the processed queries in postfix order. """

    def __init__(self):
        self.stack = []

    def __repr__(self):
        return str(self.stack)

    def peek(self):
        if len(self.stack) > 0:
            return self.stack[-1]
        return None

    def pop(self):
        try:
            return self.stack.pop()
        except IndexError:
            return None

    def push(self, obj):
        self.stack.append(obj)

    def empty(self):
        self.stack = []

    def is_empty(self):
        if len(self.stack) == 0:
            return True
        else:
            return False