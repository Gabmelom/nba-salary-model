import os
import pandas as pd

cols = ['player', '2020', '2021', '2022', '2023']

df_salary = pd.DataFrame(columns=cols)
df_salary_inflation = pd.DataFrame(columns=cols)

# Load the data
for year in ['2020','2021','2022','2023']:
    file = os.path.join(os.getcwd(), 'data','raw','salaries',f'{year}.csv')  
    df = pd.read_csv(file)
    
    # Salary data
    df_salary['player'] = df['Player']
    df_salary[year] = df['Salary']

    # Salary data adjusted for inflation
    df_salary_inflation['player'] = df['Player']
    df_salary_inflation[year] = df['Salary (adjusted)']

# Save the data
df_salary.to_csv(os.path.join(os.getcwd(), 'data','clean','salaries','salary.csv'), index=False)
df_salary_inflation.to_csv(os.path.join(os.getcwd(), 'data','clean','salaries','salary_inflation.csv'), index=False)
