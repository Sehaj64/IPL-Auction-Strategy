

import sqlite3
import pandas as pd
import os

def main():
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database', 'ipl.db'))
    sql_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database', '05_additional_questions.sql'))

    print(f"Database path: {db_path}")
    print(f"SQL file path: {sql_file_path}")

    if not os.path.exists(db_path):
        print(f"Error: Database file not found at {db_path}")
        return
    
    if not os.path.exists(sql_file_path):
        print(f"Error: SQL file not found at {sql_file_path}")
        return

    conn = sqlite3.connect(db_path)

    with open(sql_file_path, 'r') as f:
        all_queries = f.read()
    
    conn.executescript(all_queries)

    # Now run the SELECT queries and print the results
    queries = [
        "SELECT COUNT(DISTINCT city) AS total_cities FROM matches;",
        "SELECT COUNT(CASE WHEN ball_result = 'boundary' THEN 1 END) AS total_boundaries, COUNT(CASE WHEN ball_result = 'dot' THEN 1 END) AS total_dot_balls FROM deliveries_v02;",
        "SELECT batting_team, COUNT(*) AS total_boundaries FROM deliveries_v02 WHERE ball_result = 'boundary' GROUP BY batting_team ORDER BY total_boundaries DESC;",
        "SELECT bowling_team, COUNT(*) AS total_dot_balls FROM deliveries_v02 WHERE ball_result = 'dot' GROUP BY bowling_team ORDER BY total_dot_balls DESC;",
        "SELECT dismissal_kind, COUNT(*) AS total_dismissals FROM deliveries WHERE dismissal_kind IS NOT NULL GROUP BY dismissal_kind;",
        "SELECT bowler, SUM(extra_runs) AS total_extra_runs FROM deliveries GROUP BY bowler ORDER BY total_extra_runs DESC LIMIT 5;",
        "SELECT venue, SUM(total_runs) AS total_runs FROM deliveries_v03 GROUP BY venue ORDER BY total_runs DESC;",
        "SELECT SUBSTR(match_date, -4) AS year, SUM(total_runs) AS total_runs FROM deliveries_v03 WHERE venue = 'Eden Gardens' GROUP BY SUBSTR(match_date, -4) ORDER BY total_runs DESC;"
    ]

    for i, query in enumerate(queries):
        print(f"--- Query {i+1} ---")
        try:
            df = pd.read_sql_query(query, conn)
            print(df)
        except Exception as e:
            print(f"Error executing query: {e}")
        print("\n")


    conn.close()

if __name__ == '__main__':
    main()
