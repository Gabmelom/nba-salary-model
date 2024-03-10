# %%
import requests
import pandas as pd
from bs4 import BeautifulSoup
import locale

locale.setlocale(locale.LC_ALL, 'en_US.UTF8')

# %%
# Downloading contents of the web page
years = ['2019-2020', '2020-2021', '2021-2022', '2022-2023']
url = {
    '2019-2020': 'https://hoopshype.com/salaries/players/2019-2020/',
    '2020-2021': 'https://hoopshype.com/salaries/players/2020-2021/',
    '2021-2022': 'https://hoopshype.com/salaries/players/2021-2022/',
    '2022-2023': 'https://hoopshype.com/salaries/players/2022-2023/'
}
data = {
    '2019-2020': requests.get(url['2019-2020']).text,
    '2020-2021': requests.get(url['2020-2021']).text,
    '2021-2022': requests.get(url['2021-2022']).text,
    '2022-2023': requests.get(url['2022-2023']).text
}

# %%
# Defining of the dataframe
table_class = "hh-salaries-ranking-table hh-salaries-table-sortable responsive"

for year in years:
    soup = BeautifulSoup(data[year], 'html.parser')
    table = soup.find('table', {'class': table_class})
    df = pd.DataFrame(columns=['Player', year, year+'(*)'])

    # Collecting Ddata
    for row in table.tbody.find_all('tr'):    
        # Find all data for each column
        columns = row.find_all('td')
        
        if(columns != []):
            player = columns[1].text.strip()
            salary = columns[2].text.strip().strip("$").replace(',', '')
            salary_inflation = columns[3].text.strip().strip("$").replace(',', '')

            df = df._append({'Player': player, year: salary, year+'(*)': salary_inflation}, ignore_index=True)

    # Exporting the dataframe to a csv file
    df.to_csv('nba_salaries_'+year+'.csv', index=False)


