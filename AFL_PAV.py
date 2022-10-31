import pandas as pd
import glob
import matplotlib.pyplot as plt
%matplotlib inline

# taken from here....

latest_year = 2020
earliest_year = 2003

paths = [r'player_stats/', r'team_stats_against/', r'team_stats_for/']
file_prefix = [r'player_stats_', r'team_stats_against_', r'team_stats_for_']

player_stats_files = glob.glob(paths[0] + "/*.csv")
team_stats_against_files = glob.glob(paths[1] + "/*.csv")
team_stats_for_files = glob.glob(paths[2] + "/*.csv")

# get all team against stats from CSVs then add to a list of dfs then turn that list of dfs into a single df

team_against_li = []

for year in range(earliest_year, latest_year + 1):
    team_against_df = pd.read_csv(paths[1] + 'team_stats_against_' + str(year) + '.csv', index_col=None, header=0)
    team_against_df['Year'] = year
    team_against_li.append(team_against_df)

team_against_frame = pd.concat(team_against_li, axis=0, ignore_index=True)

# ... to here and added to app route in server.py

# get all team for stats from CSVs then add to a list of dfs then turn that list of dfs into a single df

team_for_li = []

for year in range(earliest_year, latest_year + 1):
    team_for_df = pd.read_csv(paths[2] + 'team_stats_for_' + str(year) + '.csv', index_col=None, header=0)
    team_for_df['Year'] = year
    team_for_li.append(team_for_df)

team_for_frame = pd.concat(team_for_li, axis=0, ignore_index=True)

# get all player stats from CSVs then add to a list of dfs then turn that list of dfs into a single df

player_li = []

for year in range(earliest_year, latest_year + 1):
    player_df = pd.read_csv(paths[0] + 'player_stats_' + str(year) + '.csv', index_col=None, header=0)
    player_df['Year'] = year
    player_li.append(player_df)

player_frame = pd.concat(player_li, axis=0, ignore_index=True)

# change team names in player_frame to match other data

player_frame['Team'] = player_frame['Team'].replace(
    ['AD', 'BL', 'CA', 'CW', 'ES', 'FR', 'GE', 'GC', 'GW', 'HW', 'ME', 'NM', 'PA', 'RI','SK', 'SY', 'WC', 'WB'],

    ['Adelaide', 'Brisbane Lions', 'Carlton', 'Collingwood', 'Essendon', 'Fremantle', 'Geelong', 'Gold Coast',
     'Greater Western Sydney', 'Hawthorn', 'Melbourne', 'North Melbourne', 'Port Adelaide', 'Richmond', 'St Kilda',
     'Sydney', 'West Coast', 'Western Bulldogs'])

# change data types for all numbers in table

headers = []
for col in player_frame.columns:
    headers.append(col)

for head in headers[2:]:
#     print('print: ' + str(head))
#     print(frame[head].dtype)
    try:
        player_frame[head] = player_frame[head].str.replace(" ", "0")
        player_frame[head] = player_frame[head].str.replace(u'\xa0', "0")
        player_frame[head] = pd.to_numeric(player_frame[head])
    except:
        pass


# calculate and add offence_value_total, defence_value_total and midfield_value_total to player_frame

free_kick_differential = (player_frame['Frees For'] - player_frame['Frees Against'])
score = ((player_frame['Goals'] * 6) + player_frame['Behinds'])

player_frame['offence_value_total'] = score  + (player_frame['Hit Outs'] / 4) + (player_frame['Goal Assists'] * 3) + player_frame['Inside 50s'] + player_frame['Marks Inside 50'] + free_kick_differential

player_frame['defence_value_total'] = (2 * player_frame['Rebound 50s']) + (2 * player_frame['One Percenters']) + ((player_frame['Marks'] - (4 * player_frame['Marks Inside 50']) - (2 * free_kick_differential)) - ((2/3) * player_frame['Hit Outs']))


player_frame['midfield_value_total'] = (15 * player_frame['Inside 50s']) + (20 * player_frame['Clearances']) + (3 * player_frame['Tackles']) + (1.5 * player_frame['Hit Outs']) + free_kick_differential


# calculate points for and against and put them into team_for_frame and team_against_frame

team_for_frame['Score'] = (team_for_frame['Goals'] * 6) + team_for_frame['Behinds']

team_for_frame['Score/Inside 50s'] = team_for_frame['Score'] / team_for_frame['Inside 50s']

team_against_frame['Score'] = (team_against_frame['Goals'] * 6) + team_against_frame['Behinds']

team_against_frame['Score/Inside 50s'] = team_against_frame['Score'] / team_against_frame['Inside 50s']

# calculate the Team Offence: (Team Points/Team Inside-50s) / League Average, then make a new df called team_offence_df

# this is required tp prevent the for loop assigning year_team_for_frame many times over causing an assignment error
pd.options.mode.chained_assignment = None

team_offence_li = []

for year in range(earliest_year, latest_year + 1):
    year_filt = (team_for_frame['Year'] == year)
    year_team_for_frame = team_for_frame.loc[year_filt]
    year_team_for_frame['Score/Inside 50s Mean'] = year_team_for_frame['Score/Inside 50s'].mean()
    year_team_for_frame['team_offence'] = 100 * year_team_for_frame['Score/Inside 50s'] / year_team_for_frame['Score/Inside 50s Mean']
    team_offence_li.append(year_team_for_frame[['Year', 'Team', 'team_offence']])

team_offence_df = pd.concat(team_offence_li, axis=0, ignore_index=True)

# calculate the Team Defence: Defence Number (DN) = (Team Points Conceded/Team Inside-50s Conceded)/ League Average
# Team Defence = (100*((2*DN-DN^2)/(2*DN)))*2, then make a new df called team_defence_df

pd.options.mode.chained_assignment = None

team_defence_li = []

for year in range(earliest_year, latest_year + 1):
    year_filt = (team_against_frame['Year'] == year)
    year_team_against_frame = team_against_frame.loc[year_filt]
    year_team_against_frame['Score/Inside 50s Mean'] = year_team_against_frame['Score/Inside 50s'].mean()
    year_team_against_frame['DN'] = year_team_against_frame['Score/Inside 50s'] / year_team_against_frame['Score/Inside 50s Mean']
    team_defence_li.append(year_team_against_frame[['Year', 'Team', 'DN']])

team_defence_df = pd.concat(team_defence_li, axis=0, ignore_index=True)

DN = team_defence_df['DN']

team_defence_df['team_defence'] = (100 * ((2 * DN - DN**2) / (2 * DN)))*2

# calculate the Team Midfield: (Team Inside-50s/Opposition Inside-50s), then make a new df called team_midfield_df

team_midfield_df = 100 * team_for_frame[['Inside 50s']] / team_against_frame[['Inside 50s']]

team_midfield_df[['Team', 'Year']] = team_for_frame[['Team', 'Year']]

team_midfield_df.rename(columns={"Inside 50s": "team_midfield"}, inplace=True)

# combine team_offence_df, team_midfield_df, team_defence_df into team_rating_df
# TODO use multiple indexing to make this neater, a bit over my head atm

team_rating = [team_offence_df, team_midfield_df, team_defence_df]

team_rating_df = pd.concat(team_rating, axis=1).T.drop_duplicates().T

team_rating_df['team_rating'] = (team_rating_df['team_offence'] + team_rating_df['team_midfield'] + team_rating_df['team_defence']) / 3
# team_rating_df.sort_values(by=['team_rating'], ascending=True).head(10

plt.style.use('seaborn')

team = "Carlton"

team_rating_df[team_rating_df['Team'] == team].plot(x ='Year', y='team_rating', kind = 'line', label=team)

team_rating_df[team_rating_df['Team'] == team].plot(x ='Year', y='team_offence', kind = 'line', label=team)
team_rating_df[team_rating_df['Team'] == team].plot(x ='Year', y='team_midfield', kind = 'line', label=team)
team_rating_df[team_rating_df['Team'] == team].plot(x ='Year', y='team_defence', kind = 'line', label=team)
