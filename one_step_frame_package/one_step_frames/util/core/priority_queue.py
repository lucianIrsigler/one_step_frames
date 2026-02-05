import heapq

class PriorityQueue:
    """A priority queue that uses a max-heap
     to manage items based on their priority.
    """
    def __init__(self):
        self.heap = []
        self.counter = 0  # Increases with every push

    def push(self, priority:int, item):
        """Push an item onto the queue with a given priority.

        Args:
            priority (int): The priority of the item. Higher values indicate higher priority.
            item (any): The item to be pushed onto the queue.
        """
        # Negate priority because heapq is a min-heap (higher priority first)
        # Negate counter so newer items come out first when priorities are equal
        # Changed to make it more queue like. For queue behaviour, make counter negative
        heapq.heappush(self.heap, (-priority, self.counter, item))
        self.counter += 1
    
    
    def make_unique(self):
        """ Make the items in the priority queue unique based on their item value.
        """
        unique_items = {}
        for priority, count, item in self.heap:
            if item not in unique_items:
                unique_items[item] = (priority, count, item)
        
        self.heap = list(unique_items.values())
        heapq.heapify(self.heap)


    def pop(self):
        """ Pop the item with the highest priority from the queue.

        Returns:
            any: The item with the highest priority, or None if the queue is empty.
        """
        if self.heap:
            return heapq.heappop(self.heap)
        return None

    def empty(self):
        """ Check if the queue is empty.

        Returns:
            bool: True if the queue is empty, False otherwise.
        """
        return not self.heap
    
    def clear(self):
        """
            Clears the priority queue
        """
        self.heap.clear()
        self.counter = 0
