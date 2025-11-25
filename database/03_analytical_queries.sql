-- 03_analytical_queries.sql

-- This script contains several complex, insightful queries for analysis.
-- These queries will be executed from our Jupyter Notebook.

-- Query 1: Find the top 5 most "value-for-money" players for the most recent season (2023).
-- This demonstrates filtering on the engineered feature view.
SELECT
    name,
    role,
    performance_score,
    value_for_money
FROM
    player_features
WHERE
    season = 2023
ORDER BY
    value_for_money DESC
LIMIT 5;


-- Query 2: Show the performance trend of a specific player (e.g., Virat Kohli) across seasons.
-- This demonstrates tracking performance over time.
SELECT
    season,
    name,
    batting_avg,
    strike_rate,
    performance_score
FROM
    player_features
WHERE
    name = 'Virat Kohli'
ORDER BY
    season;


-- Query 3: Compare the average performance of key roles (Batsman, Bowler) between seasons.
-- This demonstrates trend analysis at an aggregate level.
SELECT
    season,
    role,
    COUNT(id) as number_of_players,
    AVG(performance_score) as avg_performance_score
FROM
    player_features
WHERE
    role IN ('Batsman', 'Bowler')
GROUP BY
    season,
    role
ORDER BY
    role,
    season;
