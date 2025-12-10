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



# +
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os



DB_FILE = os.path.join('database', 'ipl_auction.db')


def execute_sql_from_file(conn, filepath):
    with open(filepath, 'r') as f:
        conn.executescript(f.read())


if os.path.exists(DB_FILE):
    os.remove(DB_FILE)

conn = sqlite3.connect(DB_FILE)


execute_sql_from_file(conn, os.path.join('database', 'schema.sql'))
execute_sql_from_file(conn, os.path.join('database', 'data.sql'))
execute_sql_from_file(conn, os.path.join('database', '02_feature_engineering.sql'))

print("Database initialized and features engineered successfully.")


# ## 2. Execute and Visualize Analytical Queries




# +
# Read the specific query from the SQL file
with open(os.path.join('database', '03_analytical_queries.sql'), 'r') as f:
    all_queries = f.read().split(';')
    query1 = all_queries[0]

df_top_value_2023 = pd.read_sql_query(query1, conn)

print("Top 5 'Value for Money' Players in the 2023 Season:")
print(df_top_value_2023)


plt.figure(figsize=(10, 6))
sns.barplot(data=df_top_value_2023, x='value_for_money', y='name', palette='viridis')
plt.title('Top 5 "Value for Money" Players (2023 Season)', fontsize=16)
plt.xlabel('Value for Money Score (Performance Score per $1M)', fontsize=12)
plt.ylabel('Player Name', fontsize=12)
plt.tight_layout()
plt.show()
# -

# ### Query 2: Performance Trend for a Single Player (Virat Kohli)


# +
query2 = all_queries[1]
df_player_trend = pd.read_sql_query(query2, conn)

print("\nPerformance Trend for Virat Kohli:")
print(df_player_trend)

# Visualize the results
plt.figure(figsize=(10, 6))
plt.plot(df_player_trend['season'], df_player_trend['performance_score'], marker='o', linestyle='-', color='b')
plt.title('Virat Kohli: Performance Score Trend', fontsize=16)
plt.xlabel('Season', fontsize=12)
plt.ylabel('Calculated Performance Score', fontsize=12)
plt.xticks(df_player_trend['season'])
plt.grid(True)
plt.tight_layout()
plt.show()
# -

# ### Query 3: Comparing Role Performance Across Seasons



# +
# Read Query 3
query3 = all_queries[2]
df_role_trends = pd.read_sql_query(query3, conn)

print("\nAverage Performance Score by Role and Season:")
print(df_role_trends)

plt.figure(figsize=(12, 7))
sns.barplot(data=df_role_trends, x='role', y='avg_performance_score', hue='season', palette='magma')
plt.title('Comparison of Average Performance Score by Role Across Seasons', fontsize=16)
plt.xlabel('Player Role', fontsize=12)
plt.ylabel('Average Performance Score', fontsize=12)
plt.legend(title='Season')
plt.tight_layout()
plt.show()
# -




conn.close()
print("\nDatabase connection closed.")
