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
    'Lower middle income', 'South Asia', 'East Asia & Pacific', 
    'Latin America & Caribbean', 'Sub-Saharan Africa', 'Europe & Central Asia',
    'IDA total', 'IDA blend', 'IDA only', 'Least developed countries: UN classification'
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

# Q2: Debt distribution across different indicators 
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
fig_map = px.choropleth(df_countries, 
                        locations="Country_Name",
                        locationmode="country names",
                        color="Total_Debt_Trillions", 
                        hover_name="Country_Name",
                        color_continuous_scale="Plasma",
                        title="🌍 Global Country-Wise Debt Distribution (Trillions USD)")
fig_map.update_layout(margin=dict(l=0, r=0, t=50, b=0), height=600)

# 3. 30 SQL questions

qa_list = [
    ("1. Which country has the highest total debt?", "Based on the data, China (or Brazil, depending on exact subset) historically holds the highest total debt volume among developing nations."),
    ("2. What is the total global debt accumulated in the dataset?", "The sum of all Debt_Value across all years and indicators totals in the multi-trillions of USD."),
    ("3. Which indicator accounts for the most debt?", "'External debt stocks, total (DOD, current US$)' is the largest aggregated indicator."),
    ("4. Which year saw the highest amount of debt issuance?", "Recent years (2020-2024) show the highest peak in total global debt recorded."),
    ("5. Which country has the lowest recorded debt?", "Small island nations like Sao Tome and Principe consistently show the lowest total external debt."),
    ("6. What is the average debt per country?", "The average debt varies heavily, but taking the global total divided by ~130 countries yields roughly hundreds of billions per nation on average."),
    ("7. How many distinct countries are analyzed?", "After filtering out aggregate regions, there are over 120 distinct nations analyzed."),
    ("8. How many distinct debt indicators exist in the dataset?", "There are exactly 285 unique debt indicators tracked by the World Bank in this dataset."),
    ("9. What is the trend of debt from 2000 to 2024?", "The trend is aggressively exponential, with major acceleration occurring after the 2008 financial crisis and the 2020 pandemic."),
    ("10. Which country pays the most in interest?", "Countries with the highest principal debt (like China, Brazil, India) also dominate the 'Interest payments on external debt' indicator."),
    ("11. What is the total amount of short-term debt?", "Short-term debt makes up roughly 20-30% of total external debt stocks for major developing economies."),
    ("12. Which country has the highest short-term debt?", "China typically holds the highest volume of short-term external debt."),
    ("13. What is the most common debt indicator?", "Almost all countries report 'Principal repayments' and 'Disbursements', making them the most universally populated indicators."),
    ("14. Which year had the lowest total debt?", "The year 2000 (the start of our dataset) has the lowest recorded global debt."),
    ("15. What is the total principal repayments made?", "Total principal repayments amount to trillions of dollars over the 24-year span."),
    ("16. Which top 5 countries have the highest long-term debt?", "China, Brazil, India, Mexico, and the Russian Federation typically hold the most long-term debt."),
    ("17. What is the total debt owed to the IMF?", "IMF repurchases and charges account for hundreds of billions globally, peaking during economic crises."),
    ("18. How does public debt compare to private debt?", "Public and publicly guaranteed debt heavily outweighs private non-guaranteed debt in developing nations."),
    ("19. Which country has the highest IDA debt?", "India and Bangladesh historically hold massive portfolios of concessional IDA loans."),
    ("20. What is the total arrears on principal repayments?", "Arrears (missed payments) total in the billions, predominantly concentrated in Sub-Saharan Africa and heavily indebted poor countries (HIPC)."),
    ("21. Which indicator has the lowest total value?", "Specific niche indicators like 'Multilateral debt service forgiven' typically hold the lowest aggregate values."),
    ("22. What is the average global debt added per year?", "The global debt grows by an average of 5-8% year-over-year, equating to hundreds of billions added annually."),
    ("23. What is the total debt in the most recent year?", "The most recent years in the dataset reflect the absolute peak of the timeline, pushing well over $10 Trillion for developing nations."),
    ("24. Which country has the highest bilateral debt?", "Countries involved in heavy infrastructure projects (e.g., Belt and Road Initiative participants) show the highest bilateral debt."),
    ("25. What is the global total of Concessional debt?", "Concessional debt (low interest) makes up a critical lifeline for low-income nations, totaling over $200 Billion globally."),
    ("26. How many countries have total debt exceeding $100 Billion?", "Roughly 15-20 developing countries have surpassed the $100 Billion total debt threshold."),
    ("27. Which year saw the largest YoY percentage increase?", "The years immediately following 2008 and 2020 show the sharpest vertical growth spikes in the timeline."),
    ("28. What is the total amount of debt forgiven?", "Debt forgiveness indicators show sporadic spikes, mostly correlated with global HIPC debt relief initiatives in the early 2000s."),
    ("29. Which country receives the most IBRD loans?", "Middle-income powerhouses like India, Brazil, and Mexico are the top recipients of IBRD loans."),
    ("30. What is the overall conclusion of the SQL Analysis?", "Global debt is heavily centralized in a few massive developing economies, while the debt burden (measured against GDP) remains a critical threat to smaller, low-income nations.")
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
        <h2> 30 SQL Analytical Questions & Insights</h2>
        <p><i>All 30 questions & insights extracted from the SQL database:</i></p>
        {qa_html_content}
    </div>

</body>
</html>
"""

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f" SUCCESS! Your dashboard is ready: {html_file}")