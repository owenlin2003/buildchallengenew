"""
CSV Data Analysis using Functional Programming Patterns.

Performs various analytical queries on sales data using map, filter, reduce,
and other functional programming constructs.
"""

import csv
from collections import defaultdict
from functools import reduce
from datetime import datetime
from typing import List, Dict, Tuple


def load_csv_data(filename: str) -> List[Dict[str, str]]:
    """
    Load CSV data into a list of dictionaries.
    
    Args:
        filename: Path to CSV file
        
    Returns:
        List of dictionaries, one per row
    """
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        return list(reader)


def total_revenue_by_product(transactions: List[Dict[str, str]]) -> Dict[str, float]:
    """
    Calculate total revenue grouped by product name.
    
    Uses functional programming: map to extract product and amount,
    then reduce to sum by product.
    
    Args:
        transactions: List of transaction dictionaries
        
    Returns:
        Dictionary mapping product names to total revenue
    """
    def add_to_product(acc, transaction):
        product = transaction["product_name"]
        amount = float(transaction["total_amount"])
        acc[product] = acc.get(product, 0) + amount
        return acc
    
    return reduce(add_to_product, transactions, {})


def total_revenue_by_category(transactions: List[Dict[str, str]]) -> Dict[str, float]:
    """
    Calculate total revenue grouped by category.
    
    Args:
        transactions: List of transaction dictionaries
        
    Returns:
        Dictionary mapping categories to total revenue
    """
    def add_to_category(acc, transaction):
        category = transaction["category"]
        amount = float(transaction["total_amount"])
        acc[category] = acc.get(category, 0) + amount
        return acc
    
    return reduce(add_to_category, transactions, {})


def top_salespeople_by_revenue(transactions: List[Dict[str, str]], top_n: int = 5) -> List[Tuple[str, float]]:
    """
    Find top N salespeople by total revenue.
    
    Uses map/reduce to calculate totals, then sorts functionally.
    
    Args:
        transactions: List of transaction dictionaries
        top_n: Number of top salespeople to return
        
    Returns:
        List of tuples (salesperson, revenue) sorted by revenue descending
    """
    def add_to_salesperson(acc, transaction):
        salesperson = transaction["salesperson"]
        amount = float(transaction["total_amount"])
        acc[salesperson] = acc.get(salesperson, 0) + amount
        return acc
    
    revenue_by_person = reduce(add_to_salesperson, transactions, {})
    
    sorted_items = sorted(
        revenue_by_person.items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    return sorted_items[:top_n]


def sales_by_region(transactions: List[Dict[str, str]]) -> Dict[str, float]:
    """
    Calculate total sales grouped by region.
    
    Args:
        transactions: List of transaction dictionaries
        
    Returns:
        Dictionary mapping regions to total sales
    """
    def add_to_region(acc, transaction):
        region = transaction["region"]
        amount = float(transaction["total_amount"])
        acc[region] = acc.get(region, 0) + amount
        return acc
    
    return reduce(add_to_region, transactions, {})


def average_transaction_value(transactions: List[Dict[str, str]]) -> float:
    """
    Calculate average transaction value.
    
    Uses map to extract amounts, then calculates average functionally.
    
    Args:
        transactions: List of transaction dictionaries
        
    Returns:
        Average transaction value
    """
    amounts = list(map(lambda t: float(t["total_amount"]), transactions))
    
    if not amounts:
        return 0.0
    
    total = reduce(lambda x, y: x + y, amounts, 0.0)
    return total / len(amounts)


def monthly_sales_trend(transactions: List[Dict[str, str]]) -> Dict[str, float]:
    """
    Calculate monthly sales trend.
    
    Groups transactions by month and sums revenue.
    
    Args:
        transactions: List of transaction dictionaries
        
    Returns:
        Dictionary mapping month strings (YYYY-MM) to total revenue
    """
    def add_to_month(acc, transaction):
        date_str = transaction["date"]
        month = date_str[:7]
        amount = float(transaction["total_amount"])
        acc[month] = acc.get(month, 0) + amount
        return acc
    
    return reduce(add_to_month, transactions, {})


def print_analysis_results(transactions: List[Dict[str, str]]) -> None:
    """
    Print all analysis results to console.
    
    Args:
        transactions: List of transaction dictionaries
    """
    print("=" * 60)
    print("SALES DATA ANALYSIS RESULTS")
    print("=" * 60)
    
    print("\n1. Total Revenue by Product:")
    print("-" * 60)
    revenue_by_product = total_revenue_by_product(transactions)
    for product, revenue in sorted(revenue_by_product.items(), key=lambda x: x[1], reverse=True):
        print(f"  {product:30s} ${revenue:>12,.2f}")
    
    print("\n2. Total Revenue by Category:")
    print("-" * 60)
    revenue_by_category = total_revenue_by_category(transactions)
    for category, revenue in sorted(revenue_by_category.items(), key=lambda x: x[1], reverse=True):
        print(f"  {category:30s} ${revenue:>12,.2f}")
    
    print("\n3. Top 5 Salespeople by Revenue:")
    print("-" * 60)
    top_salespeople = top_salespeople_by_revenue(transactions, 5)
    for i, (salesperson, revenue) in enumerate(top_salespeople, 1):
        print(f"  {i}. {salesperson:30s} ${revenue:>12,.2f}")
    
    print("\n4. Sales by Region:")
    print("-" * 60)
    sales_by_reg = sales_by_region(transactions)
    for region, revenue in sorted(sales_by_reg.items(), key=lambda x: x[1], reverse=True):
        print(f"  {region:30s} ${revenue:>12,.2f}")
    
    print("\n5. Average Transaction Value:")
    print("-" * 60)
    avg_value = average_transaction_value(transactions)
    print(f"  ${avg_value:,.2f}")
    
    print("\n6. Monthly Sales Trend:")
    print("-" * 60)
    monthly_trend = monthly_sales_trend(transactions)
    for month in sorted(monthly_trend.keys()):
        revenue = monthly_trend[month]
        print(f"  {month:30s} ${revenue:>12,.2f}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    transactions = load_csv_data("data/sales_data.csv")
    print_analysis_results(transactions)

