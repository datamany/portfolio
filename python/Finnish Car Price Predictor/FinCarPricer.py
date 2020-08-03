#Loading all libraries
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time
import random
from IPython.display import clear_output
import string
import numpy as np
from sklearn.preprocessing import StandardScaler
from tabulate import tabulate
import re
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


# Collecting variable from user
#make = 'Audi'
def main_block_user_data():
    print("Hi there, please specify the parameters of your car \nand we will make the price prediction based on real market data in Finland\n")
    make = input ('Car Manufacture (ex.: Audi, Toyota):')
    make = ''.join (re.split (r'\W+',make)[0]).title()
    #clear_output()
    #model = 'q15'
    
    model = input ('Car Model:')
    model = '-'.join (re.split (r'\W+',model)).title()
    #clear_output()
    #year = 2015
    print('Car year')
    year = str(1)
    while (not year.isdigit() or int(year)<1900 or int(year)>2030):
        #clear_output()
        #print('Car year')
        year = input ('write year between 1900 and 2030:')
    #clear_output()
    #gear_box = ['Automatti','Manuaali']
    
    print ("Car Mileage (km)")
    mileage = 'f'
    while not mileage.isdigit():
        #clear_output()
        #print ("Car Mileage (km)")
        mileage = input('Write mileage as a whole number in km (ex.:250200)')
    
    print ("Engine size")
    eng_size = 'h'
    while re.match(r'^-?\d+(?:\.\d+)?$', eng_size) is None:
        #clear_output()
        #print ("Engine size")
        eng_size = input ('Write in decimals(ex.: 1.2, 2.0...)')
    eng_size = round(float(eng_size),1)
   
    gear_box = None
    print('Gear box')
    while gear_box not in ['1','2']:
        #clear_output()
        #print('Gear box')
        gear_box = input (' Write 1 or 2:\n 1.Automatti \n 2.Manuaali')  
    gear_box = ['Automatti','Manuaali'][int(gear_box)-1]
    #clear_output()
    #fuel = ['Bensiini', 'Deiesel','Hybridi', 'Sähkö', 'Kaasu', 'E85/bensiini']
    
    fuel =None
    print("Fuel Type")
    while fuel not in list('123456'):
        #clear_output()
        #print("Fuel Type")
        fuel  = input(" Write Number from 1 to 6:\n 1.Bensiini \n 2.Diesel\n 3.Hybridi\n 4.Sähkö\n 5.Kaasu\n 6.E85/bensiini")
    fuel = ['Bensiini', 'Diesel','Hybridi', 'Sähkö', 'Kaasu', 'E85/bensiini'][int(fuel)-1]
    clear_output()
    request_info = f'Your request: \n Make: {make} \n Model: {model} \n Year: {year} \n Mileage: {mileage} km \n Engine size: {eng_size} \n Gear Box: {gear_box} \n Fuel Type: {fuel}'
    print(request_info)
    return request_info,make,model,year,mileage,gear_box,fuel,eng_size;


def user_data_collector():
    request_info,make,model,year,mileage,gear_box,fuel,eng_size = main_block_user_data()
    print('\nDo you want to make changes to your request?')
    repeat = 'h'
    while repeat.lower() not in ['yes', 'no']:
        #print('Do you want to make changes to your request?')
        repeat =input ('Please write "yes" or "no"')
    while repeat == 'yes':
        clear_output()
        request_info,make,model,year,mileage,gear_box,fuel,eng_size = main_block_user_data()
        repeat = 'h'
        print('\nDo you want to make changes to your request?')
        while repeat.lower() not in ['yes', 'no']:
            repeat =input ('Please write "yes" or "no"')
        #for name in [request_info,make,model,year,mileage,gear_box,fuel,eng_size]:
        #    del globals()[name]
                
    if repeat == 'no':
        #clear_output()
        print("\nAlrigth, then we will estimate the price based on your car specifications")
        return request_info,make,model,year,mileage,gear_box,fuel,eng_size;


# form a link
def link_form (make,model,year):
    year_from = str(int(year)-2)
    year_to = str(int(year)+2)
    link = 'https://www.nettiauto.com/'+make+'/'+model+'/?yfrom='+year_from+'&yto='+year_to+'&id_country[]=73'
    return link


def alert_check(link):
    #link = link_form()
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')
    if len(soup.find_all('div', id='msg'))>0 or soup.find_all('h1')[0].text == 'Hups, sivua ei löytynyt':
        alert = 1
    else:
        alert = 0
    return alert


def user_request_processing():
    request_info,make,model,year,mileage,gear_box,fuel,eng_size =user_data_collector()
    link = link_form(make,model,year)
    alert = alert_check(link)
    while alert==1:
        print("Sorry, we could not find any data based on your request\n")
        print(request_info)
        print("\nPlease make sure there is no spelling errors")
        print("\nWould you like to make a new request or exit from session?")
        answer = None
        while answer not in ('1','2'):
            print("Would you like to make a new request or exit from session?")
            answer = input("\n1.Make new request \n2. Exit from session")
        if answer == '1':
            clear_output()
            request_info,make,model,year,mileage,gear_box,fuel,eng_size =user_data_collector()
            link = link_form(make,model,year)
            alert = alert_check(link)
        if answer == '2':
            print('Alrigth, come back next time.')
            break
    if alert==0:
        print('\nWe found the data based on your request, so now please chill and relax, soon we will get back with estimated price.')
        return request_info,make,model,year,mileage,gear_box,fuel,eng_size, link;


# code for scraping 
def scrapper(link,make,model,year,mileage,eng_size,gear_box,fuel):
#link = 'https://www.nettiauto.com/toyota/corolla?id_country[]=73&page=1'
    sleep_period = 4
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')
    try:
        last_page_to_scrap = int(soup.find_all(class_="pageNavigation dot_block")[-1].text)
    except IndexError:
        try:
            last_page_to_scrap = int(soup.find_all(class_="pageNavigation")[-2].text)
        except:
            last_page_to_scrap =1

    #lists 
    car_id_ls = []
    make_ls = []
    mileage_ls = []
    model_ls = []
    year_ls = []
    car_type_ls = []
    price_ls = []
    eng_size_ls = []
    gear_box_ls = []
    fuel_ls = []
    loc_town_ls=[]
    link_ls = []


    for i in range(1,last_page_to_scrap+1):
        #link = 'https://www.nettiauto.com/toyota/corolla?id_country[]=73&page='+str(i)
        link = link+'&page='+str(i)
        page = requests.get(link)
        soup = BeautifulSoup(page.text, 'html.parser')
        blocks = soup.find_all(class_= re.compile("^listingVifUrl"))
        for block in blocks:
            bl1_part = block.find(class_= re.compile("^childVifUrl"))
            keys = list(bl1_part.attrs.keys())

            car_id_ls.append(bl1_part['data-id'] if 'data-id' in keys else None)
            make_ls.append(bl1_part['data-make'] if 'data-make' in keys else None)
            mileage_ls.append(bl1_part['data-mileage'] if 'data-mileage' in keys else None)
            model_ls.append(bl1_part['data-model'] if 'data-model' in keys else None)
            year_ls.append(bl1_part['data-year'] if 'data-year' in keys else None)
            car_type_ls.append(bl1_part['data-vtype'] if 'data-vtype' in keys else None)
            price_ls.append(bl1_part['data-price'] if 'data-price' in keys else None)
            link_ls.append(bl1_part['href'] if 'href' in keys else None)

            eng_size_ls.append(float(re.findall(r"[-+]?\d*\.\d+|\d+", block.find(class_="eng_size").text)[0]) if len(block.find(class_="eng_size").text)>0 else None)
            loc_town_ls.append(block.find('b', class_="gray_text").text.translate(str.maketrans('', '', string.punctuation+' '+'›')).replace('\n','') if len(block.find('b', class_="gray_text").text)>0 else None)
            gear_and_fuel_block = block.find('div', class_=re.compile('^vehicle_other_info clearfix_nett')).ul.find_all('li')
            fuel_ls.append(gear_and_fuel_block[2].text if len(gear_and_fuel_block)>=4 else None)
            gear_box_ls.append(gear_and_fuel_block[3].text if len(gear_and_fuel_block)>=4 else None)
            clear_output()
            print("Cars' data loaded:", len(car_id_ls))
            print('Pages loaded:', i)
            print('Pages left:', (last_page_to_scrap)-i)
        if i % sleep_period ==0:
            time.sleep(random.randint(1,2))
            sleep_period = random.randint(2,6)
#     df_scraped = pd.DataFrame({'car_id':car_id_ls,'make':make_ls,'model': model_ls, 'milage':mileage_ls
#                        ,'year':year_ls, 'car_type':car_type_ls, 'price':price_ls, 'eng_size':eng_size_ls,
#                       'gear_box': gear_box_ls,'fuel': fuel_ls, 'loc_town':loc_town_ls,'link': link_ls})
#     df_scraped = df_scraped.fillna(method = 'bfill')
#     df_scraped['eng_size'] = df_scraped['eng_size'].astype(float)
#     df_scraped = df_scraped.dropna(axis= 0, how = 'any')
#     df_scraped = df_scraped[df_scraped['price'] >0]
    #df_scraped.to_csv(f'{make}_{model}_{year}_{eng_size}_{mileage}_{gear_box}_{fuel}_table.csv', index = False)
    print('Data loading has completed')
    return car_id_ls,make_ls,model_ls,mileage_ls,year_ls,car_type_ls,price_ls,eng_size_ls,gear_box_ls,fuel_ls,loc_town_ls,link_ls



def df_creation (car_id_ls,make_ls,model_ls,mileage_ls,year_ls,car_type_ls,price_ls,eng_size_ls,gear_box_ls,fuel_ls,loc_town_ls,link_ls):
    df_scraped = pd.DataFrame({'car_id':car_id_ls,'make':make_ls,'model': model_ls, 'milage':mileage_ls
                       ,'year':year_ls, 'car_type':car_type_ls, 'price':price_ls, 'eng_size':eng_size_ls,
                      'gear_box': gear_box_ls,'fuel': fuel_ls, 'loc_town':loc_town_ls,'link': link_ls})
    df_scraped = df_scraped.fillna(method = 'bfill')
    df_scraped['eng_size'] = df_scraped['eng_size'].astype(float)
    df_scraped = df_scraped.dropna(axis= 0, how = 'any')
    df_scraped['price'] = df_scraped['price'].astype(int)#.apply(lambda x: int(x) if x is not None else x)
    df_scraped = df_scraped[df_scraped['price'] >0]
    #df_scraped.to_csv(f'{make}_{model}_{year}_{eng_size}_{mileage}_{gear_box}_{fuel}_table.csv', index = False)
    print('Data Frame created')
    return df_scraped



def creat_ML_dfs (df_scraped,mileage,year,eng_size,gear_box,fuel):
    df_scraped_for_ml = df_scraped[['milage', 'year','eng_size','gear_box','fuel', 'price']]
    df_user = pd.DataFrame({'milage': mileage, 'year': year, 'eng_size': eng_size, 'gear_box': gear_box, 'fuel': fuel, 'price':None }, index = [0])
    df_ml_user_data_in = df_scraped_for_ml.append(df_user, ignore_index = True )
    
    
    df_ml_user_data_in['milage']= df_ml_user_data_in['milage'].astype(int)
    df_ml_user_data_in['year']= df_ml_user_data_in['year'].astype(int)
    #Encoding categorical variables
    df_ml_user_data_in['gear_box_num'] = df_ml_user_data_in.gear_box.astype('category').cat.codes
    df_ml_user_data_in['fuel_num'] = df_ml_user_data_in.fuel.astype('category').cat.codes
    return df_ml_user_data_in



def train_and_test_split_scale(df_ml_user_data_in):
    from sklearn.preprocessing import StandardScaler
    # transforming outliers to mean
    df_out = df_ml_user_data_in[df_ml_user_data_in.columns]
    #df_out['price'] = df_out['price'].apply(lambda x: int(x) if x is not None else x)
    func = lambda x : np.where(x == x.max(), x.mean(), x)
    df_out['price'] = df_out.groupby('year')['price'].transform(func)
    #df_out['price'] = df_out.groupby('year')['price'].transform(func)
    #df_out['price'] = df_out.groupby('year')['price'].transform(func)
    
    X = df_out.iloc[:-1,:][['milage', 'year', 'eng_size','gear_box_num', 'fuel_num']]
    y = df_out.iloc[:-1,:][['price']]
    
    #for kNeighbours
    X_train_knn = df_ml_user_data_in.iloc[:-1,:][['milage', 'year', 'eng_size','gear_box_num', 'fuel_num','price']]

    X_predict_not_transformed = df_ml_user_data_in.iloc[-1,:][['milage', 'year', 'eng_size','gear_box_num', 'fuel_num']].tolist()

    #Scaling
        #for GradientBoostingRegressor
    sc = StandardScaler().fit(X)
    #X_train = sc.transform(X_train)
    #y_train = sc.transform(y_train)
    X_predict = sc.transform([X_predict_not_transformed])
            #for knn
    sc = StandardScaler().fit(X_train_knn)
    X_train_knn = sc.transform(X_train_knn)
    return X, y, X_predict, X_train_knn,X_predict_not_transformed, sc;

def Prediction_ML(X, y, X_predict):
    from sklearn import metrics
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size  =0.1)
    sc = StandardScaler().fit(X_train)
    X_train = sc.transform(X_train)
    X_test = sc.transform(X_test)

    from sklearn.neighbors import KNeighborsRegressor
    import warnings
    from math import sqrt
    warnings.warn('my warning')
    error_rate = []
    # Will take some time
    for i in range(1,40):
        knn = KNeighborsRegressor(n_neighbors=i)
        knn.fit(X_train,y_train)
        pred_i = knn.predict(X_test)
        error_rate.append(sqrt(metrics.mean_squared_error(y_test, pred_i)))
    optimal_k = error_rate.index(min(error_rate))+1
    # Make predictions with best k
    sc = StandardScaler().fit(X)
    X_scaled = sc.transform(X)

    knn = KNeighborsRegressor(n_neighbors=optimal_k, weights = 'uniform')
    knn.fit(X_scaled,y)
    predict_value = knn.predict(X_predict)[0][0]
    predict_value = int(round(predict_value))
    predict_value = (predict_value-100)//100*100+100
    return predict_value


def most_similar_ads(X_train_knn, X_predict_not_transformed,predict_value,sc):
    from sklearn.neighbors import NearestNeighbors
    value_to_predict = [X_predict_not_transformed +[predict_value]]
    value_to_predict_scaled = sc.transform(value_to_predict)
    neigh = NearestNeighbors(n_neighbors=5)
    neigh.fit(X_train_knn)
    neigh_indexes = neigh.kneighbors(value_to_predict_scaled,return_distance=False)[0]
    return neigh_indexes



def output (df_scraped,predict_value,request_info,neigh_indexes):
    from tabulate import tabulate
    output_df = df_scraped.iloc[:-1,1:].loc[neigh_indexes.tolist(),:].reset_index(drop = True)
    print('Estimated price for your car:',predict_value,'€\n' )
    print(request_info,'\n\n')
    print('Simillar cars to your request\n')
    print(tabulate(output_df,headers='keys', showindex = 'not'))


def main_script():
    # collecting user data
    request_info,make,model,year,mileage,gear_box,fuel,eng_size, link = user_request_processing()
    # scrapping 
    car_id_ls,make_ls,model_ls,mileage_ls,year_ls,car_type_ls,price_ls,eng_size_ls,gear_box_ls,fuel_ls,loc_town_ls,link_ls = scrapper(link,make,model,year,mileage,eng_size,gear_box,fuel)
    # Creating df
    df_scraped = df_creation (car_id_ls,make_ls,model_ls,mileage_ls,year_ls,car_type_ls,price_ls,eng_size_ls,gear_box_ls,fuel_ls,loc_town_ls,link_ls)
    # creating ml df
    df_ml_user_data_in = creat_ML_dfs (df_scraped,mileage,year,eng_size,gear_box,fuel)
    #data split for ml
    X, y, X_predict, X_train_knn,X_predict_not_transformed, sc = train_and_test_split_scale(df_ml_user_data_in)
    #Knn alg approach
    predict_value = Prediction_ML(X, y, X_predict)
    # finding neighbors index numbers
    neigh_indexes = most_similar_ads(X_train_knn, X_predict_not_transformed,predict_value,sc)
    # Creating the report
    output (df_scraped,predict_value,request_info,neigh_indexes)

# Final question exit or make new request
def car_pricer():
    main_script()
    end_response = None
    print('Would you like to make another request?')
    while end_response not in ('1','2'):
        #print('Would you like to make another request?')
        end_response = input('Plese write 1 or 2 \n1.No, exit the program \n2.Yes,please')
    while end_response == '2':
        clear_output()
        main_script()
        end_response = None
        print('\n\n\nWould you like to make another request?')
        while end_response not in ('1','2'):
            #print('Would you like to make another request?')
            end_response = input('\nPlese write 1 or 2 \n1.No, exit the program \n2.Yes,please')
        if end_response == '1':
            #clear_output()
            print('\nAlrigth, see you next time.')
            break  