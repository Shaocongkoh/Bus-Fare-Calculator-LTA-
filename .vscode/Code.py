# Get fare fees from data.gov website
import pandas as pd

fare_list=pd.read_csv('fares-for-mrt-and-lrt-effective-from-28-december-2019.csv')

fare_list.info() #no na values; clean data file
fare_list.head()

# Get bus-routes from LTA Data Mall API
# Problems faced: API responses returned are limited to only 500 records of the dataset per call (To circumvent this, used a While loop
url='http://datamall2.mytransport.sg/ltaodataservice/BusServices'

results =requests.get(url, 
            headers=headers).json()['value']  

print(len(results)) # Verify if really just 500 records

import requests

headers = { 'AccountKey': 'XXXX','accept': 'application/json'}

resp=requests.get('http://datamall2.mytransport.sg/ltaodataservice/BusServices', headers=headers)
print(resp.status_code)

result= resp.json() #use Json to get dictionary
result 

# Define a function to return all results instead of just 500 records
def fetch_all(url):
    results = []
    while True:
        new_results =requests.get(url, 
            headers=headers,
            params={'$skip': (len(results)-1)}
        ).json()['value']
        if new_results == []:
            break
        else:
            results += new_results
    return results

print(len(new_results))

