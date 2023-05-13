from subprocess import call
import plotly.express as px
import numpy as np
import pandas as pd
from graphviz import Source
from matplotlib import pyplot as plt
from sklearn import linear_model
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn import tree
import graphviz #https://graphviz.org/download/
from sklearn.tree import export_graphviz, DecisionTreeClassifier


def decision_tree():
    data_train = None
    data_predecir = None

    with open("data/devices_IA_clases.json") as f:
        data_train = pd.read_json(f)

    with open("data/devices_IA_predecir_v2.json") as f:
        data_predecir = pd.read_json(f)

    data = pd.concat([data_train, data_predecir]).reset_index(drop=True)
    data_x = data[['servicios_inseguros', 'servicios']]
    data_y = data[['peligroso']]

    decision_tree = tree.DecisionTreeClassifier()
    decision_tree.fit(data_x, data_y)

    pred = decision_tree.predict(data_x)

    xy_train = data_x.copy()
    xy_train["predicted_y"] = pred.astype(str)
    xy_train["actual_y"] = data_y.copy()
    # compare
    print("Mean Squared error: %.2f" % mean_squared_error(data_y, pred))
    print("Coefficient of determination: %.2f" % r2_score(data_y, pred))

    data_fig = data.copy()
    data_fig["peligroso"] = pred.astype(str)

    aux = data_fig.groupby(["peligroso"])["peligroso"].count().values
    num_no = aux[0]
    num_si = aux[1]
    fig = px.scatter(data_fig, x="servicios", y="servicios_inseguros", color="peligroso", opacity=0.7, labels={"servicios": "Numero de servicios", "servicios_inseguros": "Numero de servicios inseguros", "id": "ID", "peligroso": "Peligroso"})


    fig2 = tree.export_graphviz(decision_tree, out_file=None, feature_names=["servicios", "servicios_inseguros"],class_names=["no peligroso", "peligroso"],filled=True, rounded=True,special_characters=True)
    graph = graphviz.Source(fig2)
    #graph.format = "png"
    graph.render(outfile='static/graph.png', format="png", view=True, cleanup=True).replace('\\', '/')
    #call(['dot', '-Tpng', '-o', 'graph.png', 'Source.gv'])

    #graph.view()
    return graph,num_no, num_si