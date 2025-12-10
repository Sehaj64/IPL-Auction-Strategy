
-- Additional Questions

-- Q1: Total number of cities
SELECT COUNT(DISTINCT city) AS total_cities FROM matches;

-- Q2: Create a view with ball result (boundary, dot, other)
DROP VIEW IF EXISTS deliveries_v02;
CREATE TEMP VIEW deliveries_v02 AS
SELECT *,
       CASE
           WHEN total_runs >= 4 THEN 'boundary'
           WHEN total_runs = 0 THEN 'dot'
           ELSE 'other'
       END AS ball_result
FROM deliveries;

-- Q3: Total boundaries and dot balls
SELECT
    COUNT(CASE WHEN ball_result = 'boundary' THEN 1 END) AS total_boundaries,
    COUNT(CASE WHEN ball_result = 'dot' THEN 1 END) AS total_dot_balls
FROM deliveries_v02;

-- Q4: Total boundaries by team
SELECT
    batting_team,
    COUNT(*) AS total_boundaries
FROM deliveries_v02
WHERE ball_result = 'boundary'
GROUP BY batting_team
ORDER BY total_boundaries DESC;

-- Q5: Total dot balls by team
SELECT
    bowling_team,
    COUNT(*) AS total_dot_balls
FROM deliveries_v02
WHERE ball_result = 'dot'
GROUP BY bowling_team
ORDER BY total_dot_balls DESC;

-- Q6: Total dismissals by dismissal kind
SELECT
    dismissal_kind,
    COUNT(*) AS total_dismissals
FROM deliveries
WHERE dismissal_kind IS NOT NULL
GROUP BY dismissal_kind;

-- Q7: Top 5 bowlers with most extra runs
SELECT
    bowler,
    SUM(extra_runs) AS total_extra_runs
FROM deliveries
GROUP BY bowler
ORDER BY total_extra_runs DESC
LIMIT 5;

-- Q8: Create a view with venue and match date
DROP VIEW IF EXISTS deliveries_v03;
CREATE TEMP VIEW deliveries_v03 AS
SELECT d.*,
       m.venue,
       m.date AS match_date
FROM deliveries_v02 d
JOIN matches m ON d.id = m.id;

-- Q9: Total runs by venue
SELECT
    venue,
    SUM(total_runs) AS total_runs
FROM deliveries_v03
GROUP BY venue
ORDER BY total_runs DESC;

-- Q10: Total runs at Eden Gardens by year
SELECT
    SUBSTR(match_date, -4) AS year,
    SUM(total_runs) AS total_runs
FROM deliveries_v03
WHERE venue = 'Eden Gardens'
GROUP BY SUBSTR(match_date, -4)
ORDER BY total_runs DESC;
