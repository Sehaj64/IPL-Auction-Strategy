-- 02_feature_engineering.sql

-- This script creates a view that adds engineered features to the player data.
-- These features will help in more advanced analysis.

-- Drop the view if it already exists to make this script idempotent
DROP VIEW IF EXISTS player_features;

-- Create a view with engineered features
CREATE VIEW player_features AS
WITH calculated_scores AS (
    SELECT
        id,
        name,
        role,
        base_price_usd,
        nationality,
        batting_avg,
        strike_rate,
        wickets,
        economy_rate,
        is_drafted,
        -- Calculate a simple performance score based on role
        CASE
            WHEN role = 'Batsman' THEN (batting_avg * 1.5) + (strike_rate * 0.5)
            WHEN role = 'Wicketkeeper' THEN (batting_avg * 1.5) + (strike_rate * 0.5)
            WHEN role = 'Bowler' THEN (wickets * 2.0) - (economy_rate * 1.0)
            WHEN role = 'All-rounder' THEN (batting_avg * 1.0) + (strike_rate * 0.5) + (wickets * 1.5) - (economy_rate * 0.5)
            ELSE 0
        END AS performance_score
    FROM
        players
)
SELECT
    *,
    -- Calculate value for money (score per million USD)
    -- Avoid division by zero for players with no price
    CASE
        WHEN base_price_usd > 0 THEN (performance_score / (base_price_usd / 1000000))
        ELSE 0
    END AS value_for_money
FROM
    calculated_scores;

-- Example of how to use this view:
-- SELECT name, role, performance_score, value_for_money
-- FROM player_features
-- ORDER BY value_for_money DESC;
