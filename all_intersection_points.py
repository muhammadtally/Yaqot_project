import pandas as pd
import math
from decimal import Decimal
from math import cos, sin, sqrt, asin, radians
import numpy as np

#A function that receives an places XLSX file, and returns the places that have latitude and longitude data
def get_places_with_point(file):
    df = pd.DataFrame(file, columns= ['placename','LONG','LAT'])
    df = df.fillna(0)
    places = []
    counter = 0
    dflength = len(df)
    for row in df.iterrows():
        if((df['LONG'].iloc[counter] != 0) and (df['LAT'].iloc[counter] != 0)):
            places.append(df['placename'].iloc[counter])
        counter += 1
    return places


#A function that receives an places XLSX file , and returns the places that dont have latitude and longitude data
def get_places_without_point(file):
    df = pd.DataFrame(file, columns= ['placename','LONG','LAT'])
    df = df.fillna(0)
    places = []
    counter = 0
    dflength = len(df)
    for row in df.iterrows():
        if((df['LONG'].iloc[counter] == 0) and (df['LAT'].iloc[counter] == 0)):
            places.append(df['placename'].iloc[counter])
        counter += 1
    return places  

#function that gets a dataframe and deleted the rows where original_place = reference_place
#return a updated dataframe
def clean_duplicated(df):
    df = df.fillna(0)
    labels = []
    counter = 0
    for row in df.iterrows():
        if(df['orig_place_id'].iloc[counter] == df['reference_place_id'].iloc[counter]):
            labels.append(counter)
        counter += 1
    return df.drop(labels=labels, axis=0)  

#func that get placeName and a file of Distances 
#return the latitude and longitude of the places that have relation with this place
def get_places_latlong_for_place(placename, file):
    file = file.fillna(0)
    counter = 0
    rowcounter = 0
    df=pd.DataFrame(data=None, index=None, columns= ["origin_place_name","Place_ID","reference_place_name","reference_place_id"
                                                     ,"longitude","latitude","radius"])
    for row in file.iterrows():
        if(file['orig_place_name'].iloc[counter] == placename):
            if(file['reference_lat'].iloc[counter] != 0.000000):
                df.loc[rowcounter] = [file['orig_place_name'].iloc[counter]
                                      ,file['orig_place_id'].iloc[counter]
                                      ,file['reference_place_name'].iloc[counter]
                                      ,file['reference_place_id'].iloc[counter]
                                      ,file['reference_long'].iloc[counter]
                                      ,file['reference_lat'].iloc[counter]
                                      ,file['total_distance'].iloc[counter] ]
            rowcounter += 1
        counter += 1
    return df

#func that get LONG/LAT and Radius for two circles
#return a converted Points to Radians
def intersection(xp1,yp1, r1_meter, xp2,yp2, r2_meter):
    '''
    1. Convert (lat, lon) to (x,y,z) geocentric coordinates.
    '''
    x_p1 = Decimal(cos(math.radians(xp1))*cos(math.radians(yp1)))  # x = cos(lon)*cos(lat)
    y_p1 = Decimal(sin(math.radians(xp1))*cos(math.radians(yp1)))  # y = sin(lon)*cos(lat)
    z_p1 = Decimal(sin(math.radians(yp1)))                           # z = sin(lat)
    x1 = (x_p1, y_p1, z_p1)
    x_p2 = Decimal(cos(math.radians(xp2))*cos(math.radians(yp2)))  # x = cos(lon)*cos(lat)
    y_p2 = Decimal(sin(math.radians(xp2))*cos(math.radians(yp2)))  # y = sin(lon)*cos(lat)
    z_p2 = Decimal(sin(math.radians(yp2)))                           # z = sin(lat)
    x2 = (x_p2, y_p2, z_p2)
    '''
    2. Convert the radii r1 and r2 (which are measured along the sphere) to angles along the sphere.
    By definition, one nautical mile (NM) is 1/60 degree of arc (which is pi/180 * 1/60 = 0.0002908888 radians).
    '''
    r1 = Decimal(math.radians((r1_meter/1852) / 60)) # r1_meter/1852 converts meter to Nautical mile.
    r2 = Decimal(math.radians((r2_meter/1852) / 60))
    
    
    q = Decimal(np.dot(x1, x2))
    if q**2 != 1 :
        a = (Decimal(cos(r1)) - Decimal(cos(r2))*q) / (1 - q**2)
        b = (Decimal(cos(r2)) - Decimal(cos(r1))*q) / (1 - q**2)
        n = np.cross(x1, x2)
        x0_1 = [a*f for f in x1]
        x0_2 = [b*f for f in x2]
        x0 = [sum(f) for f in zip(x0_1, x0_2)]
        if (np.dot(x0, x0) <= 1) & (np.dot(n,n) != 0): # This is to secure that (1 - np.dot(x0, x0)) / np.dot(n,n) > 0
            t = Decimal(sqrt((1 - np.dot(x0, x0)) / np.dot(n,n)))
            t1 = t
            t2 = -t

            i1 = x0 + t1*n
            i2 = x0 + t2*n
            i1_lat = math.degrees( math.asin(i1[2]))
            i1_lon = math.degrees( math.atan2(i1[1], i1[0] ) )
            ip1 = (i1_lat, i1_lon)

            i2_lat = math.degrees( math.asin(i2[2]))
            i2_lon = math.degrees( math.atan2(i2[1], i2[0] ) )
            ip2 = (i2_lat, i2_lon)
            return [ip1, ip2]
        else:
            return None

#func that get a dataframe of latitude and longitude of the places that have relation with this place
#return a dataframe of the intersection points of this place
def get_intersection_points(lon,lat,df):
    column_names = ["place_name","place_ID", "place_long", "place_lat","reference_place_1","reference_place_ID_1"
                    ,"reference_place_2","reference_place_ID_2","intersection_point_lon",
                    "intersection_point_lat"]
    df_distance_data1 = pd.DataFrame(columns = column_names)
    counter =0
    rangeto = len(df)
    rowcounter = 0
    placepoint = [lat,lon]
    for i in range(0, rangeto):
        lon1=df['longitude'].iloc[i]
        lat1=df['latitude'].iloc[i]
        radius1=df['radius'].iloc[i] * 1000
        for j in range(0, rangeto):
            if(i < j):
                lon2=df['longitude'].iloc[j]
                lat2=df['latitude'].iloc[j]
                radius2=df['radius'].iloc[j] * 1000
                if(intersection(lon1,lat1,radius1,lon2,lat2,radius2) != None):
                    ip1,ip2 = intersection(lon1,lat1,radius1,lon2,lat2,radius2)
                    df_distance_data1.loc[rowcounter] = [df['origin_place_name'].iloc[i]
                                                         ,df['Place_ID'].iloc[i]
                                                         ,lon
                                                         ,lat
                                                         ,df['reference_place_name'].iloc[i]
                                                         ,df['reference_place_id'].iloc[i]
                                                         ,df['reference_place_name'].iloc[j]
                                                         ,df['reference_place_id'].iloc[j]
                                                         ,ip1[1]
                                                         ,ip1[0]]
                    df_distance_data1.loc[rowcounter+1] = [df['origin_place_name'].iloc[i]
                                                         ,df['Place_ID'].iloc[i]
                                                         ,lon
                                                         ,lat
                                                         ,df['reference_place_name'].iloc[i]
                                                         ,df['reference_place_id'].iloc[i]
                                                         ,df['reference_place_name'].iloc[j]
                                                         ,df['reference_place_id'].iloc[j]
                                                         ,ip2[1]
                                                         ,ip2[0]]
                    rowcounter += 2
    return df_distance_data1

#get place name and distances dataframe
#return Long,Lat for place
def get_LONG_LAT_For_place(placename, file):
    df = pd.DataFrame(file, columns= ['placename','LONG','LAT'])
    df = df.fillna(0)
    Long=0
    Lat=0
    counter = 0
    dflength = len(df)
    for row in df.iterrows():
        if(df['placename'].iloc[counter] == placename):
            Long = df['LONG'].iloc[counter]
            Lat = df['LAT'].iloc[counter]
        counter += 1
    return Long,Lat

Yaqut_PlcaeTypeGeo = pd.read_excel(r"Yaqut-PlcaeTypeGeo.xlsx")
places_with_point = get_places_with_point(Yaqut_PlcaeTypeGeo)
places_without_point = get_places_without_point(Yaqut_PlcaeTypeGeo)
Distances = pd.read_excel(r"distance2.xlsx")
Distances = clean_duplicated(Distances)

df_distance_data = pd.DataFrame()
df_distance_data2 = pd.DataFrame()

for i in range (0, len(places_with_point)):
    placename = places_with_point[i]
    df_of_lat_lon_for_place = get_places_latlong_for_place(placename,Distances)
    if len(df_of_lat_lon_for_place) > 1:
        LONG,LAT = get_LONG_LAT_For_place(placename, Yaqut_PlcaeTypeGeo)
        df_distance_data = df_distance_data.append(get_intersection_points(LONG,LAT,df_of_lat_lon_for_place), ignore_index = True)
        df_distance_data = df_distance_data.drop_duplicates(subset=None, keep='first', inplace=False, ignore_index=False)
for i in range (0, len(places_without_point)):
    placename = places_without_point[i]
    df_of_lat_lon_for_place2 = get_places_latlong_for_place(placename,Distances)
    if len(df_of_lat_lon_for_place2) > 1:
        LONG = 0
        LAT= 0
        df_distance_data2 = df_distance_data2.append(get_intersection_points(LONG,LAT,df_of_lat_lon_for_place2), ignore_index = True)
        df_distance_data2 = df_distance_data2.drop_duplicates(subset=None, keep='first', inplace=False, ignore_index=False)

df_distance_data = df_distance_data.append(df_distance_data2, ignore_index = True)
df_distance_data.to_excel("distance_data.xlsx")