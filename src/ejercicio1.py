import flask
import sqlite3
import pandas as pd

###############
# EJERCICIO 1 #
###############

# Connect to the database
con = sqlite3.connect('data/practica1.db')

# Retrieve tables as pd Dataframes
alertas = pd.read_sql("SELECT * FROM alertas", con)
analisis = pd.read_sql("SELECT * FROM analisis", con)

# Get most problematic IP addresses
top_ip = alertas.groupby('origen')['origen'] \
    .count().sort_values(ascending=False)\
    .to_frame()

# Get most vulnerable devices
top_vuln = analisis[['id', 'vulnerabilidades_detectadas']] \
    .sort_values('vulnerabilidades_detectadas', ascending=False) \
    .reset_index()

print("===Top most frequent IP origin===")
print(top_ip)
print("\n===Top Most vulnerable===")
print(top_vuln)
