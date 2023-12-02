#Read in csv data from github

import pandas as pd
import requests
from io import StringIO

#Read a Singular File
base_url = 'https://raw.githubusercontent.com/djbrauckman/ffb_historical_data/main/'
filename = 'matchup_history_22.csv'
response = requests.get(base_url + filename)
csv_data = StringIO(response.text)    
df = pd.read_csv(csv_data)

#Read in multiple datasets
years = [18,19,20,21,22]
dfs = {}

for i in years:

    base_url = 'https://raw.githubusercontent.com/djbrauckman/ffb_historical_data/main/'
    filename = f'matchup_history_{i}.csv'
    response = requests.get(base_url + filename)
    csv_data = StringIO(response.text)    
    df = pd.read_csv(csv_data)
    df['year'] = i
    dfs[f'df_{i}'] = df 
      

dfs['df_18']
