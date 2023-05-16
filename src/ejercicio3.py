import pandas as pd
import requests

url = "https://cve.circl.lu/api/last"



###############
# EJERCICIO 3 #
###############

def f():
    # Get latest vulnerabilities JSON
    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload).text

    # Read JSON into dataframe and get ID and Publish time
    df = pd.read_json(response)

    latest = df[['id', 'cwe', 'Published']]
    latest = latest.replace(["NVD-CWE-noinfo", "Unknown"], "—")
    #print(latest)
    return latest
