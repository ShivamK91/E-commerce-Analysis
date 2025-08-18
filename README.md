# Ecommerce Analysis Dashboard

An interactive E-commerce Sales Analysis Dashboard built with **Django**, **Pandas**, and **Plotly.js**.

## 🎯 Project Objective
Analyze and visualize sales data from a Superstore dataset, providing actionable insights for business decisions.

## 🚀 Features
- Loads sales data from `media/superstore.csv`
- Monthly Sales (highest & lowest month)
- Sales by Category (highest & lowest)
- Sales by Sub-category
- Monthly Profit (highest profit month)
- Profit by Category & Sub-category
- Sales & Profit by Customer Segment
- Sales-to-Profit Ratio
- Interactive charts with Plotly.js

## 🛠️ Tech Stack
- Django 5+
- Pandas
- Plotly.js

## 📦 Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd "Ecommerce Analysis"
   ```

2. **Install dependencies**
   ```bash
   pip install django pandas plotly
   ```

3. **Add your data**
   - Place your `superstore.csv` file in the `media/` folder (ensure the file is named exactly `superstore.csv`).

4. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

5. **Run the development server**
   ```bash
   python manage.py runserver
   ```

6. **View the dashboard**
   - Open your browser and go to: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## 📊 Dashboard Preview
- Interactive bar charts for all key metrics
- Summary of top/bottom months and categories

## 📝 Notes
- The dashboard is for development/demo use. For production, configure static/media serving and security settings.
- If you encounter encoding errors with your CSV, the loader will try both `utf-8-sig` and `latin1`.

## 📁 Project Structure
```
Ecommerce Analysis/
├── dashboard/
│   ├── analysis.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│       └── dashboard/
│           └── dashboard.html
├── ecommerce_analysis/
│   ├── settings.py
│   └── urls.py
├── media/
│   └── superstore.csv
├── static/
├── manage.py
└── README.md
```

## 🙋‍♂️ Contributing
Pull requests and suggestions are welcome!

## 📜 License
MIT (or specify your license)
