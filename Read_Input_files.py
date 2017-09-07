## Read Input files and store them as pickle file for later analysis 
## By Goma Rajaram

import pandas as pd
import cPickle as pickle

## Airports.dat file  
airports_label=pd.read_table('airports_labels.txt',sep=',')
print(airports_label)

airports_data = pd.read_table('airports.dat',sep=',',header=None,names=airports_label.columns) 
print(airports_data.head())
print(airports_data.index,airports_data.columns)

## Airlines.dat file
## Note: "N/A" in the file is read as NaN
airlines_labels=pd.read_csv('airlines_labels.csv')
print(airlines_labels)

airlines_data = pd.read_table('airlines.dat',sep=',',header=None,names=airlines_labels.columns,na_values=['\N','-']) 
print(airlines_data.head())
print(airlines_data.index,airlines_data.columns)

## Routes.dat file

## Routes.dat file
routes_labels=pd.read_csv('routes_labels.csv')
print(routes_labels)

routes_data = pd.read_table('routes.dat',sep=',',header=None,names=routes_labels.columns) 
print(routes_data.head())
print(routes_data.index,routes_data.columns)

pickle.dump(airports_data,open('airports.p','wb'))
read_back_ap=pickle.load(open('airports.p','rb'))
print(read_back_ap.head())

pickle.dump(airlines_data,open('airlines.p','wb'))
read_back_al=pickle.load(open('airlines.p','rb'))
print(read_back_al.head())

pickle.dump(routes_data,open('routes.p','wb'))
read_back_ap=pickle.load(open('routes.p','rb'))
print(read_back_ap.head())

nearest_ap = airports_data[airports_data['Ap_city'] == 'Milwaukee']
print nearest_ap['Ap_IATA_code']

departing_routes = routes_data[routes_data['Orig_ap_code'] == 'MKE']
print departing_routes['Orig_ap_code'].count()

routes_into_EGO = routes_data[routes_data['Dest_ap_code'] == 'EGO']
print routes_into_EGO['Dest_ap_code'].count()

## Program End 