from flask import Flask, render_template
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

    player_stats_files = glob.glob(paths[0] + "/*.csv")
    team_stats_against_files = glob.glob(paths[1] + "/*.csv")
    team_stats_for_files = glob.glob(paths[2] + "/*.csv")

    team_against_li = []
    for year in range(earliest_year, latest_year + 1):
        team_against_df = pd.read_csv(paths[1] + 'team_stats_against_' + str(year) + '.csv', index_col=None, header=0)
        team_against_df['Year'] = year
        team_against_li.append(team_against_df)
    team_against_frame = pd.concat(team_against_li, axis=0, ignore_index=True)
    return {"results": "true", "content": "testing"}


if __name__ == '__main__':
    app.run(debug=True)