import streamlit as st
import pandas as pd
import sqlite3
import os

DB_FILE = os.path.join(os.path.dirname(__file__), 'database', 'ipl.db')

def main():
    st.set_page_config(layout="wide")
    st.title("IPL Data Analysis Dashboard")

    # DEBUG: Check if DB file exists and print size
    if not os.path.exists(DB_FILE):
        st.error(f"Database file not found at: {DB_FILE}")
        return
    
    file_size = os.path.getsize(DB_FILE)
    if file_size == 0:
        st.error(f"Database file is empty: {DB_FILE}")
        return
        
    # st.write(f"Database loaded. Size: {file_size / (1024*1024):.2f} MB")

    st.write("""
    This interactive dashboard presents a comprehensive analysis of Indian Premier League (IPL) cricket data,
    exploring key aspects of player performance, team strategies, and match dynamics.
    """)

    try:
        conn = sqlite3.connect(DB_FILE)
        
        # Question 1: Total Cities
        st.header("Q1: Total Number of Cities")
        query1 = "SELECT COUNT(DISTINCT city) AS total_cities FROM matches;"
        df1 = pd.read_sql_query(query1, conn)
        st.metric("Total Cities", df1['total_cities'][0])

        # Question 4: Total Boundaries by Team
        st.header("Q4: Total Boundaries by Team")
        query4 = "SELECT batting_team, COUNT(*) AS total_boundaries FROM deliveries WHERE total_runs >= 4 GROUP BY batting_team ORDER BY total_boundaries DESC;"
        df4 = pd.read_sql_query(query4, conn)
        st.dataframe(df4)
        st.bar_chart(df4.set_index('batting_team'))

        # Question 5: Total Dot Balls by Team
        st.header("Q5: Total Dot Balls by Team")
        query5 = "SELECT bowling_team, COUNT(*) AS total_dot_balls FROM deliveries WHERE total_runs = 0 GROUP BY bowling_team ORDER BY total_dot_balls DESC;"
        df5 = pd.read_sql_query(query5, conn)
        st.dataframe(df5)
        st.bar_chart(df5.set_index('bowling_team'))

        # Question 6: Dismissal Kinds
        st.header("Q6: Dismissal Kinds")
        query6 = "SELECT dismissal_kind, COUNT(*) AS total_dismissals FROM deliveries WHERE dismissal_kind IS NOT NULL GROUP BY dismissal_kind;"
        df6 = pd.read_sql_query(query6, conn)
        st.dataframe(df6)
        st.bar_chart(df6.set_index('dismissal_kind'))

        # New Analysis: Top Run Scorers
        st.header("Top 10 Run Scorers")
        query_runs = "SELECT batsman, SUM(batsman_runs) AS total_runs FROM deliveries GROUP BY batsman ORDER BY total_runs DESC LIMIT 10;"
        df_runs = pd.read_sql_query(query_runs, conn)
        st.dataframe(df_runs)
        st.bar_chart(df_runs.set_index('batsman'))

        # New Analysis: Top Wicket Takers
        st.header("Top 10 Wicket Takers")
        query_wickets = "SELECT bowler, COUNT(*) AS total_wickets FROM deliveries WHERE is_wicket = 1 AND dismissal_kind NOT IN ('run out', 'retired hurt', 'obstructing the field') GROUP BY bowler ORDER BY total_wickets DESC LIMIT 10;"
        df_wickets = pd.read_sql_query(query_wickets, conn)
        st.dataframe(df_wickets)
        st.bar_chart(df_wickets.set_index('bowler'))

        # New Analysis: Most Player of the Match Awards
        st.header("Top 10 Player of the Match Awards")
        query_pom = "SELECT player_of_match, COUNT(*) AS total_awards FROM matches WHERE player_of_match IS NOT NULL GROUP BY player_of_match ORDER BY total_awards DESC LIMIT 10;"
        df_pom = pd.read_sql_query(query_pom, conn)
        st.dataframe(df_pom)
        st.bar_chart(df_pom.set_index('player_of_match'))

        # New Analysis: Runs per Venue
        st.header("Total Runs Scored per Venue")
        query_venue = "SELECT venue, SUM(total_runs) AS total_runs_scored FROM matches JOIN deliveries ON matches.id = deliveries.id GROUP BY venue ORDER BY total_runs_scored DESC LIMIT 15;"
        df_venue = pd.read_sql_query(query_venue, conn)
        st.dataframe(df_venue)
        st.bar_chart(df_venue.set_index('venue'))

        conn.close()
        
    except Exception as e:
        st.error(f"An error occurred accessing the database: {e}")

if __name__ == '__main__':
    main()