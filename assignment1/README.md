# Assignment 1: Producer-Consumer Pattern

Producer-consumer pattern implementation with thread synchronization. Producers read from a source container and put items into a shared queue. Consumers pull from the queue and store items in a destination container.

## Features

- Thread-safe queue using Python's `queue.Queue`
- Blocking operations - `put()` waits when queue is full, `get()` waits when queue is empty
- Supports multiple producers and consumers
- Graceful shutdown with event signaling
- Tracks statistics per thread

## Implementation

Four main classes:

- `SharedQueue`: Wrapper around `queue.Queue` with max capacity
- `Producer`: Thread that reads from source and puts items in queue
- `Consumer`: Thread that gets items from queue and stores in destination
- `ProducerConsumer`: Orchestrator that manages everything

The queue handles all synchronization internally. When it's full, `put()` blocks. When it's empty, `get()` blocks. No manual locks needed for queue operations.

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

Tests cover:
- Single producer/consumer
- Multiple producers, single consumer
- Single producer, multiple consumers
- Multiple producers and consumers
- Queue capacity limits
- Thread synchronization correctness
- Graceful shutdown
- Edge cases like empty source and concurrent access

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

Used `queue.Queue` instead of manual locks because it handles thread safety and blocking automatically. Separate Producer/Consumer classes for cleaner code and easier testing. Statistics use locks for thread-safe counting. Shutdown uses an Event to signal all threads to stop cleanly. Consumers check producer completion status only after queue timeouts to avoid race conditions where consumers exit before producers start.

