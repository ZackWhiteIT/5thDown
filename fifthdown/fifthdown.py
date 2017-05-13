# -*- coding: utf-8 -*-

import records
import requests
import click
import csv
from os import path
from os import makedirs
from bs4 import BeautifulSoup

DATA_DIR = path.abspath(path.join(path.dirname(__file__), 'data'))
DB_FILE = path.join(DATA_DIR, 'fifthdown.db')

def build_database():
    ''' Build the SQLite3 Database '''
    db = records.Database('sqlite:///' + DB_FILE)
    DB_BUILD_COMMAND = path.abspath(path.join(path.dirname(__file__), 'sql', 'create_db.sql'))
    db.query_file(DB_BUILD_COMMAND)
    click.echo('Fifth Down database created at ' + DB_FILE)

@click.group()
def cli():
    ''' Data behind the blocking and tackling '''
    pass


@cli.command('load', help='Load CSV into database')
@click.argument('file', type=click.Path(exists=True), required=True)
def load(file):
    ''' Load CSV into database'''
    click.echo(click.format_filename(file))


@cli.command('scrapemega', help='Retrieve annual team data for multiple teams from CSV file containing URL/export path pair')
@click.argument('file', type=click.Path(exists=True), required=True)
@click.pass_context
def scrape_mega(ctx, file):
    ''' Retrieve annual team data for multiple teams from CSV file containing URL/export path pair '''
    # Parse CSV file for URL/export path pairs
    with open(file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            url = row[0]
            export_path = path.dirname(path.abspath(row[1]))
            export_file = path.basename(path.abspath(row[1]))

            # Create the path if it does not exist
            if path.exists(export_path) is False:
                makedirs(export_path)
                click.echo(export_path + " created")

            csv_export = path.join(export_path, export_file)

            # Don't scrape if the file already exists
            if path.exists(csv_export) is False:
                # Scrape
                team_data = ctx.invoke(scrape, url=url)
                with open(csv_export, 'w') as output:
                    writer = csv.writer(output)
                    for data in team_data:
                        writer.writerow(data)
            else:
                click.echo('Data file ' + csv_export + ' already exists')


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

    results = []

    for key, value in team.items():
        click.echo('{:<25} {:>15} {:>15}'.format(key, value, opponent[key]))
        results.append([key, value, opponent[key]])

    return results


def main(agrs=None):
    ''' Simple testing '''
    if path.isfile(DB_FILE) is False:
        build_database()
    else:
        click.echo('Fifth Down database ' + DB_FILE + ' already exists')
    cli()


if __name__ == "__main__":
    main()
