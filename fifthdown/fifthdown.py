# -*- coding: utf-8 -*-

import records
import requests
import click
import csv
from os import path
from os import makedirs
from os import listdir
from os import walk
from bs4 import BeautifulSoup

DATA_DIR = path.abspath(path.join(path.dirname(__file__), 'data'))
DB_FILE = path.join(DATA_DIR, 'fifthdown.db')


def build_database():
    ''' Build the SQLite3 Database '''
    db = records.Database('sqlite:///' + DB_FILE)
    DB_BUILD_COMMAND = path.abspath(
        path.join(path.dirname(__file__), 'sql', 'create_db.sql'))
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
    with open(file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            click.echo(row)


@cli.command('loadmega', help='Recursively load all CSV files in a path into database')
@click.argument('dir', type=click.Path(exists=True), required=True)
def load_mega(dir):
    ''' Load CSV into database'''
    for root, subdirectory, files in walk(dir):
        for file in files:
            file_path = path.join(path.abspath(root), file)
            offense_dict = {}
            defense_dict = {}
            with open(file_path, 'r') as f:
                click.echo('Processing data file ' + file_path + '...')
                reader = csv.reader(f)
                reader_data = [row for row in reader]
                if len(reader_data) > 0:
                    # Parse offense
                    offense_dict['team'] = reader_data[0][1]
                    offense_dict['year'] = path.dirname(
                        file_path).split('/')[-2]
                    if int(offense_dict['year']) < 2012:
                        ''' 2008-2012 data map for SideArm Sports '''
                        offense_dict['off_def'] = 'offense'
                        offense_dict['points'] = reader_data[1][1]
                        offense_dict['points_per_game'] = reader_data[2][1]
                        offense_dict['first_downs'] = reader_data[3][1]
                        offense_dict['rush_first_downs'] = reader_data[4][1]
                        offense_dict['pass_first_downs'] = reader_data[5][1]
                        offense_dict['penalty_first_downs'] = reader_data[6][1]
                        offense_dict['rush_yards'] = reader_data[7][1]
                        offense_dict['rush_yards_gained'] = reader_data[8][1]
                        offense_dict['rush_yards_lost'] = reader_data[9][1]
                        offense_dict['rush_attempts'] = reader_data[10][1]
                        offense_dict['rush_yards_per_attempt'] = reader_data[11][1]
                        offense_dict['rush_yards_per_game'] = reader_data[12][1]
                        offense_dict['rush_td'] = reader_data[13][1]
                        offense_dict['pass_yards'] = reader_data[14][1]
                        pass_tuple = str(reader_data[15][1]).split('-')
                        offense_dict['pass_attempts'] = pass_tuple[0]
                        offense_dict['pass_completions'] = pass_tuple[1]
                        offense_dict['interceptions'] = pass_tuple[2]
                        offense_dict['pass_yards_per_attempt'] = reader_data[16][1]
                        offense_dict['pass_yards_per_completion'] = reader_data[17][1]
                        offense_dict['pass_td'] = reader_data[18][1]
                        offense_dict['yards'] = reader_data[19][1]
                        offense_dict['plays'] = reader_data[20][1]
                        offense_dict['yards_per_play'] = reader_data[21][1]
                        kick_return_tuple = str(reader_data[22][1]).split('-')
                        offense_dict['kick_return_attempts'] = kick_return_tuple[0]
                        offense_dict['kick_return_yards'] = kick_return_tuple[1]
                        punt_return_tuple = str(reader_data[23][1]).split('-')
                        offense_dict['punt_return_attempts'] = punt_return_tuple[0]
                        offense_dict['punt_return_yards'] = punt_return_tuple[1]
                        int_return_tuple = str(reader_data[24][1]).split('-')
                        offense_dict['int_return_attempts'] = int_return_tuple[0]
                        offense_dict['int_return_yards'] = int_return_tuple[1]
                        offense_dict['kick_return_yards_per_attempt'] = reader_data[25][1]
                        offense_dict['punt_return_yards_per_attempt'] = reader_data[26][1]
                        offense_dict['int_return_yards_per_attempt'] = reader_data[27][1]
                        fumble_tuple = str(reader_data[28][1]).split('-')
                        offense_dict['fumbles'] = fumble_tuple[0]
                        offense_dict['fumbles_lost'] = fumble_tuple[1]
                        penalty_tuple = str(reader_data[29][1]).split('-')
                        offense_dict['penalties'] = penalty_tuple[0]
                        offense_dict['penalty_yards'] = penalty_tuple[1]
                        punt_tuple = str(reader_data[30][1]).split('-')
                        offense_dict['punt_attempts'] = punt_tuple[0]
                        offense_dict['punt_yards'] = punt_tuple[1]
                        offense_dict['punt_yards_per_attempt'] = reader_data[31][1]
                        offense_dict['punt_net_yards_per_attempt'] = reader_data[32][1]
                        offense_dict['time_of_possession_per_game'] = reader_data[33][1]
                        third_down_tuple = str(reader_data[34][1]).split('/')
                        offense_dict['third_down_conversions'] = third_down_tuple[0]
                        offense_dict['third_down_attempts'] = third_down_tuple[1]
                        offense_dict['third_down_pct'] = str(
                            reader_data[35][1]).replace('%', '')
                        fourth_down_tuple = str(reader_data[36][1]).split('/')
                        offense_dict['fourth_down_conversions'] = fourth_down_tuple[0]
                        offense_dict['fourth_down_attempts'] = fourth_down_tuple[1]
                        offense_dict['fourth_down_pct'] = str(
                            reader_data[37][1]).replace('%', '')
                        sacks_tuple = str(reader_data[38][1]).split('-')
                        offense_dict['sacks_by'] = sacks_tuple[0]
                        offense_dict['sacks_yards'] = sacks_tuple[1]
                        offense_dict['yards_misc'] = reader_data[39][1]
                        offense_dict['touchdowns'] = reader_data[40][1]
                        field_goal_tuple = str(reader_data[41][1]).split('-')
                        offense_dict['field_goal_makes'] = field_goal_tuple[0]
                        offense_dict['field_goal_attempts'] = field_goal_tuple[1]
                        onside_tuple = str(reader_data[42][1]).split('-')
                        offense_dict['onside_kick_makes'] = onside_tuple[0]
                        offense_dict['onside_kick_attempts'] = onside_tuple[1]
                        offense_dict['red_zone_scores'] = str(
                            reader_data[43][1]).split('-')[0]
                        offense_dict['red_zone_attempts'] = str(
                            reader_data[43][1]).split('-')[1].split(' ')[0]
                        offense_dict['red_zone_score_pct'] = str(reader_data[43][1]).split(
                            '-')[1].split(' ')[1].replace('%', '')
                        offense_dict['red_zone_touchdowns'] = str(
                            reader_data[44][1]).split('-')[0]
                        offense_dict['red_zone_td_pct'] = str(reader_data[44][1]).split(
                            '-')[1].split(' ')[1].replace('%', '')
                        offense_dict['pat_makes'] = str(
                            reader_data[45][1]).split('-')[0]
                        offense_dict['pat_attempts'] = str(
                            reader_data[45][1]).split('-')[1].split(' ')[0]
                        offense_dict['pat_pct'] = str(reader_data[45][1]).split(
                            '-')[1].split(' ')[1].replace('%', '')
                        offense_dict['attendance'] = reader_data[46][1]
                        attendance_tuple = str(reader_data[47][1]).split('/')
                        offense_dict['games'] = attendance_tuple[0]
                        offense_dict['attendance_per_game'] = attendance_tuple[1]
                        if len(str(reader_data[48][1])) > 0:
                            neutral_tuple = str(reader_data[48][1]).split('/')
                            offense_dict['games_neutral'] = neutral_tuple[0]
                            offense_dict['games_neutral_attendance_per_game'] = neutral_tuple[1]
                        else:
                            offense_dict['games_neutral'] = '0'
                            offense_dict['games_neutral_attendance_per_game'] = '0'
                        offense_dict['kickoff_attempts'] = '0'
                        offense_dict['kickoff_yards'] = '0'
                        offense_dict['kickoff_yards_per_attempt'] = '0'
                        offense_dict['kickoff_net_yards_per_attempt'] = '0'
                        offense_dict['points_off_turnovers'] = '0'
                        click.echo(offense_dict)

                        # Parse defense
                        defense_dict['team'] = reader_data[0][1]
                        defense_dict['year'] = path.dirname(
                            file_path).split('/')[-2]
                        defense_dict['off_def'] = 'defense'
                        defense_dict['points'] = reader_data[1][2]
                        defense_dict['points_per_game'] = reader_data[2][2]
                        defense_dict['first_downs'] = reader_data[3][2]
                        defense_dict['rush_first_downs'] = reader_data[4][2]
                        defense_dict['pass_first_downs'] = reader_data[5][2]
                        defense_dict['penalty_first_downs'] = reader_data[6][2]
                        defense_dict['rush_yards'] = reader_data[7][2]
                        defense_dict['rush_yards_gained'] = reader_data[8][2]
                        defense_dict['rush_yards_lost'] = reader_data[9][2]
                        defense_dict['rush_attempts'] = reader_data[10][2]
                        defense_dict['rush_yards_per_attempt'] = reader_data[11][2]
                        defense_dict['rush_yards_per_game'] = reader_data[12][2]
                        defense_dict['rush_td'] = reader_data[13][2]
                        defense_dict['pass_yards'] = reader_data[14][2]
                        pass_tuple = str(reader_data[15][2]).split('-')
                        defense_dict['pass_attempts'] = pass_tuple[0]
                        defense_dict['pass_completions'] = pass_tuple[1]
                        defense_dict['interceptions'] = pass_tuple[2]
                        defense_dict['pass_yards_per_attempt'] = reader_data[16][2]
                        defense_dict['pass_yards_per_completion'] = reader_data[17][2]
                        defense_dict['pass_td'] = reader_data[18][2]
                        defense_dict['yards'] = reader_data[19][2]
                        defense_dict['plays'] = reader_data[20][2]
                        defense_dict['yards_per_play'] = reader_data[21][2]
                        kick_return_tuple = str(reader_data[22][2]).split('-')
                        defense_dict['kick_return_attempts'] = kick_return_tuple[0]
                        defense_dict['kick_return_yards'] = kick_return_tuple[1]
                        punt_return_tuple = str(reader_data[23][2]).split('-')
                        defense_dict['punt_return_attempts'] = punt_return_tuple[0]
                        defense_dict['punt_return_yards'] = punt_return_tuple[1]
                        int_return_tuple = str(reader_data[24][2]).split('-')
                        defense_dict['int_return_attempts'] = int_return_tuple[0]
                        defense_dict['int_return_yards'] = int_return_tuple[1]
                        defense_dict['kick_return_yards_per_attempt'] = reader_data[25][2]
                        defense_dict['punt_return_yards_per_attempt'] = reader_data[26][2]
                        defense_dict['int_return_yards_per_attempt'] = reader_data[27][2]
                        fumble_tuple = str(reader_data[28][2]).split('-')
                        defense_dict['fumbles'] = fumble_tuple[0]
                        defense_dict['fumbles_lost'] = fumble_tuple[1]
                        penalty_tuple = str(reader_data[29][2]).split('-')
                        defense_dict['penalties'] = penalty_tuple[0]
                        defense_dict['penalty_yards'] = penalty_tuple[1]
                        punt_tuple = str(reader_data[30][2]).split('-')
                        defense_dict['punt_attempts'] = punt_tuple[0]
                        defense_dict['punt_yards'] = punt_tuple[1]
                        defense_dict['punt_yards_per_attempt'] = reader_data[31][2]
                        defense_dict['punt_net_yards_per_attempt'] = reader_data[32][2]
                        defense_dict['time_of_possession_per_game'] = reader_data[33][2]
                        third_down_tuple = str(reader_data[34][2]).split('/')
                        defense_dict['third_down_conversions'] = third_down_tuple[0]
                        defense_dict['third_down_attempts'] = third_down_tuple[1]
                        defense_dict['third_down_pct'] = str(
                            reader_data[35][2]).replace('%', '')
                        fourth_down_tuple = str(reader_data[36][2]).split('/')
                        defense_dict['fourth_down_conversions'] = fourth_down_tuple[0]
                        defense_dict['fourth_down_attempts'] = fourth_down_tuple[1]
                        defense_dict['fourth_down_pct'] = str(
                            reader_data[37][2]).replace('%', '')
                        sacks_tuple = str(reader_data[38][2]).split('-')
                        defense_dict['sacks_by'] = sacks_tuple[0]
                        defense_dict['sacks_yards'] = sacks_tuple[1]
                        defense_dict['yards_misc'] = reader_data[39][2]
                        defense_dict['touchdowns'] = reader_data[40][2]
                        field_goal_tuple = str(reader_data[41][2]).split('-')
                        defense_dict['field_goal_makes'] = field_goal_tuple[0]
                        defense_dict['field_goal_attempts'] = field_goal_tuple[1]
                        onside_tuple = str(reader_data[42][2]).split('-')
                        defense_dict['onside_kick_makes'] = onside_tuple[0]
                        defense_dict['onside_kick_attempts'] = onside_tuple[1]
                        defense_dict['red_zone_scores'] = str(
                            reader_data[43][2]).split('-')[0]
                        defense_dict['red_zone_attempts'] = str(
                            reader_data[43][2]).split('-')[1].split(' ')[0]
                        defense_dict['red_zone_score_pct'] = str(reader_data[43][2]).split(
                            '-')[1].split(' ')[1].replace('%', '')
                        defense_dict['red_zone_touchdowns'] = str(
                            reader_data[44][2]).split('-')[0]
                        defense_dict['red_zone_td_pct'] = str(reader_data[44][2]).split(
                            '-')[1].split(' ')[1].replace('%', '')
                        defense_dict['pat_makes'] = str(
                            reader_data[45][2]).split('-')[0]
                        defense_dict['pat_attempts'] = str(
                            reader_data[45][2]).split('-')[1].split(' ')[0]
                        defense_dict['pat_pct'] = str(reader_data[45][2]).split(
                            '-')[1].split(' ')[1].replace('%', '')
                        defense_dict['attendance'] = reader_data[46][2]
                        attendance_tuple = str(reader_data[47][2]).split('/')
                        defense_dict['games'] = attendance_tuple[0]
                        defense_dict['attendance_per_game'] = attendance_tuple[1]
                        if len(str(reader_data[48][2])) > 0:
                            neutral_tuple = str(reader_data[48][2]).split('/')
                            defense_dict['games_neutral'] = neutral_tuple[0]
                            defense_dict['games_neutral_attendance_per_game'] = neutral_tuple[1]
                        else:
                            defense_dict['games_neutral'] = '0'
                            defense_dict['games_neutral_attendance_per_game'] = '0'
                        defense_dict['kickoff_attempts'] = '0'
                        defense_dict['kickoff_yards'] = '0'
                        defense_dict['kickoff_yards_per_attempt'] = '0'
                        defense_dict['kickoff_net_yards_per_attempt'] = '0'
                        defense_dict['points_off_turnovers'] = '0'
                        click.echo(defense_dict)
                    elif int(offense_dict['year']) > 2010 and int(offense_dict['year']) < 2014:
                        ''' Data map for SideArm Sports 2011-2013 '''
                        ''' Added kickoff data '''
                        offense_dict['off_def'] = 'offense'
                        offense_dict['points'] = reader_data[1][1]
                        offense_dict['points_per_game'] = reader_data[2][1]
                        offense_dict['first_downs'] = reader_data[3][1]
                        offense_dict['rush_first_downs'] = reader_data[4][1]
                        offense_dict['pass_first_downs'] = reader_data[5][1]
                        offense_dict['penalty_first_downs'] = reader_data[6][1]
                        offense_dict['rush_yards'] = reader_data[7][1]
                        offense_dict['rush_yards_gained'] = reader_data[8][1]
                        offense_dict['rush_yards_lost'] = reader_data[9][1]
                        offense_dict['rush_attempts'] = reader_data[10][1]
                        offense_dict['rush_yards_per_attempt'] = reader_data[11][1]
                        offense_dict['rush_yards_per_game'] = reader_data[12][1]
                        offense_dict['rush_td'] = reader_data[13][1]
                        offense_dict['pass_yards'] = reader_data[14][1]
                        pass_tuple = str(reader_data[15][1]).split('-')
                        offense_dict['pass_completions'] = pass_tuple[0]
                        offense_dict['pass_attempts'] = pass_tuple[1]
                        offense_dict['interceptions'] = pass_tuple[2]
                        offense_dict['pass_yards_per_attempt'] = reader_data[16][1]
                        offense_dict['pass_yards_per_completion'] = reader_data[17][1]
                        offense_dict['pass_td'] = reader_data[18][1]
                        offense_dict['yards'] = reader_data[19][1]
                        offense_dict['plays'] = reader_data[20][1]
                        offense_dict['yards_per_play'] = reader_data[21][1]
                        kick_return_tuple = str(reader_data[22][1]).split('-')
                        offense_dict['kick_return_attempts'] = kick_return_tuple[0]
                        offense_dict['kick_return_yards'] = kick_return_tuple[1]
                        punt_return_tuple = str(reader_data[23][1]).split('-')
                        offense_dict['punt_return_attempts'] = punt_return_tuple[0]
                        offense_dict['punt_return_yards'] = punt_return_tuple[1]
                        int_return_tuple = str(reader_data[24][1]).split('-')
                        offense_dict['int_return_attempts'] = int_return_tuple[0]
                        offense_dict['int_return_yards'] = int_return_tuple[1]
                        offense_dict['kick_return_yards_per_attempt'] = reader_data[25][1]
                        offense_dict['punt_return_yards_per_attempt'] = reader_data[26][1]
                        offense_dict['int_return_yards_per_attempt'] = reader_data[27][1]
                        fumble_tuple = str(reader_data[28][1]).split('-')
                        offense_dict['fumbles'] = fumble_tuple[0]
                        offense_dict['fumbles_lost'] = fumble_tuple[1]
                        penalty_tuple = str(reader_data[29][1]).split('-')
                        offense_dict['penalties'] = penalty_tuple[0]
                        offense_dict['penalty_yards'] = penalty_tuple[1]
                        punt_tuple = str(reader_data[30][1]).split('-')
                        offense_dict['punt_attempts'] = punt_tuple[0]
                        offense_dict['punt_yards'] = punt_tuple[1]
                        offense_dict['punt_yards_per_attempt'] = reader_data[31][1]
                        offense_dict['punt_net_yards_per_attempt'] = reader_data[32][1]
                        kickoff_tuple = reader_data[33][1].split('-')
                        offense_dict['kickoff_attempts'] = kickoff_tuple[0]
                        offense_dict['kickoff_yards'] = kickoff_tuple[1]
                        offense_dict['kickoff_yards_per_attempt'] = reader_data[34][1]
                        offense_dict['kickoff_net_yards_per_attempt'] = reader_data[35][1]
                        offense_dict['time_of_possession_per_game'] = reader_data[36][1]
                        third_down_tuple = str(reader_data[37][1]).split('/')
                        offense_dict['third_down_conversions'] = third_down_tuple[0]
                        offense_dict['third_down_attempts'] = third_down_tuple[1]
                        offense_dict['third_down_pct'] = str(
                            reader_data[38][1]).replace('%', '')
                        fourth_down_tuple = str(reader_data[39][1]).split('/')
                        offense_dict['fourth_down_conversions'] = fourth_down_tuple[0]
                        offense_dict['fourth_down_attempts'] = fourth_down_tuple[1]
                        offense_dict['fourth_down_pct'] = str(
                            reader_data[40][1]).replace('%', '')
                        sacks_tuple = str(reader_data[41][1]).split('-')
                        offense_dict['sacks_by'] = sacks_tuple[0]
                        offense_dict['sacks_yards'] = sacks_tuple[1]
                        offense_dict['yards_misc'] = reader_data[42][1]
                        offense_dict['touchdowns'] = reader_data[43][1]
                        field_goal_tuple = str(reader_data[44][1]).split('-')
                        offense_dict['field_goal_makes'] = field_goal_tuple[0]
                        offense_dict['field_goal_attempts'] = field_goal_tuple[1]
                        onside_tuple = str(reader_data[45][1]).split('-')
                        offense_dict['onside_kick_makes'] = onside_tuple[0]
                        offense_dict['onside_kick_attempts'] = onside_tuple[1]
                        offense_dict['red_zone_scores'] = str(
                            reader_data[46][1]).split('-')[0].replace('(', '')
                        offense_dict['red_zone_attempts'] = str(
                            reader_data[46][1]).split('-')[1].split(' ')[0].replace(')', '')
                        offense_dict['red_zone_score_pct'] = str(reader_data[46][1]).split(
                            '-')[1].split(' ')[1].replace('%', '')
                        offense_dict['red_zone_touchdowns'] = str(
                            reader_data[47][1]).split('-')[0].replace('(', '')
                        offense_dict['red_zone_td_pct'] = str(reader_data[47][1]).split(
                            '-')[1].split(' ')[1].replace('%', '')
                        offense_dict['pat_makes'] = str(
                            reader_data[48][1]).split('-')[0].replace('(', '')
                        offense_dict['pat_attempts'] = str(
                            reader_data[48][1]).split('-')[1].split(' ')[0].replace(')', '')
                        offense_dict['pat_pct'] = str(reader_data[48][1]).split(
                            '-')[1].split(' ')[1].replace('%', '')
                        offense_dict['attendance'] = reader_data[49][1]
                        attendance_tuple = str(reader_data[50][1]).split('/')
                        offense_dict['games'] = attendance_tuple[0]
                        offense_dict['attendance_per_game'] = attendance_tuple[1]
                        if len(str(reader_data[51][1])) > 0:
                            neutral_tuple = str(reader_data[51][1]).split('/')
                            offense_dict['games_neutral'] = neutral_tuple[0]
                            offense_dict['games_neutral_attendance_per_game'] = neutral_tuple[1]
                        else:
                            offense_dict['games_neutral'] = '0'
                            offense_dict['games_neutral_attendance_per_game'] = '0'
                        offense_dict['points_off_turnovers'] = '0'
                        click.echo(offense_dict)

                        # Parse defense
                        defense_dict['team'] = reader_data[0][1]
                        defense_dict['year'] = path.dirname(
                            file_path).split('/')[-2]
                        defense_dict['off_def'] = 'defense'
                        defense_dict['points'] = reader_data[1][2]
                        defense_dict['points_per_game'] = reader_data[2][2]
                        defense_dict['first_downs'] = reader_data[3][2]
                        defense_dict['rush_first_downs'] = reader_data[4][2]
                        defense_dict['pass_first_downs'] = reader_data[5][2]
                        defense_dict['penalty_first_downs'] = reader_data[6][2]
                        defense_dict['rush_yards'] = reader_data[7][2]
                        defense_dict['rush_yards_gained'] = reader_data[8][2]
                        defense_dict['rush_yards_lost'] = reader_data[9][2]
                        defense_dict['rush_attempts'] = reader_data[10][2]
                        defense_dict['rush_yards_per_attempt'] = reader_data[11][2]
                        defense_dict['rush_yards_per_game'] = reader_data[12][2]
                        defense_dict['rush_td'] = reader_data[13][2]
                        defense_dict['pass_yards'] = reader_data[14][2]
                        pass_tuple = str(reader_data[15][2]).split('-')
                        defense_dict['pass_completions'] = pass_tuple[0]
                        defense_dict['pass_attempts'] = pass_tuple[1]
                        defense_dict['interceptions'] = pass_tuple[2]
                        defense_dict['pass_yards_per_attempt'] = reader_data[16][2]
                        defense_dict['pass_yards_per_completion'] = reader_data[17][2]
                        defense_dict['pass_td'] = reader_data[18][2]
                        defense_dict['yards'] = reader_data[19][2]
                        defense_dict['plays'] = reader_data[20][2]
                        defense_dict['yards_per_play'] = reader_data[21][2]
                        kick_return_tuple = str(reader_data[22][2]).split('-')
                        defense_dict['kick_return_attempts'] = kick_return_tuple[0]
                        defense_dict['kick_return_yards'] = kick_return_tuple[1]
                        punt_return_tuple = str(reader_data[23][2]).split('-')
                        defense_dict['punt_return_attempts'] = punt_return_tuple[0]
                        defense_dict['punt_return_yards'] = punt_return_tuple[1]
                        int_return_tuple = str(reader_data[24][2]).split('-')
                        defense_dict['int_return_attempts'] = int_return_tuple[0]
                        defense_dict['int_return_yards'] = int_return_tuple[1]
                        defense_dict['kick_return_yards_per_attempt'] = reader_data[25][2]
                        defense_dict['punt_return_yards_per_attempt'] = reader_data[26][2]
                        defense_dict['int_return_yards_per_attempt'] = reader_data[27][2]
                        fumble_tuple = str(reader_data[28][2]).split('-')
                        defense_dict['fumbles'] = fumble_tuple[0]
                        defense_dict['fumbles_lost'] = fumble_tuple[1]
                        penalty_tuple = str(reader_data[29][2]).split('-')
                        defense_dict['penalties'] = penalty_tuple[0]
                        defense_dict['penalty_yards'] = penalty_tuple[1]
                        punt_tuple = str(reader_data[30][2]).split('-')
                        defense_dict['punt_attempts'] = punt_tuple[0]
                        defense_dict['punt_yards'] = punt_tuple[1]
                        defense_dict['punt_yards_per_attempt'] = reader_data[31][2]
                        defense_dict['punt_net_yards_per_attempt'] = reader_data[32][2]
                        kickoff_tuple = reader_data[33][2].split('-')
                        offense_dict['kickoff_attempts'] = kickoff_tuple[0]
                        offense_dict['kickoff_yards'] = kickoff_tuple[1]
                        offense_dict['kickoff_yards_per_attempt'] = reader_data[34][2]
                        offense_dict['kickoff_net_yards_per_attempt'] = reader_data[35][2]
                        defense_dict['time_of_possession_per_game'] = reader_data[36][2]
                        third_down_tuple = str(reader_data[37][2]).split('/')
                        defense_dict['third_down_conversions'] = third_down_tuple[0]
                        defense_dict['third_down_attempts'] = third_down_tuple[1]
                        defense_dict['third_down_pct'] = str(
                            reader_data[38][2]).replace('%', '')
                        fourth_down_tuple = str(reader_data[39][2]).split('/')
                        defense_dict['fourth_down_conversions'] = fourth_down_tuple[0]
                        defense_dict['fourth_down_attempts'] = fourth_down_tuple[1]
                        defense_dict['fourth_down_pct'] = str(
                            reader_data[40][2]).replace('%', '')
                        sacks_tuple = str(reader_data[41][2]).split('-')
                        defense_dict['sacks_by'] = sacks_tuple[0]
                        defense_dict['sacks_yards'] = sacks_tuple[1]
                        defense_dict['yards_misc'] = reader_data[42][2]
                        defense_dict['touchdowns'] = reader_data[43][2]
                        field_goal_tuple = str(reader_data[44][2]).split('-')
                        defense_dict['field_goal_makes'] = field_goal_tuple[0]
                        defense_dict['field_goal_attempts'] = field_goal_tuple[1]
                        onside_tuple = str(reader_data[45][2]).split('-')
                        defense_dict['onside_kick_makes'] = onside_tuple[0]
                        defense_dict['onside_kick_attempts'] = onside_tuple[1]
                        defense_dict['red_zone_scores'] = str(
                            reader_data[46][2]).split('-')[0].replace('(', '')
                        defense_dict['red_zone_attempts'] = str(
                            reader_data[46][2]).split('-')[1].split(' ')[0].replace(')', '')
                        defense_dict['red_zone_score_pct'] = str(reader_data[46][2]).split(
                            '-')[1].split(' ')[1].replace('%', '')
                        defense_dict['red_zone_touchdowns'] = str(
                            reader_data[47][2]).split('-')[0].replace('(', '')
                        defense_dict['red_zone_td_pct'] = str(reader_data[48][2]).split(
                            '-')[1].split(' ')[1].replace('%', '')
                        defense_dict['pat_makes'] = str(
                            reader_data[48][2]).split('-')[0].replace('(', '')
                        defense_dict['pat_attempts'] = str(
                            reader_data[48][2]).split('-')[1].split(' ')[0].replace(')', '')
                        defense_dict['pat_pct'] = str(reader_data[48][2]).split(
                            '-')[1].split(' ')[1].replace('%', '')
                        defense_dict['attendance'] = reader_data[49][2]
                        attendance_tuple = str(reader_data[50][2]).split('/')
                        defense_dict['games'] = attendance_tuple[0]
                        defense_dict['attendance_per_game'] = attendance_tuple[1]
                        if len(str(reader_data[51][2])) > 0:
                            neutral_tuple = str(reader_data[51][2]).split('/')
                            defense_dict['games_neutral'] = neutral_tuple[0]
                            defense_dict['games_neutral_attendance_per_game'] = neutral_tuple[1]
                        else:
                            defense_dict['games_neutral'] = '0'
                            defense_dict['games_neutral_attendance_per_game'] = '0'
                        defense_dict['points_off_turnovers'] = '0'
                        click.echo(defense_dict)
                    else:
                        ''' Data map for SideArm Sports after 2013 '''
                        ''' Added points off turnovers '''
                        offense_dict['off_def'] = 'offense'
                        offense_dict['points'] = reader_data[1][1]
                        offense_dict['points_per_game'] = reader_data[2][1]
                        offense_dict['points_off_turnovers'] = reader_data[3][1]
                        offense_dict['first_downs'] = reader_data[4][1]
                        offense_dict['rush_first_downs'] = reader_data[5][1]
                        offense_dict['pass_first_downs'] = reader_data[6][1]
                        offense_dict['penalty_first_downs'] = reader_data[7][1]
                        offense_dict['rush_yards'] = reader_data[8][1]
                        offense_dict['rush_yards_gained'] = reader_data[9][1]
                        offense_dict['rush_yards_lost'] = reader_data[10][1]
                        offense_dict['rush_attempts'] = reader_data[1][1]
                        offense_dict['rush_yards_per_attempt'] = reader_data[12][1]
                        offense_dict['rush_yards_per_game'] = reader_data[13][1]
                        offense_dict['rush_td'] = reader_data[14][1]
                        offense_dict['pass_yards'] = reader_data[15][1]
                        pass_tuple = str(reader_data[16][1]).split('-')
                        offense_dict['pass_completions'] = pass_tuple[0]
                        offense_dict['pass_attempts'] = pass_tuple[1]
                        offense_dict['interceptions'] = pass_tuple[2]
                        offense_dict['pass_yards_per_attempt'] = reader_data[17][1]
                        offense_dict['pass_yards_per_completion'] = reader_data[18][1]
                        offense_dict['pass_td'] = reader_data[19][1]
                        offense_dict['yards'] = reader_data[20][1]
                        offense_dict['plays'] = reader_data[21][1]
                        offense_dict['yards_per_play'] = reader_data[22][1]
                        kick_return_tuple = str(reader_data[23][1]).split('-')
                        offense_dict['kick_return_attempts'] = kick_return_tuple[0]
                        offense_dict['kick_return_yards'] = kick_return_tuple[1]
                        punt_return_tuple = str(reader_data[24][1]).split('-')
                        offense_dict['punt_return_attempts'] = punt_return_tuple[0]
                        offense_dict['punt_return_yards'] = punt_return_tuple[1]
                        int_return_tuple = str(reader_data[25][1]).split('-')
                        offense_dict['int_return_attempts'] = int_return_tuple[0]
                        offense_dict['int_return_yards'] = int_return_tuple[1]
                        offense_dict['kick_return_yards_per_attempt'] = reader_data[26][1]
                        offense_dict['punt_return_yards_per_attempt'] = reader_data[27][1]
                        offense_dict['int_return_yards_per_attempt'] = reader_data[28][1]
                        fumble_tuple = str(reader_data[29][1]).split('-')
                        offense_dict['fumbles'] = fumble_tuple[0]
                        offense_dict['fumbles_lost'] = fumble_tuple[1]
                        penalty_tuple = str(reader_data[30][1]).split('-')
                        offense_dict['penalties'] = penalty_tuple[0]
                        offense_dict['penalty_yards'] = penalty_tuple[1]
                        punt_tuple = str(reader_data[31][1]).split('-')
                        offense_dict['punt_attempts'] = punt_tuple[0]
                        offense_dict['punt_yards'] = punt_tuple[1]
                        offense_dict['punt_yards_per_attempt'] = reader_data[32][1]
                        offense_dict['punt_net_yards_per_attempt'] = reader_data[33][1]
                        kickoff_tuple = reader_data[34][1].split('-')
                        offense_dict['kickoff_attempts'] = kickoff_tuple[0]
                        offense_dict['kickoff_yards'] = kickoff_tuple[1]
                        offense_dict['kickoff_yards_per_attempt'] = reader_data[35][1]
                        offense_dict['kickoff_net_yards_per_attempt'] = reader_data[36][1]
                        offense_dict['time_of_possession_per_game'] = reader_data[37][1]
                        third_down_tuple = str(reader_data[38][1]).split('/')
                        offense_dict['third_down_conversions'] = third_down_tuple[0]
                        offense_dict['third_down_attempts'] = third_down_tuple[1]
                        offense_dict['third_down_pct'] = str(
                            reader_data[39][1]).replace('%', '')
                        fourth_down_tuple = str(reader_data[40][1]).split('/')
                        offense_dict['fourth_down_conversions'] = fourth_down_tuple[0]
                        offense_dict['fourth_down_attempts'] = fourth_down_tuple[1]
                        offense_dict['fourth_down_pct'] = str(
                            reader_data[41][1]).replace('%', '')
                        sacks_tuple = str(reader_data[42][1]).split('-')
                        offense_dict['sacks_by'] = sacks_tuple[0]
                        offense_dict['sacks_yards'] = sacks_tuple[1]
                        offense_dict['yards_misc'] = reader_data[43][1]
                        offense_dict['touchdowns'] = reader_data[44][1]
                        field_goal_tuple = str(reader_data[45][1]).split('-')
                        offense_dict['field_goal_makes'] = field_goal_tuple[0]
                        offense_dict['field_goal_attempts'] = field_goal_tuple[1]
                        onside_tuple = str(reader_data[46][1]).split('-')
                        offense_dict['onside_kick_makes'] = onside_tuple[0]
                        offense_dict['onside_kick_attempts'] = onside_tuple[1]
                        offense_dict['red_zone_scores'] = str(
                            reader_data[47][1]).split('-')[0].replace('(', '')
                        offense_dict['red_zone_attempts'] = str(
                            reader_data[47][1]).split('-')[1].split(' ')[0].replace(')', '')
                        offense_dict['red_zone_score_pct'] = str(reader_data[47][1]).split(
                            '-')[1].split(' ')[1].replace('%', '')
                        offense_dict['red_zone_touchdowns'] = str(
                            reader_data[48][1]).split('-')[0].replace('(', '')
                        offense_dict['red_zone_td_pct'] = str(reader_data[48][1]).split(
                            '-')[1].split(' ')[1].replace('%', '')
                        offense_dict['pat_makes'] = str(
                            reader_data[49][1]).split('-')[0].replace('(', '')
                        offense_dict['pat_attempts'] = str(
                            reader_data[49][1]).split('-')[1].split(' ')[0].replace(')', '')
                        offense_dict['pat_pct'] = str(reader_data[49][1]).split(
                            '-')[1].split(' ')[1].replace('%', '')
                        offense_dict['attendance'] = reader_data[50][1]
                        attendance_tuple = str(reader_data[51][1]).split('/')
                        offense_dict['games'] = attendance_tuple[0]
                        offense_dict['attendance_per_game'] = attendance_tuple[1]
                        if len(str(reader_data[52][1])) > 0:
                            neutral_tuple = str(reader_data[52][1]).split('/')
                            offense_dict['games_neutral'] = neutral_tuple[0]
                            offense_dict['games_neutral_attendance_per_game'] = neutral_tuple[1]
                        else:
                            offense_dict['games_neutral'] = '0'
                            offense_dict['games_neutral_attendance_per_game'] = '0'
                        click.echo(offense_dict)

                        # Parse defense
                        defense_dict['team'] = reader_data[0][1]
                        defense_dict['year'] = path.dirname(
                            file_path).split('/')[-2]
                        defense_dict['off_def'] = 'defense'
                        defense_dict['points'] = reader_data[1][2]
                        defense_dict['points_per_game'] = reader_data[2][2]
                        defense_dict['points_off_turnovers'] = reader_data[3][2]
                        defense_dict['first_downs'] = reader_data[4][2]
                        defense_dict['rush_first_downs'] = reader_data[5][2]
                        defense_dict['pass_first_downs'] = reader_data[6][2]
                        defense_dict['penalty_first_downs'] = reader_data[7][2]
                        defense_dict['rush_yards'] = reader_data[8][2]
                        defense_dict['rush_yards_gained'] = reader_data[9][2]
                        defense_dict['rush_yards_lost'] = reader_data[10][2]
                        defense_dict['rush_attempts'] = reader_data[11][2]
                        defense_dict['rush_yards_per_attempt'] = reader_data[12][2]
                        defense_dict['rush_yards_per_game'] = reader_data[13][2]
                        defense_dict['rush_td'] = reader_data[14][2]
                        defense_dict['pass_yards'] = reader_data[15][2]
                        pass_tuple = str(reader_data[16][2]).split('-')
                        defense_dict['pass_completions'] = pass_tuple[0]
                        defense_dict['pass_attempts'] = pass_tuple[1]
                        defense_dict['interceptions'] = pass_tuple[2]
                        defense_dict['pass_yards_per_attempt'] = reader_data[17][2]
                        defense_dict['pass_yards_per_completion'] = reader_data[18][2]
                        defense_dict['pass_td'] = reader_data[19][2]
                        defense_dict['yards'] = reader_data[20][2]
                        defense_dict['plays'] = reader_data[21][2]
                        defense_dict['yards_per_play'] = reader_data[22][2]
                        kick_return_tuple = str(reader_data[23][2]).split('-')
                        defense_dict['kick_return_attempts'] = kick_return_tuple[0]
                        defense_dict['kick_return_yards'] = kick_return_tuple[1]
                        punt_return_tuple = str(reader_data[24][2]).split('-')
                        defense_dict['punt_return_attempts'] = punt_return_tuple[0]
                        defense_dict['punt_return_yards'] = punt_return_tuple[1]
                        int_return_tuple = str(reader_data[25][2]).split('-')
                        defense_dict['int_return_attempts'] = int_return_tuple[0]
                        defense_dict['int_return_yards'] = int_return_tuple[1]
                        defense_dict['kick_return_yards_per_attempt'] = reader_data[26][2]
                        defense_dict['punt_return_yards_per_attempt'] = reader_data[27][2]
                        defense_dict['int_return_yards_per_attempt'] = reader_data[28][2]
                        fumble_tuple = str(reader_data[29][2]).split('-')
                        defense_dict['fumbles'] = fumble_tuple[0]
                        defense_dict['fumbles_lost'] = fumble_tuple[1]
                        penalty_tuple = str(reader_data[30][2]).split('-')
                        defense_dict['penalties'] = penalty_tuple[0]
                        defense_dict['penalty_yards'] = penalty_tuple[1]
                        punt_tuple = str(reader_data[31][2]).split('-')
                        defense_dict['punt_attempts'] = punt_tuple[0]
                        defense_dict['punt_yards'] = punt_tuple[1]
                        defense_dict['punt_yards_per_attempt'] = reader_data[32][2]
                        defense_dict['punt_net_yards_per_attempt'] = reader_data[33][2]
                        kickoff_tuple = reader_data[34][2].split('-')
                        offense_dict['kickoff_attempts'] = kickoff_tuple[0]
                        offense_dict['kickoff_yards'] = kickoff_tuple[1]
                        offense_dict['kickoff_yards_per_attempt'] = reader_data[35][2]
                        offense_dict['kickoff_net_yards_per_attempt'] = reader_data[36][2]
                        defense_dict['time_of_possession_per_game'] = reader_data[37][2]
                        third_down_tuple = str(reader_data[38][2]).split('/')
                        defense_dict['third_down_conversions'] = third_down_tuple[0]
                        defense_dict['third_down_attempts'] = third_down_tuple[1]
                        defense_dict['third_down_pct'] = str(
                            reader_data[39][2]).replace('%', '')
                        fourth_down_tuple = str(reader_data[40][2]).split('/')
                        defense_dict['fourth_down_conversions'] = fourth_down_tuple[0]
                        defense_dict['fourth_down_attempts'] = fourth_down_tuple[1]
                        defense_dict['fourth_down_pct'] = str(
                            reader_data[41][2]).replace('%', '')
                        sacks_tuple = str(reader_data[42][2]).split('-')
                        defense_dict['sacks_by'] = sacks_tuple[0]
                        defense_dict['sacks_yards'] = sacks_tuple[1]
                        defense_dict['yards_misc'] = reader_data[43][2]
                        defense_dict['touchdowns'] = reader_data[44][2]
                        field_goal_tuple = str(reader_data[45][2]).split('-')
                        defense_dict['field_goal_makes'] = field_goal_tuple[0]
                        defense_dict['field_goal_attempts'] = field_goal_tuple[1]
                        onside_tuple = str(reader_data[46][2]).split('-')
                        defense_dict['onside_kick_makes'] = onside_tuple[0]
                        defense_dict['onside_kick_attempts'] = onside_tuple[1]
                        defense_dict['red_zone_scores'] = str(
                            reader_data[47][2]).split('-')[0].replace('(', '')
                        defense_dict['red_zone_attempts'] = str(
                            reader_data[47][2]).split('-')[1].split(' ')[0].replace(')', '')
                        defense_dict['red_zone_score_pct'] = str(reader_data[47][2]).split(
                            '-')[1].split(' ')[1].replace('%', '')
                        defense_dict['red_zone_touchdowns'] = str(
                            reader_data[48][2]).split('-')[0].replace('(', '')
                        defense_dict['red_zone_td_pct'] = str(reader_data[49][2]).split(
                            '-')[1].split(' ')[1].replace('%', '')
                        defense_dict['pat_makes'] = str(
                            reader_data[49][2]).split('-')[0].replace('(', '')
                        defense_dict['pat_attempts'] = str(
                            reader_data[49][2]).split('-')[1].split(' ')[0].replace(')', '')
                        defense_dict['pat_pct'] = str(reader_data[49][2]).split(
                            '-')[1].split(' ')[1].replace('%', '')
                        defense_dict['attendance'] = reader_data[50][2]
                        attendance_tuple = str(reader_data[51][2]).split('/')
                        defense_dict['games'] = attendance_tuple[0]
                        defense_dict['attendance_per_game'] = attendance_tuple[1]
                        if len(str(reader_data[52][2])) > 0:
                            neutral_tuple = str(reader_data[52][2]).split('/')
                            defense_dict['games_neutral'] = neutral_tuple[0]
                            defense_dict['games_neutral_attendance_per_game'] = neutral_tuple[1]
                        else:
                            defense_dict['games_neutral'] = '0'
                            defense_dict['games_neutral_attendance_per_game'] = '0'
                        click.echo(defense_dict)

                    click.echo('Data file ' + file_path + ' processed')
                else:
                    click.echo('Data file ' + file_path + ' skipped')


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
    click.echo('Scraping ' + url + '...')
    # Request the page
    headers = {'user-agent': 'Mozilla/5.0:'}
    page = requests.get(url, headers=headers)
    results = []
    if page.status_code != 404:
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
            click.echo('{:<25} {:>15} {:>15}'.format(
                key, value, opponent[key]))
            results.append([key, value, opponent[key]])

        click.echo(url + ' scraped')
    else:
        click.echo(url + ' returned HTTP response 404 - not found')

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
