The project attempts to give the estimated price of a car based on the real time data on the Finnish market.
 Process:
1. Acquiring the data from the user (Make, Model, Year,Mileage, Fuel Type, Engine size) 
2. Aggregate (crawl) the data from the local Finnish car sale platform
3. Process the collected data
4. Predict the price by approaching KNN algorithm with the best No of K for individual case
5. Return the estimated price and 5 similar car ads that are close to the user's specifications 
