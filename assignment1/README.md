# Assignment 1: Producer-Consumer Pattern

Producer-consumer pattern implementation with thread synchronization. Producers read from a source container and put items into a shared queue. Consumers pull from the queue and store items in a destination container.

The implementation uses Python's queue.Queue which handles thread safety and blocking automatically. When the queue is full, put() blocks until space is available. When it's empty, get() blocks until an item is available. No manual locks are needed for queue operations.

Four main classes make up the implementation. SharedQueue wraps queue.Queue with max capacity. Producer threads read from a source and put items in the queue. Consumer threads get items from the queue and store them in a destination. ProducerConsumer orchestrates everything together.

The sentinel pattern is used for clean shutdown. Each producer puts a sentinel value (None) into the queue when finished. Consumers stop immediately when they see a sentinel. ProducerConsumer ensures there are enough sentinels for all consumers by adding extras if needed.

## Usage

```python
from producer_consumer import ProducerConsumer

source_data = [f"Item-{i}" for i in range(50)]
destination = []

pc = ProducerConsumer(queue_size=10)
pc.add_producer(1, source_data[:25])
pc.add_producer(2, source_data[25:])
pc.add_consumer(1, destination)
pc.add_consumer(2, destination)

pc.start()
pc.wait_for_completion()

stats = pc.get_statistics()
print(f"Total produced: {stats['total_produced']}")
```

Run the example:
```bash
cd assignment1
python producer_consumer.py
```

## Tests

```bash
pytest assignment1/test_producer_consumer.py -v
```

Tests cover single producer/consumer, multiple producers with single consumer, single producer with multiple consumers, multiple producers and consumers, queue capacity limits, thread synchronization correctness, graceful shutdown, and edge cases like empty source and concurrent access.

## Sample Output

```
Starting producer-consumer system...
Producer 1 finished. Produced 25 items.
Producer 2 finished. Produced 25 items.
Consumer 1 finished. Consumed 25 items.
Consumer 2 finished. Consumed 25 items.

=== Statistics ===
Total produced: 50
Total consumed: 50
Items in destination: 50
Queue size: 0

✓ All items successfully transferred!
```

## Design Notes

Used queue.Queue instead of manual locks because it handles thread safety and blocking automatically. Separate Producer/Consumer classes make the code cleaner and easier to test. Statistics use locks for thread-safe counting. The sentinel pattern eliminates race conditions by having producers signal completion directly through the queue rather than checking thread status.
