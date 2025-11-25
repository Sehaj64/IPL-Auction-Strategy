# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.5
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Part 1: Exploratory Data Analysis (EDA) and Visualization
#
# In this notebook, we will explore the IPL player dataset to uncover initial insights.
# We will perform the following steps:
# 1.  Initialize the database using our SQL scripts.
# 2.  Execute advanced analytical queries from our SQL scripts.
# 3.  Visualize the results of these queries to communicate findings.

# ## 1. Setup and Database Initialization
#
# First, let's import the necessary libraries and set up our database connection. We will then run all our SQL scripts to ensure the database is ready and our feature view is created.

# + 
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Setup database connection
# Assuming the notebook is run from the root of the project directory
DB_FILE = os.path.join('database', 'ipl_auction.db')

# Function to execute a script
def execute_sql_from_file(conn, filepath):
    with open(filepath, 'r') as f:
        conn.executescript(f.read())

# Initialize a clean database
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)

conn = sqlite3.connect(DB_FILE)

# Run all setup scripts
execute_sql_from_file(conn, os.path.join('database', 'schema.sql'))
execute_sql_from_file(conn, os.path.join('database', 'data.sql'))
execute_sql_from_file(conn, os.path.join('database', '02_feature_engineering.sql'))

print("Database initialized and features engineered successfully.")
# - 

# ## 2. Execute and Visualize Analytical Queries
#
# Now we will run the complex queries defined in `03_analytical_queries.sql` and visualize their results.

# ### Query 1: Top 5 "Value for Money" Players per Role
#
# This query uses a Common Table Expression (CTE) and a window function (`ROW_NUMBER`) to rank players within their role based on our `value_for_money` score.

# + 
# Read the specific query from the SQL file
with open(os.path.join('database', '03_analytical_queries.sql'), 'r') as f:
    all_queries = f.read().split(';')
    query1 = all_queries[0]

df_value_for_money = pd.read_sql_query(query1, conn)

print("Top 5 'Value for Money' Players per Role:")
print(df_value_for_money)

# Visualize the results
plt.figure(figsize=(12, 8))
sns.barplot(data=df_value_for_money, x='value_for_money', y='name', hue='role', dodge=False)
plt.title('Top 5 "Value for Money" Players per Role', fontsize=16)
plt.xlabel('Value for Money Score (Performance Score per $1M)', fontsize=12)
plt.ylabel('Player Name', fontsize=12)
plt.legend(title='Role')
plt.tight_layout()
plt.show()
# - 

# ### Query 2: Average Performance of Indian vs. Overseas Players
#
# This query uses `GROUP BY` and `AVG` to compare the average `performance_score` across different roles and nationalities.

# + 
# Read Query 2
query2 = all_queries[1]
df_nationality_comparison = pd.read_sql_query(query2, conn)

print("\nAverage Performance: Indian vs. Overseas:")
print(df_nationality_comparison)

# Visualize the results
plt.figure(figsize=(12, 7))
sns.barplot(data=df_nationality_comparison, x='role', y='avg_performance_score', hue='nationality')
plt.title('Average Performance Score: Indian vs. Overseas', fontsize=16)
plt.xlabel('Player Role', fontsize=12)
plt.ylabel('Average Performance Score', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.legend(title='Nationality')
plt.tight_layout()
plt.show()
# - 

# ### Query 3: Identifying "Bargain" Players
#
# This query finds players who are priced below the average for their role but perform above the average for their role. This is a great way to spot undervalued talent.

# + 
# Read Query 3
query3 = all_queries[2]
df_bargains = pd.read_sql_query(query3, conn)

print("\nPotential 'Bargain' Players (Below Avg. Price, Above Avg. Performance):")
print(df_bargains)

# Visualize the results using a scatter plot to show all players
# and highlight the bargains
df_all_players = pd.read_sql_query("SELECT * FROM player_features", conn)

plt.figure(figsize=(14, 9))
sns.scatterplot(data=df_all_players, x='base_price_usd', y='performance_score', hue='role', style='nationality', s=100, alpha=0.7)

# Highlight the bargain players
sns.scatterplot(data=df_bargains, x='base_price_usd', y='performance_score', color='red', s=150, edgecolor='black', marker='*', label='Bargain')

plt.title('Performance vs. Price of All Players', fontsize=16)
plt.xlabel('Base Price (USD)', fontsize=12)
plt.ylabel('Performance Score', fontsize=12)
plt.legend(title='Player Role / Status')
plt.grid(True)
plt.tight_layout()
plt.show()
# - 

# ## 3. Conclusion
#
# This notebook demonstrates how to leverage advanced SQL queries directly from a Python environment to perform data analysis. We executed pre-defined SQL scripts to:
# 1.  Create a database schema.
# 2.  Load data.
# 3.  Engineer new features like `performance_score` and `value_for_money` in a SQL `VIEW`.
#
# We then executed complex analytical queries and used Python's visualization libraries to chart the results, providing clear, actionable insights into player value and performance. This workflow is a powerful combination of SQL's data processing capabilities and Python's analytical and visualization strengths.

# Close the connection
conn.close()
print("\nDatabase connection closed.")