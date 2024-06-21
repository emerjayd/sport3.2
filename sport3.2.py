import sqlite3
import pandas as pd
from prettytable import PrettyTable

def insert_data_from_csv(cursor, csv_file_path):
    column_names = ['FirstName', 'LastName', 'Score', 'Team']
    players_df = pd.read_csv(csv_file_path, names=column_names, header=None)

    for _, row in players_df.iterrows():
        cursor.execute('''
        INSERT INTO PLAYER (first_name, last_name, score, team)
        VALUES (?, ?, ?, ?)
        ''', (row['FirstName'], row['LastName'], row['Score'], row['Team']))

def populate_game_table(cursor):
    games = [
        ("Home1", "Away1", "2024-06-25", "15:00", "Location1"),
        ("Home2", "Away2", "2024-06-26", "16:00", "Location2"),
        ("Home3", "Away3", "2024-06-27", "17:00", "Location3")
    ]

    for game in games:
        cursor.execute('''
        INSERT INTO GAME (home, away, date, time, location)
        VALUES (?, ?, ?, ?, ?)
        ''', game)
    print("GAME table populated with sample data.")

def read_db(cursor):
    cursor.execute('SELECT * FROM PLAYER')
    players = cursor.fetchall()

    table = PrettyTable()
    table.field_names = ["Player ID", "First Name", "Last Name", "Score", "Team"]

    for player in players:
        table.add_row(player)

    print(table)

def read_game_db(cursor):
    cursor.execute('SELECT * FROM GAME')
    games = cursor.fetchall()

    table = PrettyTable()
    table.field_names = ["Game ID", "Home", "Away", "Date", "Time", "Location"]

    for game in games:
        table.add_row(game)

    print(table)

def read_player_game_db(cursor):
    cursor.execute('SELECT * FROM PLAYER_GAME')
    player_games = cursor.fetchall()

    table = PrettyTable()
    table.field_names = ["Player ID", "Game ID"]

    for player_game in player_games:
        table.add_row(player_game)

    print(table)

def read_linked_players_games(cursor):
    cursor.execute('''
    SELECT PLAYER.player_id, PLAYER.first_name, PLAYER.last_name, GAME.game_id, GAME.home, GAME.away, GAME.date
    FROM PLAYER
    JOIN PLAYER_GAME ON PLAYER.player_id = PLAYER_GAME.player_id
    JOIN GAME ON PLAYER_GAME.game_id = GAME.game_id
    ''')
    links = cursor.fetchall()

    table = PrettyTable()
    table.field_names = ["Player ID", "First Name", "Last Name", "Game ID", "Home", "Away", "Date"]

    for link in links:
        table.add_row(link)

    print(table)

def delete_data(cursor):
    cursor.execute('DELETE FROM PLAYER_GAME')
    cursor.execute('DELETE FROM PLAYER')
    cursor.execute('DELETE FROM GAME')
    print("All data deleted from PLAYER, PLAYER_GAME, and GAME tables.")

def custom_sql(cursor, conn):
    sql = input("Enter your SQL command: ")
    try:
        cursor.execute(sql)
        if sql.strip().lower().startswith("select"):
            results = cursor.fetchall()
            table = PrettyTable()
            table.field_names = [desc[0] for desc in cursor.description]
            for result in results:
                table.add_row(result)
            print(table)
        else:
            conn.commit()
            print("SQL command executed successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def link_player_to_game(cursor):
    player_id = input("Enter player_id to link: ")
    game_id = input("Enter game_id to link: ")
    try:
        cursor.execute('''
        INSERT INTO PLAYER_GAME (player_id, game_id)
        VALUES (?, ?)
        ''', (player_id, game_id))
        print("Player linked to game successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def view_player_games(cursor):
    player_id = input("Enter player_id to view games: ")
    try:
        cursor.execute('''
        SELECT PLAYER.player_id, PLAYER.first_name, PLAYER.last_name, GAME.game_id, GAME.home, GAME.away, GAME.date
        FROM PLAYER
        JOIN PLAYER_GAME ON PLAYER.player_id = PLAYER_GAME.player_id
        JOIN GAME ON PLAYER_GAME.game_id = GAME.game_id
        WHERE PLAYER.player_id = ?
        ''', (player_id,))
        games = cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["Player ID", "First Name", "Last Name", "Game ID", "Home", "Away", "Date"]
        for game in games:
            table.add_row(game)
        print(table)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def main():
    conn = sqlite3.connect('sports.db')
    cursor = conn.cursor()

    while True:
        print("Options - 1: Read PLAYER table, 2: Read GAME table, 3: Read PLAYER_GAME table, 4: Delete data, 5: Populate PLAYER table, 6: Populate GAME table, 7: Link player to game, 8: View player games, 9: View linked players and games, 99: CUSTOM SQL, 0: Exit")
        choice = input("Make a choice: ")

        if choice == '1':
            read_db(cursor)
        elif choice == '2':
            read_game_db(cursor)
        elif choice == '3':
            read_player_game_db(cursor)
        elif choice == '4':
            delete_data(cursor)
            conn.commit()
        elif choice == '5':
            csv_file_path = 'C:\\Documents P5 2\\Academy\\Databases\\sport3.1\\players.csv'  # Update with the correct path
            insert_data_from_csv(cursor, csv_file_path)
            conn.commit()
            print("PLAYER table populated with data from CSV.")
        elif choice == '6':
            populate_game_table(cursor)
            conn.commit()
        elif choice == '7':
            link_player_to_game(cursor)
            conn.commit()
        elif choice == '8':
            view_player_games(cursor)
        elif choice == '9':
            read_linked_players_games(cursor)
        elif choice == '99':
            custom_sql(cursor, conn)
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

    conn.close()

if __name__ == "__main__":
    main()
