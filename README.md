# Advanced SQL and Data Visualization for IPL Player Analysis

This project demonstrates a professional data science workflow, using advanced SQL for in-database analysis and feature engineering, and Python for execution and visualization. The analysis is centered on a dataset of IPL (Indian Premier League) cricket players, with the goal of uncovering insights about player performance and value.

This project serves as a direct, practical application of the concepts detailed in the "Decoding SQL: A Foundational Guide" presentation. It showcases how fundamental SQL knowledge can be extended to solve complex data analysis problems.

## Key Skills Demonstrated

*   **Advanced SQL:** Use of Common Table Expressions (CTEs), Window Functions (`ROW_NUMBER`), complex joins, and aggregations to perform analysis directly within the database.
*   **Feature Engineering:** Creating new, insightful features (e.g., `performance_score`, `value_for_money`) from base data using SQL.
*   **Data Analysis:** Asking and answering analytical questions with data to provide actionable insights.
*   **Data Visualization:** Using Python libraries (`matplotlib`, `seaborn`) to create clear and professional charts that communicate the results of the SQL queries.
*   **Python & Jupyter Notebooks:** Using Python as a control layer to execute SQL and present findings in a standard data science environment.

## Project Structure

```
.
├── database/
│   ├── schema.sql                     # Base table schema for players
│   ├── data.sql                       # INSERT statements for sample player data
│   ├── 02_feature_engineering.sql     # Creates a SQL VIEW with new calculated features
│   └── 03_analytical_queries.sql      # Contains complex queries for analysis
│
├── notebooks/
│   └── 01_EDA_and_Visualization.py    # Jupyter Notebook (as .py) to run the analysis and create plots
│
└── README.md
```

## How to Run the Analysis

1.  **Clone the repository.**

2.  **Navigate to the project directory.**

3.  **Create and activate a virtual environment (recommended):**
    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

4.  **Install the required Python libraries:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Start the Jupyter Notebook server:**
    ```bash
    jupyter notebook
    ```
    This will open a new tab in your web browser.

6.  **Open and run the notebook:**
    Navigate to the `notebooks/` directory in the Jupyter interface and open the `01_EDA_and_Visualization.py` file. You can then run the cells sequentially to see the analysis and visualizations.

## Analysis Highlights

The analysis performed in this project leverages multi-year data to answer several key questions:

*   **Who were the top "value-for-money" players in the most recent season?**
    *   This is determined by a custom `performance_score` relative to the player's base price for the 2023 season.
*   **How has a star player's performance trended over time?**
    *   The analysis tracks Virat Kohli's performance score across the 2022 and 2023 seasons to visualize his form.
*   **How has the average performance of key roles changed year-over-year?**
    *   The project compares the average performance of Batsmen and Bowlers between seasons to identify trends.