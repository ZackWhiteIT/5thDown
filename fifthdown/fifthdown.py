# -*- coding: utf-8 -*-

import sqlite3
import requests
import click
from os import path
from bs4 import BeautifulSoup

DATA_DIR = path.abspath(path.join(path.dirname(__file__), '..', 'data'))
SQL_FILE = path.join(DATA_DIR, 'fifthdown.sqlite')


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


@click.group()
def cli():
    ''' Data behind the blocking and tackling '''
    pass


@cli.command('scrape', help='Retrieve annual team data')
@click.argument('url', required=True)
def scrape(url):
    ''' Scrape the specified team's statistics page '''
    # Request the page
    headers = {'user-agent': 'Mozilla/5.0:'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'lxml')

    # Find the team's overall statistics table
    # This table index works for 2008-current data
    team_totals_table = soup.findAll('table')[5]

    # Table setup:
    # TEAM STATISTICS, Team, Opponent
    # Left header, team data, opponent data
    # Left header, team data, opponent data
    # Left header, team data, opponent data

    # Create a pair of dictionaries (team & opponent)
    team = {}
    opponent = {}

    # Find data
    data_rows = team_totals_table.findAll('tr')
    for row in data_rows:
        data = [cell.text.strip() for cell in row.findAll('td')]
        team[data[0]] = data[1]  # Load team data
        opponent[data[0]] = data[2]  # Load opponent data

    for key, value in team.items():
        click.echo('{:<25} {:>15} {:>15}'.format(key, value, opponent[key]))


def main(agrs=None):
    ''' Simple testing '''
    cli()

if __name__ == "__main__":
    main()
