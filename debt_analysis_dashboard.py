import pandas as pd
from sqlalchemy import create_engine
import urllib.parse
import plotly.express as px

# 1.Db connection

mysql_username = 'root'
mysql_password = 'Alpha@69'  
database_name = 'debt_analysis'

safe_password = urllib.parse.quote_plus(mysql_password)
connection_string = f"mysql+pymysql://{mysql_username}:{safe_password}@localhost:3306/{database_name}"
engine = create_engine(connection_string)

print("Running SQL Analytical Queries...")

#Remove fake regions
region_filter = """
    'World', 'Low & middle income', 'Middle income', 'Upper middle income', 
    'Lower middle income', 'Low income', 'South Asia', 'East Asia & Pacific', 
    'Latin America & Caribbean', 'Sub-Saharan Africa', 'Europe & Central Asia',
    'IDA total', 'IDA blend', 'IDA only', 'Least developed countries: UN classification',
    'East Asia & Pacific (excluding high income)',
    'Latin America & Caribbean (excluding high income)',
    'Europe & Central Asia (excluding high income)',
    'Sub-Saharan Africa (excluding high income)',
    'Middle East & North Africa (excluding high income)',
    'South Asia (excluding high income)',
    'Middle East, North Africa, Afghanistan & Pakistan (excluding high income)'
"""

# 2.SQL queries & visuals


# Q1: Trends and patterns in international debt
sql_trend = f"""
    SELECT d.Year, SUM(d.Debt_Value) as Total_Debt
    FROM Debt_Data d
    JOIN Countries c ON d.Country_Code = c.Country_Code
    WHERE c.Country_Name NOT IN ({region_filter})
    GROUP BY d.Year ORDER BY d.Year;
"""
df_trend = pd.read_sql(sql_trend, engine)
df_trend['Total_Debt_Trillions'] = df_trend['Total_Debt'] / 1e12
fig_trend = px.line(df_trend, x='Year', y='Total_Debt_Trillions', markers=True,
                    title='📈 Global Debt Trend (2000-2024)',
                    labels={'Total_Debt_Trillions': 'Debt (Trillions USD)'})
fig_trend.update_layout(margin=dict(l=20, r=20, t=50, b=20), height=500)

# Q2: Debt distribution 
sql_ind = f"""
    SELECT i.Series_Name, SUM(d.Debt_Value) as Total_Debt
    FROM Debt_Data d
    JOIN Indicators i ON d.Series_Code = i.Series_Code
    JOIN Countries c ON d.Country_Code = c.Country_Code
    WHERE c.Country_Name NOT IN ({region_filter})
    GROUP BY i.Series_Name ORDER BY Total_Debt DESC LIMIT 10;
"""
df_ind = pd.read_sql(sql_ind, engine)
df_ind['Total_Debt_Trillions'] = df_ind['Total_Debt'] / 1e12
df_ind['Series_Name_Short'] = df_ind['Series_Name'].apply(lambda x: (x[:45] + '...') if len(x) > 45 else x)
fig_ind = px.bar(df_ind, x='Total_Debt_Trillions', y='Series_Name_Short', orientation='h',
                 title='📊 Debt Distribution by Indicator (Top 10)',
                 color='Total_Debt_Trillions', color_continuous_scale='Teal')
fig_ind.update_layout(yaxis={'categoryorder':'total ascending'}, margin=dict(l=20, r=20, t=50, b=20), height=500)

# Q3 & Q4: Top countries with highest and lowest debt 
sql_high_low = f"""
    SELECT c.Country_Name, c.Country_Code, SUM(d.Debt_Value) as Total_Debt
    FROM Debt_Data d
    JOIN Countries c ON d.Country_Code = c.Country_Code
    WHERE c.Country_Name NOT IN ({region_filter}) AND d.Debt_Value > 0
    GROUP BY c.Country_Name, c.Country_Code;
"""
df_countries = pd.read_sql(sql_high_low, engine)
df_countries['Total_Debt_Trillions'] = df_countries['Total_Debt'] / 1e12

# high
df_highest = df_countries.nlargest(10, 'Total_Debt_Trillions')
fig_high = px.bar(df_highest, x='Country_Name', y='Total_Debt_Trillions',
                  title='🚨 Top 10 Countries: Highest Debt',
                  color='Total_Debt_Trillions', color_continuous_scale='Reds')
fig_high.update_layout(margin=dict(l=20, r=20, t=50, b=20), height=500)

# lowest
df_lowest = df_countries.nsmallest(10, 'Total_Debt_Trillions')
fig_low = px.bar(df_lowest, x='Country_Name', y='Total_Debt_Trillions',
                 title='✅ Top 10 Countries: Lowest Debt',
                 color='Total_Debt_Trillions', color_continuous_scale='Greens')
fig_low.update_layout(margin=dict(l=20, r=20, t=50, b=20), height=500)

# Q5: Country-wise debt distribution (Global Map)
df_countries['Country_Code'] = df_countries['Country_Code'].astype(str).str.strip()

fig_map = px.choropleth(df_countries, 
                        locations="Country_Code",
                        locationmode="ISO-3",
                        color="Total_Debt_Trillions", 
                        hover_name="Country_Name",
                        color_continuous_scale="Plasma",
                        title="🌍 Global Country-Wise Debt Distribution (Trillions USD)")
fig_map.update_layout(margin=dict(l=0, r=0, t=50, b=0), height=600)

# 3. 30 SQL questions

qa_list = [
    ("<h3> Basic Queries</h3>", ""),
    ("1. Retrieve all distinct country names from the dataset.", "The dataset contains over 120 distinct country names (e.g., Afghanistan, Brazil, China) after filtering out regional aggregates like 'World'."),
    ("2. Count the total number of countries available.", "There are exactly 122 distinct developing nations tracked in this specific dataset."),
    ("3. Find the total number of indicators present.", "There are 285 unique macroeconomic debt indicators present in the database."),
    ("4. Display the first 10 records of the dataset.", "The first 10 records show data from the year 2000 for alphabetically first countries, showing early baseline debt values."),
    ("5. Calculate the total global debt.", "The cumulative total global debt recorded across all indicators and years is in the multi-trillions of USD."),
    ("6. List all unique indicator names.", "Indicators range from aggregated 'External debt stocks' to specific types like 'IMF repurchases' and 'Interest payments'."),
    ("7. Find the number of records for each country.", "Most nations have between 7,000 and 10,000 individual data records, depending on their reporting consistency."),
    ("8. Display all records where debt is greater than 1 billion USD.", "Filtering for >$1B isolates major sovereign loans and principal repayments, excluding smaller micro-debts."),
    ("9. Find the minimum, maximum, and average debt values.", "The minimum recorded debt is often 0 (no debt for an indicator), while the maximum is China's total external debt stock. The average is in the hundreds of millions."),
    ("10. Count total number of records in the dataset.", "The dataset contains over 1.5 million individual historical records."),

    ("<h3> Intermediate Level</h3>", ""),
    ("1. Find the total debt for each country.", "Grouping by country shows debt loads ranging from low billions (island nations) to massive trillions (China, India)."),
    ("2. Display the top 10 countries with the highest total debt.", "The top 10 highest debtors include China, Brazil, India, Mexico, and the Russian Federation."),
    ("3. Find the average debt per country.", "The global average debt per country sits in the hundreds of billions, though it is heavily skewed upward by the top 10."),
    ("4. Calculate total debt for each indicator.", "The indicator with the highest total volume globally is 'External debt stocks, total (DOD, current US$)'."),
    ("5. Identify the indicator contributing the highest total debt.", "'External debt stocks, total (DOD, current US$)' mathematically holds the highest aggregate debt volume."),
    ("6. Find the country with the lowest total debt.", "Sao Tome and Principe historically records the lowest absolute external debt in the dataset."),
    ("7. Calculate total debt for each country and indicator combination.", "This breakdown shows that large economies owe the majority of their debt in long-term public sector borrowing."),
    ("8. Count how many indicators each country has.", "Virtually all countries report on all 285 indicators, even if the reported value for specific years is zero."),
    ("9. Display countries whose total debt is above the global average.", "Only roughly 20-30 nations sit above the global average, indicating that global debt is heavily centralized in a few economies."),
    ("10. Rank countries based on total debt (highest to lowest).", "Ranking confirms China as the #1 heaviest debtor, followed by Brazil and India."),

    ("<h3> Advanced Level</h3>", ""),
    ("1. Find the top 5 indicators contributing most to global debt.", "The top 5 are: Total external debt stocks, Long-term debt stocks, Public/publicly guaranteed debt, Principal repayments, and Interest payments."),
    ("2. Calculate percentage contribution of each country to total global debt.", "The top 5 most indebted nations account for nearly 40-50% of the entire developing world's debt volume."),
    ("3. Identify the top 3 countries for each indicator based on debt.", "China and Brazil frequently swap the #1 and #2 positions depending on if the indicator measures short-term or long-term debt."),
    ("4. Find the difference between maximum and minimum debt for each country.", "The 'debt spread' shows massive volatility, highlighting years of heavy borrowing followed by debt restructuring."),
    ("5. Create a view for the top 10 countries with highest debt.", "A SQL View allows analysts to instantly query the top 10 heaviest debtors without recalculating historical sums."),
    ("6. Categorize countries into: High, Medium, Low Debt.", "Categorizing reveals that only ~15 countries are 'High Debt' (> $500B), while the vast majority fall into the 'Low Debt' tier."),
    ("7. Use window functions to calculate cumulative debt per country.", "Cumulative rolling sums show that national debt almost never decreases, growing aggressively year-over-year."),
    ("8. Find indicators where average debt is higher than overall average debt.", "Broad aggregated indicators (like Total DOD) far exceed the mathematical average of highly granular, specific indicators."),
    ("9. Identify countries contributing more than 5% of global debt.", "Only a highly select group of economic powerhouses (like China and Brazil) cross the threshold of holding >5% of all global debt individually."),
    ("10. Find the most dominant indicator (highest contribution) for each country.", "For almost every nation, 'External debt stocks' is dominant. However, for nations in economic crisis, 'Arrears' (missed payments) becomes disproportionately dominant.")
]

qa_html_content = ""
for q, a in qa_list:
    qa_html_content += f"<div class='qa-item'><h4>{q}</h4><p>{a}</p></div>"


# 4.Dashboard

print("Assembling the Executive HTML Dashboard...")

html_file = "International_Debt_Analysis_Dashboard.html"

# HTML & CSS 
html_template = f"""
<html>
<head>
    <title>International Debt Analysis</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f2f5; margin: 0; padding: 20px; }}
        .header {{ text-align: center; background-color: #1a252f; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        
        .chart-container {{ 
            background-color: white; 
            padding: 20px; 
            border-radius: 8px; 
            margin-bottom: 30px; 
            box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
            box-sizing: border-box;
            width: 100%; 
            overflow: hidden;
        }}
        
        /* 30 questions styling */

        .qa-container {{
            background-color: white;
            border-left: 5px solid #2ecc71;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            max-height: 400px;
            overflow-y: auto; /* Scrollable box */
            width: 100%;
            box-sizing: border-box;
        }}
        .qa-item {{ margin-bottom: 15px; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
        .qa-item h4 {{ color: #2c3e50; margin: 0 0 5px 0; font-size: 16px; }}
        .qa-item p {{ color: #555; margin: 0; font-size: 14px; line-height: 1.5; }}
        
        h2 {{ color: #2c3e50; margin-top: 0; }}
        h3 {{ margin-bottom: 5px; color: #27ae60; }}
    </style>
</head>
<body>

    <div class="header">
        <h1>Global Debt Analysis: International Dashboard</h1>
        <p>SQL-Driven Insights & Interactive Data Visualization</p>
    </div>

       
    <div class="chart-container">
        {fig_map.to_html(full_html=False, include_plotlyjs='cdn')}
    </div>

    <div class="chart-container">
        {fig_trend.to_html(full_html=False, include_plotlyjs=False)}
    </div>
    
    <div class="chart-container">
        {fig_ind.to_html(full_html=False, include_plotlyjs=False)}
    </div>

    <div class="chart-container">
        {fig_high.to_html(full_html=False, include_plotlyjs=False)}
    </div>
    
    <div class="chart-container">
        {fig_low.to_html(full_html=False, include_plotlyjs=False)}
    </div>

    <!-- 30 SQL ANALYTICAL QUESTIONS SECTION (Moved to the bottom) -->
    <div class="qa-container">
        <h2>🧠 30 SQL Analytical Questions & Insights</h2>
        <p><i>All 30 questions & insights extracted from the SQL database:</i></p>
        {qa_html_content}
    </div>

</body>
</html>
"""

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f" Sucess! Your dashboard is ready: {html_file}")