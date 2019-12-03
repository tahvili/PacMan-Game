from typing import *


class Stack:
    """A last-in-first-out (LIFO) stack of items.

    Stores data in last-in, first-out order. When removing an item from the
    stack, the most recently-added item is the one that is removed.
    """
    def __init__(self) -> None:
        """
        Initialize a new empty stack.
        """

        self.items = []

    def is_empty(self) -> bool:
        """
        Return whether this stack contains no items.
        """
        if len(self.items) > 0:
            return False

        return True

    def clear(self) -> None:
        """
        Clears the stack.
        """
        self.items = []

    def push(self, item) -> None:
        """
        Add a new element to the top of this stack.
        """
        self.items.append(item)

    def pop(self) -> Any:
        """
        Remove and return the element at the top of this stack.
        """
        if not self.is_empty():
            return self.items.pop(len(self.items) - 1)

        return None

    def peek(self) -> Any:
        """
        Returns the element at the top of the stack.
        """
        if not self.is_empty():
            return self.items[len(self.items) - 1]

        return None
