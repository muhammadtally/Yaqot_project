import pandas as pd
import math
from sympy.geometry import Point, Circle

#A function that receives an places XLSX file, and returns the places that have latitude and longitude data
#return an array of the places names
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


#func that get placeName and a file of Distances 
#and return the latitude and longitude of the places that have relation with this place
def get_places_latlong_for_place(placename, file):
    file = file.fillna(0)
    counter = 0
    rowcounter = 0
    df=pd.DataFrame(data=None, index=None, columns= ["longitude","latitude","radius"])
    for row in file.iterrows():
        if(file['orig_place_name'].iloc[counter] == placename):
            if(file['reference_lat'].iloc[counter] != 0.000000):
                df.loc[rowcounter] = [file['reference_long'].iloc[counter]
                                      ,file['reference_lat'].iloc[counter]
                                      ,file['total_distance'].iloc[counter] ]
            rowcounter += 1
        counter += 1
    return df

#func that get a dataframe of latitude and longitude of the places that have relation with this place
#return a dataframe of the intersection points of this place
def get_intersection_points(placename,df):
    column_names = ["orig_place_id","place_name", "place_long", "place_lat","ref_place_id_1","ref_place_id_2","intersection_point_lon",
                    "intersection_point_lat", "intersection_point_distance"]
    df_distance_data1 = pd.DataFrame(columns = column_names)
    counter =0
    rangeto = len(df)-1
    for i in range (0, rangeto):
        for j in range (0, rangeto):
            if(j != i):
                lon1=df['longitude'].iloc[i]
                lat1=df['latitude'].iloc[i]
                radius1=df['radius'].iloc[i] * 1000
                lon2=df['longitude'].iloc[j]
                lat2=df['latitude'].iloc[j]
                radius2=df['radius'].iloc[j] * 1000
                d=math.sqrt((lon1-lon2)**2 + (lat1-lat2)**2)
                if d < radius1 + radius2 and d < abs(radius1-radius2) and d != 0:
                    a=((radius1**2) - (radius2**2) + (d**2)) /(2*d)
                    h=math.sqrt( abs((radius1**2) - (a**2)))
                    x2=lon1+a*(lon2-lon1)/d
                    y2=lat1+a*(lat2-lat1)/d
                    x3=x2+h*(lat2-lat1)/d     
                    y3=y2-h*(lon2-lon1)/d
                    x4=x2-h*(lat2-lat1)/d
                    y4=y2+h*(lon2-lon1)/d
                    df_distance_data1.loc[counter] = [placename, 0,0, x3,y3,0]
                    df_distance_data1.loc[counter+1] = [placename, 0,0, x4,y4,0]
                counter += 2
    return df_distance_data1

#func that get a dataframe of latitude and longitude of the places that have relation with this place
#return a dataframe of the intersection points of the places
def get_intersection_points_from_circles(placename,df):   
    column_names = ["place_name", "place_long", "place_lat","intersection_point_lon",
                    "intersection_point_lat", "intersection_point_distance"]
    df_distance_data1 = pd.DataFrame(columns = column_names)
    counter =0
    rangeto = len(df)-1
    for i in range (0, rangeto):
        lon1=df['longitude'].iloc[i]
        lat1=df['latitude'].iloc[i]
        radius1=df['radius'].iloc[i] * 1000
        c1 = Circle(Point(lon1, lat1), radius1)
        for j in range (0, rangeto):
            if(j != i):
                lon2=df['longitude'].iloc[j]
                lat2=df['latitude'].iloc[j]
                radius2=df['radius'].iloc[j] * 1000
                c2 = Circle(Point(lon2, lat2), radius2)
                i_0 = c1.intersection(c2)
                print(i_0)

Yaqut_PlcaeTypeGeo = pd.read_excel(r"Yaqut-PlcaeTypeGeo - Copy.xlsx")
Distances = pd.read_excel(r"Distances.xlsx")

places_with_point = get_places_with_point(Yaqut_PlcaeTypeGeo)

column_names = ["place_name", "place_long", "place_lat","intersection_point_lon","intersection_point_lat", "intersection_point_distance"]
df_distance_data = pd.DataFrame(columns = column_names)  

df_of_lat_lon_for_place = get_places_latlong_for_place("هجر",Distances)
get_intersection_points_from_circles("هجر", df_of_lat_lon_for_place)

for i in range (0, len(places_with_point)):
    placename = places_with_point[i]
    df_of_lat_lon_for_place = get_places_latlong_for_place(placename,Distances)
    if len(df_of_lat_lon_for_place) > 1:
        rmdf = get_intersection_points(placename, df_of_lat_lon_for_place)
        df_distance_data.append(rmdf, ignore_index = True, sort=None)
df_distance_data    