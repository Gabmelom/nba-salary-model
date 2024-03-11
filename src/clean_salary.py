import os
import pandas as pd

cols = ['player', '2020', '2021', '2022', '2023']

df_salary = pd.DataFrame(columns=cols)
df_salary_inflation = pd.DataFrame(columns=[c + ' (adjusted)' if c != 'player' else 'player' for c in cols ])

# Load the data
for year in ['2020','2021','2022','2023']:
    file = os.path.join(os.getcwd(), 'data','raw','salaries',f'{year}.csv')  
    df = pd.read_csv(file)

    # Rename columns
    df.rename(columns={'Player': 'player'}, inplace=True)
    df.rename(columns={'Salary':year}, inplace=True)
    df.rename(columns={'Salary (adjusted)':year + ' (adjusted)'}, inplace=True)


    # Insert salary data
    if df_salary.empty:
        df_salary = df[['player', year]]
        df_salary_inflation = df[['player', year + ' (adjusted)']]

    else:
        df_salary = df_salary.merge(df[['player', year]], on='player', how='outer')
        df_salary_inflation = df_salary_inflation.merge(df[['player', year + ' (adjusted)']], on='player', how='outer')

    # Change floats to ints, ignore NaN
    df_salary[year] = df_salary[year].astype('Int64',errors='ignore')
    df_salary_inflation[year + ' (adjusted)'] = df_salary_inflation[year + ' (adjusted)'].astype('Int64',errors='ignore')

# Save the data
df_salary.to_csv(os.path.join(os.getcwd(), 'data','clean','salaries','salary.csv'), index=False)
df_salary_inflation.to_csv(os.path.join(os.getcwd(), 'data','clean','salaries','salary_inflation.csv'), index=False)
