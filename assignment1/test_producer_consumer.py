"""
Unit tests for Producer-Consumer Pattern Implementation
"""

import unittest
import time
import sys
import os
import threading

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from producer_consumer import SharedQueue, Producer, Consumer, ProducerConsumer


class TestSharedQueue(unittest.TestCase):
    """Test the SharedQueue class."""
    
    def test_queue_initialization(self):
        """Test queue initialization with maxsize."""
        q = SharedQueue(maxsize=5)
        self.assertEqual(q.maxsize, 5)
        self.assertTrue(q.empty())
        self.assertFalse(q.full())
    
    def test_queue_put_get(self):
        """Test basic put and get operations."""
        q = SharedQueue(maxsize=10)
        q.put("test_item")
        self.assertFalse(q.empty())
        item = q.get()
        self.assertEqual(item, "test_item")
        self.assertTrue(q.empty())
    
    def test_queue_full(self):
        """Test queue full condition."""
        q = SharedQueue(maxsize=2)
        q.put("item1")
        q.put("item2")
        self.assertTrue(q.full())
    
    def test_queue_blocking_put(self):
        """Test that put blocks when queue is full."""
        q = SharedQueue(maxsize=1)
        q.put("item1")
        
        start_time = time.time()
        try:
            q.put("item2", block=True, timeout=0.5)
            self.fail("Should have raised queue.Full")
        except Exception:
            pass
        elapsed = time.time() - start_time
        self.assertGreaterEqual(elapsed, 0.4)
    
    def test_queue_blocking_get(self):
        """Test that get blocks when queue is empty."""
        q = SharedQueue(maxsize=1)
        
        start_time = time.time()
        try:
            q.get(block=True, timeout=0.5)
            self.fail("Should have raised queue.Empty")
        except Exception:
            pass
        elapsed = time.time() - start_time
        self.assertGreaterEqual(elapsed, 0.4)


class TestProducer(unittest.TestCase):
    """Test the Producer class."""
    
    def test_producer_reads_from_source(self):
        """Test that producer reads items from source and puts them in queue."""
        source = [f"item-{i}" for i in range(10)]
        queue = SharedQueue(maxsize=20)
        shutdown_event = threading.Event()
        
        producer = Producer(1, source, queue, shutdown_event)
        producer.start()
        producer.join()
        
        self.assertEqual(producer.get_items_produced(), 10)
        # Queue contains 10 items + 1 sentinel
        self.assertEqual(queue.qsize(), 11)
        
        for i in range(10):
            item = queue.get()
            self.assertIn(item, source)
    
    def test_producer_handles_empty_source(self):
        """Test producer with empty source."""
        source = []
        queue = SharedQueue(maxsize=10)
        shutdown_event = threading.Event()
        
        producer = Producer(1, source, queue, shutdown_event)
        producer.start()
        producer.join()
        
        self.assertEqual(producer.get_items_produced(), 0)
        # Queue contains 1 sentinel (even with empty source)
        self.assertEqual(queue.qsize(), 1)
    
    def test_producer_respects_shutdown_event(self):
        """Test that producer stops when shutdown event is set."""
        source = [f"item-{i}" for i in range(100)]
        queue = SharedQueue(maxsize=10)
        shutdown_event = threading.Event()
        
        producer = Producer(1, source, queue, shutdown_event)
        producer.start()
        
        time.sleep(0.1)
        shutdown_event.set()
        producer.join(timeout=2.0)
        
        self.assertFalse(producer.is_alive())
        items_produced = producer.get_items_produced()
        self.assertLess(items_produced, len(source))
    
    def test_multiple_producers(self):
        """Test multiple producers working concurrently."""
        source1 = [f"item1-{i}" for i in range(5)]
        source2 = [f"item2-{i}" for i in range(5)]
        queue = SharedQueue(maxsize=20)
        shutdown_event = threading.Event()
        
        producer1 = Producer(1, source1, queue, shutdown_event)
        producer2 = Producer(2, source2, queue, shutdown_event)
        
        producer1.start()
        producer2.start()
        
        producer1.join()
        producer2.join()
        
        self.assertEqual(producer1.get_items_produced(), 5)
        self.assertEqual(producer2.get_items_produced(), 5)
        # Queue contains 10 items + 2 sentinels (one per producer)
        self.assertEqual(queue.qsize(), 12)


class TestConsumer(unittest.TestCase):
    """Test the Consumer class."""
    
    def test_consumer_reads_from_queue(self):
        """Test that consumer reads items from queue and stores in destination."""
        destination = []
        queue = SharedQueue(maxsize=20)
        shutdown_event = threading.Event()
        
        for i in range(10):
            queue.put(f"item-{i}")
        
        producer = Producer(1, [], queue, shutdown_event)
        producer.start()
        producer.join()
        
        consumer = Consumer(1, destination, queue, shutdown_event, 1)
        
        consumer.start()
        consumer.join(timeout=2.0)
        
        self.assertEqual(consumer.get_items_consumed(), 10)
        self.assertEqual(len(destination), 10)
        self.assertTrue(queue.empty())
    
    def test_consumer_with_producer(self):
        """Test consumer working with a producer."""
        source = [f"item-{i}" for i in range(10)]
        destination = []
        queue = SharedQueue(maxsize=20)
        shutdown_event = threading.Event()
        
        producer = Producer(1, source, queue, shutdown_event)
        consumer = Consumer(1, destination, queue, shutdown_event, 1)
        
        consumer.start()
        producer.start()
        
        producer.join()
        consumer.join(timeout=2.0)
        
        self.assertEqual(producer.get_items_produced(), 10)
        self.assertEqual(consumer.get_items_consumed(), 10)
        self.assertEqual(len(destination), 10)
        self.assertEqual(set(destination), set(source))
    
    def test_consumer_handles_empty_queue(self):
        """Test consumer with empty queue stops correctly."""
        destination = []
        queue = SharedQueue(maxsize=10)
        shutdown_event = threading.Event()
        
        producer = Producer(1, [], queue, shutdown_event)
        producer.start()
        producer.join()
        
        consumer = Consumer(1, destination, queue, shutdown_event, [producer])
        consumer.start()
        consumer.join(timeout=2.0)
        
        self.assertEqual(consumer.get_items_consumed(), 0)
        self.assertEqual(len(destination), 0)
    
    def test_multiple_consumers(self):
        """Test multiple consumers working concurrently."""
        source = [f"item-{i}" for i in range(20)]
        destination1 = []
        destination2 = []
        queue = SharedQueue(maxsize=20)
        shutdown_event = threading.Event()
        
        producer = Producer(1, source, queue, shutdown_event)
        consumer1 = Consumer(1, destination1, queue, shutdown_event, 1)
        consumer2 = Consumer(2, destination2, queue, shutdown_event, 1)
        
        consumer1.start()
        consumer2.start()
        producer.start()
        
        producer.join()
        consumer1.join(timeout=2.0)
        consumer2.join(timeout=2.0)
        
        total_consumed = len(destination1) + len(destination2)
        self.assertEqual(total_consumed, 20)
        self.assertEqual(producer.get_items_produced(), 20)
        self.assertEqual(consumer1.get_items_consumed() + consumer2.get_items_consumed(), 20)
        
        all_items = destination1 + destination2
        self.assertEqual(len(all_items), len(set(all_items)))
    
    def test_consumer_respects_shutdown_event(self):
        """Test that consumer stops when shutdown event is set."""
        destination = []
        queue = SharedQueue(maxsize=10)
        shutdown_event = threading.Event()
        
        for i in range(5):
            queue.put(f"item-{i}")
        
        producer = Producer(1, [], queue, shutdown_event)
        producer.start()
        producer.join()
        
        consumer = Consumer(1, destination, queue, shutdown_event, [producer])
        consumer.start()
        
        time.sleep(0.1)
        shutdown_event.set()
        consumer.join(timeout=2.0)
        
        self.assertFalse(consumer.is_alive())
        self.assertGreaterEqual(consumer.get_items_consumed(), 0)


class TestProducerConsumer(unittest.TestCase):
    """Test the ProducerConsumer orchestrator class."""
    
    def test_single_producer_single_consumer(self):
        """Test single producer and single consumer."""
        source = [f"item-{i}" for i in range(10)]
        destination = []
        
        pc = ProducerConsumer(queue_size=5)
        pc.add_producer(1, source)
        pc.add_consumer(1, destination)
        
        pc.start()
        pc.wait_for_completion()
        
        self.assertEqual(len(destination), len(source))
        self.assertEqual(set(destination), set(source))
        
        stats = pc.get_statistics()
        self.assertEqual(stats['total_produced'], 10)
        self.assertEqual(stats['total_consumed'], 10)
    
    def test_multiple_producers_single_consumer(self):
        """Test multiple producers with single consumer."""
        source1 = [f"item1-{i}" for i in range(5)]
        source2 = [f"item2-{i}" for i in range(5)]
        destination = []
        
        pc = ProducerConsumer(queue_size=10)
        pc.add_producer(1, source1)
        pc.add_producer(2, source2)
        pc.add_consumer(1, destination)
        
        pc.start()
        pc.wait_for_completion()
        
        expected_items = set(source1 + source2)
        self.assertEqual(len(destination), 10)
        self.assertEqual(set(destination), expected_items)
        
        stats = pc.get_statistics()
        self.assertEqual(stats['total_produced'], 10)
        self.assertEqual(stats['total_consumed'], 10)
    
    def test_single_producer_multiple_consumers(self):
        """Test single producer with multiple consumers."""
        source = [f"item-{i}" for i in range(20)]
        destination1 = []
        destination2 = []
        
        pc = ProducerConsumer(queue_size=10)
        pc.add_producer(1, source)
        pc.add_consumer(1, destination1)
        pc.add_consumer(2, destination2)
        
        pc.start()
        pc.wait_for_completion()
        
        total_consumed = len(destination1) + len(destination2)
        self.assertEqual(total_consumed, len(source))
        
        all_items = destination1 + destination2
        self.assertEqual(len(all_items), len(set(all_items)))
        
        stats = pc.get_statistics()
        self.assertEqual(stats['total_produced'], 20)
        self.assertEqual(stats['total_consumed'], 20)
    
    def test_multiple_producers_multiple_consumers(self):
        """Test multiple producers with multiple consumers."""
        source1 = [f"item1-{i}" for i in range(10)]
        source2 = [f"item2-{i}" for i in range(10)]
        destination = []
        
        pc = ProducerConsumer(queue_size=5)
        pc.add_producer(1, source1)
        pc.add_producer(2, source2)
        pc.add_consumer(1, destination)
        pc.add_consumer(2, destination)
        
        pc.start()
        pc.wait_for_completion()
        
        expected_items = set(source1 + source2)
        self.assertEqual(len(destination), 20)
        self.assertEqual(set(destination), expected_items)
        
        stats = pc.get_statistics()
        self.assertEqual(stats['total_produced'], 20)
        self.assertEqual(stats['total_consumed'], 20)
    
    def test_queue_capacity_limit(self):
        """Test that queue capacity limits are respected."""
        source = [f"item-{i}" for i in range(50)]
        destination = []
        
        pc = ProducerConsumer(queue_size=5)
        pc.add_producer(1, source)
        pc.add_consumer(1, destination)
        
        pc.start()
        
        time.sleep(0.1)
        queue_size = pc.shared_queue.qsize()
        self.assertLessEqual(queue_size, 5)
        
        pc.wait_for_completion()
        
        self.assertEqual(len(destination), len(source))
    
    def test_empty_source(self):
        """Test behavior with empty source."""
        source = []
        destination = []
        
        pc = ProducerConsumer(queue_size=10)
        pc.add_producer(1, source)
        pc.add_consumer(1, destination)
        
        pc.start()
        pc.wait_for_completion()
        
        self.assertEqual(len(destination), 0)
        stats = pc.get_statistics()
        self.assertEqual(stats['total_produced'], 0)
        self.assertEqual(stats['total_consumed'], 0)
    
    def test_graceful_shutdown(self):
        """Test graceful shutdown mechanism."""
        source = [f"item-{i}" for i in range(100)]
        destination = []
        
        pc = ProducerConsumer(queue_size=10)
        pc.add_producer(1, source)
        pc.add_consumer(1, destination)
        
        pc.start()
        
        time.sleep(0.1)
        pc.shutdown()
        
        for producer in pc.producers:
            self.assertFalse(producer.is_alive())
        for consumer in pc.consumers:
            self.assertFalse(consumer.is_alive())
    
    def test_thread_synchronization(self):
        """Test that thread synchronization works correctly."""
        source = [f"item-{i}" for i in range(100)]
        destination = []
        
        pc = ProducerConsumer(queue_size=10)
        pc.add_producer(1, source[:50])
        pc.add_producer(2, source[50:])
        pc.add_consumer(1, destination)
        pc.add_consumer(2, destination)
        
        pc.start()
        pc.wait_for_completion()
        
        self.assertEqual(len(destination), 100)
        self.assertEqual(set(destination), set(source))
        
        stats = pc.get_statistics()
        self.assertEqual(stats['total_produced'], 100)
        self.assertEqual(stats['total_consumed'], 100)
    
    def test_concurrent_access(self):
        """Test concurrent access to shared resources."""
        source = [f"item-{i}" for i in range(200)]
        destination = []
        
        pc = ProducerConsumer(queue_size=20)
        for i in range(3):
            start_idx = i * 67
            end_idx = start_idx + 67 if i < 2 else len(source)
            pc.add_producer(i+1, source[start_idx:end_idx])
        
        for i in range(3):
            pc.add_consumer(i+1, destination)
        
        pc.start()
        pc.wait_for_completion()
        
        self.assertEqual(len(destination), len(source))
        self.assertEqual(set(destination), set(source))
        
        stats = pc.get_statistics()
        self.assertEqual(stats['total_produced'], 200)
        self.assertEqual(stats['total_consumed'], 200)


if __name__ == "__main__":
    unittest.main()

