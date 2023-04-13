
from flask import Flask, render_template, request
import ejercicio1
import pandas as pd

###############
# EJERCICIO 2 #
###############

app = Flask(__name__)


@app.route('/')
def index():
    top_per = list(ejercicio1.top_per().itertuples(index=False, name=None))
    return render_template('index.html', df=top_per)

app.run()
