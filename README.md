# Intuit Software Engineering Build Challenge

This repository contains solutions for the Intuit Software Engineering Build Challenge, demonstrating proficiency in Python, threading, synchronization, and functional programming.

## Projects

### Assignment 1: Producer-Consumer Pattern

Thread synchronization implementation using Python's queue module. Demonstrates proper thread communication and synchronization with multiple producers and consumers.

**Key Features:**
- Thread-safe queue using `queue.Queue`
- Blocking operations - `put()` waits when queue is full, `get()` waits when queue is empty
- Supports multiple producers and consumers
- Graceful shutdown with sentinel pattern
- Tracks statistics per thread

**Implementation:**
- `SharedQueue`: Wrapper around `queue.Queue` with max capacity
- `Producer`: Thread that reads from source and puts items in queue
- `Consumer`: Thread that gets items from queue and stores in destination
- `ProducerConsumer`: Orchestrator that manages everything

**Usage:**
```bash
cd assignment1
python producer_consumer.py
```

**Tests:**
```bash
pytest assignment1/test_producer_consumer.py -v
```

**Documentation:** See [assignment1/README.md](assignment1/README.md) for detailed documentation.

---

### Assignment 2: CSV Data Analysis with Functional Programming

CSV data analysis implementation using functional programming paradigms. Reads sales transaction data and performs analytical queries using map, filter, reduce, and other functional constructs.

**Key Features:**
- CSV data loading and parsing
- Six analytical queries using functional programming patterns
- Grouping and aggregation operations
- Sorting and filtering operations
- Comprehensive unit test coverage

**Analytical Queries:**
1. Total revenue by product
2. Total revenue by category
3. Top 5 salespeople by revenue
4. Sales by region
5. Average transaction value
6. Monthly sales trend

**Usage:**
```bash
cd assignment2
python generate_data.py  # Generate sample data
python data_analyzer.py  # Run analysis
```

**Tests:**
```bash
pytest assignment2/test_data_analyzer.py -v
```

**Documentation:** See [assignment2/README.md](assignment2/README.md) for detailed documentation.

---

## Requirements

- Python 3.11+
- pytest (for running tests)

## Repository Structure

```
.
├── assignment1/
│   ├── producer_consumer.py      # Main implementation
│   ├── test_producer_consumer.py # Unit tests
│   └── README.md                 # Detailed documentation
├── assignment2/
│   ├── generate_data.py          # CSV data generator
│   ├── data_analyzer.py          # Analysis functions
│   ├── test_data_analyzer.py     # Unit tests
│   ├── data/
│   │   └── sales_data.csv        # Sample data
│   └── README.md                 # Detailed documentation
└── README.md                     # This file
```

## Running All Tests

```bash
# Run all tests for both assignments
pytest assignment1/test_producer_consumer.py assignment2/test_data_analyzer.py -v
```

## Design Philosophy

**Assignment 1** demonstrates thread synchronization using Python's built-in `queue.Queue`, which handles all synchronization automatically. The sentinel pattern is used for clean shutdown logic, eliminating race conditions.

**Assignment 2** emphasizes functional programming patterns (reduce, map, sorted, lambda) over imperative loops, making the code more declarative and easier to reason about.

Both assignments include comprehensive test coverage and detailed documentation.

