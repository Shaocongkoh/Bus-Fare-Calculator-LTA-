# Get fare fees from data.gov website
import pandas as pd

fare_list=pd.read_csv('fares-for-mrt-and-lrt-effective-from-28-december-2019.csv')

fare_list.info() # no na values; clean data file
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

result= resp.json() # use Json to get dictionary
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

# Get Bus Routes
routes = fetch_all("http://datamall2.mytransport.sg/ltaodataservice/BusRoutes")
routes[0].keys()
bus_route=[r for r in routes if r['ServiceNo'] == '111']
bus_route

# Prompt for boarding stop and alighting stop; used for loop and if-else to compute distance travelled
for busstop in bus_route:
    if busstop['ServiceNo'] == '174' and busstop['BusStopCode'] == '41089':
        print(busstop)

# Distance Calculator
start=int(input('Enter boarding busstop: '))
end=int(input('Enter alighting busstop:'))
distance= 0
for busstop in bus_route:
        if int(busstop['BusStopCode'])==start:
#             print(busstop['Distance'])
             distance-=busstop['Distance']
        elif int(busstop['BusStopCode'])==end:
#             print(busstop['Distance'])
            distance+=busstop['Distance']

print('Distance travelled:{:.1f}km'.format(distance))

# Compute corresponding fare based on distance travelled- Pre-processing
f= fare_list['distance'].str.split('-', 1, expand=True) #Split the range into min and max
f.columns = ['Min', 'Max']
# f 
f['Min']= f['Min'].str.replace('km', '') #take out the 'km' in the Min and Max column
f['Max']= f['Max'].str.replace('km', '')
f
f=f.mask(f.eq('None')).dropna() # change the none values to NA values (to be processed later)
f
new_fare_list = pd.concat([fare_list,f], axis=1) # Attach to existing farelist and creata a new farelist
new_fare_list['Min']= new_fare_list['Min'].astype(float)
new_fare_list['Max']= new_fare_list['Max'].astype(float)
new_fare_list['applicable_time']=new_fare_list['applicable_time'].astype('str')
new_fare_list.info()
new_fare_list.head()

# Find out which are the null values
new_fare_list_na= new_fare_list['Min'].isna()
new_fare_list[new_fare_list_na]

# Filter for Up to and Over
# Over
filter_over = (new_fare_list['Min'].isna() | new_fare_list['Max'].isna()) & (new_fare_list['distance'].str.startswith('Over'))
filter_over_index = new_fare_list[filter_over].index
new_fare_list.loc[filter_over_index, 'Min'] = 40.2
new_fare_list.loc[filter_over_index, 'Max'] = 999

# Up to
filter_up_to = (new_fare_list['Min'].isna() | new_fare_list['Max'].isna()) & (new_fare_list['distance'].str.startswith('Up'))
filter_up_to_index = new_fare_list[filter_up_to].index
new_fare_list.loc[filter_up_to_index, 'Min'] = 0
new_fare_list.loc[filter_up_to_index, 'Max'] = 3.2

# Check and make sure no more null values
new_fare_list.info()

# Fare Calculator
fare_type= input('Enter fare type : ')
applicable_time= input('Enter timings :')
new_fare_list.applicable_time
fare_to_pay = new_fare_list.loc[(new_fare_list.applicable_time== applicable_time) 
                  & (new_fare_list.fare_type== fare_type)
                  & (new_fare_list['Min'] <= distance) 
                  & (new_fare_list['Max'] >= distance)]
print(fare_to_pay)