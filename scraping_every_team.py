import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', 500)

abbreviations_df = pd.read_csv('data/PFR Abbreviations Fixed.csv')
# print(abbreviations_df['Abbreviation'])

abbreviations_list = abbreviations_df['Abbreviation'].to_list()
team_names = abbreviations_df['Team'].to_list()
start_list = abbreviations_df['From'].to_list()
end_list= abbreviations_df['To'].to_list()

franchise_dict = dict(zip(abbreviations_list, start_list))
end_dict = dict(zip(abbreviations_list, end_list))
names_dict = dict(zip(abbreviations_list,team_names))

for team in abbreviations_list:
    seasons = []
    for i in range (franchise_dict.get(team),end_dict.get(team)):
            seasons.append(i)
    for i in seasons:
        url = f'https://www.pro-football-reference.com/teams/{team}/{i}.htm'
        df = pd.read_html(url, header=0)
        df = df[1]
        df['Season'] = i
        df['Team'] = names_dict.get(team)
        df = df[['Unnamed: 0', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5', 'Unnamed: 6',
                 'Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9', 'Score', 'Score.1', 'Offense', 'Offense.1', 'Offense.2',
                 'Offense.3', 'Offense.4', 'Defense', 'Defense.1', 'Defense.2', 'Defense.3', 'Defense.4', 'Season',
                 'Team']]
        df['Week'] = df['Unnamed: 0']
        df['team_score'] = df['Score']
        df['opp score'] = df['Score.1']
        df['ID'] = df['Season'].astype(str) + "|" + df['Week'].astype(str)
        df = df.drop(
            columns=['Unnamed: 0', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5', 'Unnamed: 6',
                     'Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9', 'Score', 'Score.1', 'Offense', 'Offense.1', 'Offense.2',
                     'Offense.3', 'Offense.4', 'Defense', 'Defense.1', 'Defense.2', 'Defense.3', 'Defense.4'])

        # df['ID'] = df['Season']+"|"+df['Week']
        # df = df[['Week','Tm Score','Opp Score','Season', 'Team','ID']]
        df.to_csv(f'data/every_game_ever_three.csv', mode='a')
    print(f"{team} good")