"""
Project 4 - Circular Queues
Name: Justin Vesche
"""
from collections import defaultdict


class CircularQueue:
    """
    Circular Queue Class.
    """

    # DO NOT MODIFY THESE METHODS
    def __init__(self, capacity=4):
        """
        Initialize the queue with an initial capacity
        :param capacity: the initial capacity of the queue
        """
        self.capacity = capacity
        self.size = 0
        self.data = [None] * capacity
        self.head = 0
        self.tail = 0

    def __eq__(self, other):
        """
        Defines equality for two queues
        :return: true if two queues are equal, false otherwise
        """
        if self.capacity != other.capacity or self.size != other.size:
            return False

        if self.head != other.head or self.tail != other.tail:
            return False

        for i in range(self.capacity):
            if self.data[i] != other.data[i]:
                return False

        return True

    def __str__(self):
        """
        String representation of the queue
        :return: the queue as a string
        """
        if self.is_empty():
            return "Empty queue"

        str_list = [str(self.data[(self.head + i) % self.capacity]) for i in range(self.size)]
        return "Queue: " + ", ".join(str_list)

    # -----------MODIFY BELOW--------------

    def is_empty(self):
        """
        check if queue is empty
        :return: True if is empty false otherwise
        """
        return not bool(self.size)

    def __len__(self):
        """
        Checks the length of the queue, not including None
        :return: occupied space in the queue
        """
        return self.size

    def head_element(self):
        """
        Check index of the queues head value
        :return: the index of the head value, none if empty
        """
        if self.is_empty():
            return None
        return self.data[self.head]

    def tail_element(self):
        """
        Check index of the queues tail value
        :return: the index of the tail value, none if empty
        """
        if self.is_empty():
            return None
        return self.data[self.tail - 1]

    def grow(self):
        """
        Grows the capacity of the list, doubles it each time called
        :return: None
        """
        if self.capacity == self.size:
            old = self.data
            self.capacity *= 2
            self.data = [None] * self.capacity
            change = self.head
            for i in range(self.size):
                self.data[i] = old[change]
                change = (1 + change) % len(old)
            self.head = 0
            self.tail = len(self)

    def shrink(self):
        """
        shrinks the capacity of the list, divides it by 2 when scenario is met
        :return: None
        """
        if self.capacity // 2 >= 4:
            if len(self) * 4 <= self.capacity:
                self.capacity = self.capacity // 2
                old = self.data
                self.data = [None] * self.capacity
                change = self.head
                for i in range(self.size):
                    self.data[i] = old[change]
                    change = (1 + change) % len(old)
                self.head = 0
                self.tail = len(self)

    def enqueue(self, val):
        """
        Adds to queue and calls grow to check to see if growth needed
        :return: None
        """
        self.grow()
        self.data[self.tail] = val
        self.size += 1
        self.tail = (1 + self.tail) % self.capacity
        self.grow()
        return None

    def dequeue(self):
        """
        Removes from the queue and calls shrink to check to see if shrink needed
        :return: removed element
        """
        if self.is_empty():
            return None
        return_value = self.data[self.head]
        self.data[self.head] = None
        self.head = (1 + self.head) % self.capacity
        self.size -= 1
        self.shrink()
        return return_value

class QStack:
    """
    Stack class, implemented with underlying Circular Queue
    """
    # DO NOT MODIFY THESE METHODS
    def __init__(self):
        self.cq = CircularQueue()
        self.size = 0

    def __eq__(self, other):
        """
        Defines equality for two QStacks
        :return: true if two stacks are equal, false otherwise
        """
        if self.size != other.size:
            return False

        if self.cq != other.cq:
            return False

        return True

    def __str__(self):
        """
        String representation of the QStack
        :return: the stack as a string
        """
        if self.size == 0:
            return "Empty stack"

        str_list = [str(self.cq.data[(self.cq.head + i) % self.cq.capacity]) for i in range(self.size)]
        return "Stack: " + ", ".join(str_list)

    # -----------MODIFY BELOW--------------
    def push(self, val):
        """
        Push the value into the stack
        :return: None
        """
        self.size += 1
        self.cq.enqueue(val)
        for i in range(self.size - 1):
            temp = self.cq.dequeue()
            self.cq.enqueue(temp)
        return None

    def pop(self):
        """
        Pop the value from the stack
        :return: the removed item
        """
        if self.size == 0:
            return None
        val = self.cq.dequeue()
        self.size -= 1
        return val

    def top(self):
        """
        Check to see if there is a top, if there is return it
        :return: None, or top value
        """
        if self.size == 0:
            return None
        return self.cq.head_element()


def digit_swap(nums, replacements):
    """
    Checks sequence values with replacements, checks if there is sequential pairs
    with a queue and a dictionary
    :return: the max number of the number of sequential values in the string with replacements
    """
    max_length = 0
    queue = CircularQueue()
    number_dictionary = defaultdict(int)
    for i in nums:
        number_dictionary[i] += 1
        queue.enqueue(i)
        length = len(queue)
        duplicates = max(number_dictionary.values())
        if length - duplicates > replacements:
            number_dictionary[queue.head_element()] -= 1
            queue.dequeue()
        if len(queue) > max_length:
            max_length = len(queue)
    return max_length