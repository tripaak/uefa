import requests
import csv
import os
import time
import datetime


def scrap(start_year,end_year):
    if start_year == end_year:
        flag = start_year
    else:
        flag = 'tous'    


    for year in range(start_year,end_year+1):
        print(f"Scraping for year : {year}")

        url = f"https://comp.uefa.com/v2/coefficients?coefficientType=MEN_CLUB&coefficientRange=OVERALL&seasonYear={year}&page=1&pagesize=500&language=EN"

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

        response = response.json()
        data = response['data']['members']

        for member in data:
            item = {}
            item['team_UEFA'] = member['member']['displayOfficialName']
            item['team_id_UEFA'] = member['member']['id']
            item['country_UEFA'] = member['member']['countryName']
            item['Note_UEFA'] = member['overallRanking']['totalPoints']
            item['seasonId']= year-1
            item['seasonName']= f"{year-1}-{year}"
            item['last_updated_UEFA'] = datetime.datetime.today().strftime('%d/%m/%Y')
            item['coef_UEFA'] = None
            
            for season in member['seasonRankings']:
                if season['seasonYear'] == year:
                    item['coef_UEFA'] = season['totalPoints']

            is_file_exist = os.path.exists(f"club/club_coef_{flag}_{datetime.datetime.today().strftime('%d-%m-%Y')}.csv")
            is_folder_exist = os.path.exists(os.path.join(os.getcwd(),'club'))

            if not is_folder_exist:
                try:
                    os.mkdir(os.path.join(os.getcwd(),'club'))
                except:
                    print('Directory creation error . continuing ..') 

            with open(f"club/club_coef_{flag}_{datetime.datetime.today().strftime('%d-%m-%Y')}.csv",'a',encoding='utf8',newline='') as fle:
                writer = csv.DictWriter(fle,delimiter=';',fieldnames=['seasonId','seasonName','coef_UEFA','Note_UEFA','team_id_UEFA','team_UEFA','country_UEFA','last_updated_UEFA'])
                if not is_file_exist:
                    writer.writeheader()
                writer.writerow(item)   
        time.sleep(4) 
        

if __name__ == '__main__':
    if os.path.exists(os.path.join(os.getcwd(),'club')):
        print("Sauvegarde d'un ancien dossier" )
        os.rename(os.path.join(os.getcwd(),'club'),os.path.join(os.getcwd(),f"club_backup_{datetime.datetime.today().strftime('%d-%m-%Y.%H%M%S')}"))
    
    print("Choix de l'opération: \n")
    print(" 1 - Extraction de toutes les données \n")
    print(" 2 - Extraction des données pour une année spécifique \n")
    
    choice = ["-1"]
    while choice not in ["1","2"]:
        choice =input("Entrez le choix de l'opération : ")
    if choice=="1":
        start_year = 2010
        end_year = 2023
        scrap(start_year,end_year)
    elif choice=="2":
        start_year = int(input("Indiquer l'année: "))
        end_year = start_year
        scrap(start_year,end_year)
