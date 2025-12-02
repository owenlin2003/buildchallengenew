"""
Generate synthetic sales data CSV for analysis.

Creates a CSV file with sales transaction data including:
- transaction_id, date, product_name, category, region, salesperson,
  quantity, unit_price, total_amount
"""

import csv
import random
from datetime import datetime, timedelta

PRODUCTS = [
    ("Laptop Pro", "Electronics"),
    ("Wireless Mouse", "Electronics"),
    ("USB-C Cable", "Electronics"),
    ("Office Chair", "Furniture"),
    ("Desk Lamp", "Furniture"),
    ("Standing Desk", "Furniture"),
    ("Coffee Maker", "Appliances"),
    ("Blender", "Appliances"),
    ("Toaster", "Appliances"),
    ("Notebook Set", "Office Supplies"),
    ("Pen Collection", "Office Supplies"),
    ("Desk Organizer", "Office Supplies"),
    ("Monitor Stand", "Furniture"),
    ("Keyboard", "Electronics"),
]

REGIONS = ["North", "South", "East", "West", "Central"]

SALESPEOPLE = [
    "Alice Johnson",
    "Bob Smith",
    "Carol Williams",
    "David Brown",
    "Emma Davis",
    "Frank Miller",
    "Grace Wilson",
    "Henry Moore",
    "Ivy Taylor",
]

def generate_sales_data(num_records=150):
    """Generate synthetic sales transaction data."""
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 6, 30)
    date_range = (end_date - start_date).days
    
    records = []
    
    for i in range(1, num_records + 1):
        transaction_date = start_date + timedelta(days=random.randint(0, date_range))
        product_name, category = random.choice(PRODUCTS)
        region = random.choice(REGIONS)
        salesperson = random.choice(SALESPEOPLE)
        quantity = random.randint(1, 5)
        unit_price = round(random.uniform(10.0, 500.0), 2)
        total_amount = round(quantity * unit_price, 2)
        
        records.append({
            "transaction_id": f"TXN-{i:04d}",
            "date": transaction_date.strftime("%Y-%m-%d"),
            "product_name": product_name,
            "category": category,
            "region": region,
            "salesperson": salesperson,
            "quantity": quantity,
            "unit_price": unit_price,
            "total_amount": total_amount,
        })
    
    return records

def write_csv(filename, records):
    """Write records to CSV file."""
    fieldnames = [
        "transaction_id",
        "date",
        "product_name",
        "category",
        "region",
        "salesperson",
        "quantity",
        "unit_price",
        "total_amount",
    ]
    
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

if __name__ == "__main__":
    records = generate_sales_data(150)
    write_csv("data/sales_data.csv", records)
    print(f"Generated {len(records)} sales records in data/sales_data.csv")

