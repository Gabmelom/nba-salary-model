# Read JSON file and covert to CSV

import json
import pandas as pd
import os

files = ['22 roster.json', '23 roster.json', '24 roster.json']

# Read JSON files
for file in files:
    with open(f'{os.getcwd()}/data/raw/2k detailed/{file}') as f:
        data = json.load(f)

    # Convert to dataframe
    df = pd.DataFrame(data)

    # Remove 'team' columns
    df = df.drop(columns=['team'])

    # Order by player name
    df = df.sort_values(by='name')

    # Export to CSV
    df.to_csv(f'2k{file[:2]}.csv', index=False)
