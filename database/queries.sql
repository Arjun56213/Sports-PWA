-- Step 1: Setup database and tables

-- Users Table: Stores user credentials and data
CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    created_at TEXT NOT NULL
);

-- Cricket Batting Table: Stores batting performance data

CREATE TABLE IF NOT EXISTS Cricket_Batting (
    batting_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    opposition TEXT NOT NULL,
    venue TEXT NOT NULL,
    format TEXT NOT NULL,
    runs INTEGER DEFAULT 0,
    balls INTEGER DEFAULT 0,
    dismissal TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Cricket Bowling Table: Stores bowling performance data

CREATE TABLE IF NOT EXISTS Cricket_Bowling (
    bowling_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    opposition TEXT NOT NULL,
    venue TEXT NOT NULL,
    format TEXT NOT NULL,
    overs REAL DEFAULT 0,
    wickets INTEGER DEFAULT 0,
    runs_conceded INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Soccer Performance Table: Stores soccer performance data

CREATE TABLE IF NOT EXISTS Soccer_Performance (
    match_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    opposition TEXT NOT NULL,
    venue TEXT NOT NULL,
    goals INTEGER DEFAULT 0,
    assists INTEGER DEFAULT 0,
    result TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);