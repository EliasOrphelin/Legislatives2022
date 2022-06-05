from plotly import graph_objects as go
import pandas as pd
import json

with open('SondagesLegislatives2022Loess.json', 'r') as f:
  data = json.load(f)

couleurs={
    "Ensemble": "#edca21",
    "NUPES": "#c44740",
    "ExtG": "red",
    "RN": "black",
    "LR": "blue"
}

print(data.keys())

fig = go.Figure()

for parti in data:
    
    if parti not in ["Autre", "ExtG", "DivEco", "PA", "DivG"]:
        print(parti)
        fig.add_trace(
            go.Scatter(
                x=data[parti]["fin_enquete"],
                y=data[parti]["sieges_haut_loess"],
                marker_color=couleurs.get(parti, "black"),
                line_width=0,
                mode="lines+text",
                showlegend=False,
                text=[""] * (len(data[parti]["sieges_haut_loess"])-1) + [round(data[parti]["sieges_haut_loess"][-1])],
                textposition="middle right",
                textfont=dict(color=couleurs.get(parti, "black")),
            )
        )

        fig.add_trace(
            go.Scatter(
                x=data[parti]["fin_enquete"],
                y=data[parti]["sieges_bas_loess"],
                fill="tonexty",
                line_width=0,
                mode="lines+text",
                marker_color=couleurs.get(parti, "black"),
                name=parti,
                text=[""] * (len(data[parti]["sieges_haut_loess"])-1) + [round(data[parti]["sieges_bas_loess"][-1])],
                textposition="middle right",
                textfont=dict(color=couleurs.get(parti, "black")),
                
            )
        )

fig.add_shape(type="line",
    x0="2022-01-01", y0=289, x1="2022-10-01", y1=289,
    line=dict(
        color="black",
        width=1,
        dash="dash",
    )
)

fig.add_shape(type="line",
    x0="2022-06-12", y0=0, x1="2022-06-12", y1=360,
    line=dict(
        color="grey",
        width=1,
    )
)

fig.add_shape(type="line",
    x0="2022-06-19", y0=0, x1="2022-06-19", y1=360,
    line=dict(
        color="grey",
        width=1,
    )
)

fig.update_xaxes(range=[data["Ensemble"]["fin_enquete"][0], "2022-06-24"])
fig.update_yaxes(range=[0, 360])

fig.write_image("SondagesLegislativesLoess.jpeg", width=1000, height=700, scale=2)