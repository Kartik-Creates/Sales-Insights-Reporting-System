import random
import datetime

class DataGenerator:
    def __init__(self):
        # Sample data for realistic generation
        self.categories = ['Electronics', 'Clothing', 'Books', 'Home & Garden', 
                          'Sports', 'Toys', 'Beauty', 'Food']
        
        self.products_data = {
            'Electronics': ['Smartphone', 'Laptop', 'Headphones', 'Tablet'],
            'Clothing': ['T-Shirt', 'Jeans', 'Jacket', 'Dress'],
            'Books': ['Novel', 'Textbook', 'Biography', 'Cookbook'],
            'Home & Garden': ['Lamp', 'Chair', 'Plant', 'Cookware'],
            'Sports': ['Basketball', 'Yoga Mat', 'Running Shoes', 'Bicycle'],
            'Toys': ['Lego Set', 'Doll', 'Puzzle', 'Board Game'],
            'Beauty': ['Shampoo', 'Perfume', 'Makeup Kit', 'Hair Dryer'],
            'Food': ['Chocolate', 'Coffee', 'Snacks', 'Tea']
        }
        
        self.states = ['CA', 'TX', 'NY', 'FL', 'IL']
        self.cities_by_state = {
            'CA': ['Los Angeles', 'San Francisco', 'San Diego'],
            'TX': ['Houston', 'Dallas', 'Austin'],
            'NY': ['New York', 'Buffalo', 'Rochester'],
            'FL': ['Miami', 'Orlando', 'Tampa'],
            'IL': ['Chicago', 'Springfield', 'Peoria']
        }
        
        # Common first and last names
        self.first_names = ['James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 
                           'Michael', 'Linda', 'William', 'Elizabeth']
        self.last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 
                          'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
    
    def generate_customers(self, count=200):
        """Generate customer data"""
        customers = []
        used_emails = set()
        
        for i in range(1, count + 1):
            state = random.choice(self.states)
            city = random.choice(self.cities_by_state[state])
            name = f"{random.choice(self.first_names)} {random.choice(self.last_names)}"
            
            # Generate unique email
            email_num = i
            email = f"{name.lower().replace(' ', '.')}{email_num}@example.com"
            while email in used_emails:
                email_num += 1
                email = f"{name.lower().replace(' ', '.')}{email_num}@example.com"
            used_emails.add(email)
            
            customers.append({
                'customer_id': i,
                'name': name,
                'email': email,
                'city': city,
                'state': state
            })
        
        return customers
    
    def generate_products(self, count=50):
        """Generate product data"""
        products = []
        product_id = 1
        
        for category in self.categories:
            category_products = self.products_data[category]
            for product_name in category_products:
                if product_id > count:
                    break
                
                # Generate realistic prices based on category
                base_prices = {
                    'Electronics': (300, 1500),
                    'Clothing': (20, 150),
                    'Books': (10, 40),
                    'Home & Garden': (25, 300),
                    'Sports': (30, 200),
                    'Toys': (15, 80),
                    'Beauty': (10, 120),
                    'Food': (5, 40)
                }
                
                min_price, max_price = base_prices[category]
                unit_price = round(random.uniform(min_price, max_price), 2)
                
                products.append({
                    'product_id': product_id,
                    'product_name': f"{product_name} {random.randint(1, 5)}",
                    'category': category,
                    'unit_price': unit_price
                })
                product_id += 1
        
        # Fill remaining products if needed
        while product_id <= count:
            category = random.choice(self.categories)
            product_name = f"Generic {category} Item {product_id}"
            min_price, max_price = 10, 200
            unit_price = round(random.uniform(min_price, max_price), 2)
            
            products.append({
                'product_id': product_id,
                'product_name': product_name,
                'category': category,
                'unit_price': unit_price
            })
            product_id += 1
        
        return products
    
    def generate_orders(self, customer_count=200, order_count=2000):
        """Generate order data"""
        orders = []
        
        # Generate orders over a 1-year period
        start_date = datetime.date(2023, 1, 1)
        end_date = datetime.date(2023, 12, 31)
        delta_days = (end_date - start_date).days
        
        for i in range(1, order_count + 1):
            # More orders in recent months
            days_offset = random.randint(0, delta_days)
            # Weight towards recent dates
            if random.random() > 0.4:
                days_offset = random.randint(int(delta_days * 0.6), delta_days)
            
            order_date = start_date + datetime.timedelta(days=days_offset)
            customer_id = random.randint(1, customer_count)
            
            orders.append({
                'order_id': i,
                'customer_id': customer_id,
                'order_date': order_date.strftime('%Y-%m-%d')
            })
        
        return orders
    
    def generate_order_items(self, order_count=2000, product_count=50, min_items=5000):
        """Generate order items"""
        order_items = []
        item_id = 1
        
        for order_id in range(1, order_count + 1):
            # Each order has 1-5 items
            items_in_order = random.randint(1, 5)
            
            for _ in range(items_in_order):
                product_id = random.randint(1, product_count)
                quantity = random.randint(1, 3)
                
                # Apply discount to 30% of items
                discount_percent = 0
                if random.random() < 0.3:
                    discount_percent = round(random.choice([5, 10, 15, 20]), 2)
                
                order_items.append({
                    'order_item_id': item_id,
                    'order_id': order_id,
                    'product_id': product_id,
                    'quantity': quantity,
                    'discount_percent': discount_percent
                })
                item_id += 1
        
        # Ensure minimum items count
        while len(order_items) < min_items:
            order_id = random.randint(1, order_count)
            product_id = random.randint(1, product_count)
            quantity = random.randint(1, 2)
            discount_percent = round(random.choice([0, 5, 10]), 2)
            
            order_items.append({
                'order_item_id': item_id,
                'order_id': order_id,
                'product_id': product_id,
                'quantity': quantity,
                'discount_percent': discount_percent
            })
            item_id += 1
        
        return order_items