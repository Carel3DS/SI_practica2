import math
import sqlite3
import pandas as pd


###############
# EJERCICIO 1 #
###############

def analysis():
    # Connect to the database
    con = sqlite3.connect('data/practica1.db')

    # Retrieve tables as pd Dataframes
    alertas = pd.read_sql("SELECT * FROM alertas", con)
    analisis = pd.read_sql("SELECT * FROM analisis", con)

    # Get most problematic IP addresses
    top_ip = alertas.groupby('origen')['origen'] \
        .count().sort_values(ascending=False) \
        .to_frame()

    # Get most vulnerable devices
    top_vuln = analisis[['id', 'vulnerabilidades_detectadas']] \
        .sort_values('vulnerabilidades_detectadas', ascending=False) \
        .reset_index()
    return top_vuln, top_ip


def top_per():
    con = sqlite3.connect('data/practica1.db')
    analisis = pd.read_sql("SELECT * FROM analisis", con)
    per = round(analisis['servicios_inseguros']/analisis['servicios']*100, 2)
    res = pd.merge(analisis['id'], per.rename('percentage'), right_index=True,left_index=True).sort_values(by='percentage',ascending=False)
    return res.dropna()


top_per()
top_vuln, top_ip = analysis()
print("===Top most frequent IP origin===")
print(top_ip)
print("\n===Top Most vulnerable===")
print(top_vuln)
