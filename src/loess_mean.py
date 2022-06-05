import pandas as pd
from loess import loess_1d
import numpy as np
import datetime
import json

df = pd.read_csv("https://raw.githubusercontent.com/EliasOrphelin/Legislatives2022/main/SondagesLegislatives2022.csv")

partis = df.parti.unique()
print(partis)
dict_json = {}

def add_to_json(parti, xout_dt, yout_sieges_haut, yout_sieges_bas):
    dict_json[parti] = {"fin_enquete": list(xout_dt), "sieges_haut_loess": list(yout_sieges_haut), "sieges_bas_loess": list(yout_sieges_bas)}

def export_json():
    with open('SondagesLegislatives2022Loess.json', 'w') as outfile:
        json.dump(dict_json, outfile)

def get_loess_mean(df_parti):
    fin_enquete_ts = pd.to_datetime(df_parti["fin_enquete"], format="%d/%m/%Y").astype(np.int64) // 10 ** 9
    y = df_parti.intentions.values
    xout, yout, wout = loess_1d.loess_1d(fin_enquete_ts.values, y, xnew=None, degree=1, frac=0.8, npoints=None, rotate=False, sigy=None)
    xout_dt = [datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d') for date in xout]
    return xout_dt, yout


for parti in partis:
    print(parti)
    try:
        df_parti = df[df["parti"]==parti].reset_index()

        df_parti_sieges_haut = df_parti[df_parti["type"]=="sieges-haut"]
        xout_dt, yout_sieges_haut = get_loess_mean(df_parti_sieges_haut)

        df_parti_sieges_bas = df_parti[df_parti["type"]=="sieges-bas"]
        xout_dt, yout_sieges_bas = get_loess_mean(df_parti_sieges_bas)

        add_to_json(parti, xout_dt, yout_sieges_haut = np.round(yout_sieges_haut, 2), yout_sieges_bas = np.round(yout_sieges_bas, 2))

        print("✅ success\n")
    except:
        print("❌ error\n")

    export_json()