import pandas as pd
from loess import loess_1d
import numpy as np
import datetime
import json

df = pd.read_csv("https://raw.githubusercontent.com/EliasOrphelin/Legislatives2022/main/SondagesLegislatives2022.csv")
partis = df.parti.unique()
dict_json = {}

def add_to_json(parti, xout_dt, yout, y):
    dict_json[parti] = {"fin_enquete": list(xout_dt), "intention": list(y), "intention_loess": list(yout)}

def export_json():
    with open('SondagesLegislatives2022Loess.json', 'w') as outfile:
        json.dump(dict_json, outfile)

for parti in partis:
    try:
        df_parti = df[df["parti"]==parti].reset_index()
        fin_enquete_ts = pd.to_datetime(df_parti["fin_enquete"], format="%d/%m/%Y").astype(np.int64) // 10 ** 9
        print(parti)
        y = df_parti.intentions.values
        xout, yout, wout = loess_1d.loess_1d(fin_enquete_ts.values, y, xnew=None, degree=1, frac=0.5, npoints=None, rotate=False, sigy=None)
        xout_dt = [datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d') for date in xout]
        add_to_json(parti, xout_dt, np.round(yout, 2), y)
        print("✅ success\n")
    except:
        print("❌ error\n")

    export_json()