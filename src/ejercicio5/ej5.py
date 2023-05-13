from subprocess import call

import numpy as np
import pandas as pd
from graphviz import Source
from matplotlib import pyplot as plt
from sklearn import linear_model
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error
from sklearn import tree
import graphviz #https://graphviz.org/download/
from sklearn.tree import export_graphviz

data_train = pd.read_json("../data/devices_IA_clases.json")
data_test = pd.read_json("../data/devices_IA_predecir_v2.json")


#regresionLineal

# Mostrar una muestra de los datos cargados

# Use only one feature
x_train = data_train["servicios_inseguros"]
y_train = data_train["peligroso"]

x_test = data_test["servicios_inseguros"]
y_test = data_test["peligroso"]



# Create linear regression object
regr = linear_model.LinearRegression()
# Train the model using the training sets

x_train = x_train.to_numpy().reshape(-1, 1)
x_test = x_test.to_numpy().reshape(-1, 1)
y_train = y_train.to_numpy().reshape(-1, 1)
y_test = y_test.to_numpy().reshape(-1, 1)


regr.fit(x_train, y_train)
print("regr coeficiente" + str(regr.coef_))
# Make predictions using the testing set
data_y_pred = regr.predict(x_test)
# The mean squared error
print("Mean squared error: %.2f" % mean_squared_error(y_test, data_y_pred))
# Plot outputs
plt.scatter(x_test, y_test, color="black")
plt.plot(x_test, data_y_pred, color="blue", linewidth=3)
plt.xticks(())
plt.yticks(())
plt.show()
num_pred_peligrosos = np.sum(np.round(data_y_pred) == 1)
print("Número de dispositivos predichos como peligrosos:", num_pred_peligrosos)

##Decision Tree


x = data_test.drop(["peligroso", "id"], axis=1)
y = data_test["peligroso"]

# obtener los nombres de las columnas



clf = tree.DecisionTreeClassifier()
clf = clf.fit(x, y)
#Predict
clf_model = tree.DecisionTreeClassifier()
clf_model.fit(x,y)
#Print plot
dot_data = tree.export_graphviz(clf, out_file=None)
graph = graphviz.Source(dot_data)
graph.render('Ej5previous')
#y_test_df = pd.DataFrame(y_test, columns=data_test.target_names)
dot_data = tree.export_graphviz(clf, out_file=None,
                      feature_names=x.columns,
                      class_names=y.unique().astype(str).tolist(),
                     filled=True, rounded=True,
                    special_characters=True)
graph = graphviz.Source(dot_data)
graph.render('Ej5.gv', view=True).replace('\\', '/')
pred_y_test = clf_model.predict(x)
num_peligrosos = np.sum(pred_y_test == 1)
print("Numero de disposittivos predichos como peligrosos con el decision tree: ", num_peligrosos)

##Random Forest


#Split data
x = data_test.drop(["peligroso", "id"], axis=1)
y = data_test["peligroso"]
clf = RandomForestClassifier(max_depth=2, random_state=0,n_estimators=10)
clf.fit(x, y)

y_pred = clf.predict(x)
num_peligrosos = sum(y_pred==1)

print("Numero de dispositivos predichos como peligrosos con el random forest", num_peligrosos)

for i in range(len(clf.estimators_)):
    estimator = clf.estimators_[i]
    export_graphviz(estimator,
                    out_file='tree.dot',
                    feature_names=x.columns,
                    class_names=y.unique().astype(str).tolist(),
                    rounded=True, proportion=False,
                    precision=2, filled=True)
    call(['dot', '-Tpng', 'tree.dot', '-o', 'ForestTree'+str(i)+'.png', '-Gdpi=600'])


# Obtener la importancia de las características del modelo
importances = clf.feature_importances_
indices = np.argsort(importances)[::-1]

# Imprimir la importancia de cada característica
print("Importancia de las características:")
for f in range(x.shape[1]):
    print(f"{f+1}. {x.columns[indices[f]]}: {round(importances[indices[f]], 3)}")

