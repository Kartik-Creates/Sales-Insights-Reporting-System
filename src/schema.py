import sqlite3

def create_tables(conn):
    """Create all database tables with proper constraints and indexes"""
    
    cursor = conn.cursor()
    
    # Drop tables if they exist (for clean setup)
    tables = ['order_items', 'orders', 'products', 'customers']
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")
    
    # Create customers table
    cursor.execute('''
    CREATE TABLE customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        city TEXT NOT NULL,
        state TEXT NOT NULL
    )
    ''')
    
    # Create products table
    cursor.execute('''
    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT NOT NULL,
        category TEXT NOT NULL,
        unit_price DECIMAL(10, 2) NOT NULL CHECK (unit_price >= 0)
    )
    ''')
    
    # Create orders table
    cursor.execute('''
    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        order_date DATE NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
    )
    ''')
    
    # Create order_items table
    cursor.execute('''
    CREATE TABLE order_items (
        order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL CHECK (quantity > 0),
        discount_percent DECIMAL(5, 2) DEFAULT 0 CHECK (discount_percent >= 0 AND discount_percent <= 100),
        FOREIGN KEY (order_id) REFERENCES orders (order_id),
        FOREIGN KEY (product_id) REFERENCES products (product_id)
    )
    ''')
    
    # Create indexes for performance
    indexes = [
        'CREATE INDEX idx_orders_customer ON orders(customer_id)',
        'CREATE INDEX idx_orders_date ON orders(order_date)',
        'CREATE INDEX idx_order_items_order ON order_items(order_id)',
        'CREATE INDEX idx_order_items_product ON order_items(product_id)',
        'CREATE INDEX idx_customers_state ON customers(state)',
        'CREATE INDEX idx_products_category ON products(category)'
    ]
    
    for index_sql in indexes:
        cursor.execute(index_sql)
    
    conn.commit()
    print("Database schema created successfully with 6 indexes")