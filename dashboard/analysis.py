import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / 'media' / 'superstore.csv'

def load_data():
    try:
        df = pd.read_csv(DATA_PATH, encoding='utf-8-sig', parse_dates=['Order Date', 'Ship Date'])
    except UnicodeDecodeError:
        df = pd.read_csv(DATA_PATH, encoding='latin1', parse_dates=['Order Date', 'Ship Date'])
    return df

# 1. Monthly Sales (highest & lowest month)
def monthly_sales(df):
    df['Month'] = df['Order Date'].dt.to_period('M')
    sales = df.groupby('Month')['Sales'].sum().sort_index()
    highest = sales.idxmax().strftime('%Y-%m') if not sales.empty else None
    lowest = sales.idxmin().strftime('%Y-%m') if not sales.empty else None
    return sales, highest, lowest

# 2. Sales by Category (highest & lowest)
def sales_by_category(df):
    if 'Product Category' not in df.columns:
        return pd.Series(dtype=float), None, None
    sales = df.groupby('Product Category')['Sales'].sum().sort_values(ascending=False)
    highest = sales.idxmax() if not sales.empty else None
    lowest = sales.idxmin() if not sales.empty else None
    return sales, highest, lowest

# 3. Sales by Sub-category
def sales_by_subcategory(df):
    if 'Product Sub-Category' not in df.columns:
        return pd.Series(dtype=float)
    return df.groupby('Product Sub-Category')['Sales'].sum().sort_values(ascending=False)

# 4. Monthly Profit (highest profit month)
def monthly_profit(df):
    df['Month'] = df['Order Date'].dt.to_period('M')
    profit = df.groupby('Month')['Profit'].sum().sort_index()
    highest = profit.idxmax().strftime('%Y-%m') if not profit.empty else None
    return profit, highest

# 5. Profit by Category & Sub-category
def profit_by_category(df):
    if 'Product Category' not in df.columns:
        return pd.Series(dtype=float)
    return df.groupby('Product Category')['Profit'].sum().sort_values(ascending=False)

def profit_by_subcategory(df):
    if 'Product Sub-Category' not in df.columns:
        return pd.Series(dtype=float)
    return df.groupby('Product Sub-Category')['Profit'].sum().sort_values(ascending=False)

# 6. Sales & Profit by Customer Segment
def sales_profit_by_segment(df):
    if 'Customer Segment' not in df.columns:
        return pd.DataFrame(columns=['Sales', 'Profit'])
    grouped = df.groupby('Customer Segment').agg({'Sales': 'sum', 'Profit': 'sum'})
    return grouped

# 7. Sales-to-Profit Ratio
def sales_to_profit_ratio(df):
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    ratio = total_sales / total_profit if total_profit != 0 else None
    return ratio

# 8. Sales by Region
def sales_by_region(df):
    if 'Region' not in df.columns:
        return pd.Series(dtype=float)
    return df.groupby('Region')['Sales'].sum().sort_values(ascending=False)

# 9. Sales by Province
def sales_by_province(df):
    if 'Province' not in df.columns:
        return pd.Series(dtype=float)
    return df.groupby('Province')['Sales'].sum().sort_values(ascending=False)

# 10. Top Customers
def top_customers(df, n=10):
    if 'Customer Name' not in df.columns:
        return pd.Series(dtype=float)
    return df.groupby('Customer Name')['Sales'].sum().sort_values(ascending=False).head(n)

# 11. Top Products
def top_products(df, n=10):
    if 'Product Name' not in df.columns:
        return pd.Series(dtype=float)
    return df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(n)
