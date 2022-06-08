import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/EliasOrphelin/Legislatives2022/main/SondagesLegislatives2022.csv")
df = df[df["type"]=="score"]
df = df[df["nom_institut"]!="Cluster17"]
df = df[df["parti"]=="Ensemble"]
print(df)