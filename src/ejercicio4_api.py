import json

import pandas as pd
import requests

def f(username : str):
    response = requests.get(f"https://api.github.com/users/{username}").json()
    #print(response)
    return response

#f("jovancvl")