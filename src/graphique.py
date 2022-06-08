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
    "LR": "blue",
    "R": "pink"
}

print(data.keys())

def graphique_sieges():
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
                    text=[""] * (len(data[parti]["sieges_haut_loess"])-1) + ["  " + str(round(data[parti]["sieges_haut_loess"][-1]))],
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
                    text=[""] * (len(data[parti]["sieges_haut_loess"])-1) + ["  " + str(round(data[parti]["sieges_bas_loess"][-1]))],
                    textposition="middle right",
                    textfont=dict(color=couleurs.get(parti, "black")),
                )
            )

            for numero_sondage in range(len(data[parti]["sieges_bas"])):
                fig.add_trace(
                    go.Scatter(
                        x=[data[parti]["fin_enquete"][numero_sondage], data[parti]["fin_enquete"][numero_sondage]],
                        y=[data[parti]["sieges_bas"][numero_sondage], data[parti]["sieges_haut"][numero_sondage]],
                        mode="markers+lines",
                        marker_color=couleurs.get(parti, "black"),
                        name=parti,
                        text=[""] * (len(data[parti]["sieges_haut_loess"])-1) + [round(data[parti]["sieges_bas_loess"][-1])],
                        textposition="middle right",
                        textfont=dict(color=couleurs.get(parti, "black")),
                        opacity=0.3,
                        showlegend=False
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

    fig.update_xaxes(range=[data["Ensemble"]["fin_enquete"][0], "2022-06-20"])
    fig.update_yaxes(range=[0, 360])

    fig.add_annotation(
        {
            "x": 0.5,
            "y": 1.15,
            "xref": "paper",
            "yref": "paper",
            "text": f"Projection des sièges aux élections législatives",
            "font": {"size": 25,},
            "xanchor": "center",
            "showarrow": False,
        })

    fig.add_annotation(
        {
            "x": 0.52,
            "y": 1.07,
            "xref": "paper",
            "yref": "paper",
            "text": f"Aggrégation de l'ensemble des sondages (Ipsos, Ifop, Opinionway...) • @ElecTracker • electracker.fr • Données Elias Orphelin • dernier sondage : {data['Ensemble']['fin_enquete'][-1]}",
            "font": {"size": 15},
            "xanchor": "center",
            "showarrow": False,
        }
    )

    fig.write_image("SondagesLegislativesLoessSieges.jpeg", width=1100, height=700, scale=2)

def graphique_score():
    fig = go.Figure()

    for parti in data:
        
        if parti not in ["Autre", "ExtG", "DivEco", "PA", "DivG"]:
            print(parti)
            fig.add_trace(
                go.Scatter(
                    x=data[parti]["fin_enquete_score"],
                    y=data[parti]["score"],
                    marker_color=couleurs.get(parti, "black"),
                    mode="markers",
                    showlegend=False,
                    textfont=dict(color=couleurs.get(parti, "black")),
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=data[parti]["fin_enquete_score"],
                    y=data[parti]["score_loess"],
                    marker_color=couleurs.get(parti, "black"),
                    mode="lines+text",
                    showlegend=True,
                    text=[""] * (len(data[parti]["score"])-1) + ["  " + str(round(data[parti]["score_loess"][-1], 1)) + " %"],
                    textposition="middle right",
                    textfont=dict(color=couleurs.get(parti, "black")),
                    name=parti
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

    fig.update_xaxes(range=[data["Ensemble"]["fin_enquete"][0], "2022-06-20"])
    fig.update_yaxes(range=[0, 30])

    fig.add_annotation(
        {
            "x": 0.5,
            "y": 1.15,
            "xref": "paper",
            "yref": "paper",
            "text": f"Intentions de vote aux élections législatives",
            "font": {"size": 25,},
            "xanchor": "center",
            "showarrow": False,
        })

    fig.add_annotation(
        {
            "x": 0.52,
            "y": 1.07,
            "xref": "paper",
            "yref": "paper",
            "text": f"Aggrégation de l'ensemble des sondages (Ipsos, Ifop, Opinionway...) • @ElecTracker • electracker.fr • Données Elias Orphelin • dernier sondage : {data['Ensemble']['fin_enquete'][-1]}",
            "font": {"size": 15},
            "xanchor": "center",
            "showarrow": False,
        }
    )

    fig.write_image("SondagesLegislativesLoessScore.jpeg", width=1100, height=700, scale=2)


graphique_sieges()
graphique_score()
