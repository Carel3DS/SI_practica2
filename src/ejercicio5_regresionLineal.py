import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB


def regresion_lineal():
    data_train = None
    data_predecir = None

    with open("data/devices_IA_clases.json") as f:
        data_train = pd.read_json(f)

    with open("data/devices_IA_predecir_v2.json") as f:
        data_predecir = pd.read_json(f)

    data = pd.concat([data_train, data_predecir]).reset_index(drop=True)
    data_x = data[['servicios_inseguros', 'servicios']]
    data_y = data[['peligroso']]

    # no utilizado
    data_x_logistic_regression = data["servicios_inseguros"] / data["servicios"]
    data_x_logistic_regression = data_x_logistic_regression.fillna(0).to_frame()

    # training the model
    # With data from x guess y
    x_train, x_test, y_train, y_test = train_test_split(data_x, data_y, test_size=0.2)

    # logisticregression es una opcion para tener resultado binario (% de servicios inseguros -> si/no peligroso)
    # multinomialnb usa mas de un parametro (# de servicios + # de servicios inseguros -> si/no peligroso)
    # they are both shit
    # pred solo puede ser 1 o 0, sin valores entremedias
    regresion = LogisticRegression()
    regresion.fit(x_train, y_train["peligroso"].values.ravel())
    pred = regresion.predict(data_x)
    # print(pred)

    xy_train = data_x.copy()
    xy_train["predicted_y"] = pred.astype(str)
    xy_train["actual_y"] = data_y.copy()
    #print(xy_train)

    # compare
    print("Mean Squared error: %.2f" % mean_squared_error(data_y, pred))
    print("Coefficient of determination: %.2f" % r2_score(data_y, pred))

    data_fig = data.copy()
    data_fig["peligroso"] = pred.astype(str)
    aux = data_fig.groupby(["peligroso"])["peligroso"].count().values
    num_no = aux[0]
    num_si = aux[1]
    #print(num_no, num_si)
    fig = px.scatter(data_fig, x="servicios", y="servicios_inseguros", color="peligroso", opacity=0.7, labels={"servicios": "Numero de servicios", "servicios_inseguros": "Numero de servicios inseguros", "id": "ID", "peligroso": "Peligroso"})
    # fig.show()
    return fig, num_no, num_si


#regresion_lineal()
