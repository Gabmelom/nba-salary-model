import pandas as pd
import os

years = ['20','21','22','23']

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
    missing.to_csv('20'+year+'_missing_stats.csv', index=False)

    # Add salary to the joined table
    ratings_salary_stats = ratings_stats.merge(salary, left_on='name', right_on='Player', how='inner')
    ratings_salary_stats = ratings_salary_stats.drop(columns=['Player'])

    # Save players that didn't match between joined stats and salary
    ratings_stats_names = ratings_stats['name'].values
    salary_names = salary['Player'].values
    missing_salary_names = list(set(ratings_stats_names) - set(salary_names))

    missing_salary = ratings_stats[ratings_stats['name'].isin(missing_salary_names)]
    missing_salary.to_csv('20'+year+'_missing_salaries.csv', index=False)

    # Save the joined table
    ratings_salary_stats.to_csv('20'+year+'_joined.csv', index=False)

# # Join 2020 tables per year and player name
# data_folder = os.path.join(os.getcwd(),'data', 'clean')

# ratings = pd.read_csv(os.path.join(data_folder, '2k ratings','2k20_clean.csv'))
# salary = pd.read_csv(os.path.join(data_folder, 'salaries','salary.csv'))
# stats = pd.read_csv(os.path.join(data_folder, 'stats','19-20 Regular.csv'))

# # Join ratings and stats by player name
# ratings_stats = ratings.merge(stats, left_on='name', right_on='Player', how='inner')
# ratings_stats = ratings_stats.drop(columns=['Player'])
# ratings_stats.to_csv('2k20_rating_stats.csv', index=False)

# # Save players that didn't match between ratings and stats
# ratings_names = ratings['name'].values
# stats_names = stats['Player'].values
# missing_names = list(set(ratings_names) - set(stats_names))
# missing = ratings[ratings['name'].isin(missing_names)]
# missing.to_csv('2020_missing_stats.csv', index=False)

# # Add salary to the joined table
# ratings_salary_stats = ratings_stats.merge(salary, left_on='name', right_on='player', how='inner')
# ratings_salary_stats = ratings_salary_stats.drop(columns=['player'])

# # Save players that didn't match between joined stats and salary
# ratings_stats_names = ratings_stats['name'].values
# salary_names = salary['player'].values
# missing_salary_names = list(set(ratings_stats_names) - set(salary_names))

# missing_salary = ratings_stats[ratings_stats['name'].isin(missing_salary_names)]
# missing_salary.to_csv('2020_missing_salaries.csv', index=False)

# # Save the joined table
# ratings_salary_stats.to_csv('2020_joined.csv', index=False)