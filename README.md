# Intuit Software Engineering Build Challenge

This repository contains solutions for the Intuit Software Engineering Build Challenge, demonstrating proficiency in Python, threading, synchronization, and functional programming.

## Setup Instructions

Uses only Python standard library. Python 3.11+ recommended. Only requires pytest for running tests: `pip install pytest`

## Assignment 1: Producer-Consumer Pattern

Thread synchronization implementation using Python's queue module. Demonstrates proper thread communication and synchronization with multiple producers and consumers.

The implementation uses Python's queue.Queue which handles thread safety and blocking automatically. When the queue is full, put() blocks until space is available. When it's empty, get() blocks until an item is available. No manual locks are needed for queue operations.

Four main classes make up the implementation. SharedQueue wraps queue.Queue with max capacity. Producer threads read from a source and put items in the queue. Consumer threads get items from the queue and store them in a destination. ProducerConsumer orchestrates everything together.

The sentinel pattern is used for clean shutdown. Each producer puts a sentinel value (None) into the queue when finished. Consumers stop immediately when they see a sentinel. ProducerConsumer ensures there are enough sentinels for all consumers by adding extras if needed.

### Setup and Usage

Run the example:
```bash
cd assignment1
python producer_consumer.py
```

The program creates a producer-consumer system with 2 producers and 2 consumers, processes 50 items, and prints statistics to the console.

### Sample Output

```
Starting producer-consumer system...
Producer 1 finished. Produced 25 items.
Consumer 1 finished. Consumed 25 items.
Producer 2 finished. Produced 25 items.
Consumer 2 finished. Consumed 25 items.

=== Statistics ===
Total produced: 50
Total consumed: 50
Items in destination: 50
Queue size: 0

✓ All items successfully transferred!
```

Note: The order of producer/consumer completion messages may vary due to thread scheduling.

### Testing

```bash
pytest assignment1/test_producer_consumer.py -v
```

Tests cover single producer/consumer, multiple producers with single consumer, single producer with multiple consumers, multiple producers and consumers, queue capacity limits, thread synchronization correctness, graceful shutdown, and edge cases like empty source and concurrent access.

## Assignment 2: CSV Data Analysis with Functional Programming

CSV data analysis implementation using functional programming paradigms. Reads sales transaction data from CSV and performs various analytical queries using map, filter, reduce, and other functional programming constructs.

The CSV file contains sales transaction data with transaction_id, date, product_name, category, region, salesperson, quantity, unit_price, and total_amount fields. Dates are in YYYY-MM-DD format.

The analysis module implements six analytical queries. Total revenue by product groups transactions by product and sums total revenue. Total revenue by category does the same but groups by category. Top 5 salespeople by revenue groups by salesperson, sums revenue, and returns the top 5. Sales by region groups transactions by region and sums total sales. Average transaction value calculates the mean transaction amount across all transactions. Monthly sales trend groups transactions by month and sums revenue.

All functions use functional programming patterns. reduce() with accumulator functions handles grouping and aggregation. map() transforms data. sorted() with lambda functions handles ordering. List comprehensions are used where appropriate.

### Setup and Usage

First, generate the sample data:
```bash
cd assignment2
python generate_data.py
```

This creates a CSV file at `data/sales_data.csv` with 150 sales transactions.

Then run the analysis:
```bash
python data_analyzer.py
```

The program loads the CSV data, performs all six analytical queries, and prints the results to the console.

### Sample Output

Running `python data_analyzer.py` prints all six analysis results to the console. Note that since data is randomly generated, the actual numbers will vary each time you run generate_data.py, but the format and structure remain the same:

```
============================================================
SALES DATA ANALYSIS RESULTS
============================================================

1. Total Revenue by Product:
------------------------------------------------------------
  Notebook Set                   $   15,303.65
  Keyboard                       $   10,995.71
  Office Chair                   $   10,551.51
  Wireless Mouse                 $   10,485.92
  Pen Collection                 $    9,583.36
  Blender                        $    8,865.06
  Desk Lamp                      $    8,589.54
  Standing Desk                  $    8,280.33
  USB-C Cable                    $    7,716.71
  Laptop Pro                     $    7,440.59
  Toaster                        $    6,802.75
  Desk Organizer                 $    6,278.99
  Monitor Stand                  $    4,682.47
  Coffee Maker                   $    3,525.88

2. Total Revenue by Category:
------------------------------------------------------------
  Electronics                    $   36,638.93
  Furniture                      $   32,103.85
  Office Supplies                $   31,166.00
  Appliances                     $   19,193.69

3. Top 5 Salespeople by Revenue:
------------------------------------------------------------
  1. Carol Williams                 $   20,802.96
  2. Frank Miller                   $   16,254.70
  3. Bob Smith                      $   14,881.92
  4. Alice Johnson                  $   13,460.98
  5. Henry Moore                    $   12,872.29

4. Sales by Region:
------------------------------------------------------------
  East                           $   30,677.64
  North                          $   25,753.10
  South                          $   23,144.65
  Central                        $   20,235.03
  West                           $   19,292.05

5. Average Transaction Value:
------------------------------------------------------------
  $794.02

6. Monthly Sales Trend:
------------------------------------------------------------
  2024-01                        $   22,690.93
  2024-02                        $   26,988.20
  2024-03                        $   14,922.34
  2024-04                        $   18,280.91
  2024-05                        $   15,652.89
  2024-06                        $   20,567.20

============================================================
```

All six analyses are printed to the console in the order shown above.

### Testing

```bash
pytest assignment2/test_data_analyzer.py -v
```

The test suite includes 12 test cases covering all 6 analysis functions with sample data, edge cases like empty lists and single transactions, CSV loading functionality, multiple month scenarios, and top N count validation. All tests pass and validate that functional programming patterns work correctly.

## Running All Tests

Run all tests for both assignments:
```bash
pytest assignment1/test_producer_consumer.py assignment2/test_data_analyzer.py -v
```

## Repository Structure

```
.
├── assignment1/
│   ├── producer_consumer.py
│   └── test_producer_consumer.py
├── assignment2/
│   ├── generate_data.py
│   ├── data_analyzer.py
│   ├── test_data_analyzer.py
│   └── data/
│       └── sales_data.csv
└── README.md
```

## Design Philosophy

Assignment 1 demonstrates thread synchronization using Python's built-in queue.Queue, which handles all synchronization automatically. The sentinel pattern is used for clean shutdown logic, eliminating race conditions.

Assignment 2 emphasizes functional programming patterns over imperative loops, making the code more declarative and easier to reason about. All analysis functions use reduce, map, sorted, and lambda functions rather than traditional loops.

Both assignments include comprehensive test coverage.
