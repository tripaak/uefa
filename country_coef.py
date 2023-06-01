import requests
import csv
import os
import time
import glob
import pandas as pd
import datetime


def scrap():
    start_year = 2010
    end_year = 2023

    for year in range(start_year,end_year+1):
        print(f"Scraping for year : {year}")
        url = f"https://comp.uefa.com/v2/coefficients?coefficientType=MEN_ASSOCIATION&coefficientRange=OVERALL&seasonYear={year}&page=1&pagesize=500&language=EN"

        payload={}
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.uefa.com/',
        'x-api-key': 'ceeee1a5bb209502c6c438abd8f30aef179ce669bb9288f2d1cf2fa276de03f4',
        'Origin': 'https://www.uefa.com',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        response = requests.request("GET", url, headers=headers, data=payload)

        response = response.json()
        data = response['data']['members']


        for member in data:
            item = {}
            item['country'] = member['member']['displayOfficialName']
            item['id_country'] = member['member']['associationId']
            # item['pos'] = member['overallRanking']['position']
            session = f"{year-4}/{year}"
            # numberOfTeamsStillInPlaying = member['overallRanking']['numberOfTeamsStillInPlaying']
            # numberOfTeams = member['overallRanking']['numberOfTeams']
            # if numberOfTeamsStillInPlaying == 0:
            #     item['clubs'] = numberOfTeams
            # else:
            #     item['clubs'] = str(f"{numberOfTeamsStillInPlaying}/{numberOfTeams}")
            item[session] = member['overallRanking']['totalPoints']

            for season in member['seasonRankings']:
                if season['seasonYear'] == year:
                    item[season['seasonYear']]= season['totalPoints']

            
            
            is_file_exist = os.path.exists(f'country/country_coef_saison_{year}.csv')
            is_folder_exist = os.path.exists(os.path.join(os.getcwd(),'country'))
            if not is_folder_exist:
                try:
                    os.mkdir(os.path.join(os.getcwd(),'country'))
                except:
                    print('Directory creation error . continuing ..')    
            with open(f'country/country_coef_saison_{year}.csv','a',encoding='utf8',newline='') as fle:
                writer = csv.DictWriter(fle,delimiter=';',fieldnames=['id_country','country',year,session])
                if not is_file_exist:
                    writer.writeheader()
                writer.writerow(item)
        time.sleep(4)


def process():
    print("Merging all files to single file ")
    filelist = glob.glob('./country/*.csv')
    merged_df = pd.read_csv(filelist[0],delimiter=';')

    for filename in filelist:
        df = pd.read_csv(filename,delimiter=';')
        merged_df = pd.merge(merged_df, df, how = 'outer')

    merged_df['last_updated'] = datetime.datetime.today().strftime('%d/%m/%Y')
    merged_df.to_csv('./country/Final_country_coef_2010-2023.csv',sep=';',index=False)

if __name__ == '__main__':
    if os.path.exists(os.path.join(os.getcwd(),'country')):
        os.rename(os.path.join(os.getcwd(),'country'),os.path.join(os.getcwd(),f"country_backup_{datetime.datetime.today().strftime('%d-%m-%Y%H%M%S')}"))
    scrap()
    process()    