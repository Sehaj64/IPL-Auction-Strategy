# IPL Data Analysis Dashboard

This project presents an end-to-end data science solution for analyzing Indian Premier League (IPL) cricket data. It leverages advanced SQL for in-depth analysis and feature engineering, and provides an interactive web dashboard built with Streamlit for intuitive data exploration.

The goal of this project is to uncover insights about player performance, team strategies, and match dynamics, making the findings accessible to a broad audience.

## Key Features

*   **Data Pipeline:** Robust data loading and cleaning processes for ball-by-ball and match data into a structured SQLite database.
*   **Advanced SQL Analysis:** Utilizes complex SQL queries, including Window Functions and Common Table Expressions (CTEs), to derive key performance indicators and answer various analytical questions.
*   **Interactive Dashboard:** A user-friendly web application developed with Streamlit for visualizing player statistics, team performance, and match insights.
*   **Player Performance Metrics:** Calculation of custom metrics to evaluate player value and identify key trends.

## Skills Demonstrated

*   **Programming Languages:** Python, SQL
*   **Data Manipulation & Analysis:** Pandas, SQLite
*   **Data Visualization:** Matplotlib, Seaborn, Streamlit
*   **Software Engineering Practices:** Git, GitHub, virtual environments, modular scripting, application development.
*   **Data Storytelling:** Communicating complex analytical insights through an interactive web interface.

## Project Structure

```
.
├── database/
│   ├── data.sql                        # Original sample player data (deprecated)
│   ├── deliveries.csv                  # Raw ball-by-ball data
│   ├── ipl.db                          # SQLite database
│   ├── load_data.py                    # Script to load CSV data into ipl.db
│   ├── matches.csv                     # Raw match summary data
│   ├── schema.sql                      # Original player schema (deprecated)
│   ├── schema_presentation.sql         # New schema for matches and deliveries tables
│   ├── 02_feature_engineering.sql      # SQL for feature engineering (deprecated with new data)
│   ├── 03_analytical_queries.sql       # Original analytical queries (deprecated with new data)
│   ├── 04_wicketkeeper_analysis.sql    # SQL for wicketkeeper analysis
│   └── 05_additional_questions.sql     # SQL for new analytical questions
│
├── notebooks/
│   ├── 01_EDA_and_Visualization.py     # Original EDA and visualization notebook (deprecated with new data)
│   ├── 02_Additional_Analysis.py       # Script to run and display new analytical questions
│   └── 02_Player_Value_Prediction_Model.py # Placeholder for ML model
│
├── app.py                              # Streamlit web application for interactive dashboard
├── check_env.py                        # Environment checking script (for debugging)
├── .gitignore
├── README.md
└── requirements.txt
```

## How to Run the Project

Follow these steps to set up and run the IPL Data Analysis Dashboard locally:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Sehaj64/IPL-Auction-Strategy.git
    cd IPL-Auction-Strategy
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required Python libraries:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Load the data into the SQLite database:**
    This script will create `ipl.db` and populate it with `matches.csv` and `deliveries.csv`.
    ```bash
    python database/load_data.py
    ```

5.  **Run the Interactive Dashboard:**
    ```bash
    streamlit run /workspaces/IPL-Auction-Strategy/app.py
    ```
    *   **Local Machine:** Your web browser will automatically open to the Streamlit dashboard (usually at `http://localhost:8501`).
    *   **GitHub Codespaces:** Once the command runs, Streamlit will typically provide a link in the terminal or a pop-up notification (via the "Ports" tab) to open the application in your browser. Click on this provided external link to access the dashboard.

## Analysis Highlights (from Dashboard)

The interactive dashboard provides insights into various aspects of IPL data, including:

*   Total number of unique cities where matches were played.
*   Distribution of boundaries and dot balls.
*   Team-wise performance metrics for boundaries and dot balls.
*   Analysis of dismissal types.
*   Top bowlers by extra runs conceded.
*   Total runs scored at different venues.
*   Year-wise run analysis for specific venues like Eden Gardens.
*   Wicketkeeper performance based on batting metrics.
