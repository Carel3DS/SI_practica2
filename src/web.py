import plotly.utils
from flask import Flask
from flask import render_template, request
import json
import ejercicio1
import ejercicio2
import ejercicio3
import ejercicio5_regresionLineal
import ejercicio4_api

# import ejercicio5.ej5

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/ejercicio_1")
def ej_1():
    top_vuln, top_ip = ejercicio1.analysis()
    top_vuln = list(top_vuln.head(10).itertuples(index=False, name=None))
    top_ip = list(top_ip.head(10).itertuples(name=None))
    return render_template("ejercicio_1.html", ip=top_ip, vuln=top_vuln)


@app.route("/ejercicio_2")
def ej_2():
    top_per = list(ejercicio2.top_per().itertuples(index=False, name=None))
    return render_template("ejercicio_2.html", df=top_per)


@app.route("/ejercicio_3")
def ej_3():
    cve = list(ejercicio3.f().head(10).itertuples(index=False, name=None))
    return render_template("ejercicio_3.html", data=cve)


@app.route("/ejercicio_4_api", methods=["GET", "POST"])
def ej_4():
    username = request.form.get("username")
    data = ejercicio4_api.f(username)
    return render_template("ejercicio_4_api.html", user=data)


@app.route("/ejercicio_5_regresion_lineal")
def ej_5_regr():
    graph, num_no, num_si = ejercicio5_regresionLineal.regresion_lineal()
    a = plotly.utils.PlotlyJSONEncoder
    graphJSON = json.dumps(graph, cls=a)
    return render_template("ejercicio_5_regresion_lineal.html", graphJSON=graphJSON, num_no=num_no, num_si=num_si)


if __name__ == '__main__':
    app.run(debug=True)
