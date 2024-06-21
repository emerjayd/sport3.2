-- Drop existing tables to reset the schema
DROP TABLE IF EXISTS PLAYER_GAME;
DROP TABLE IF EXISTS PLAYER;
DROP TABLE IF EXISTS GAME;
DROP TABLE IF EXISTS COACH;

-- Create COACH table
CREATE TABLE COACH (
    coach_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    address TEXT,
    yrs_experience INTEGER
);

-- Create PLAYER table
CREATE TABLE PLAYER (
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    score INTEGER,
    team TEXT
);

-- Create GAME table
CREATE TABLE GAME (
    game_id INTEGER PRIMARY KEY AUTOINCREMENT,
    home TEXT,
    away TEXT,
    date TEXT,
    time TEXT,
    location TEXT
);

-- Create PLAYER_GAME table for many-to-many relationship
CREATE TABLE PLAYER_GAME (
    player_id INTEGER,
    game_id INTEGER,
    PRIMARY KEY (player_id, game_id),
    FOREIGN KEY (player_id) REFERENCES PLAYER(player_id),
    FOREIGN KEY (game_id) REFERENCES GAME(game_id)
);
