import io
import pandas as pd
import requests as r

path = '/users/dbrauckman/Desktop/Football Stats/'

#############################################
# Dak Prescott
#############################################

#file read in, DF creation
dak_file = 'dak_career_gamelogs.csv'
df_dak = pd.read_csv(path + dak_file)


#reset first row to column names, drop first row
df_dak.columns = df_dak.iloc[0]
df_dak = df_dak.drop(index=0)

#Drop records where QB was inactive
df_dak.drop(df_dak.loc[df_dak['Rate']=='Injured Reserve'].index, inplace=True)
df_dak.drop(df_dak.loc[df_dak['Rate']=='Inactive'].index, inplace=True)

#Convert Rating to numeric value
df_dak['Rate'] = pd.to_numeric(df_dak['Rate'])


#Count of ratings below 50 - bad games
len(df_dak[['Year', 'Opp', 'Rate']][df_dak['Rate'] <= 61.0])

#Count of ratings above 75 - good games
len(df_dak[['Year', 'Opp', 'Rate']][df_dak['Rate'] >= 75.0])


#rename passing attempt column for distinction
df_dak.columns.values[12] = "pass_att"

#drop totals row
df_dak = df_dak.drop(index=120)

df_dak['pass_att'] = pd.to_numeric(df_dak['pass_att'])

df_dak[['Year', 'Opp', 'Result']][df_dak['pass_att'] >= 30 & df_dak['Result'][0] == 'W']
w_filtered_df = df_dak[(df_dak['Result'].str.startswith('W')) & (df_dak['pass_att'] >= 30)]
l_filtered_df = df_dak[(df_dak['Result'].str.startswith('L')) & (df_dak['pass_att'] >= 30)]

#############################################
# Josh Allen
#############################################

#file read in, DF creation
jallen_file = 'jallen_career_gamelogs.csv'
df_jallen = pd.read_csv(path + jallen_file)

#reset first row to column names, drop first row
df_jallen.columns = df_jallen.iloc[0]
df_jallen = df_jallen.drop(index=0)

#Drop records where QB was inactive
df_jallen.drop(df_jallen.loc[df_jallen['Rate']=='Injured Reserve'].index, inplace=True)
df_jallen.drop(df_jallen.loc[df_jallen['Rate']=='Inactive'].index, inplace=True)

#Convert Rating to numeric value
df_jallen['Rate'] = pd.to_numeric(df_jallen['Rate'])


#Count of ratings below 50 - bad games
len(df_jallen[['Year', 'Opp', 'Rate']][df_jallen['Rate'] <= 61.0])

#Count of ratings above 75 - good games
len(df_jallen[['Year', 'Opp', 'Rate']][df_jallen['Rate'] >= 75.0])

