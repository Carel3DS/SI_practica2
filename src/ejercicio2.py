import sqlite3
import pandas as pd

###############
# EJERCICIO 2 #
###############

def top_per():
    con = sqlite3.connect('data/practica1.db')
    analisis = pd.read_sql("SELECT * FROM analisis", con)
    con.close()
    per = round(analisis['servicios_inseguros']/analisis['servicios']*100, 2)
    res = pd.merge(analisis['id'], per.rename('percentage'), right_index=True,left_index=True).sort_values(by='percentage',ascending=False)
    return res.dropna()
