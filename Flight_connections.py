## Flight connections - Data Analysis
## By Goma Rajaram


import pandas as pd
import cPickle as pickle
import numpy as np
import math
 
#----------------------------------------------------------------------------
# Function to return distance between two airports based on 
# the location of the airport defined as (latitude, longitude) pair
# Note : Function downloaded from internet
def distance_on_unit_sphere(lat1, long1, lat2, long2):
 
    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
         
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
         
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
         
    # Compute spherical distance from spherical coordinates.
         
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta', phi')
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
     
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )
    distance = arc * 3960
 
    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    return distance

#----------------------------------------------------------------------------
# read each of the input data files into pandas DataFrames

airports=pickle.load(open('airports.p','rb'))
#print(airports.head())

airlines=pickle.load(open('airlines.p','rb'))
#print(airlines.head())

routes=pickle.load(open('routes.p','rb'))
#print(routes.head())

print airports.dtypes
print airlines.dtypes
print routes.dtypes

print airports.index[:10]
print airlines.index[:10]
print routes.index[:10]
#-----------------------------------------------------------------------------
## Check the airports, routes, and airlines data for duplicate records.
print airports.duplicated().sum()
print airlines.duplicated().sum()
print routes.duplicated().sum()

## Checking for duplicated() usage
al_temp = airlines[1:5] 
al_temp_dup = al_temp.append(airlines[1:10])
print al_temp_dup.duplicated().sum()
al_temp_no_dup= al_temp_dup.drop_duplicates();
print al_temp_no_dup;

#-----------------------------------------------------------------------------
## Determine how many "defunct" airlines are in the data.
print (airlines['Al_active'] == 'N').sum()
defunct_airlines = airlines[airlines['Al_active'] == 'N']
print defunct_airlines.Al_active.count()

## Check to see whether the routes data include any "flights from nowhere," flights that don't originate from an airport included in the airports data.
r_orig_apc = pd.Series(routes.Orig_ap_code.unique())
a_apc = pd.Series(airports.Ap_IATA_code.unique())
result = r_orig_apc[r_orig_apc.isin(a_apc) == False]
print result.count()
print airports.Ap_IATA_code.isin(result).sum()
print routes.Orig_ap_code.isin(result).sum()
 

#------------------------------------------------------------------------------
# Find the ten (10) longest flight routes from Chicago O'Hare.
# Compute distances based on lattitude and longitude pairs.

ORD_loc = airports[airports.Ap_IATA_code == 'ORD']
print ORD_loc

routes_from_ORD = routes[routes.Orig_ap_code == 'ORD'].Dest_ap_code
print routes_from_ORD

temp1 = airports[airports.Ap_IATA_code.isin(routes_from_ORD)] 

temp = temp1.reindex(columns=['Ap_name','Ap_latitude','Ap_longitude','Dist_from_ORD'],fill_value=0.0)

temp.to_csv('from_ORD.csv',index=False)

from_ORD_DF = pd.read_csv('from_ORD.csv')

new_DF = from_ORD_DF


i= 0
while i < 206:
    x=distance_on_unit_sphere(ORD_loc.Ap_latitude,ORD_loc.Ap_longitude,new_DF.get_value(i,'Ap_latitude'),new_DF.get_value(i,'Ap_longitude'))
    new_DF.set_value(i,'Dist_from_ORD',x)
    i = i + 1

ord_DF = new_DF.sort_index(by='Dist_from_ORD',ascending=False)
out_DF = ord_DF[ord_DF.Dist_from_ORD > 5400.00]
out_DF.drop(['Ap_latitude','Ap_longitude'],axis=1,inplace=True)
print out_DF

#------------------------------------------------------------------------------
## Save DataFrames
pickle.dump(airports,open('airports.p','wb'))
read_back_ap=pickle.load(open('airports.p','rb'))
print(read_back_ap.head())

pickle.dump(airlines,open('airlines.p','wb'))
read_back_al=pickle.load(open('airlines.p','rb'))
print(read_back_al.head())

pickle.dump(routes,open('routes.p','wb'))
read_back_ap=pickle.load(open('routes.p','rb'))
print(read_back_ap.head())