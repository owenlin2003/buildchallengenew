# Assignment 2: CSV Data Analysis with Functional Programming

CSV data analysis implementation using functional programming paradigms. Reads sales transaction data from CSV and performs various analytical queries using map, filter, reduce, and other functional programming constructs.

## Features

- CSV data loading and parsing
- Six analytical queries using functional programming patterns
- Grouping and aggregation operations
- Sorting and filtering operations
- Comprehensive unit test coverage

## Dataset Structure

The CSV file contains sales transaction data with the following fields:

- `transaction_id`: Unique transaction identifier
- `date`: Transaction date (YYYY-MM-DD format)
- `product_name`: Name of the product sold
- `category`: Product category
- `region`: Sales region
- `salesperson`: Name of the salesperson
- `quantity`: Quantity sold
- `unit_price`: Price per unit
- `total_amount`: Total transaction amount (quantity * unit_price)

## Implementation

The analysis module (`data_analyzer.py`) implements six analytical queries:

1. **Total Revenue by Product**: Groups transactions by product and sums total revenue
2. **Total Revenue by Category**: Groups transactions by category and sums total revenue
3. **Top 5 Salespeople by Revenue**: Groups by salesperson, sums revenue, and returns top 5
4. **Sales by Region**: Groups transactions by region and sums total sales
5. **Average Transaction Value**: Calculates mean transaction amount across all transactions
6. **Monthly Sales Trend**: Groups transactions by month and sums revenue

All functions use functional programming patterns:
- `reduce()` with accumulator functions for grouping and aggregation
- `map()` for data transformation
- `sorted()` with lambda functions for ordering
- List comprehensions where appropriate

## Usage

Generate sample data:
```bash
cd assignment2
python generate_data.py
```

Run analysis:
```bash
python data_analyzer.py
```

Run tests:
```bash
pytest assignment2/test_data_analyzer.py -v
```

## Sample Output

```
============================================================
SALES DATA ANALYSIS RESULTS
============================================================

1. Total Revenue by Product:
------------------------------------------------------------
  Laptop Pro                     $   12,574.35
  Desk Lamp                      $   11,367.88
  Keyboard                       $   10,880.33
  Notebook Set                   $   10,484.57
  Wireless Mouse                 $    9,869.49
  Coffee Maker                   $    9,244.76
  Blender                        $    8,555.57
  Desk Organizer                 $    8,398.22
  Toaster                        $    7,571.60
  Pen Collection                 $    7,562.24
  Standing Desk                  $    6,915.53
  Monitor Stand                  $    6,557.84
  Office Chair                   $    4,118.70
  USB-C Cable                    $    4,104.87

2. Total Revenue by Category:
------------------------------------------------------------
  Electronics                    $   37,429.04
  Furniture                      $   28,959.95
  Office Supplies                $   26,445.03
  Appliances                     $   25,371.93

3. Top 5 Salespeople by Revenue:
------------------------------------------------------------
  1. Frank Miller                   $   21,880.60
  2. Carol Williams                 $   18,134.12
  3. Grace Wilson                   $   15,387.50
  4. Emma Davis                     $   12,923.35
  5. David Brown                    $   11,454.36

4. Sales by Region:
------------------------------------------------------------
  South                          $   28,889.73
  North                          $   25,528.16
  East                           $   24,222.60
  West                           $   21,819.18
  Central                        $   17,746.28

5. Average Transaction Value:
------------------------------------------------------------
  $788.04

6. Monthly Sales Trend:
------------------------------------------------------------
  2024-01                        $   18,305.06
  2024-02                        $   20,206.26
  2024-03                        $   22,159.82
  2024-04                        $   14,498.63
  2024-05                        $   17,749.43
  2024-06                        $   25,286.75

============================================================
```

## Design Decisions

**Functional Programming Approach**: All analysis functions use functional programming patterns (reduce, map, sorted) rather than imperative loops. This makes the code more declarative and easier to reason about.

**Reduce for Aggregation**: Grouping operations use `reduce()` with accumulator functions that build dictionaries incrementally. This is more functional than using defaultdict or manual loops.

**Immutable Data Structures**: Functions take lists of dictionaries and return new data structures without modifying input, following functional programming principles.

**Lambda Functions**: Used with `sorted()` and `map()` for concise, functional transformations.

**No External Dependencies**: Uses only Python standard library (csv, functools, collections) to keep the implementation simple and portable.

## Testing

The test suite (`test_data_analyzer.py`) includes 12 test cases covering:
- All 6 analysis functions with sample data
- Edge cases (empty lists, single transactions)
- CSV loading functionality
- Multiple month scenarios
- Top N count validation

All tests pass and validate that functional programming patterns work correctly.

## Data Generation

The `generate_data.py` script creates synthetic sales data with:
- 150 transactions
- 14 products across 4 categories
- 5 regions
- 9 salespeople
- Dates spanning 6 months (January - June 2024)

Data is randomly generated but maintains realistic relationships (e.g., total_amount = quantity * unit_price).

