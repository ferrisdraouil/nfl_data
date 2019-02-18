import numpy as np
import pandas as pd
from models import Team, League, Matchup
from df_creator import df_creator
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import pprint
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


def generate_set_of_row_attribute(attr):
    """Generates a set of all vals for certain row"""

    new_set = set()
    for index, row in data.iterrows():
        new_set.add(row[attr])
    return new_set


def skl_lin_reg():

    df = df_creator()

    y = df['ATS wins']

    feature_cols = []
    args_dict = {}
    cols_dict = {}

    close = [True, False]
    quarter = [1, 2, 3, 4]
    down = [1, 2, 3, 4]
    half = [1, 2]

    q = Team.all()
    for team in q:
        i = Team(team)
        for x in close:
            for r in quarter:
                for z in down:
                    args_dict[f"down{z} quarter{r} close{x}"] = {
                        "down": z,
                        "quarter": r,
                        "close": x
                    }
    for x in args_dict:
        cols_dict[x] = []
    for team in q:
        i = Team(team)
        for x in close:
            for r in quarter:
                for z in down:
                    u = i.margin_for_stat(
                        'mean', 'wpa', 'o',
                        **args_dict[f"down{z} quarter{r} close{x}"])
                    cols_dict[f"down{z} quarter{r} close{x}"].append(u)
                    feature_cols.append(f"down{z} quarter{r} close{x}")
    X = df[feature_cols]

    print('FEATURE COLS', X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
    linreg = LinearRegression()
    linreg.fit(X_train, y_train)

    y_pred = linreg.predict(X_test)

    coefs_list = []

    q = list(zip(linreg.coef_, feature_cols))
    q = sorted(q, key=lambda x: x[0])
    pprint.pprint(q)
    for i in q:
        coefs_list.append(i[0])
    rmse = np.sqrt(metrics.mean_squared_error(y_test, y_pred))
    # print('Y PRED', y_pred)
    print('RMSE', rmse)
    return coefs_list


df = df_creator()
# df.corr()
# x = skl_lin_reg()
wins_mean = df.corr()['Wins'].mean()
wins_std = df.corr()['Wins'].std()
wins_var = df.corr()['Wins'].var()
ats_wins_mean = df.corr()['ATS wins'].mean()
ats_wins_std = df.corr()['ATS wins'].std()
ats_wins_var = df.corr()['ATS wins'].var()

df.corr().sort_values(by=['Wins'])['Wins']
df.corr().sort_values(by=['ATS wins'])['ATS wins']

# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#     print(df.corr())

# def predict(home, away):
# stat1 = Matchup.generate(
#     home, away, 'mean', 'wpa', since='nov', close=True, half=2)
# stat2 = Matchup.generate(
#     home, away, 'mean', 'wpa', since='nov', close=True, half=1)
# stat3 = Matchup.generate(
#     home, away, 'mean', 'wpa', since='nov', close=True, down=1)
# stat4 = Matchup.generate(
#     home, away, 'mean', 'wpa', since='nov', close=True, quarter=1, down=1)
# final_num = 0
# final_num += (stat1[home] * x[0]) + (stat2[home] * x[1]) + (
#     stat3[home] * x[2]) + (stat4[home] * x[3])
# return {home: final_num, away: -final_num}

# print(
#     Matchup.generate('NE', 'LA', 'median', 'wpa', close=True, down=3, quarter=4))
# print(Matchup.generate('NE', 'LA', 'median', 'wpa', close=True, half=2, down=1))
# print(
#     Matchup.generate('LA', 'NE', 'median', 'wpa', close=True, down=3, quarter=4))
# print(Matchup.generate('LA', 'NE', 'median', 'wpa', close=True, half=2, down=1))
