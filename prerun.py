import numpy as np
import pandas as pd
from models import Team, League, Matchup
from df_creator import df_creator
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
# import pprint
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


def skl_lin_reg(target):

    df = df_creator()

    y = df[target]

    feature_cols = []
    args_dict = {}
    cols_dict = {}

    close = [True, False]
    quarter = [1, 2, 3, 4]
    down = [1, 2, 3, 4]
    half = [1, 2]
    rz = [True, False]

    q = Team.all()
    for team in q:
        for x in close:
            for r in quarter:
                for z in down:
                    args_dict[f"down{z} quarter{r} close{x}"] = {
                        "down": z,
                        "quarter": r,
                        "close": x
                    }
                for b in rz:
                    for z in down:
                        args_dict[f"down{z} quarter{r} close{x} rz{b}"] = {
                            "down": z,
                            "quarter": r,
                            "close": x,
                            "rz": b
                        }
            for r in half:
                for z in down:
                    args_dict[f"down{z} half{r} close{x}"] = {
                        "down": z,
                        "half": r,
                        "close": x
                    }
                for b in rz:
                    for z in down:
                        args_dict[f"down{z} half{r} close{x} rz{b}"] = {
                            "down": z,
                            "half": r,
                            "close": x,
                            "rz": b
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
                for b in rz:
                    for z in down:
                        u = i.margin_for_stat(
                            'mean', 'wpa', 'o',
                            **args_dict[f"down{z} quarter{r} close{x} rz{b}"])
                        cols_dict[f"down{z} quarter{r} close{x} rz{b}"].append(u)
                        feature_cols.append(f"down{z} quarter{r} close{x} rz{b}")
            for r in half:
                for z in down:
                    u = i.margin_for_stat(
                        'mean', 'wpa', 'o',
                        **args_dict[f"down{z} half{r} close{x}"])
                    cols_dict[f"down{z} half{r} close{x}"].append(u)
                    feature_cols.append(f"down{z} half{r} close{x}")
                for b in rz:
                    for z in down:
                        u = i.margin_for_stat(
                            'mean', 'wpa', 'o',
                            **args_dict[f"down{z} half{r} close{x} rz{b}"])
                        cols_dict[f"down{z} half{r} close{x} rz{b}"].append(u)
                        feature_cols.append(f"down{z} half{r} close{x} rz{b}")

    feature_cols = list(set(feature_cols))
    X = df[feature_cols]

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=5)
    linreg = LinearRegression()
    linreg.fit(X_train, y_train)

    y_pred = linreg.predict(X_test)

    coefs_list = []

    q = list(zip(linreg.coef_, feature_cols))
    q = sorted(q, key=lambda x: x[0])
    for i in q:
        coefs_list.append((i[0], i[1]))
    rmse = np.sqrt(metrics.mean_squared_error(y_test, y_pred))
    print('RMSE', rmse)
    return coefs_list


df = df_creator()
x = skl_lin_reg('ATS wins')
wins_mean = df.corr()['Wins'].abs().mean()
wins_std = df.corr()['Wins'].abs().std()
wins_var = df.corr()['Wins'].abs().var()
ats_wins_mean = df.corr()['ATS wins'].abs().mean()
ats_wins_std = df.corr()['ATS wins'].abs().std()
ats_wins_var = df.corr()['ATS wins'].abs().var()

wins_corr = df.corr().sort_values(by=['Wins'])['Wins']
ats_wins_corr = df.corr().sort_values(by=['ATS wins'])['ATS wins']


def win_ats_differential():
    wins_dict = wins_corr.to_dict()
    ats_dict = ats_wins_corr.to_dict()
    print('ATS DICT', ats_dict)
    final_list = []
    for key in wins_dict:
        final_list.append({key: wins_dict[key] - ats_dict[key]})
        # final_dict[key] = wins_dict[key] - ats_dict[key]
    # sorted(final_list, key=lambda x: x[1])
    return final_list


# diff = win_ats_differential()
# print('SORTED DIFF', sorted_diff)

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

