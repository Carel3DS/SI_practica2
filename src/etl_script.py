# Sistema ETL para la extracción de datos.
# Autor: Carel Sánchez

import sqlite3

import pandas as pd
import json

# Note: Data is already extracted

######################
# TRANSFORM AND LOAD #
######################

# Connect to the database
con = sqlite3.connect('src/data/practica1.db')
cur = con.cursor()

# Open the devices info as JSON and transform into SQL
with open("src/data/devices.json") as f:
    data = json.load(f)
    df = pd.DataFrame(data)

    # Extract analisis and puertos, and create an extended dataframe
    analisis = []
    ports = []

    for i in range(df.__len__()):
        line = df['analisis'][i]
        line['id'] = df['id'][i]
        port = {'id': line['id'], 'puertos': line.pop('puertos_abiertos')}
        if port['puertos'] == "None":
            port['puertos'] = ["None"]

        ports.append(pd.DataFrame(port))
        analisis.append(pd.Series(line))

    analisis = pd.concat(analisis, axis=1).transpose()
    ports = pd.concat(ports, ignore_index=True)

    # Extract responsable and create usuarios dataframe
    usuarios = []
    nombres = []
    for i in range(df.__len__()):
        line = df['responsable'][i]
        nombres.append(line['nombre'])  # Save names to craft maquinas dataframe
        if line['nombre'] not in [s['nombre'] for s in usuarios]:
            usuarios.append(pd.Series(line))  # Save unique usuarios

    nombres = pd.Series(nombres)
    usuarios = pd.concat(usuarios, axis=1).transpose()

    # Drop 'analisis' column, replace 'responsable' with 'nombres' array and merge with 'analisis' dataframe
    maquinas = df.drop(columns='analisis')
    maquinas['responsable'] = nombres

    # Save ports and final df to database
    ports.to_sql('puertos', con, if_exists='replace')  # 'Replace' avoids failure when filling the table
    usuarios.to_sql('usuarios', con, if_exists='replace')
    maquinas.to_sql('maquinas', con, if_exists='replace')
    analisis.to_sql('analisis', con, if_exists='replace')

# Extract transform CSV into alertas table
with open("src/data/alerts.csv") as f:
    alertas = pd.read_csv(f)
    alertas.to_sql('alertas', con, if_exists='replace')

# TEST the database
# cur.execute("SELECT * FROM usuarios JOIN maquinas ON maquinas.responsable=usuarios.nombre ")

# Commit changes and close
con.commit()
con.close()

############
# ANALYSIS #
############

# Use all the dataframes we created to analyze data

# Prepare Ports dataframe for analysis
portGroup = ports[ports['puertos'] != "None"].groupby('id').count()

# COUNTS
devices = maquinas.__len__()  # Number of devices (1)
alerts = alertas.__len__()  # Number of alerts (2)
numNones = maquinas\
    .merge(usuarios, right_on="nombre", left_on="responsable")\
    .merge(analisis, on="id").isin(["None"]).sum().sum()\
    +ports.isin(["None"]).sum().sum()

# MEANS
meanPorts = portGroup['puertos'].mean()
meanInsec = analisis['servicios_inseguros'].mean()
meanVulns = analisis['vulnerabilidades_detectadas'].mean()

# STANDARD DEVIATION
stdPorts = portGroup['puertos'].std()
stdInsec = analisis['servicios_inseguros'].std()
stdVulns = analisis['vulnerabilidades_detectadas'].std()

# MINIMUMS
minVulns = analisis['vulnerabilidades_detectadas'].min()
minPorts = portGroup['puertos'].min()

# MAXIMUMS
maxVulns = analisis['vulnerabilidades_detectadas'].max()
maxPorts = portGroup['puertos'].max()

print(
    "=== STATISTICS ===",
    f"devices:\t{devices}",
    f"alerts:\t\t{alerts}",
    f"numNones:\t{numNones}\n",
    "=== INSECURE SERVICES ===",
    f"meanInsec:\t{meanInsec:.2f}",
    f"stdInsec:\t{stdInsec:.2f}\n",
    "=== VULNERABILITIES ===",
    f"meanVulns:\t{meanVulns:.2f}",
    f"stdVulns:\t{stdVulns:.2f}",
    f"minVulns:\t{minVulns}",
    f"maxVulns:\t{maxVulns}\n",
    "=== OPEN PORTS ===",
    f"meanPorts:\t{meanPorts:.2f}",
    f"stdPorts:\t{stdPorts:.2f}",
    f"minPorts:\t{minPorts}",
    f"maxPorts:\t{maxPorts}",
    sep="\n"
)

