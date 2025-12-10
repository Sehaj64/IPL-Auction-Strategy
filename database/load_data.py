
import sqlite3
import pandas as pd
import os

def main():
    db_path = os.path.join(os.path.dirname(__file__), 'ipl.db')
    schema_path = os.path.join(os.path.dirname(__file__), 'schema_presentation.sql')
    matches_csv_path = os.path.join(os.path.dirname(__file__), 'matches.csv')
    deliveries_csv_path = os.path.join(os.path.dirname(__file__), 'deliveries.csv')

    # Connect to the database and create tables
    with open(schema_path, 'r') as f:
        schema_sql = f.read()
    
    with sqlite3.connect(db_path) as conn:
        conn.executescript(schema_sql)

    # Load data from CSVs into the database
    with sqlite3.connect(db_path) as conn:
        # Load matches data
        df_matches = pd.read_csv(matches_csv_path)
        df_matches.to_sql('matches', conn, if_exists='replace', index=False)

        # Load deliveries data
        df_deliveries = pd.read_csv(deliveries_csv_path)
        df_deliveries.to_sql('deliveries', conn, if_exists='replace', index=False)

if __name__ == '__main__':
    main()
