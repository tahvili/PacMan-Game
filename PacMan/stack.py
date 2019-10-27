class Stack:
    """
    If you took csc148, i don't need to explain anything here
    """

    def __init__(self):
        self.items = []

    def is_empty(self):
        if len(self.items) > 0:
            return False

        return True

    def clear(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop(len(self.items) - 1)

        return None

    def peek(self):
        if not self.is_empty():
            return self.items[len(self.items) - 1]

        return None
