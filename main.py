
"""
Sales Insights & Reporting System
"""
import argparse
import sys
import os
import sqlite3

# Import from current directory
from src.db import get_connection, close_connection
from src.schema import create_tables
from src.loader import load_generated_data
from src.reporting import ReportGenerator

def init_database():
    """Initialize database with schema"""
    print("Initializing database...")
    conn = get_connection()
    create_tables(conn)
    close_connection(conn)
    print("✅ Database initialized successfully.")

def load_data():
    """Load data into database"""
    print("Loading synthetic data...")
    conn = get_connection()
    load_generated_data(conn)
    close_connection(conn)

def run_reports(include_charts=False):
    """Generate analytics reports"""
    print("Running analytics reports...")
    conn = get_connection()
    
    # Generate reports
    report_gen = ReportGenerator(conn)
    report_gen.generate_all_reports()
    report_gen.print_summary()
    
    if include_charts:
        report_gen.create_charts()
    
    close_connection(conn)

def export_all(include_charts=False):
    """Run full pipeline: init, load data, generate reports"""
    print("🚀 Starting full pipeline...\n")
    
    # Initialize
    print("="*50)
    print("STEP 1: Database Initialization")
    print("="*50)
    init_database()
    
    # Load data
    print("\n" + "="*50)
    print("STEP 2: Data Generation & Loading")
    print("="*50)
    load_data()
    
    # Generate reports
    print("\n" + "="*50)
    print("STEP 3: Analytics & Reporting")
    print("="*50)
    run_reports(include_charts)
    
    print("\n✅ Pipeline completed successfully!")

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Sales Insights & Reporting System',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Init database command
    subparsers.add_parser('init-db', help='Initialize database schema')
    
    # Load data command
    subparsers.add_parser('load-data', help='Load synthetic data into database')
    
    # Run reports command
    report_parser = subparsers.add_parser('run-reports', help='Generate analytics reports')
    report_parser.add_argument('--charts', action='store_true',
                             help='Generate charts in addition to CSV reports')
    
    # Export all command
    export_parser = subparsers.add_parser('export-all', help='Run full pipeline')
    export_parser.add_argument('--charts', action='store_true',
                             help='Generate charts')
    
    args = parser.parse_args()
    
    if not args.command:
        print("\nSales Insights & Reporting System")
        print("="*40)
        print("Usage: python main.py [command]\n")
        print("Commands:")
        print("  init-db      Initialize database schema")
        print("  load-data    Load synthetic data")
        print("  run-reports  Generate analytics reports")
        print("  export-all   Run full pipeline\n")
        print("Example: python main.py export-all --charts")
        sys.exit(1)
    
    # Create necessary directories
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/generated', exist_ok=True)
    os.makedirs('reports/csv', exist_ok=True)
    os.makedirs('reports/charts', exist_ok=True)
    
    # Execute command
    if args.command == 'init-db':
        init_database()
    elif args.command == 'load-data':
        load_data()
    elif args.command == 'run-reports':
        run_reports(args.charts)
    elif args.command == 'export-all':
        export_all(args.charts)

if __name__ == '__main__':
    main()