import pandas as pd
import os

years = ['20','21','22','23']

def outputFolder(filename):
    return os.path.join(os.getcwd(),'data', 'joined', filename)

# Join every year's tables
for year in years:
    data_folder = os.path.join(os.getcwd(),'data', 'clean')
    ratings = pd.read_csv(os.path.join(data_folder, '2k ratings','2k'+year+'_clean.csv'))
    salary = pd.read_csv(os.path.join(data_folder, 'salaries',f'20{year}.csv'))
    stats = pd.read_csv(os.path.join(data_folder, 'stats',f'{str(int(year)-1)}-{year} Regular.csv'))

    # Join ratings and stats by player name
    ratings_stats = ratings.merge(stats, left_on='name', right_on='Player', how='inner')
    ratings_stats = ratings_stats.drop(columns=['Player'])
    # ratings_stats.to_csv('2k'+year+'_rating_stats.csv', index=False)

    # Save players that didn't match between ratings and stats
    ratings_names = ratings['name'].values
    stats_names = stats['Player'].values
    missing_names = list(set(ratings_names) - set(stats_names))
    missing = ratings[ratings['name'].isin(missing_names)]
    missing.to_csv(outputFolder('20'+year+'_missing.csv'), index=False)

    # Add salary to the joined table
    ratings_salary_stats = ratings_stats.merge(salary, left_on='name', right_on='Player', how='inner')
    ratings_salary_stats = ratings_salary_stats.drop(columns=['Player'])

    # Save players that didn't match between joined stats and salary
    ratings_stats_names = ratings_stats['name'].values
    salary_names = salary['Player'].values
    missing_salary_names = list(set(ratings_stats_names) - set(salary_names))

    missing_salary = ratings_stats[ratings_stats['name'].isin(missing_salary_names)]
    missing_salary.to_csv(outputFolder('20'+year+'_missing_salary.csv'), index=False)

    # Rename columns based on glossary
    glossary = {
        'Rk': 'Rank',
        'Pos': 'Position',
        'Age': 'Age',
        'Tm': 'Team',
        'G': 'Games',
        'GS': 'Games Started',
        'MP': 'Minutes Played',
        'FG': 'Field Goals',
        'FGA': 'Field Goal Attempts',
        'FG%': 'Field Goal %',
        '3P': '3-Point Field Goals',
        '3PA': '3-Point Field Goal Attempts',
        '3P%': '3-Point Field Goal %',
        '2P': '2-Point Field Goals',
        '2PA': '2-point Field Goal Attempts',
        '2P%': '2-Point Field Goal %',
        'eFG%': 'Effective Field Goal %',
        'FT': 'Free Throws',
        'FTA': 'Free Throw Attempts',
        'FT%': 'Free Throw %',
        'ORB': 'Offensive Rebounds',
        'DRB': 'Defensive Rebounds',
        'TRB': 'Total Rebounds',
        'AST': 'Assists',
        'STL': 'Steals',
        'BLK': 'Blocks',
        'TOV': 'Turnovers',
        'PF': 'Personal Fouls',
        'PTS': 'Points'
    }
    glossary_lower = {k: v.lower().replace(' ','_') for k, v in glossary.items()}
    ratings_salary_stats = ratings_salary_stats.rename(columns=glossary_lower)
    ratings_salary_stats = ratings_salary_stats.rename(columns={'Salary': 'salary', 'Salary (adjusted)': 'salary_adjusted'})
    ratings_salary_stats = ratings_salary_stats.drop(columns=['rank', 'team','position','secondary_position'])

    ratings_salary_stats['height'] = ratings_salary_stats['height'].apply(lambda x: int(x.split('\'')[0])*12 + int(x.split('\'')[1]))

    # Save the joined table
    ratings_salary_stats.to_csv(outputFolder('20'+year+'_joined.csv'), index=False)