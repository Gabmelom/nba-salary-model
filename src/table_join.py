import pandas as pd
import os

# Join tables per year and player name
def join_tables():
    # Read all files in the directory
    files = os.listdir('data/clean/salaries')
    files = [file for file in files if file.endswith('.csv')]

    # Create a list of dataframes
    dfs = [pd.read_csv(f'data/clean/salaries/{file}') for file in files]

    # Join dataframes
    df = pd.concat(dfs, axis=0)

    # Export the dataframe to a csv file
    df.to_csv('data/raw/salaries/all.csv', index=False)

    return df

