import time
from time import sleep
import datetime
from random import randint
import random

from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
#from IPython.display import clear_output
import pandas as pd
import os.path

from IPython.display import clear_output
import timeit
#import threading
#from threading import Thread
import timeit
import substring
from bs4 import BeautifulSoup



## Chrome setup

### Set proxy & user agent


# Pass
def chose_proxy(pr_num):
    proxy_df = pd.read_csv('proxy.csv')
    chose_proxy.PROXY_HOST = str(proxy_df.PROXY_HOST[pr_num])
    chose_proxy.PROXY_PORT = str(proxy_df.PROXY_PORT[pr_num])
    chose_proxy.USERNAME = str(proxy_df.USERNAME[pr_num])
    chose_proxy.PASSWORD = str(proxy_df.PASSWORD[pr_num])

### User Agent setup

#https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=data&sc.keyword=data&locT=&locId=&jobType=
     
def user_set():
#Creating User agent
    options = webdriver.ChromeOptions() #Options()
    
    #Turn of image load and specifying cache size
    prefs={"profile.managed_default_content_settings.images": 2, 'disk-cache-size': 4096 }
    options.add_experimental_option('prefs', prefs)
    
    ua = UserAgent()
    userAgent = ua.random
    print(userAgent)
    print(f'{chose_proxy.PROXY_HOST}:{chose_proxy.PROXY_PORT}')
    
    options.add_argument('--headless')
    options.add_argument('--disable-gpu') 
    
    options.add_argument('--proxy-server={}'.format(chose_proxy.PROXY_HOST + ":" + chose_proxy.PROXY_PORT))
    options.add_argument(f'user-agent={userAgent}')
    user_set.browser = webdriver.Chrome(options=options, executable_path='chromedriver.exe')

## Creating lists

def job_lists(page_amt):   
    #page_amt=1
    job_lists.job_id_lst = []
    job_lists.company_name_lst = []
    job_lists.job_titile_lst =[]
    job_lists.location_lst = []
    job_lists.job_cat_list = []
    job_lists.salary_lst = []
    job_lists.loaded_time_lst = []
    job_lists.job_links_list=[]
    job_lists.search_page_list = []
    job_lists.total_pages_per_session = []
    
    
    timelist = [1.3,1.4,1.5,1.7,1.8,2.1,2.3,2.4,2.5,2.6]
    for i in range(page_amt):
        current_page = user_set.browser.current_url
        
        register = user_set.browser.find_elements_by_xpath("//div[@class='ModalStyle__xBtn___29PT9']")
        Accept_cookies= user_set.browser.find_elements_by_id('_evidon-accept-button')
        job_alert_box = user_set.browser.find_elements_by_class_name('ModalStyle__xBtn___34qya')

        if len(register)>0:
            sleep(randint(1,3))
            register[0].click()
        if len(Accept_cookies)>0:
            time.sleep(randint(1,4))
            Accept_cookies[0].click()
        if len(job_alert_box)>0:
            time.sleep(randint(2,4))
            job_alert_box[0].click()
        else:
            sleep(randint(2,4))
            soup = BeautifulSoup(user_set.browser.page_source, 'html.parser')
             #Extracting the containers
            containers = soup.find_all('li', class_='jl')
        try:
            for i in range(len(containers)):
                register = user_set.browser.find_elements_by_xpath("//div[@class='ModalStyle__xBtn___29PT9']")
                if len(register)>0:
                    time.sleep (2)
                    register[0].click()


                id = containers[i]['data-id']
                job_lists.job_id_lst.append(id)

                #company_name
                company_name_loc_text = containers[i].find("div", class_="jobContainer").div.div.text
                job_lists.company_name_lst.append(company_name_loc_text)

                #Job_title
                job_title_name = containers[i].find_all('a')[2].text
                job_lists.job_titile_lst.append(job_title_name)

                # City and State
                city_and_state = containers[i]['data-job-loc']
                job_lists.location_lst.append(city_and_state)


                #Job Category 
                job_cat_names = containers[i]["data-normalize-job-title"]
                job_lists.job_cat_list.append(job_cat_names)

                #Salaries
                salary_i_list = containers[i].find_all('span' ,class_='salaryText')
                if len(salary_i_list) > 0:
                    sal_value = salary_i_list[0].text
                    job_lists.salary_lst.append(sal_value)
                else:
                    job_lists.salary_lst.append('NaN')

                time_loaded = datetime.datetime.now()
                job_lists.loaded_time_lst.append (time_loaded)

                link = soup.find_all('div', class_='logoWrap')[i].find('a')['href']
                link = 'https://www.glassdoor.com'+link
                job_lists.job_links_list.append(link)

                page_current = soup.find_all('li',class_='page current')
                if len(page_current)>0:
                    page_current = soup.find('li', class_= 'page current').text
                    job_lists.search_page_list.append(page_current)
                else:
                    job_lists.search_page_list.append('1')

                total_pages_per_session = soup.find('div', class_='cell middle hideMob padVertSm').text.partition('of ')[-1:][0]
                job_lists.total_pages_per_session.append(total_pages_per_session)

            clear_output()
            print(f'Location: {job_lists.location_lst[i]}')
            print(f'jobs scraped: {len(job_lists.job_id_lst)}')
            print(f'Total pages: {total_pages_per_session}')
            print(f'Search_page: {page_current}')

            if len(user_set.browser.find_elements_by_class_name('page.current.last'))>0:
                    break

            if len(user_set.browser.find_elements_by_class_name('next'))>0:
                job_containers = user_set.browser.find_elements_by_xpath("//li[@class='jl']")
                job_containers[randint(0,len(job_containers))].click()
                register = user_set.browser.find_elements_by_xpath("//div[@class='ModalStyle__xBtn___29PT9']")
                sleep(3)
                if len(register)>0:
                    time.sleep (1)
                    register[0].click()
                sleep(random.choice(timelist))

                job_lists.prev_page = user_set.browser.find_element_by_class_name('next').find_element_by_css_selector("a").get_attribute('href')
                job_lists.next_page = user_set.browser.find_element_by_class_name('next')
                job_lists.next_page.click()
                #user_set.browser.implicitly_wait(10)
                sleep(randint(2,4))
            else:
                break
            if user_set.browser.find_element_by_css_selector("h1").text == "Sorry, we can't find that page.":
                break     
        except NoSuchElementException:
            user_set.browser.refresh()
            sleep(13)
            #user_set.browser.implicity_wait(20)
            continue
        except:
            user_set.browser.quit()
            print(f"Restart page: {current_page}")
            sleep(randint(2,3))
            user_set()
            sleep(randint(12,15))
            user_set.browser.get(current_page)
            continue  

def df_create():    
    df_create.glassdoor_jobs = pd.DataFrame({
                    'id': pd.Series(job_lists.job_id_lst),
                    'job_title': pd.Series(job_lists.job_titile_lst),
                    'job_category': pd.Series(job_lists.job_cat_list),
                    'company_name':pd.Series(job_lists.company_name_lst), 
                    'salary':pd.Series(job_lists.salary_lst),
                    'city_and_state': pd.Series(job_lists.location_lst),
                    'job_link': pd.Series(job_lists.job_links_list),
                    'loaded_time': pd.Series(job_lists.loaded_time_lst),
                    'page_in_search': pd.Series(job_lists.search_page_list),
                    'tota_pages_per_session': pd.Series(job_lists.total_pages_per_session)
    })


def df_save(country_name):
    country_name = df_save.country_name
    if os.path.isfile('tables/lists/df_glassdoor_'+df_save.country_name+'_jobs_list.csv') is True:
        print("file in folder, then load is increment")
        df_create.glassdoor_jobs.drop_duplicates(subset = 'id',keep='last', inplace = True)
        prev_ver = pd.read_csv('tables/lists/df_glassdoor_'+df_save.country_name+'_jobs_list.csv')
        prev_ver.drop_duplicates(subset = 'id',keep='last', inplace = True)
        updated_merged =pd.concat([prev_ver,df_create.glassdoor_jobs])
        updated_merged.drop_duplicates(subset = 'id',keep='last', inplace = True)
        updated_merged.to_csv('tables/lists/df_glassdoor_'+df_save.country_name+'_jobs_list.csv', index= False)
        print ('sucesfully saved')
    else:
        file_name = 'tables/lists/df_glassdoor_'+df_save.country_name+'_jobs_list.csv'
        df_create.glassdoor_jobs.drop_duplicates(subset = 'id',keep='last', inplace = True)
        df_create.glassdoor_jobs.to_csv('tables/lists/df_glassdoor_'+df_save.country_name+'_jobs_list.csv', index= False)
        print(f'new file {file_name} in project folder')

def save_overall(country_name):
    df_save.country_name=country_name
    df_create()
    df_save(country_name)
    
def easy_scrap_lists(country_num,pr_num='', link='',  a="&fromAge=1"):
    
    """
    - add this symbol to load data published for particular period: "&fromAge=1"
    - country_num is the index number of element from 25 countries 
    - proxy_number is the location of element from proxy.csv
    """
    country_num = int(country_num)
    chose_proxy(pr_num = pr_num)
    user_set()
    countries_25_df = pd.read_csv('top_25_countries_data.csv')
    #easy_scrap_lists.link = link
    if len(link)>0:
        easy_scrap_lists.load_link = user_set.browser.get(link)
        
    else:
        easy_scrap_lists.load_link = user_set.browser.get(countries_25_df.link_data[country_num]+a)
    easy_scrap_lists.load_link
    
    job_lists(page_amt = 45)      
    print('Saiving')
    save_overall(countries_25_df.City[country_num])
    user_set.browser.quit() 
    print('All saved')