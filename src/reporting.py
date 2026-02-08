import pandas as pd
import matplotlib.pyplot as plt
import os

class AnalyticsQueries:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()
    
    def revenue_per_month(self):
        """Total revenue per month"""
        query = """
        SELECT 
            strftime('%Y-%m', o.order_date) as month,
            SUM(oi.quantity * p.unit_price * (1 - oi.discount_percent / 100)) as revenue
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        GROUP BY month
        ORDER BY month
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def revenue_by_category(self):
        """Total revenue by product category"""
        query = """
        SELECT 
            p.category,
            SUM(oi.quantity * p.unit_price * (1 - oi.discount_percent / 100)) as revenue
        FROM products p
        JOIN order_items oi ON p.product_id = oi.product_id
        GROUP BY p.category
        ORDER BY revenue DESC
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def top_products_by_revenue(self, limit=10):
        """Top N products by revenue"""
        query = """
        SELECT 
            p.product_name,
            p.category,
            SUM(oi.quantity) as total_quantity,
            SUM(oi.quantity * p.unit_price * (1 - oi.discount_percent / 100)) as revenue
        FROM products p
        JOIN order_items oi ON p.product_id = oi.product_id
        GROUP BY p.product_id
        ORDER BY revenue DESC
        LIMIT ?
        """
        self.cursor.execute(query, (limit,))
        return self.cursor.fetchall()
    
    def top_customers_by_spending(self, limit=10):
        """Top N customers by total spending"""
        query = """
        SELECT 
            c.name,
            c.email,
            c.state,
            COUNT(DISTINCT o.order_id) as order_count,
            SUM(oi.quantity * p.unit_price * (1 - oi.discount_percent / 100)) as total_spent
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        GROUP BY c.customer_id
        ORDER BY total_spent DESC
        LIMIT ?
        """
        self.cursor.execute(query, (limit,))
        return self.cursor.fetchall()
    
    def revenue_by_region(self):
        """Revenue by state and city"""
        query = """
        SELECT 
            c.state,
            c.city,
            COUNT(DISTINCT o.order_id) as order_count,
            SUM(oi.quantity * p.unit_price * (1 - oi.discount_percent / 100)) as revenue
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        GROUP BY c.state, c.city
        ORDER BY revenue DESC
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def average_order_value(self):
        """Calculate Average Order Value (AOV)"""
        query = """
        SELECT 
            ROUND(AVG(order_value), 2) as avg_order_value
        FROM (
            SELECT 
                o.order_id,
                SUM(oi.quantity * p.unit_price * (1 - oi.discount_percent / 100)) as order_value
            FROM orders o
            JOIN order_items oi ON o.order_id = oi.order_id
            JOIN products p ON oi.product_id = p.product_id
            GROUP BY o.order_id
        )
        """
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]
    
    def discount_impact_analysis(self):
        """Analyze revenue loss due to discounts"""
        query = """
        SELECT 
            ROUND(SUM(oi.quantity * p.unit_price * (oi.discount_percent / 100)), 2) as total_discount_loss,
            ROUND(AVG(oi.discount_percent), 2) as avg_discount_percent,
            COUNT(CASE WHEN oi.discount_percent > 0 THEN 1 END) as discounted_items_count,
            COUNT(*) as total_items_count
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        """
        self.cursor.execute(query)
        return self.cursor.fetchone()
    
    def repeat_customer_rate(self):
        """Calculate repeat customer rate"""
        query = """
        SELECT 
            COUNT(CASE WHEN order_count > 1 THEN 1 END) as repeat_customers,
            COUNT(*) as total_customers,
            ROUND(COUNT(CASE WHEN order_count > 1 THEN 1 END) * 100.0 / COUNT(*), 2) as repeat_rate_percent
        FROM (
            SELECT 
                c.customer_id,
                COUNT(o.order_id) as order_count
            FROM customers c
            LEFT JOIN orders o ON c.customer_id = o.customer_id
            GROUP BY c.customer_id
        )
        """
        self.cursor.execute(query)
        return self.cursor.fetchone()
    
    def monthly_sales_growth(self):
        """Calculate month-over-month sales growth percentage"""
        query = """
        WITH monthly_revenue AS (
            SELECT 
                strftime('%Y-%m', order_date) as month,
                SUM(oi.quantity * p.unit_price * (1 - oi.discount_percent / 100)) as revenue
            FROM orders o
            JOIN order_items oi ON o.order_id = oi.order_id
            JOIN products p ON oi.product_id = p.product_id
            GROUP BY month
        )
        SELECT 
            month,
            revenue,
            LAG(revenue) OVER (ORDER BY month) as previous_month_revenue,
            CASE 
                WHEN LAG(revenue) OVER (ORDER BY month) > 0 
                THEN ROUND((revenue - LAG(revenue) OVER (ORDER BY month)) * 100.0 / 
                      LAG(revenue) OVER (ORDER BY month), 2)
                ELSE NULL
            END as growth_percentage
        FROM monthly_revenue
        ORDER BY month
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()


class ReportGenerator:
    def __init__(self, conn):
        self.conn = conn
        self.queries = AnalyticsQueries(conn)
        self.report_dir = 'reports/csv'
        self.chart_dir = 'reports/charts'
        
        # Create directories if they don't exist
        os.makedirs(self.report_dir, exist_ok=True)
        os.makedirs(self.chart_dir, exist_ok=True)
    
    def generate_all_reports(self):
        """Generate all reports and save as CSV"""
        print("\n📊 Generating Reports...")
        
        print(" 1. Monthly Revenue Report")
        self.save_report(
            'monthly_revenue.csv',
            self.queries.revenue_per_month(),
            ['Month', 'Revenue']
        )
        
        print(" 2. Revenue by Category Report")
        self.save_report(
            'revenue_by_category.csv',
            self.queries.revenue_by_category(),
            ['Category', 'Revenue']
        )
        
        print(" 3. Top Products Report")
        self.save_report(
            'top_products.csv',
            self.queries.top_products_by_revenue(10),
            ['Product', 'Category', 'Total Quantity', 'Revenue']
        )
        
        print(" 4. Top Customers Report")
        self.save_report(
            'top_customers.csv',
            self.queries.top_customers_by_spending(10),
            ['Customer Name', 'Email', 'State', 'Order Count', 'Total Spent']
        )
        
        print(" 5. Regional Revenue Report")
        self.save_report(
            'regional_revenue.csv',
            self.queries.revenue_by_region(),
            ['State', 'City', 'Order Count', 'Revenue']
        )
        
        print(" 6. Monthly Growth Report")
        self.save_report(
            'monthly_growth.csv',
            self.queries.monthly_sales_growth(),
            ['Month', 'Revenue', 'Previous Month Revenue', 'Growth Percentage']
        )
        
        print(f"✅ Reports saved to: {self.report_dir}")
    
    def save_report(self, filename, data, columns):
        """Save report data to CSV file"""
        df = pd.DataFrame(data, columns=columns)
        filepath = os.path.join(self.report_dir, filename)
        df.to_csv(filepath, index=False)
        return df
    
    def print_summary(self):
        """Print summary statistics to terminal"""
        print("\n" + "="*60)
        print("SALES INSIGHTS - EXECUTIVE SUMMARY")
        print("="*60)
        
        # Average Order Value
        aov = self.queries.average_order_value()
        print(f"\n💰 Average Order Value: ${aov}")
        
        # Discount Impact
        discount_data = self.queries.discount_impact_analysis()
        print(f"\n🎯 Discount Analysis:")
        print(f"   • Total discount loss: ${discount_data[0]:,.2f}")
        print(f"   • Average discount: {discount_data[1]}%")
        print(f"   • Discounted items: {discount_data[2]:,} of {discount_data[3]:,}")
        
        # Repeat Customer Rate
        repeat_data = self.queries.repeat_customer_rate()
        print(f"\n👥 Customer Loyalty:")
        print(f"   • Repeat customers: {repeat_data[0]} of {repeat_data[1]}")
        print(f"   • Repeat rate: {repeat_data[2]}%")
        
        # Top Category
        categories = self.queries.revenue_by_category()
        if categories:
            print(f"\n🏆 Top Performing Category: {categories[0][0]} (${categories[0][1]:,.2f})")
        
        # Recent Growth
        growth_data = self.queries.monthly_sales_growth()
        if len(growth_data) > 1:
            latest = growth_data[-1]
            if latest[3] is not None:
                trend = "📈" if latest[3] > 0 else "📉"
                print(f"\n📈 Latest Monthly Growth: {trend} {latest[3]}%")
        
        print("\n" + "="*60)
    
    def create_charts(self):
        """Generate simple visualizations"""
        try:
            print("\n📈 Generating Charts...")
            
            # Revenue by Category Chart
            categories_data = self.queries.revenue_by_category()
            if categories_data:
                categories = [row[0] for row in categories_data]
                revenues = [row[1] for row in categories_data]
                
                plt.figure(figsize=(10, 6))
                bars = plt.bar(categories, revenues, color='skyblue')
                plt.title('Revenue by Product Category', fontsize=14, fontweight='bold')
                plt.xlabel('Category', fontsize=12)
                plt.ylabel('Revenue ($)', fontsize=12)
                plt.xticks(rotation=45, ha='right')
                
                # Add value labels on bars
                for bar in bars:
                    height = bar.get_height()
                    plt.text(bar.get_x() + bar.get_width()/2., height,
                            f'${height:,.0f}', ha='center', va='bottom', fontsize=9)
                
                plt.tight_layout()
                plt.savefig(os.path.join(self.chart_dir, 'revenue_by_category.png'), dpi=150)
                plt.close()
                print("  ✅ Created: Revenue by Category Chart")
            
            # Monthly Revenue Chart
            monthly_data = self.queries.revenue_per_month()
            if monthly_data:
                months = [row[0] for row in monthly_data]
                revenues = [row[1] for row in monthly_data]
                
                plt.figure(figsize=(12, 6))
                plt.plot(months, revenues, marker='o', linewidth=2, color='green')
                plt.fill_between(months, revenues, alpha=0.3, color='lightgreen')
                plt.title('Monthly Revenue Trend', fontsize=14, fontweight='bold')
                plt.xlabel('Month', fontsize=12)
                plt.ylabel('Revenue ($)', fontsize=12)
                plt.xticks(rotation=45, ha='right')
                plt.grid(True, alpha=0.3)
                
                # Add data labels for last point
                if revenues:
                    plt.text(months[-1], revenues[-1], f'${revenues[-1]:,.0f}', 
                            ha='center', va='bottom', fontsize=10, fontweight='bold')
                
                plt.tight_layout()
                plt.savefig(os.path.join(self.chart_dir, 'monthly_revenue_trend.png'), dpi=150)
                plt.close()
                print("  ✅ Created: Monthly Revenue Trend Chart")
                
            print(f"✅ Charts saved to: {self.chart_dir}")
            
        except Exception as e:
            print(f"⚠️  Chart generation skipped: {str(e)}")