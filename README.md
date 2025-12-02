# Intuit Software Engineering Build Challenge

This repository contains solutions for the Intuit Software Engineering Build Challenge, demonstrating proficiency in Python, threading, synchronization, and functional programming.

## Projects

### Assignment 1: Producer-Consumer Pattern

Thread synchronization implementation using Python's queue module. Demonstrates proper thread communication and synchronization with multiple producers and consumers.

The implementation includes a thread-safe queue wrapper, producer threads that read from a source and put items into the queue, consumer threads that get items from the queue and store them in a destination, and an orchestrator class that manages everything together.

Key features include blocking operations where put() waits when the queue is full and get() waits when the queue is empty, support for multiple producers and consumers, graceful shutdown using the sentinel pattern, and statistics tracking per thread.

To run the example:
```bash
cd assignment1
python producer_consumer.py
```

To run tests:
```bash
pytest assignment1/test_producer_consumer.py -v
```

See assignment1/README.md for detailed documentation.

### Assignment 2: CSV Data Analysis with Functional Programming

CSV data analysis implementation using functional programming paradigms. Reads sales transaction data and performs analytical queries using map, filter, reduce, and other functional constructs.

The implementation includes six analytical queries: total revenue by product, total revenue by category, top 5 salespeople by revenue, sales by region, average transaction value, and monthly sales trend. All queries use functional programming patterns like reduce() for aggregation, map() for transformation, and sorted() with lambda functions for ordering.

To generate sample data:
```bash
cd assignment2
python generate_data.py
```

To run analysis:
```bash
python data_analyzer.py
```

To run tests:
```bash
pytest assignment2/test_data_analyzer.py -v
```

See assignment2/README.md for detailed documentation.

## Requirements

Python 3.11+ and pytest for running tests.

## Repository Structure

```
.
├── assignment1/
│   ├── producer_consumer.py
│   ├── test_producer_consumer.py
│   └── README.md
├── assignment2/
│   ├── generate_data.py
│   ├── data_analyzer.py
│   ├── test_data_analyzer.py
│   ├── data/
│   │   └── sales_data.csv
│   └── README.md
└── README.md
```

## Running All Tests

Run all tests for both assignments:
```bash
pytest assignment1/test_producer_consumer.py assignment2/test_data_analyzer.py -v
```

## Design Philosophy

Assignment 1 demonstrates thread synchronization using Python's built-in queue.Queue, which handles all synchronization automatically. The sentinel pattern is used for clean shutdown logic, eliminating race conditions.

Assignment 2 emphasizes functional programming patterns over imperative loops, making the code more declarative and easier to reason about. All analysis functions use reduce, map, sorted, and lambda functions rather than traditional loops.

Both assignments include comprehensive test coverage and detailed documentation.
