# Sales Insights & Reporting System

A comprehensive analytics system that stores business sales data in a SQLite database and generates actionable reports using Python and SQL.

## Features
- **Normalized Database Design**: 4 tables with proper relationships and indexes
- **Synthetic Data Generation**: 200+ customers, 50+ products, 2000+ orders
- **10+ Analytics Reports**: Revenue, growth, customer insights, regional analysis
- **CSV Export**: All reports saved as CSV files
- **Visualization**: Matplotlib charts for key metrics
- **CLI Interface**: Easy-to-use command line interface

## Tech Stack
- Python 3.x
- SQLite (embedded database)
- pandas (data manipulation)
- matplotlib (data visualization)
- argparse (CLI interface)

## Quick Start

1. **Clone and setup**:
```bash
git clone <repo-url>
cd sales_insights
pip install -r requirements.txt