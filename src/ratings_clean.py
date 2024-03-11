# Read JSON file and covert to CSV

import json
import pandas as pd
import os
import unidecode as ud

json_files = ['22 roster.json', '23 roster.json', '24 roster.json']

# Read JSON files
for file in json_files:
    with open(f'{os.getcwd()}/data/raw/2k detailed/{file}', encoding='utf-8') as f:
        data = json.load(f)

    # Convert to dataframe
    df = pd.DataFrame(data)

    # Remove 'team' columns
    df = df.drop(columns=['team'])

    # Clean player names
    df['name'] = df['name'].apply(lambda x: x.replace('’', "'"))
    df['name'] = df['name'].apply(lambda x: ud.unidecode(x))

    # Order by player name
    df = df.sort_values(by='name')

    # Export to CSV
    df.to_csv(f'{os.getcwd()}/data/clean/2k ratings/2k{file[:2]}.csv', index=False)

# Read CSV files
csv_files = ['20 roster.csv']

for file in csv_files:
    df = pd.read_csv(f'{os.getcwd()}/data/raw/2k detailed/{file}')

    # Remove columns Nationality,Team,Archetype,Position1,Position2,Height,Weight,Jersey
    df = df.drop(columns=['Nationality','Team','Archetype','Position1','Position2','Height','Weight','Jersey','Year(s) in the NBA','Prior to NBA','Rank current','Rank all','Team_Category'])

    # Clean player names
    df['player'] = df['player'].apply(lambda x: x.replace('’', "'"))
    df['player'] = df['player'].apply(lambda x: ud.unidecode(x))

    # Order by player name
    df = df.sort_values(by='player')

    # Export to CSV
    df.to_csv(f'{os.getcwd()}/data/clean/2k detailed/2k{file[:2]}.csv', index=False)