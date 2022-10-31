from flask import Flask, render_template
import glob
import pandas as pd

app = Flask(__name__)

@app.route('/')
def hello():
    return {"members": ["Member 1", "Member 2", "Member 3"]}


@app.route('/team_against_test')
def team_against_test():

    latest_year = 2020
    earliest_year = 2003

    paths = [r'player_stats/', r'team_stats_against/', r'team_stats_for/']
    file_prefix = [r'player_stats_', r'team_stats_against_', r'team_stats_for_']
    # print(paths)
    # print(file_prefix)

    player_stats_files = glob.glob(paths[0] + "/*.csv")
    team_stats_against_files = glob.glob(paths[1] + "/*.csv")
    team_stats_for_files = glob.glob(paths[2] + "/*.csv")
    # print('A', player_stats_files)
    # print('B', team_stats_against_files)
    # print('C', team_stats_for_files)

    team_against_li = []
    for year in range(earliest_year, latest_year + 1):
        team_against_df = pd.read_csv(paths[1] + 'team_stats_against_' + str(year) + '.csv', index_col=None, header=0)
        team_against_df['Year'] = year
        team_against_li.append(team_against_df)
    # print(team_against_df)
    # print(team_against_li)
    team_against_frame = pd.concat(team_against_li, axis=0, ignore_index=True)
    print(team_against_frame)
    return {"results": "true"}


if __name__ == '__main__':
    app.run(debug=True)