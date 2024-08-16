import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)


df = pd.read_csv("nba_games.csv", index_col=0)

df = df.sort_values("date")
df = df.reset_index(drop=True)

del df["mp.1"]
del df["mp_opp.1"]
del df["index_opp"]

def add_target(team):
    team["target"] = team["won"].shift(-1)
    return team

df = df.groupby("team", group_keys=False).apply(add_target)

df["target"] [pd.isnull(df["target"])] = 2
df["target"] = df["target"].astype(int, errors="ignore") # turning bool val into int

nulls = pd.isnull(df)
nulls = nulls.sum()
nulls = nulls[nulls > 0]
valid_columns = df.columns[~df.columns.isin(nulls.index)]
df = df[valid_columns].copy()

