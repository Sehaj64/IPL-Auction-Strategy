CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    season INTEGER NOT NULL,            -- e.g., 2022, 2023
    name TEXT NOT NULL,
    role TEXT NOT NULL,             -- e.g., 'Batsman', 'Bowler', 'All-rounder', 'Wicketkeeper'
    base_price_usd REAL NOT NULL,
    nationality TEXT NOT NULL,      -- e.g., 'Indian', 'Overseas'
    batting_avg REAL,               -- Nullable for bowlers
    strike_rate REAL,               -- Nullable for bowlers
    wickets INTEGER,                -- Nullable for batsmen
    economy_rate REAL,              -- Nullable for batsmen
    is_drafted INTEGER DEFAULT 0,   -- 0 for not drafted, 1 for drafted
    UNIQUE(season, name)
);
