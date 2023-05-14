import graphviz
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from matplotlib import pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.tree import plot_tree, export_graphviz


def random_forest():
    data_train = None
    data_predecir = None

    with open("data/devices_IA_clases.json") as f:
        data_train = pd.read_json(f)

    with open("data/devices_IA_predecir_v2.json") as f:
        data_predecir = pd.read_json(f)

    data = pd.concat([data_train, data_predecir]).reset_index(drop=True)
    data_x = data[['servicios_inseguros', 'servicios']]
    data_y = data[['peligroso']]

    # Random Forest
    randomForest = RandomForestClassifier(n_estimators=30)
    randomForest.fit(data_x, data_y["peligroso"].values.ravel())
    pred = randomForest.predict(data_x)

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
   # fig = px.scatter(data_fig, x="servicios", y="servicios_inseguros", color="peligroso", opacity=0.7, labels={"servicios": "Numero de servicios", "servicios_inseguros": "Numero de servicios inseguros", "id": "ID", "peligroso": "Peligroso"})

    for i in range(len(randomForest.estimators_)):
        estimator = randomForest.estimators_[i]
        fig2 = export_graphviz(estimator,
                        out_file=None,
                        feature_names=["servicios_inseguros", "servicios"],
                        class_names=["no peligroso", "peligroso"],
                        rounded=True, proportion=False,
                        precision=2, filled=True)
        graph = graphviz.Source(fig2)
        graph.render(outfile='static/graph' + str(i) + '.png', format="png", view=True, cleanup=True).replace('\\', '/')

    return num_no,num_si