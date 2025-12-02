# Assignment 2: CSV Data Analysis with Functional Programming

CSV data analysis implementation using functional programming paradigms. Reads sales transaction data from CSV and performs various analytical queries using map, filter, reduce, and other functional programming constructs.

The CSV file contains sales transaction data with transaction_id, date, product_name, category, region, salesperson, quantity, unit_price, and total_amount fields. Dates are in YYYY-MM-DD format.

The analysis module implements six analytical queries. Total revenue by product groups transactions by product and sums total revenue. Total revenue by category does the same but groups by category. Top 5 salespeople by revenue groups by salesperson, sums revenue, and returns the top 5. Sales by region groups transactions by region and sums total sales. Average transaction value calculates the mean transaction amount across all transactions. Monthly sales trend groups transactions by month and sums revenue.

All functions use functional programming patterns. reduce() with accumulator functions handles grouping and aggregation. map() transforms data. sorted() with lambda functions handles ordering. List comprehensions are used where appropriate.

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

All analysis functions use functional programming patterns rather than imperative loops. This makes the code more declarative and easier to reason about. Grouping operations use reduce() with accumulator functions that build dictionaries incrementally, which is more functional than using defaultdict or manual loops.

Functions take lists of dictionaries and return new data structures without modifying input, following functional programming principles. Lambda functions are used with sorted() and map() for concise transformations. The implementation uses only Python standard library to keep things simple and portable.

## Testing

The test suite includes 12 test cases covering all 6 analysis functions with sample data, edge cases like empty lists and single transactions, CSV loading functionality, multiple month scenarios, and top N count validation. All tests pass and validate that functional programming patterns work correctly.

## Data Generation

The generate_data.py script creates synthetic sales data with 150 transactions, 14 products across 4 categories, 5 regions, 9 salespeople, and dates spanning 6 months from January to June 2024. Data is randomly generated but maintains realistic relationships like total_amount equaling quantity times unit_price.
