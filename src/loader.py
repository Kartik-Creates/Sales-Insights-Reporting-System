import sqlite3
from .data_generator import DataGenerator

def load_generated_data(conn):
    """Load generated synthetic data into database"""
    cursor = conn.cursor()
    generator = DataGenerator()
    
    print("Generating 200 customers...")
    customers = generator.generate_customers(200)
    for customer in customers:
        cursor.execute(
            "INSERT INTO customers (customer_id, name, email, city, state) VALUES (?, ?, ?, ?, ?)",
            (customer['customer_id'], customer['name'], customer['email'], 
             customer['city'], customer['state'])
        )
    
    print("Generating 50 products...")
    products = generator.generate_products(50)
    for product in products:
        cursor.execute(
            "INSERT INTO products (product_id, product_name, category, unit_price) VALUES (?, ?, ?, ?)",
            (product['product_id'], product['product_name'], product['category'], 
             product['unit_price'])
        )
    
    print("Generating 2000 orders...")
    orders = generator.generate_orders(200, 2000)
    for order in orders:
        cursor.execute(
            "INSERT INTO orders (order_id, customer_id, order_date) VALUES (?, ?, ?)",
            (order['order_id'], order['customer_id'], order['order_date'])
        )
    
    print("Generating 5000+ order items...")
    order_items = generator.generate_order_items(2000, 50, 5000)
    for item in order_items:
        cursor.execute(
            """INSERT INTO order_items (order_item_id, order_id, product_id, quantity, discount_percent) 
               VALUES (?, ?, ?, ?, ?)""",
            (item['order_item_id'], item['order_id'], item['product_id'], 
             item['quantity'], item['discount_percent'])
        )
    
    conn.commit()
    print(f"✅ Data loaded successfully!")
    print(f"   Customers: {len(customers)}")
    print(f"   Products: {len(products)}")
    print(f"   Orders: {len(orders)}")
    print(f"   Order Items: {len(order_items)}")