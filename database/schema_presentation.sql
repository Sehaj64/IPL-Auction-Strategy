CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY,
    city TEXT,
    date TEXT,
    player_of_match TEXT,
    venue TEXT,
    neutral_venue INTEGER,
    team1 TEXT,
    team2 TEXT,
    toss_winner TEXT,
    toss_decision TEXT,
    winner TEXT,
    result TEXT,
    result_margin INTEGER,
    eliminator TEXT,
    method TEXT,
    umpire1 TEXT,
    umpire2 TEXT
);

CREATE TABLE IF NOT EXISTS deliveries (
    id INTEGER,
    inning INTEGER,
    over INTEGER,
    ball INTEGER,
    batsman TEXT,
    non_striker TEXT,
    bowler TEXT,
    batsman_runs INTEGER,
    extra_runs INTEGER,
    total_runs INTEGER,
    is_wicket INTEGER,
    dismissal_kind TEXT,
    player_dismissed TEXT,
    fielder TEXT,
    extras_type TEXT,
    batting_team TEXT,
    bowling_team TEXT
);
