"""
Unit tests for CSV Data Analysis functions.

Tests all analytical queries using functional programming patterns.
"""

import unittest
import sys
import os
import tempfile
import csv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_analyzer import (
    load_csv_data,
    total_revenue_by_product,
    total_revenue_by_category,
    top_salespeople_by_revenue,
    sales_by_region,
    average_transaction_value,
    monthly_sales_trend,
)


class TestDataAnalyzer(unittest.TestCase):
    """Test data analysis functions."""
    
    def setUp(self):
        """Create sample test data."""
        self.sample_transactions = [
            {
                "transaction_id": "TXN-0001",
                "date": "2024-01-15",
                "product_name": "Laptop Pro",
                "category": "Electronics",
                "region": "North",
                "salesperson": "Alice Johnson",
                "quantity": "2",
                "unit_price": "500.00",
                "total_amount": "1000.00",
            },
            {
                "transaction_id": "TXN-0002",
                "date": "2024-01-20",
                "product_name": "Laptop Pro",
                "category": "Electronics",
                "region": "South",
                "salesperson": "Bob Smith",
                "quantity": "1",
                "unit_price": "500.00",
                "total_amount": "500.00",
            },
            {
                "transaction_id": "TXN-0003",
                "date": "2024-02-10",
                "product_name": "Office Chair",
                "category": "Furniture",
                "region": "North",
                "salesperson": "Alice Johnson",
                "quantity": "3",
                "unit_price": "200.00",
                "total_amount": "600.00",
            },
            {
                "transaction_id": "TXN-0004",
                "date": "2024-02-15",
                "product_name": "Coffee Maker",
                "category": "Appliances",
                "region": "South",
                "salesperson": "Bob Smith",
                "quantity": "2",
                "unit_price": "150.00",
                "total_amount": "300.00",
            },
        ]
    
    def test_load_csv_data(self):
        """Test loading CSV data."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
            writer = csv.DictWriter(f, fieldnames=self.sample_transactions[0].keys())
            writer.writeheader()
            writer.writerows(self.sample_transactions)
            temp_filename = f.name
        
        try:
            loaded_data = load_csv_data(temp_filename)
            self.assertEqual(len(loaded_data), 4)
            self.assertEqual(loaded_data[0]["product_name"], "Laptop Pro")
        finally:
            os.unlink(temp_filename)
    
    def test_total_revenue_by_product(self):
        """Test total revenue grouped by product."""
        result = total_revenue_by_product(self.sample_transactions)
        
        self.assertEqual(result["Laptop Pro"], 1500.00)
        self.assertEqual(result["Office Chair"], 600.00)
        self.assertEqual(result["Coffee Maker"], 300.00)
        self.assertEqual(len(result), 3)
    
    def test_total_revenue_by_category(self):
        """Test total revenue grouped by category."""
        result = total_revenue_by_category(self.sample_transactions)
        
        self.assertEqual(result["Electronics"], 1500.00)
        self.assertEqual(result["Furniture"], 600.00)
        self.assertEqual(result["Appliances"], 300.00)
        self.assertEqual(len(result), 3)
    
    def test_top_salespeople_by_revenue(self):
        """Test top salespeople by revenue."""
        result = top_salespeople_by_revenue(self.sample_transactions, top_n=2)
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][0], "Alice Johnson")
        self.assertEqual(result[0][1], 1600.00)
        self.assertEqual(result[1][0], "Bob Smith")
        self.assertEqual(result[1][1], 800.00)
    
    def test_top_salespeople_returns_correct_count(self):
        """Test that top_salespeople returns requested number."""
        result = top_salespeople_by_revenue(self.sample_transactions, top_n=1)
        self.assertEqual(len(result), 1)
        
        result = top_salespeople_by_revenue(self.sample_transactions, top_n=10)
        self.assertEqual(len(result), 2)
    
    def test_sales_by_region(self):
        """Test sales grouped by region."""
        result = sales_by_region(self.sample_transactions)
        
        self.assertEqual(result["North"], 1600.00)
        self.assertEqual(result["South"], 800.00)
        self.assertEqual(len(result), 2)
    
    def test_average_transaction_value(self):
        """Test average transaction value calculation."""
        result = average_transaction_value(self.sample_transactions)
        
        expected_avg = (1000.00 + 500.00 + 600.00 + 300.00) / 4
        self.assertEqual(result, expected_avg)
    
    def test_average_transaction_value_empty_list(self):
        """Test average transaction value with empty list."""
        result = average_transaction_value([])
        self.assertEqual(result, 0.0)
    
    def test_monthly_sales_trend(self):
        """Test monthly sales trend grouping."""
        result = monthly_sales_trend(self.sample_transactions)
        
        self.assertEqual(result["2024-01"], 1500.00)
        self.assertEqual(result["2024-02"], 900.00)
        self.assertEqual(len(result), 2)
    
    def test_monthly_sales_trend_multiple_months(self):
        """Test monthly trend with transactions spanning multiple months."""
        transactions = [
            {
                "transaction_id": "TXN-0001",
                "date": "2024-01-15",
                "product_name": "Product A",
                "category": "Category",
                "region": "North",
                "salesperson": "Alice",
                "quantity": "1",
                "unit_price": "100.00",
                "total_amount": "100.00",
            },
            {
                "transaction_id": "TXN-0002",
                "date": "2024-01-20",
                "product_name": "Product B",
                "category": "Category",
                "region": "South",
                "salesperson": "Bob",
                "quantity": "1",
                "unit_price": "200.00",
                "total_amount": "200.00",
            },
            {
                "transaction_id": "TXN-0003",
                "date": "2024-02-10",
                "product_name": "Product C",
                "category": "Category",
                "region": "North",
                "salesperson": "Alice",
                "quantity": "1",
                "unit_price": "300.00",
                "total_amount": "300.00",
            },
        ]
        
        result = monthly_sales_trend(transactions)
        self.assertEqual(result["2024-01"], 300.00)
        self.assertEqual(result["2024-02"], 300.00)
    
    def test_empty_transactions(self):
        """Test all functions with empty transaction list."""
        empty_list = []
        
        self.assertEqual(total_revenue_by_product(empty_list), {})
        self.assertEqual(total_revenue_by_category(empty_list), {})
        self.assertEqual(top_salespeople_by_revenue(empty_list), [])
        self.assertEqual(sales_by_region(empty_list), {})
        self.assertEqual(average_transaction_value(empty_list), 0.0)
        self.assertEqual(monthly_sales_trend(empty_list), {})
    
    def test_single_transaction(self):
        """Test all functions with single transaction."""
        single_transaction = [self.sample_transactions[0]]
        
        result_product = total_revenue_by_product(single_transaction)
        self.assertEqual(result_product["Laptop Pro"], 1000.00)
        
        result_category = total_revenue_by_category(single_transaction)
        self.assertEqual(result_category["Electronics"], 1000.00)
        
        result_salespeople = top_salespeople_by_revenue(single_transaction, top_n=1)
        self.assertEqual(result_salespeople[0][0], "Alice Johnson")
        self.assertEqual(result_salespeople[0][1], 1000.00)
        
        result_region = sales_by_region(single_transaction)
        self.assertEqual(result_region["North"], 1000.00)
        
        result_avg = average_transaction_value(single_transaction)
        self.assertEqual(result_avg, 1000.00)
        
        result_monthly = monthly_sales_trend(single_transaction)
        self.assertEqual(result_monthly["2024-01"], 1000.00)


if __name__ == "__main__":
    unittest.main()

