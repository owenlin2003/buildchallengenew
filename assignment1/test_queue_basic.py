"""Basic test for ThreadSafeQueue to verify checkpoint 2."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from producer_consumer import ThreadSafeQueue


def test_queue_basic_operations():
    """Test basic queue operations."""
    queue = ThreadSafeQueue(maxsize=5)
    
    assert queue.empty()
    assert not queue.full()
    assert queue.size() == 0
    
    queue.put(1)
    queue.put(2)
    
    assert queue.size() == 2
    assert not queue.empty()
    assert not queue.full()
    
    item = queue.get()
    assert item == 1
    assert queue.size() == 1
    
    item = queue.get()
    assert item == 2
    assert queue.empty()


def test_queue_capacity():
    """Test queue capacity limits."""
    queue = ThreadSafeQueue(maxsize=2)
    
    queue.put(1)
    queue.put(2)
    
    assert queue.full()
    assert queue.size() == 2


if __name__ == "__main__":
    test_queue_basic_operations()
    test_queue_capacity()
    print("Basic queue tests passed")

