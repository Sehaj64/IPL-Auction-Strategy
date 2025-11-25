-- 03_analytical_queries.sql

-- This script contains several complex, insightful queries for analysis.
-- These queries will be executed from our Jupyter Notebook.

-- Query 1: Find the top 5 most "value-for-money" players in each role.
-- This demonstrates window functions, CTEs, and ranking.
WITH ranked_players AS (
    SELECT
        name,
        role,
        performance_score,
        value_for_money,
        ROW_NUMBER() OVER(PARTITION BY role ORDER BY value_for_money DESC) as rank_in_role
    FROM
        player_features
)
SELECT
    name,
    role,
    performance_score,
    value_for_money
FROM
    ranked_players
WHERE
    rank_in_role <= 5;


-- Query 2: Compare the average performance of Indian vs. Overseas players in each role.
-- This demonstrates grouping, aggregation, and joining.
SELECT
    role,
    nationality,
    COUNT(id) as number_of_players,
    AVG(performance_score) as avg_performance_score
FROM
    player_features
GROUP BY
    role,
    nationality
ORDER BY
    role,
    avg_performance_score DESC;


-- Query 3: Identify potential "bargain" players.
-- These are players in the lower 50% of price but upper 50% of performance score for their role.
-- Note: SQLite doesn't have PERCENTILE_CONT, so this is a conceptual query.
-- We will implement a workaround in Python if this cannot be run directly.
WITH role_medians AS (
    SELECT
        role,
        AVG(base_price_usd) as median_price, -- Using AVG as a proxy for median
        AVG(performance_score) as median_score -- Using AVG as a proxy for median
    FROM player_features
    GROUP BY role
)
SELECT
    p.name,
    p.role,
    p.base_price_usd,
    p.performance_score
FROM
    player_features p
JOIN
    role_medians rm ON p.role = rm.role
WHERE
    p.base_price_usd < rm.median_price
    AND p.performance_score > rm.median_score
ORDER BY
    p.role,
    p.performance_score DESC;
