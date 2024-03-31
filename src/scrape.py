import requests
import locale
import os
import pandas as pd
from bs4 import BeautifulSoup

locale.setlocale(locale.LC_ALL, 'en_US.UTF8')

def save_html(url, filename):
    response = requests.get(url)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(response.text)

def parse_nba_stats(infile, outfile):
    with open(infile, encoding='utf-8') as f:
        data = f.read()
    
    # Defining of the dataframe
    table_class = "stats_table"
    soup = BeautifulSoup(data, 'html.parser')
    table = soup.find('table', {'class': table_class})

    df = pd.DataFrame(columns=['Player', 'Pos', 'Age', 'Tm', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', 
                               '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 
                               'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS'])

    # Collecting data
    for row in table.tbody.find_all('tr'):    
        # Find all data for each column
        columns = row.find_all('td')
        
        if(columns != []):
            player = columns[0].text.strip()
            pos = columns[1].text.strip()
            age = columns[2].text.strip()
            tm = columns[3].text.strip()
            g = columns[4].text.strip()
            gs = columns[5].text.strip()
            mp = columns[6].text.strip()
            fg = columns[7].text.strip()
            fga = columns[8].text.strip()
            fg_per = columns[9].text.strip()
            three_p = columns[10].text.strip()
            three_pa = columns[11].text.strip()
            three_per = columns[12].text.strip()
            two_p = columns[13].text.strip()
            two_pa = columns[14].text.strip()
            two_per = columns[15].text.strip()
            efg_per = columns[16].text.strip()
            ft = columns[17].text.strip()
            fta = columns[18].text.strip()
            ft_per = columns[19].text.strip()
            orb = columns[20].text.strip()
            drb = columns[21].text.strip()
            trb = columns[22].text.strip()
            ast = columns[23].text.strip()
            stl = columns[24].text.strip()
            blk = columns[25].text.strip()
            tov = columns[26].text.strip()
            pf = columns[27].text.strip()
            pts = columns[28].text.strip()

            html_data = {'Player': player, 'Pos': pos, 'Age': age, 'Tm': tm, 'G': g, 'GS': gs, 'MP': mp, 'FG': fg, 'FGA': fga, 'FG%': fg_per, 
                         '3P': three_p, '3PA': three_pa, '3P%': three_per, '2P': two_p, '2PA': two_pa, '2P%': two_per, 'eFG%': efg_per, 'FT': ft, 'FTA': fta, 'FT%': ft_per, 
                         'ORB': orb, 'DRB': drb, 'TRB': trb, 'AST': ast, 'STL': stl, 'BLK': blk, 'TOV': tov, 'PF': pf, 'PTS': pts}
        
        df = df._append(html_data, ignore_index=True)

    # Exporting the dataframe to a csv file
    df.to_csv(f'../data/raw/stats/{outfile}.csv', index=False)

def scrape_nba_stats(save_html=False):
    # Downloading contents of the web page
    if save_html:
        for year in range(10, 24):
            reg = f'https://www.basketball-reference.com/leagues/NBA_20{year}_per_game.html'
            save_html(reg, f'./basketball_reference_stats/20{year}.html')

            playoff = f'https://www.basketball-reference.com/playoffs/NBA_20{year}_per_game.html'
            save_html(playoff, f'./basketball_reference_stats/20{year}_playoff.html')

    # Scrape player stats from basketball-reference.com
    for year in range(10, 24):
        filename = f'./basketball_reference_stats/20{year}_regular.html'
        parse_nba_stats(filename, f'20{year} Regular')

        filename = f'./basketball_reference_stats/20{year}_playoffs.html'
        parse_nba_stats(filename, f'20{year} Playoff')

def scrape_salary():
    # Downloading contents of the web page
    for year in range(10, 24):
        # if year is 9 or less, add a 0 to the year
        prev_year = str(year-1).zfill(2) if year < 10 else year
        url = f'https://hoopshype.com/salaries/players/20{prev_year}-{year}/'
        save_html(url, f'./hoopshype_salaries/20{year}.html')

    # Defining of the dataframe
    table_class = "hh-salaries-ranking-table hh-salaries-table-sortable responsive"

    for year in range(10, 24):
        with open(f'../src/hoopshype_salaries/20{year}.html', 'r') as f:
            data = f.read()
        soup = BeautifulSoup(data, 'html.parser')
        table = soup.find('table', {'class': table_class})
        df = pd.DataFrame(columns=['Player', 'Salary'])

        # Collecting Ddata
        for row in table.tbody.find_all('tr'):    
            # Find all data for each column
            columns = row.find_all('td')
            
            if(columns != []):
                player = columns[1].text.strip()
                salary = columns[2].text.strip().strip("$").replace(',', '')

                df = df._append({'Player': player, 'Salary': salary}, ignore_index=True)

        # Exporting the dataframe to a csv file
        df.to_csv(f'../data/raw/salaries/20{year}.csv', index=False)


def scrape_ratings(save_html=False):
    # Downloading contents of the web page
    if save_html:
        for year in range(10, 24):
            prev_year = str(year-1).zfill(2) if year < 10 else year
            url = f'https://hoopshype.com/nba2k/20{prev_year}-{year}/'
            save_html(url, f'./hoopshype_2k_overall/20{year}.html')

    # Defining of the dataframe
    table_class = "hh-salaries-ranking-table hh-salaries-table-sortable responsive"
    top_folder = os.path.dirname(os.getcwd())

    for year in range(10, 24):
        with open(f'../hoopshype_2k_overall/hoopshype_2k{year}.html') as f:
            data = f.read()
        soup = BeautifulSoup(data, 'html.parser')
        table = soup.find('table', {'class': table_class})
        df = pd.DataFrame(columns=['Player', 'Rating'])

        # Collecting Ddata
        for row in table.tbody.find_all('tr'):    
            # Find all data for each column
            columns = row.find_all('td')
            
            if(columns != []):
                player = columns[1].text.strip()
                rating = columns[2].text.strip()

                df = df._append({'Player': player, 'Rating': rating}, ignore_index=True)

        # Exporting the dataframe to a csv file
        df.to_csv(f'{top_folder}/data/raw/2k overall/2k{year}.csv', index=False)

if __name__ == '__main__':
    html = False
    scrape_salary(html)
    scrape_nba_stats(html)
    scrape_ratings(html)
