CREATE TABLE IF NOT EXISTS PLAYER (
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    number INTEGER,
    first_name TEXT,
    last_name TEXT,
    score INTEGER,
    team TEXT
);

CREATE TABLE IF NOT EXISTS GAME (
    game_id INTEGER PRIMARY KEY AUTOINCREMENT,
    home TEXT,
    away TEXT,
    date TEXT,
    time TEXT,
    location TEXT
);

CREATE TABLE IF NOT EXISTS PLAYER_GAME (
    player_id INTEGER,
    game_id INTEGER,
    PRIMARY KEY (player_id, game_id),
    FOREIGN KEY (player_id) REFERENCES PLAYER(player_id),
    FOREIGN KEY (game_id) REFERENCES GAME(game_id)
);
