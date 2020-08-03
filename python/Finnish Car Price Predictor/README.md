The project attempts to give the estimated price of a car based on the real time data on the Finnish market.

Process:
1. Acquire the car specifications from the user (Make, Model, Year,Mileage, Fuel Type, Engine size) 
2. Aggregate (crawl) the data from the local Finnish car sale platform
3. Process the collected data
4. Predict the price by approaching KNN algorithm with the best No of K for individual case
5. Return the estimated price and 5 similar car ads that are close to the user's specifications 


The brief Descriptive analysis and model selection process could be explored from the file named: 'carPricePrediction_Descriptive_analaysis_and_data_modelling.ipynb'

The example of a function output could be checked in 'Example of Car pricer.ipynb'

The function itself is stored in 'carPricePrediction.ipynb' file.

How to use:
1. Install 'carPricePrediction.ipynb' and make sure all necessary libraries are installed.
Library list:
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

2. Run function named 'car_pricer()' and follow the script by providing input data.

Note:  The script creator is not responsible how the user will use the provided code.
