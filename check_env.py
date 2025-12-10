import os
import sqlite3

def main():
    print(f"Current Working Directory: {os.getcwd()}")
    
    db_path = os.path.join('database', 'ipl.db')
    sql_path = os.path.join('database', '05_additional_questions.sql')

    print(f"Checking for database at: {os.path.abspath(db_path)}")
    if os.path.exists(db_path):
        print("Database file found.")
    else:
        print("!!! Database file NOT found. !!!")
        return

    print(f"Checking for SQL file at: {os.path.abspath(sql_path)}")
    if os.path.exists(sql_path):
        print("SQL file found.")
    else:
        print("!!! SQL file NOT found. !!!")
        return

    try:
        print("Connecting to the database...")
        conn = sqlite3.connect(db_path)
        print("Database connection successful.")
        
        print("Running a simple query...")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tables in the database: {tables}")
        conn.close()
        print("Database connection closed.")
    except Exception as e:
        print(f"!!! Error interacting with the database: {e} !!!")
        return

    try:
        print("Reading the SQL file...")
        with open(sql_path, 'r') as f:
            content = f.read()
        print("SQL file read successfully.")
        if content:
            print("SQL file is not empty.")
        else:
            print("!!! SQL file is empty. !!!")
    except Exception as e:
        print(f"!!! Error reading the SQL file: {e} !!!")
        return

    print("\nEnvironment check completed. If there were no errors, the environment seems to be set up correctly.")

if __name__ == '__main__':
    main()
