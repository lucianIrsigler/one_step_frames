import heapq

class PriorityStack:
    def __init__(self):
        self.heap = []
        self.counter = 0  # Increases with every push

    def push(self, priority, item):
        # Negate priority because heapq is a min-heap (higher priority first)
        # Negate counter so newer items come out first when priorities are equal
        heapq.heappush(self.heap, (-priority, -self.counter, item))
        self.counter += 1

    def pop(self):
        if self.heap:
            return heapq.heappop(self.heap)[-1]
        return None

    def empty(self):
        return not self.heap
