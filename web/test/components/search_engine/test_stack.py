from bfex.components.search_engine.stack import Stack


class TestStack(object):
    def test_peek(self):
        stk = Stack()
        assert stk.peek() is None

        stk.push(3)
        assert stk.peek() == 3

    def test_push(self):
        stk = Stack()
        stk.push(3)
        assert len(stk.stack) == 1

    def test_pop(self):
        stk = Stack()
        stk.push(5)

        assert stk.pop() == 5
        assert stk.pop() is None

    def test_empty(self):
        stk = Stack()
        stk.push(5)
        stk.push(8)
        assert len(stk.stack) == 2
        stk.empty()
        assert len(stk.stack) == 0