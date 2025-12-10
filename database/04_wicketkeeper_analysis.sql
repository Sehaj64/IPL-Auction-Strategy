-- This query ranks wicketkeepers based on their batting performance.
-- A good wicketkeeper is expected to have a high batting average and strike rate.
SELECT
    name,
    season,
    batting_avg,
    strike_rate,
    performance_score
FROM
    player_features
WHERE
    role = 'Wicketkeeper'
ORDER BY
    performance_score DESC;
