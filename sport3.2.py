import sqlite3
import pandas as pd
from prettytable import PrettyTable
def insert_data_from_csv(cursor, csv_file_path):
    # Read the CSV file and specify column names
    column_names = ['FirstName', 'LastName', 'Score', 'Team']
    players_df = pd.read_csv(csv_file_path, names=column_names, header=None)

    # Insert data into PLAYER table
    for _, row in players_df.iterrows():
        cursor.execute('''
        INSERT INTO PLAYER (number, first_name, last_name, score, team)
        VALUES (?, ?, ?, ?, ?)
        ''', (None, row['FirstName'], row['LastName'], row['Score'], row['Team']))
        
def read_db(cursor):
    cursor.execute('SELECT * FROM PLAYER')
    players = cursor.fetchall()

    # Create a PrettyTable object
    table = PrettyTable()
    table.field_names = ["Player ID", "First Name", "Last Name", "Score", "Team"]

    for player in players:
        table.add_row(player)
    
    print(table)
    
# def read_db(cursor):
#     cursor.execute('SELECT * FROM PLAYER')
#     players = cursor.fetchall()
#     for player in players:
#         print(player)

def delete_data(cursor):
    cursor.execute('DELETE FROM PLAYER')
    cursor.execute('DELETE FROM PLAYER_GAME')
    print("All data deleted from PLAYER and PLAYER_GAME tables.")

def custom_sql(cursor, conn):
    sql = input("Enter your SQL command: ")
    try:
        cursor.execute(sql)
        if sql.strip().lower().startswith("select"):
            results = cursor.fetchall()
            for result in results:
                print(result)
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
        SELECT GAME.game_id, GAME.home, GAME.away, GAME.date
        FROM GAME
        JOIN PLAYER_GAME ON GAME.game_id = PLAYER_GAME.game_id
        WHERE PLAYER_GAME.player_id = ?
        ''', (player_id,))
        games = cursor.fetchall()
        for game in games:
            print(game)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def main():
    conn = sqlite3.connect('sport3.2.db')
    cursor = conn.cursor()

    while True:
        print("Options - 1: Read db, 2: Delete data, 3: Populate database, 4: Link player to game, 5: View player games, 99: CUSTOM SQL, 0: Exit")
        choice = input("Make a choice: ")

        if choice == '1':
            read_db(cursor)
        elif choice == '2':
            delete_data(cursor)
            conn.commit()
        elif choice == '3':
            csv_file_path = 'players.csv'
            insert_data_from_csv(cursor, csv_file_path)
            conn.commit()
            print("Database populated with data from CSV.")
        elif choice == '4':
            link_player_to_game(cursor)
            conn.commit()
        elif choice == '5':
            view_player_games(cursor)
        elif choice == '99':
            custom_sql(cursor, conn)
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

    conn.close()

if __name__ == "__main__":
    main()
