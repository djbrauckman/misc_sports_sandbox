
import io
import pandas as pd
import requests as r
import numpy as np


#read in all the dataframes for matchup history
path = '/users/dbrauckman/Desktop/FFB_History/'

mhpre18 = 'matchup_history_pre18.csv'
mh18 = 'matchup_history_18.csv'
mh19 = 'matchup_history_19.csv'
mh20 = 'matchup_history_20.csv'
mh21 = 'matchup_history_21.csv'
mh22 = 'matchup_history_22.csv'
mh23 = 'matchup_history_23.csv'

df_mhpre18 = pd.read_csv(path + mhpre18)
df_mh18 = pd.read_csv(path + mh18)
df_mh19 = pd.read_csv(path + mh19)
df_mh20 = pd.read_csv(path + mh20)
df_mh21 = pd.read_csv(path + mh21)
df_mh22 = pd.read_csv(path + mh22)
df_mh23 = pd.read_csv(path + mh23)

#Create a list of dataframes to loop through
df_list = [df_mh18, df_mh19, df_mh20, df_mh21, df_mh22, df_mh23]

#Add a year column to the dataframe
year = 2018
for i in range(len(df_list)):
    df_list[i] = df_list[i].rename(columns={f'year': 'Year'})
    df_list[i]['Year'] = year
    year += 1
    
#Concatenate all of the yearly matchup history for a comprehensive dataset
df_list.append(df_mhpre18)
df_mh_all = pd.concat(df_list)

#Dataset cleanup
df_mh_all = df_mh_all.drop(columns=['Unnamed: 0'])
df_mh_all['Name1'] = df_mh_all['Name1'].fillna('Bye')
df_mh_all['Name2'] = df_mh_all['Name2'].fillna('Bye')
df_mh_all['Name1'] = df_mh_all['Name1'].fillna('Bye')
df_mh_all['Score1'] = np.where(df_mh_all['Score1'] == 'Bye', 1, df_mh_all['Score1'])
df_mh_all['Score1'] = df_mh_all['Score1'].fillna(0)
df_mh_all['Score2'] = df_mh_all['Score2'].fillna(0)
df_mh_all['Score1'] = df_mh_all['Score1'].astype(float)
df_mh_all['Score2'] = df_mh_all['Score2'].astype(float)
df_mh_all.loc[(df_mh_all['Name2'] == 'Tom Baker') & (df_mh_all['Score2'] == 0), 'Score2'] = 1


#Team Name Replacement
replacements = {
    #Aaron
    "Me Cago  En Tu Equipo": "Aaron Douglass",
    "CMC - 19": "Aaron Douglass",
    "Stefon Up and Try Me": "Aaron Douglass",
    "Kareem'n Mahomies": "Aaron Douglass",
    "Quad Squad": "Aaron Douglass",    
    
    #Colin
    "Alvin and the  Chipmunks": "Colin Calbreath",
    "Doyle’s Hard Seltzers": "Colin Calbreath",
    "Keep Kamarica Great": "Colin Calbreath",
    "This is Jeopardy": "Colin Calbreath",
    "This was Jeopardy": "Colin Calbreath",
    
    #Danny
    "Always Next Year": "Danny Brauckman",
    "Who's Your Caddy?": "Danny Brauckman",
    "I suck shit every year, too": "Danny Brauckman",
    "Mayor of  Griddy City": "Danny Brauckman",
    
    #Jordan
    "Please Trade Le'Veon": "Jordan Hahne",
    "Good JuJu": "Jordan Hahne",
    "Catalina Wine Mixon": "Jordan Hahne",
    "I Need Moore Beer": "Jordan Hahne",
    "Jameson Shots": "Jordan Hahne",
    
    #Matthew
    "Dezâs Team": "Matthew Wright",
    "Bourbon Bowl Champs": "Matthew Wright",
    "Fauci Ouchies": "Matthew Wright",
    "Loading ...": "Matthew Wright",
    
    #Geiss
    "Sippn a  Kupp of Ginn": "Jordan Geissinger",
    "Cookin' on the Conner": "Jordan Geissinger",
    "Gurleys Thielen My Chubby": "Jordan Geissinger",
    "Chubby Makes Me Waddle": "Jordan Geissinger",
    "Penny for the Herb": "Jordan Geissinger",
    
    #Robert
    "I have a Chubb  again": "Robert Schult",
    "Take a look at  my Chubb": "Robert Schult",
    "I suck shit Every year": "Robert Schult",
    "My keeper just Quit football": "Robert Schult",
    "Bumblebee Tuna": "Robert Schult",
    
    #Tom
    "The Baker Effect": "Tom Baker",
    "The Blind Ribeyes": "Tom Baker",
    "CeeDeez D Kupps": "Tom Baker",
    "Rhamondre Deez Nuts": "Tom Baker",
    "Olave Doubies": "Tom Baker",
    
    #Josh
    "Ma  Homie": "Josh Zipoy",
    "Thielen  A Repeat": "Josh Zipoy",
    "Succop Mi Johnson": "Josh Zipoy",
    "Cee Is 4 Cheesy Deer": "Josh Zipoy",
    "Oh No We Suck Again ": "Josh Zipoy",
    "Oh No We Suck Again": "Josh Zipoy",
    
    #David
    "Cosby's Sleeper Picks": "David Rodriguez",
    
    #Corey
    "Julio Think You Are, I Am": "Corey Calbreath",
    
    #Shelby
    "The Replacements": "Shelby Fritsche"
    
}


#Replace team name with manager name

df_mh_all["Name1"] = df_mh_all["Name1"].replace(replacements)
df_mh_all["Name2"] = df_mh_all["Name2"].replace(replacements)

#Split out the regular season and playoffs
#ADD A DIFFERENTIATION BETWEN A TRUE PLAYOFF GAME AND CONSOLATION
df_mh_all_reg = df_mh_all[df_mh_all["Type"] == "Regular"]
df_mh_all_ps = df_mh_all[df_mh_all["Type"] == "Playoff"]
df_mh_all_c = df_mh_all[df_mh_all["Type"] == "Consolation"]


#Manager list (extract unique managers from the dataframe)
manager_list = pd.unique(df_mh_all[['Name1', 'Name2']].values.ravel('K'))
    
#Loop through and determine everyone's record against each other
def rs_record_by_opponent(manager):
    results = {'Opponent': [], 'Wins': 0, 'Losses': 0, 'Ties': 0}
    

    
    for opponent in manager_list:
        if opponent == manager:
            continue
            
        wins = 0
        losses = 0
        ties = 0
        
        # Filter games where the manager is Name1 and opponent is Name2
        manager_as_name1 = df_mh_all_reg[(df_mh_all_reg['Name1'] == manager) 
                                         & (df_mh_all_reg['Name2'] == opponent) 
                                         & df_mh_all_reg['Name1'].notna()
                                         & df_mh_all_reg['Name2'].notna()]
        # Filter games where the manager is Name2 and opponent is Name1
        manager_as_name2 = df_mh_all_reg[(df_mh_all_reg['Name2'] == manager) & (df_mh_all_reg['Name1'] == opponent)
                                         & df_mh_all_reg['Name1'].notna()
                                         & df_mh_all_reg['Name2'].notna()]
        
        # Calculate wins, losses, and ties
        for index, row in manager_as_name1.iterrows():
            if row['Score1'] > row['Score2']:
                wins += 1
            elif row['Score1'] < row['Score2']:
                losses += 1
            else:
                ties += 1
        
        for index, row in manager_as_name2.iterrows():
            if row['Score2'] > row['Score1']:
                wins += 1
            elif row['Score2'] < row['Score1']:
                losses += 1
            else:
                ties += 1
        
        total_games = wins + losses
        
        if wins > 0:
            win_pct = (wins / total_games) * 100
        else:
            win_pct = 0
            
        results['Opponent'].append({
            'Name': opponent,
            'Wins': wins,
            'Losses': losses,
            'Total Games': total_games,
            'Win %': round(win_pct, 1)
        })
    
    
    return results

#Loop through and determine everyone's playoff record against each other
def ps_record_by_opponent(manager):
    results = {'Opponent': [], 'Wins': 0, 'Losses': 0, 'Ties': 0}
    

    
    for opponent in manager_list:
        if opponent == manager:
            continue
            
        wins = 0
        losses = 0
        ties = 0
        
        # Filter games where the manager is Name1 and opponent is Name2
        manager_as_name1 = df_mh_all_ps[(df_mh_all_ps['Name1'] == manager) 
                                         & (df_mh_all_ps['Name2'] == opponent) 
                                         & df_mh_all_ps['Name1'].notna()
                                         & df_mh_all_ps['Name2'].notna()]
        # Filter games where the manager is Name2 and opponent is Name1
        manager_as_name2 = df_mh_all_ps[(df_mh_all_ps['Name2'] == manager) & (df_mh_all_ps['Name1'] == opponent)
                                         & df_mh_all_ps['Name1'].notna()
                                         & df_mh_all_ps['Name2'].notna()]
        
        # Calculate wins, losses, and ties
        for index, row in manager_as_name1.iterrows():
            if row['Score1'] > row['Score2']:
                wins += 1
            elif row['Score1'] < row['Score2']:
                losses += 1
            else:
                ties += 1
        
        for index, row in manager_as_name2.iterrows():
            if row['Score2'] > row['Score1']:
                wins += 1
            elif row['Score2'] < row['Score1']:
                losses += 1
            else:
                ties += 1
        
        
        total_games = wins + losses
        
        if wins > 0:
            win_pct = (wins / total_games) * 100
        else:
            win_pct = 0
            
        results['Opponent'].append({
            'Name': opponent,
            'Wins': wins,
            'Losses': losses,
            'Total Games': total_games,
            'Win %': round(win_pct, 1)
        })
    
    return results


#Loop through and determine everyone's record against each other
def cons_record_by_opponent(manager):
    results = {'Opponent': [], 'Wins': 0, 'Losses': 0, 'Ties': 0}
    

    
    for opponent in manager_list:
        if opponent == manager:
            continue
            
        wins = 0
        losses = 0
        ties = 0
        
        # Filter games where the manager is Name1 and opponent is Name2
        manager_as_name1 = df_mh_all_c[(df_mh_all_c['Name1'] == manager) 
                                         & (df_mh_all_c['Name2'] == opponent) 
                                         & df_mh_all_c['Name1'].notna()
                                         & df_mh_all_c['Name2'].notna()]
        # Filter games where the manager is Name2 and opponent is Name1
        manager_as_name2 = df_mh_all_c[(df_mh_all_c['Name2'] == manager) & (df_mh_all_c['Name1'] == opponent)
                                         & df_mh_all_c['Name1'].notna()
                                         & df_mh_all_c['Name2'].notna()]
        
        # Calculate wins, losses, and ties
        for index, row in manager_as_name1.iterrows():
            if row['Score1'] > row['Score2']:
                wins += 1
            elif row['Score1'] < row['Score2']:
                losses += 1
            else:
                ties += 1
        
        for index, row in manager_as_name2.iterrows():
            if row['Score2'] > row['Score1']:
                wins += 1
            elif row['Score2'] < row['Score1']:
                losses += 1
            else:
                ties += 1
        
        
        total_games = wins + losses
        
        if wins > 0:
            win_pct = (wins / total_games) * 100
        else:
            win_pct = 0
            
        results['Opponent'].append({
            'Name': opponent,
            'Wins': wins,
            'Losses': losses,
            'Total Games': total_games,
            'Win %': round(win_pct, 1)
        })
    
    return results


#Regular season records by manager
for manager in manager_list:
    record = rs_record_by_opponent(manager)
    print("Regular Season")
    print("Manager:", manager)
    total_games_played = len(df_mh_all_reg[
        ((df_mh_all_reg['Name1'] == manager) | (df_mh_all_reg['Name2'] == manager)) &
        df_mh_all_reg['Name1'].notna() & 
        df_mh_all_reg['Name2'].notna()
    ])
    print(f"Total Regular Season Games: {total_games_played}")
    for opponent in record['Opponent']:
        print(f"vs {opponent['Name']}: {opponent['Wins']} - {opponent['Losses']}, Win %: {opponent['Win %']}")

#Playoff Records by Manager
for manager in manager_list:
    record = ps_record_by_opponent(manager)
    print("Playoffs")
    print("Manager: ", manager)
    total_games_played = len(df_mh_all_ps[
        ((df_mh_all_ps['Name1'] == manager) | (df_mh_all_ps['Name2'] == manager)) &
        df_mh_all_ps['Name1'].notna() & 
        df_mh_all_ps['Name2'].notna()
    ])

    print(f"Total Playoff Games: {total_games_played}")
    for opponent in record['Opponent']:
        print(f"vs {opponent['Name']}: {opponent['Wins']} - {opponent['Losses']}, Win %: {opponent['Win %']}")

#Consolation Records by Manager
for manager in manager_list:
    record = cons_record_by_opponent(manager)
    print("Consolation")
    print("Manager: ", manager)
    total_games_played = len(df_mh_all_c[
        ((df_mh_all_c['Name1'] == manager) | (df_mh_all_c['Name2'] == manager)) &
        df_mh_all_c['Name1'].notna() & 
        df_mh_all_c['Name2'].notna()
    ])

    print(f"Total Consolation Games: {total_games_played}")
    for opponent in record['Opponent']:
        print(f"vs {opponent['Name']}: {opponent['Wins']} - {opponent['Losses']}, Win %: {opponent['Win %']}")



#find games decided by fewer than x points, records in close games
#same for blowouts


