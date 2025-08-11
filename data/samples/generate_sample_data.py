"""
Sample sales data for testing BI Assistant
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


def generate_sales_data(num_records: int = 1000) -> pd.DataFrame:
    """
    Generate sample sales data for testing
    
    Args:
        num_records (int): Number of records to generate
        
    Returns:
        pd.DataFrame: Sample sales dataset
    """
    
    # Set random seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    # Generate date range
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Product categories and names
    categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books', 'Toys']
    products = {
        'Electronics': ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Smart Watch'],
        'Clothing': ['T-Shirt', 'Jeans', 'Dress', 'Shoes', 'Jacket'],
        'Home & Garden': ['Sofa', 'Table', 'Lamp', 'Plant', 'Curtains'],
        'Sports': ['Basketball', 'Tennis Racket', 'Running Shoes', 'Yoga Mat', 'Bicycle'],
        'Books': ['Fiction Novel', 'Cookbook', 'Biography', 'Textbook', 'Comic Book'],
        'Toys': ['Board Game', 'Action Figure', 'Puzzle', 'Doll', 'Building Blocks']
    }
    
    # Sales regions
    regions = ['North', 'South', 'East', 'West', 'Central']
    
    # Generate sample data
    data = []
    
    for _ in range(num_records):
        category = random.choice(categories)
        product = random.choice(products[category])
        region = random.choice(regions)
        
        # Generate realistic sales data with some patterns
        base_price = {
            'Electronics': random.uniform(100, 2000),
            'Clothing': random.uniform(20, 200),
            'Home & Garden': random.uniform(50, 1000),
            'Sports': random.uniform(15, 500),
            'Books': random.uniform(10, 50),
            'Toys': random.uniform(5, 100)
        }[category]
        
        quantity = random.randint(1, 10)
        discount = random.uniform(0, 0.3)  # 0-30% discount
        unit_price = base_price * (1 - discount)
        total_amount = unit_price * quantity
        
        # Add some seasonality
        sale_date = random.choice(date_range)
        if sale_date.month in [11, 12]:  # Holiday season
            total_amount *= random.uniform(1.1, 1.5)  # 10-50% boost
        
        data.append({
            'order_id': f'ORD-{random.randint(10000, 99999)}',
            'date': sale_date,
            'category': category,
            'product_name': product,
            'region': region,
            'quantity': quantity,
            'unit_price': round(unit_price, 2),
            'total_amount': round(total_amount, 2),
            'discount_percent': round(discount * 100, 1),
            'customer_id': f'CUST-{random.randint(1000, 9999)}',
            'sales_rep': f'Rep_{random.randint(1, 20)}',
            'payment_method': random.choice(['Credit Card', 'Debit Card', 'Cash', 'Online']),
            'shipping_cost': round(random.uniform(5, 25), 2) if category != 'Books' else round(random.uniform(2, 8), 2)
        })
    
    df = pd.DataFrame(data)
    
    # Add some missing values to simulate real-world data
    missing_indices = random.sample(range(len(df)), int(len(df) * 0.02))  # 2% missing
    for idx in missing_indices:
        df.loc[idx, random.choice(['sales_rep', 'payment_method'])] = np.nan
    
    # Add some duplicate orders (same customer, same day, same product)
    duplicate_indices = random.sample(range(len(df)), int(len(df) * 0.01))  # 1% duplicates
    for idx in duplicate_indices:
        if idx + 1 < len(df):
            df.loc[idx + 1, ['customer_id', 'date', 'product_name']] = df.loc[idx, ['customer_id', 'date', 'product_name']].values
    
    return df


if __name__ == "__main__":
    # Generate and save sample data
    sales_data = generate_sales_data(1000)
    
    # Save as CSV
    sales_data.to_csv('data/samples/sample_sales_data.csv', index=False)
    
    # Save as Excel
    sales_data.to_excel('data/samples/sample_sales_data.xlsx', index=False)
    
    print(f"Generated {len(sales_data)} sales records")
    print(f"Date range: {sales_data['date'].min()} to {sales_data['date'].max()}")
    print(f"Categories: {sales_data['category'].unique()}")
    print(f"Total sales amount: ${sales_data['total_amount'].sum():,.2f}")
