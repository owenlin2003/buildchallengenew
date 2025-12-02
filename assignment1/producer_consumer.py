"""
Producer-Consumer Pattern Implementation

This module implements a classic producer-consumer pattern demonstrating thread
synchronization and communication using Python's queue module.
"""

import queue
import threading
import time
from typing import Any, Optional, List


class SharedQueue:
    """
    Thread-safe queue wrapper that provides blocking operations.
    
    Uses queue.Queue internally which handles all thread synchronization
    automatically through its blocking get() and put() methods.
    """
    
    def __init__(self, maxsize: int = 10):
        """
        Initialize the shared queue.
        
        Args:
            maxsize: Maximum number of items the queue can hold.
                    When full, put() operations will block until space is available.
        """
        self._queue = queue.Queue(maxsize=maxsize)
        self.maxsize = maxsize
    
    def put(self, item: Any, block: bool = True, timeout: Optional[float] = None) -> None:
        """
        Put an item into the queue.
        
        Args:
            item: The item to add to the queue
            block: If True, block until space is available
            timeout: Maximum time to wait if block is True
        """
        self._queue.put(item, block=block, timeout=timeout)
    
    def get(self, block: bool = True, timeout: Optional[float] = None) -> Any:
        """
        Get an item from the queue.
        
        Args:
            block: If True, block until an item is available
            timeout: Maximum time to wait if block is True
            
        Returns:
            The item retrieved from the queue
        """
        return self._queue.get(block=block, timeout=timeout)
    
    def empty(self) -> bool:
        """Check if the queue is empty."""
        return self._queue.empty()
    
    def full(self) -> bool:
        """Check if the queue is full."""
        return self._queue.full()
    
    def qsize(self) -> int:
        """Return the approximate size of the queue."""
        return self._queue.qsize()


class Producer(threading.Thread):
    """
    Producer thread that reads items from a source container and places them
    into a shared queue.
    """
    
    def __init__(self, producer_id: int, source: List[Any], shared_queue: SharedQueue,
                 shutdown_event: threading.Event):
        """
        Initialize the producer thread.
        
        Args:
            producer_id: Unique identifier for this producer
            source: List of items to read from
            shared_queue: The shared queue to put items into
            shutdown_event: Event to signal shutdown
        """
        super().__init__(name=f"Producer-{producer_id}", daemon=False)
        self.producer_id = producer_id
        self.source = source
        self.shared_queue = shared_queue
        self.shutdown_event = shutdown_event
        self.items_produced = 0
        self._lock = threading.Lock()
    
    def run(self) -> None:
        """Main producer loop - reads from source and puts items into queue."""
        source_index = 0
        
        while source_index < len(self.source) and not self.shutdown_event.is_set():
            try:
                item = self.source[source_index]
                self.shared_queue.put(item, block=True, timeout=0.1)
                
                with self._lock:
                    self.items_produced += 1
                
                source_index += 1
                
            except queue.Full:
                if self.shutdown_event.is_set():
                    break
                continue
            except Exception as e:
                print(f"Producer {self.producer_id} error: {e}")
                break
        
        # Put sentinel value to signal completion
        try:
            self.shared_queue.put(None, block=True, timeout=0.1)
        except Exception as e:
            print(f"Producer {self.producer_id} error putting sentinel: {e}")
        
        print(f"Producer {self.producer_id} finished. Produced {self.items_produced} items.")
    
    def get_items_produced(self) -> int:
        """Get the number of items produced by this thread."""
        with self._lock:
            return self.items_produced


class Consumer(threading.Thread):
    """
    Consumer thread that reads items from a shared queue and stores them
    in a destination container.
    """
    
    def __init__(self, consumer_id: int, destination: List[Any], shared_queue: SharedQueue,
                 shutdown_event: threading.Event):
        """
        Initialize the consumer thread.
        
        Args:
            consumer_id: Unique identifier for this consumer
            destination: List to store consumed items
            shared_queue: The shared queue to get items from
            shutdown_event: Event to signal shutdown
        """
        super().__init__(name=f"Consumer-{consumer_id}", daemon=False)
        self.consumer_id = consumer_id
        self.destination = destination
        self.shared_queue = shared_queue
        self.shutdown_event = shutdown_event
        self.items_consumed = 0
        self._lock = threading.Lock()
        self._dest_lock = threading.Lock()
    
    def run(self) -> None:
        """Main consumer loop - gets items from queue and stores in destination."""
        while True:
            if self.shutdown_event.is_set():
                # Drain remaining items
                try:
                    while True:
                        item = self.shared_queue.get(block=False)
                        if item is not None:
                            with self._dest_lock:
                                self.destination.append(item)
                            with self._lock:
                                self.items_consumed += 1
                except queue.Empty:
                    break
            
            try:
                item = self.shared_queue.get(block=True, timeout=0.1)
                
                # Check for sentinel value - stop immediately when we see one
                if item is None:
                    if self.shutdown_event.is_set():
                        break #only stop if all producers finished
                    continue #otheriwse, skip sentinel and keep going
                with self._dest_lock:
                    self.destination.append(item)
                
                with self._lock:
                    self.items_consumed += 1
                
            except queue.Empty:
                # Timeout - check if shutdown was requested
                if self.shutdown_event.is_set():
                    break
                continue
            except Exception as e:
                print(f"Consumer {self.consumer_id} error: {e}")
                break
        
        print(f"Consumer {self.consumer_id} finished. Consumed {self.items_consumed} items.")
    
    def get_items_consumed(self) -> int:
        """Get the number of items consumed by this thread."""
        with self._lock:
            return self.items_consumed


class ProducerConsumer:
    """
    Main orchestrator class that manages producers, consumers, and the shared queue.
    """
    
    def __init__(self, queue_size: int = 10):
        """
        Initialize the producer-consumer system.
        
        Args:
            queue_size: Maximum size of the shared queue
        """
        self.queue_size = queue_size
        self.shared_queue = SharedQueue(maxsize=queue_size)
        self.shutdown_event = threading.Event()
        self.producers: List[Producer] = []
        self.consumers: List[Consumer] = []
    
    def add_producer(self, producer_id: int, source: List[Any]) -> Producer:
        """
        Create and add a producer thread.
        
        Args:
            producer_id: Unique identifier for the producer
            source: List of items for the producer to process
            
        Returns:
            The created Producer instance
        """
        producer = Producer(producer_id, source, self.shared_queue, self.shutdown_event)
        self.producers.append(producer)
        return producer
    
    def add_consumer(self, consumer_id: int, destination: List[Any]) -> Consumer:
        """
        Create and add a consumer thread.
        
        Args:
            consumer_id: Unique identifier for the consumer
            destination: List to store consumed items
            
        Returns:
            The created Consumer instance
        """
        consumer = Consumer(consumer_id, destination, self.shared_queue,
                           self.shutdown_event)
        self.consumers.append(consumer)
        return consumer
    
    def start(self) -> None:
        """Start all producer and consumer threads."""
        for consumer in self.consumers:
            consumer.start()
        
        time.sleep(0.1) #consumers waiting and ready for queue BEFORE producers putting items        
        for producer in self.producers:
            producer.start()
    
    def _ensure_sufficient_sentinels(self) -> None:
        """
        Ensure there are enough sentinel values in the queue for all consumers.
        
        Each producer puts one sentinel when it finishes. If there are more
        consumers than producers, we need to add additional sentinels so each
        consumer can receive one and stop gracefully.
        """
        num_sentinels_needed = len(self.consumers)
        num_sentinels_from_producers = len(self.producers)
        additional_sentinels = max(0, num_sentinels_needed - num_sentinels_from_producers)
        
        for _ in range(additional_sentinels):
            try:
                self.shared_queue.put(None, block=True, timeout=0.1)
            except Exception:
                pass
    
    def wait_for_completion(self, timeout: Optional[float] = None) -> None:
        """
        Wait for all threads to complete.
        
        Args:
            timeout: Maximum time to wait for completion
        """
        # Wait for all producers to finish
        for producer in self.producers:
            producer.join(timeout=timeout)
        
        # Ensure each consumer gets a sentinel to stop
        self._ensure_sufficient_sentinels()
        
        # Signal shutdown and wait for consumers
        self.shutdown_event.set()
        for consumer in self.consumers:
            consumer.join(timeout=timeout)
    
    def shutdown(self) -> None:
        """Gracefully shutdown all threads."""
        self.shutdown_event.set()
        self.wait_for_completion()
    
    def get_statistics(self) -> dict:
        """
        Get statistics about the producer-consumer execution.
        
        Returns:
            Dictionary with statistics about items produced and consumed
        """
        total_produced = sum(p.get_items_produced() for p in self.producers)
        total_consumed = sum(c.get_items_consumed() for c in self.consumers)
        
        return {
            'total_produced': total_produced,
            'total_consumed': total_consumed,
            'queue_size': self.shared_queue.qsize(),
            'producers': len(self.producers),
            'consumers': len(self.consumers)
        }


def main():
    """Example usage of the producer-consumer pattern."""
    source_data = [f"Item-{i}" for i in range(50)]
    destination = []
    
    pc = ProducerConsumer(queue_size=10)
    
    pc.add_producer(1, source_data[:25])
    pc.add_producer(2, source_data[25:])
    pc.add_consumer(1, destination)
    pc.add_consumer(2, destination)
    
    print("Starting producer-consumer system...")
    pc.start()
    
    pc.wait_for_completion()
    
    stats = pc.get_statistics()
    print("\n=== Statistics ===")
    print(f"Total produced: {stats['total_produced']}")
    print(f"Total consumed: {stats['total_consumed']}")
    print(f"Items in destination: {len(destination)}")
    print(f"Queue size: {stats['queue_size']}")
    
    if len(destination) == len(source_data):
        print("\n✓ All items successfully transferred!")
    else:
        print(f"\n✗ Mismatch: Expected {len(source_data)} items, got {len(destination)}")


if __name__ == "__main__":
    main()

