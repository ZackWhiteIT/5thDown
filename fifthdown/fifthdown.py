# -*- coding: utf-8 -*-

import sqlite3
import numpy
import os.path

SQL_FILE = 'fbsim.sqlite'


def liteDBConnect():
    ''' Connects to the database '''

    # Currently using SQLite3; Moving to Postgres eventually...

    # If the file doesn't exist, it's created automatically by the SQLite3
    # library.
    return sqlite3.connect(SQL_FILE)


def liteDBBuild():
    ''' Build the SQLite3 database for the sim engine '''

    # Build team table
    # id (int) primary key, name (varchar30), mascot (varchar30), city
    # (varchar30), state (char2)

    team_table = ''' CREATE TABLE team
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT,
                     mascot TEXT, city TEXT, state TEXT);
                 '''

    with liteDBConnect() as db:
        cursor = db.cursor()
        cursor.execute(team_table)
        db.commit()

    # Build game table
    # id (int) primary key, home_id (int), away_id (int), home_score (int),
    # away_score (int)

    game_table = ''' CREATE TABLE game
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, home_id INTEGER,
                     away_id INTEGER, home_score INTEGER, away_score INTEGER);
                 '''

    with liteDBConnect() as db:
        cursor = db.cursor()
        cursor.execute(game_table)
        db.commit()


def addTeam(name, mascot, city, state):
    ''' Add a team to the database '''

    add_team = ''' INSERT INTO team (name, mascot, city, state)
                   VALUES ('{}', '{}', '{}', '{}');
               '''.format(name, mascot, city, state)

    with liteDBConnect() as db:
        cursor = db.cursor()
        cursor.execute(add_team)
        db.commit()


def simGame(home_team_id, away_team_id):
    ''' Drop a random score in for a game on a bell curve '''

    score_mean = 17
    score_standard_deviation = 14
    home_score = -1
    away_score = -1

    # Generate scores from a normal distribution with limits of 0 and 63 points
    while home_score < 0 or home_score > 63 or home_score == 1:
        home_score = numpy.random.normal(score_mean, score_standard_deviation)
        home_score = int(home_score)

    while away_score < 0 or away_score > 63 or away_score == 1:
        away_score = numpy.random.normal(score_mean, score_standard_deviation)
        away_score = int(away_score)

    with liteDBConnect() as db:
        game_insert = ''' INSERT INTO game (home_id, away_id, home_score, away_score)
                          VALUES ({}, {}, {}, {});
                      '''.format(home_team_id, away_team_id,
                                 home_score, away_score)
        cursor = db.cursor()
        cursor.execute(game_insert)
        db.commit()


def latestGameResult():
    ''' Print the latest game result in the database '''

    latest_id = ''' SELECT g.id, h.name, ' ', g.home_score, ' - ', g.away_score,
                           ' ', a.name
                    FROM game AS g
                    JOIN team h ON g.home_id = h.id
                    JOIN team a ON g.away_id = a.id
                    ORDER BY g.id DESC LIMIT 1;
                '''
    result = None

    with liteDBConnect() as db:
        cursor = db.cursor()
        result = cursor.execute(latest_id).fetchone()
        db.commit()

    return result


def main():
    ''' Simple testing '''

    # Build the DB if needed
    if not os.path.exists(SQL_FILE):
        liteDBBuild()

        # Add a few teams for testing for the new DB
        addTeam('Adams College', 'Atoms', 'Atlanta', 'GA')
        addTeam('Faber College', 'Mongols', 'Eugene', 'OR')

    # Sim a game and return the result
    simGame(1, 2)
    print(''.join(str(column) for column in latestGameResult()[1:]))

if __name__ == "__main__":
    main()
