import numpy as np
import pandas as pd
from models import Team, League, Matchup
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
# import requests
# import io
# from rawdata import file_path, url
# import matplotlib.pyplot as plt
# import seaborn as sn

# data = pd.read_csv(io.StringIO(x.decode('utf8')), low_memory=False)

# data = pd.read_csv(file_path, low_memory=False)
# data.to_pickle('2018.pkl')
data = pd.read_pickle('2018.pkl')

# with pd.option_context('display.max_rows', 999, 'display.max_colwidth', 25):
#     print(data.head(4).transpose())

# selected_columns = [
#     'pass_attempt', 'rush_attempt', 'sack', 'qb_hit', 'touchdown', 'play_type'
# ]
# for c in selected_columns:
#     print(data[c].value_counts(normalize=True).to_frame(), '\n')

# run_pass_row_indices = data[data['play_type'].isin(
#     ['run', 'pass', 'sack'])].index

# runs_passes_sacks = data.loc[run_pass_row_indices, :]
# print(runs_passes_sacks['play_type'].value_counts(normalize=True).to_frame())


def generate_set_of_row_attribute(attr):
    """Generates a set of all vals for certain row"""

    new_set = set()
    for index, row in data.iterrows():
        new_set.add(row[attr])
    return new_set


def df_creator():
    teams = Team.all()

    ats_2018 = [
        7, 5, 8, 7, 7, 12, 9, 10, 9, 6, 9, 6, 7, 8, 5, 9, 9, 7, 8, 8, 9, 10, 8,
        5, 6, 7, 8, 5, 9, 7, 8, 9
    ]
    # ats_2017 = [6, 8, 8, 10, 10, 8, 9, 4, 8, 4, 8, 7, 7, 8, 11, 10, 8, 9, 5, 11, 12, 10, 7, 9, 5, 13, 7, 9, 6, 6, 9, 7]
    wins_2018 = [
        3, 7, 10, 6, 7, 12, 6, 7, 10, 6, 6, 6, 11, 10, 5, 12, 12, 13, 7, 8, 11,
        13, 5, 4, 4, 9, 9, 4, 10, 5, 9, 7
    ]
    final_dict = {
        "team": teams,
        "ATS wins": ats_2018,
        "Wins": wins_2018,
        "WPA margin close first half": [],
        "WPA margin close second half": [],
        "WPA margin close D1": [],
        "WPA margin close Q1 D1": []
    }

    for team in teams:
        x = Team(team)

        final_dict["WPA margin close first half"].append(
            x.margin_for_stat('mean', 'wpa', 'o', close=True, half=1))
        final_dict["WPA margin close second half"].append(
            x.margin_for_stat('mean', 'wpa', 'o', close=True, half=2))
        final_dict["WPA margin close D1"].append(
            x.margin_for_stat('mean', 'wpa', 'o', close=True, down=1))
        final_dict["WPA margin close Q1 D1"].append(
            x.margin_for_stat(
                'mean', 'wpa', 'o', close=True, down=1, quarter=1))

    df = pd.DataFrame(final_dict)
    return df


def skl_lin_reg():

    df = df_creator()

    y = df['ATS wins']

    feature_cols = [
        "WPA margin close second half", "WPA margin close first half",
        "WPA margin close D1", "WPA margin close Q1 D1", "Wins"
    ]
    X = df[feature_cols]

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=3)
    linreg = LinearRegression()
    linreg.fit(X_train, y_train)

    y_pred = linreg.predict(X_test)

    q = list(zip(linreg.coef_, feature_cols))
    for i in q:
        print(i)
    rmse = np.sqrt(metrics.mean_squared_error(y_test, y_pred))
    print('RMSE', rmse)


x = League.grid('offense', 'epa')
print(x)