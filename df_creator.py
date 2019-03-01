from models import Team, League, Matchup
# import numpy as np
import pandas as pd


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
        "Wins": wins_2018,
        "ATS wins": ats_2018,
    }

    for team in teams:
        x = Team(team)

    args_dict = {}
    cols_dict = {}

    close = [True, False]
    rz = [True, False]
    quarter = [1, 2, 3, 4]
    down = [1, 2, 3, 4]
    half = [1, 2]

    q = Team.all()
    for team in q:
        i = Team(team)
        for x in close:
            for a in half:
                for z in down:
                    args_dict[f"down{z} half{a} close{x}"] = {
                        "down": z,
                        "half": a,
                        "close": x
                    }
                for b in rz:
                    for z in down:
                        args_dict[f"down{z} half{a} close{x} rz{b}"] = {
                            "down": z,
                            "half": a,
                            "close": x,
                            "rz": b
                        }
            for y in quarter:
                for z in down:
                    args_dict[f"down{z} quarter{y} close{x}"] = {
                        "down": z,
                        "quarter": y,
                        "close": x
                    }
                for b in rz:
                    for z in down:
                        args_dict[f"down{z} quarter{y} close{x} rz{b}"] = {
                            "down": z,
                            "half": a,
                            "close": x,
                            "rz": b
                        }
    for x in args_dict:
        cols_dict[x] = []
    for team in q:
        i = Team(team)
        for x in close:
            for a in half:
                for z in down:
                    u = i.margin_for_stat(
                        'median', 'wpa', 'o',
                        **args_dict[f"down{z} half{a} close{x}"])
                    if str(u) == 'nan':
                        cols_dict[f"down{z} half{a} close{x}"].append(0)
                    else:
                        cols_dict[f"down{z} half{a} close{x}"].append(u)
                for b in rz:
                    for z in down:
                        u = i.margin_for_stat(
                            'median', 'wpa', 'o',
                            **args_dict[f"down{z} half{a} close{x} rz{b}"])
                        if str(u) == 'nan':
                            cols_dict[f"down{z} half{a} close{x} rz{b}"].append(0)
                        else:
                            cols_dict[f"down{z} half{a} close{x} rz{b}"].append(u)
            for y in quarter:
                for z in down:
                    u = i.margin_for_stat(
                        'median', 'wpa', 'o',
                        **args_dict[f"down{z} quarter{y} close{x}"])
                    if str(u) == 'nan':
                        cols_dict[f"down{z} quarter{y} close{x}"].append(0)
                    else:
                        cols_dict[f"down{z} quarter{y} close{x}"].append(u)
                for b in rz:
                    for z in down:
                        u = i.margin_for_stat(
                            'median', 'wpa', 'o',
                            **args_dict[f"down{z} quarter{y} close{x} rz{b}"])
                        if str(u) == 'nan':
                            cols_dict[f"down{z} quarter{y} close{x} rz{b}"].append(0)
                        else:
                            cols_dict[f"down{z} quarter{y} close{x} rz{b}"].append(u)

    for x in cols_dict:
        final_dict[x] = cols_dict[x]
    df = pd.DataFrame(final_dict)
    return df
