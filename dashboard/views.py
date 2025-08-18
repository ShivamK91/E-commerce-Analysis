from django.shortcuts import render
from . import analysis
import plotly.graph_objs as go
import plotly.io as pio
from datetime import datetime
import pandas as pd

# Create your views here.

def dashboard(request):
    df = analysis.load_data()
    # Date range filtering
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            df = df[(df['Order Date'] >= start) & (df['Order Date'] <= end)]
        except Exception:
            pass
    # Category drilldown
    selected_category = request.GET.get('category')
    if selected_category and 'Product Category' in df.columns:
        df = df[df['Product Category'] == selected_category]
    # Month drilldown
    selected_month = request.GET.get('month')
    if selected_month:
        try:
            month_period = pd.Period(selected_month)
            df = df[df['Order Date'].dt.to_period('M') == month_period]
        except Exception:
            pass
    # 1. Monthly Sales
    monthly_sales_data, highest_month, lowest_month = analysis.monthly_sales(df)
    monthly_sales_chart = go.Figure([go.Bar(y=monthly_sales_data.index.astype(str), x=monthly_sales_data.values, orientation='h')])
    monthly_sales_chart.update_layout(title='Monthly Sales', yaxis_title='Month', xaxis_title='Sales')
    monthly_sales_json = pio.to_json(monthly_sales_chart)

    # 2. Sales by Category
    sales_by_cat, highest_cat, lowest_cat = analysis.sales_by_category(df)
    sales_by_cat_chart = go.Figure([go.Bar(y=sales_by_cat.index, x=sales_by_cat.values, orientation='h')])
    sales_by_cat_chart.update_layout(title='Sales by Category', yaxis_title='Category', xaxis_title='Sales')
    sales_by_cat_json = pio.to_json(sales_by_cat_chart)

    # 3. Sales by Sub-category (filtered by category if selected)
    sales_by_subcat = analysis.sales_by_subcategory(df)
    sales_by_subcat_chart = go.Figure([go.Bar(y=sales_by_subcat.index, x=sales_by_subcat.values, orientation='h')])
    sales_by_subcat_chart.update_layout(title='Sales by Sub-category' + (f' ({selected_category})' if selected_category else ''), yaxis_title='Sub-category', xaxis_title='Sales')
    sales_by_subcat_json = pio.to_json(sales_by_subcat_chart)

    # 4. Monthly Profit
    monthly_profit_data, highest_profit_month = analysis.monthly_profit(df)
    monthly_profit_chart = go.Figure([go.Bar(y=monthly_profit_data.index.astype(str), x=monthly_profit_data.values, orientation='h')])
    monthly_profit_chart.update_layout(title='Monthly Profit', yaxis_title='Month', xaxis_title='Profit')
    monthly_profit_json = pio.to_json(monthly_profit_chart)

    # 5. Profit by Category & Sub-category
    profit_by_cat = analysis.profit_by_category(df)
    profit_by_cat_chart = go.Figure([go.Bar(y=profit_by_cat.index, x=profit_by_cat.values, orientation='h')])
    profit_by_cat_chart.update_layout(title='Profit by Category', yaxis_title='Category', xaxis_title='Profit')
    profit_by_cat_json = pio.to_json(profit_by_cat_chart)

    profit_by_subcat = analysis.profit_by_subcategory(df)
    profit_by_subcat_chart = go.Figure([go.Bar(y=profit_by_subcat.index, x=profit_by_subcat.values, orientation='h')])
    profit_by_subcat_chart.update_layout(title='Profit by Sub-category' + (f' ({selected_category})' if selected_category else ''), yaxis_title='Sub-category', xaxis_title='Profit')
    profit_by_subcat_json = pio.to_json(profit_by_subcat_chart)

    # 6. Sales & Profit by Customer Segment
    sales_profit_by_seg = analysis.sales_profit_by_segment(df)
    sales_profit_by_seg_chart = go.Figure()
    sales_profit_by_seg_chart.add_trace(go.Bar(y=sales_profit_by_seg.index, x=sales_profit_by_seg['Sales'], name='Sales', orientation='h'))
    sales_profit_by_seg_chart.add_trace(go.Bar(y=sales_profit_by_seg.index, x=sales_profit_by_seg['Profit'], name='Profit', orientation='h'))
    sales_profit_by_seg_chart.update_layout(title='Sales & Profit by Customer Segment', barmode='group', yaxis_title='Segment', xaxis_title='Amount')
    sales_profit_by_seg_json = pio.to_json(sales_profit_by_seg_chart)

    # 7. Sales-to-Profit Ratio
    sales_to_profit = analysis.sales_to_profit_ratio(df)

    # 8. Sales by Region
    sales_by_region = analysis.sales_by_region(df)
    has_sales_by_region = not sales_by_region.empty
    if has_sales_by_region:
        sales_by_region_chart = go.Figure([go.Bar(y=sales_by_region.index, x=sales_by_region.values, orientation='h')])
        sales_by_region_chart.update_layout(title='Sales by Region', yaxis_title='Region', xaxis_title='Sales')
        sales_by_region_json = pio.to_json(sales_by_region_chart)
    else:
        sales_by_region_json = ''

    # 9. Sales by Province
    sales_by_province = analysis.sales_by_province(df)
    has_sales_by_province = not sales_by_province.empty
    if has_sales_by_province:
        sales_by_province_chart = go.Figure([go.Bar(y=sales_by_province.index, x=sales_by_province.values, orientation='h')])
        sales_by_province_chart.update_layout(title='Sales by Province', yaxis_title='Province', xaxis_title='Sales')
        sales_by_province_json = pio.to_json(sales_by_province_chart)
    else:
        sales_by_province_json = ''

    # 10. Top Customers
    top_customers = analysis.top_customers(df)
    has_top_customers = not top_customers.empty
    if has_top_customers:
        top_customers_chart = go.Figure([go.Bar(y=top_customers.index, x=top_customers.values, orientation='h')])
        top_customers_chart.update_layout(title='Top Customers', yaxis_title='Customer', xaxis_title='Sales')
        top_customers_json = pio.to_json(top_customers_chart)
    else:
        top_customers_json = ''

    # 11. Top Products
    top_products = analysis.top_products(df)
    has_top_products = not top_products.empty
    if has_top_products:
        top_products_chart = go.Figure([go.Bar(y=top_products.index, x=top_products.values, orientation='h')])
        top_products_chart.update_layout(title='Top Products', yaxis_title='Product', xaxis_title='Sales')
        top_products_json = pio.to_json(top_products_chart)
    else:
        top_products_json = ''

    # Prepare chart data and flags for template
    has_monthly_sales = not monthly_sales_data.empty
    has_sales_by_cat = not sales_by_cat.empty
    has_sales_by_subcat = not sales_by_subcat.empty
    has_monthly_profit = not monthly_profit_data.empty
    has_profit_by_cat = not profit_by_cat.empty
    has_profit_by_subcat = not profit_by_subcat.empty
    has_sales_profit_by_seg = not sales_profit_by_seg.empty

    context = {
        'monthly_sales_json': monthly_sales_json,
        'highest_month': highest_month,
        'lowest_month': lowest_month,
        'sales_by_cat_json': sales_by_cat_json,
        'highest_cat': highest_cat,
        'lowest_cat': lowest_cat,
        'sales_by_subcat_json': sales_by_subcat_json,
        'monthly_profit_json': monthly_profit_json,
        'highest_profit_month': highest_profit_month,
        'profit_by_cat_json': profit_by_cat_json,
        'profit_by_subcat_json': profit_by_subcat_json,
        'sales_profit_by_seg_json': sales_profit_by_seg_json,
        'sales_to_profit': sales_to_profit,
        'start_date': start_date,
        'end_date': end_date,
        'selected_category': selected_category,
        'selected_month': selected_month,
        'has_monthly_sales': has_monthly_sales,
        'has_sales_by_cat': has_sales_by_cat,
        'has_sales_by_subcat': has_sales_by_subcat,
        'has_monthly_profit': has_monthly_profit,
        'has_profit_by_cat': has_profit_by_cat,
        'has_profit_by_subcat': has_profit_by_subcat,
        'has_sales_profit_by_seg': has_sales_profit_by_seg,
    }
    context.update({
        'sales_by_region_json': sales_by_region_json,
        'has_sales_by_region': has_sales_by_region,
        'sales_by_province_json': sales_by_province_json,
        'has_sales_by_province': has_sales_by_province,
        'top_customers_json': top_customers_json,
        'has_top_customers': has_top_customers,
        'top_products_json': top_products_json,
        'has_top_products': has_top_products,
    })
    return render(request, 'dashboard/dashboard.html', context)
