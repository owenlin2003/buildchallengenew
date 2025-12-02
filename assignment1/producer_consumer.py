"""
Producer-Consumer pattern implementation with manual thread synchronization.

Demonstrates thread synchronization using locks and condition variables
to implement a blocking queue for producer-consumer communication.
"""

import threading
from collections import deque
from typing import Any, Optional


class ThreadSafeQueue:
    """
    Thread-safe queue implementation using locks and condition variables.
    
    Provides blocking put() and get() operations that wait when the queue
    is full or empty, respectively. Uses Condition variables for wait/notify
    mechanism similar to Java's wait/notify pattern.
    """
    
    def __init__(self, maxsize: int = 0):
        """
        Initialize thread-safe queue.
        
        Args:
            maxsize: Maximum queue size. 0 means unlimited.
        """
        self._maxsize = maxsize
        self._queue = deque()
        self._lock = threading.Lock()
        self._not_empty = threading.Condition(self._lock)
        self._not_full = threading.Condition(self._lock)
    
    def put(self, item: Any) -> None:
        """
        Put item into queue, blocking if queue is full.
        
        Args:
            item: Item to add to queue.
        """
        with self._not_full:
            while self._maxsize > 0 and len(self._queue) >= self._maxsize:
                self._not_full.wait()
            
            self._queue.append(item)
            self._not_empty.notify()
    
    def get(self) -> Any:
        """
        Get item from queue, blocking if queue is empty.
        
        Returns:
            Item from queue.
        """
        with self._not_empty:
            while len(self._queue) == 0:
                self._not_empty.wait()
            
            item = self._queue.popleft()
            self._not_full.notify()
            return item
    
    def empty(self) -> bool:
        """Check if queue is empty."""
        with self._lock:
            return len(self._queue) == 0
    
    def full(self) -> bool:
        """Check if queue is full."""
        with self._lock:
            return self._maxsize > 0 and len(self._queue) >= self._maxsize
    
    def size(self) -> int:
        """Get current queue size."""
        with self._lock:
            return len(self._queue)

