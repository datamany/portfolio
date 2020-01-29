import json
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
import sys
import random
from random import randint
import pandas as pd
from IPython.display import clear_output
from time import sleep
import os.path

def chose_proxy(pr_num):
    proxy_df = pd.read_csv('proxy.csv')
    chose_proxy.PROXY_HOST = str(proxy_df.PROXY_HOST[pr_num])
    chose_proxy.PROXY_PORT = str(proxy_df.PROXY_PORT[pr_num])
    chose_proxy.USERNAME = str(proxy_df.USERNAME[pr_num])
    chose_proxy.PASSWORD = str(proxy_df.PASSWORD[pr_num])
    
    chose_proxy.http = "http://"+chose_proxy.USERNAME+":"+chose_proxy.PASSWORD+"@"+chose_proxy.PROXY_HOST+":"+chose_proxy.PROXY_PORT+"/"
    chose_proxy.https = "https://"+chose_proxy.USERNAME+":"+chose_proxy.PASSWORD+"@"+chose_proxy.PROXY_HOST+":"+chose_proxy.PROXY_PORT+"/"
    chose_proxy.proxies = {"http": chose_proxy.http,"https": chose_proxy.https}
    print(f'{chose_proxy.PROXY_PORT}:{chose_proxy.PROXY_HOST}')
    
#Body function
def easy_scrap_dicti(country_num, links_amt=None,proxy_onn_off = 0 ):

#country_num, links_amt,proxy_onn_off= 4, 40,1

    """
    country_num - index number of of a cell from top_25_countries appeared as a flag for country to work with
    links_amt - amount of links to scrap at one session
    proxy_onn_off - to turn on proxy put "1"
    """
    if proxy_onn_off == 1:
        proxy = chose_proxy.proxies
    else:
        proxy = None

    #list block
    id_lst = []
    dicti = []
    indexes_to_scrap = []
    indexes_scraped = []

    #opening data frames 1)countries to scrap 2)table to scrap
    countries_25_df = pd.read_csv('top_25_countries_data.csv')
    df_to_scrap = pd.read_csv('tables/lists/df_glassdoor_'+countries_25_df.City[country_num]+'_jobs_list.csv')[['id','job_link']]

    #pauses
    f_stop = randint(20,25)
    s_stop = randint(35,50)
    t_stop = randint(120, 160)

    headers = {'user-agent': UserAgent().random}
    print(headers)
    #response = requests.get(,headers=headers)
    if os.path.isfile('tables/dictionaries/df_glassdoor_'+countries_25_df.City[country_num]+'_jobs_dict.csv') is True:
        temp_dict_df = pd.read_csv('tables/dictionaries/df_glassdoor_'+countries_25_df.City[country_num]+'_jobs_dict.csv')
        for i in list(df_to_scrap.id):
            if i not in list(temp_dict_df.id):
                indexes_to_scrap.append(df_to_scrap[df_to_scrap.id == i].index[0])
            else:
                indexes_scraped.append(df_to_scrap[df_to_scrap.id == i].index[0])
    else:
        indexes_to_scrap = list(df_to_scrap.index.values)

    try:    #indexes_to_scrap = list(df_to_scrap.index.values)[:links_amt]
        for i in indexes_to_scrap[:links_amt]:
            try:
                #if df_to_scrap.id[i] not in list(temp_dict_df.id):
                response = requests.get(df_to_scrap.job_link[i],headers=headers, proxies = proxy)
                soup = BeautifulSoup(response.content, "html.parser")

                a = soup.find('div',class_='pageContentWrapper').find('script').text
                start =a.find('{')
                js_dict = json.loads(a[start:],strict = False)
                dicti.append(js_dict)

                link = js_dict['url']
                id_lst.append(int(link[link.find('jl=')+len('jl='):]))


                #id_lst.append(js_dict['urlData']['params']['jl'])

                #df_to_scrap.at[i,'scraped']='yes'

                clear_output()
                print(f'Scraping country:{countries_25_df.City[country_num]}')
                print(f'Links scraped:{len(id_lst)}/{(len(indexes_to_scrap[:links_amt]))}')
                print(f'Overall scraped links: {len(indexes_scraped)+len(id_lst)}/{len(df_to_scrap)}')

                if (indexes_to_scrap.index(i) % 27 ) == 0:
                    sleep(randint(1,2))
                    print('sleep now')
                elif (indexes_to_scrap.index(i) % 169 ) == 0:
                    print('sleep now 2')
                    sleep(randint(3,5))
                elif (indexes_to_scrap.index(i) % 315 ) == 0:
                    print('sleep now 3')
                    sleep(randint(10,20))
                    headers = {'user-agent': UserAgent().random}


            except AttributeError:
                #headers = {'user-agent': UserAgent().random}
                sleep(randint(2,3))
                continue
            except:
                headers = {'user-agent': UserAgent().random}
                sleep(randint(3,4))
                pass
    finally:
        df_link_scrap = pd.DataFrame({
            'id': id_lst,
            'dictionary': dicti
        })

        #df_to_scrap.to_csv('tables/lists/df_glassdoor_'+countries_25_df.City[country_num]+'_jobs_list.csv', index = False)
        #incr load
        if os.path.isfile('tables/dictionaries/df_glassdoor_'+countries_25_df.City[country_num]+'_jobs_dict.csv') is True:
            prev_scraped_dict= pd.read_csv('tables/dictionaries/df_glassdoor_'+countries_25_df.City[country_num]+'_jobs_dict.csv')
            #df_link_scrap.drop_duplicates(subset = 'id',keep='first', inplace = True)
            updated_merged_dict =pd.concat([prev_scraped_dict,df_link_scrap])
            updated_merged_dict.to_csv('tables/dictionaries/df_glassdoor_'+countries_25_df.City[country_num]+'_jobs_dict.csv', index = False)
        else:
            df_link_scrap.drop_duplicates(subset = 'id',keep='first', inplace = True)
            df_link_scrap.to_csv('tables/dictionaries/df_glassdoor_'+countries_25_df.City[country_num]+'_jobs_dict.csv', index = False)
        print('Tables saved')