import pandas as pd
import math
from sympy.geometry import Point, Circle

#function that receives an places XLSX file, and returns the places that have latitude and longitude data
#return an array of names of a places with points 
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

#get two circles points and radius
#return intersection points
def get_intersections(x0, y0, r0, x1, y1, r1):
    d=math.sqrt((x1-x0)**2 + (y1-y0)**2)
    # non intersecting
    if d > r0 + r1 :
        return None
    # One circle within other
    if d < abs(r0-r1):
        return None
    # coincident circles
    if d == 0 and r0 == r1:
        return None
    else:
        a=(r0**2-r1**2+d**2)/(2*d)
        h=math.sqrt(r0**2-a**2)
        x2=x0+a*(x1-x0)/d   
        y2=y0+a*(y1-y0)/d   
        x3=x2+h*(y1-y0)/d     
        y3=y2-h*(x1-x0)/d 

        x4=x2-h*(y1-y0)/d
        y4=y2+h*(x1-x0)/d
        
        return (x3, y3, x4, y4)

#func that get a dataframe of latitude and longitude of the places that have relation with this place
#return a dataframe of the intersection points of this place
def get_intersection_points(lon,lat,df):
    column_names = ["place_name","place_ID", "place_long", "place_lat","reference_place_1","reference_place_ID_1"
                    ,"reference_place_2","reference_place_ID_2","intersection_point_lon",
                    "intersection_point_lat", "intersection_point_distance_from_place_point"]
    df_distance_data1 = pd.DataFrame(columns = column_names)
    counter =0
    rangeto = len(df)
    rowcounter = 0
    placepoint = [lon,lat]
    for i in range(0, rangeto):
        lon1=df['longitude'].iloc[i]
        lat1=df['latitude'].iloc[i]
        radius1=df['radius'].iloc[i]
        for j in range(0, rangeto):
            if(i < j):
                lon2=df['longitude'].iloc[j]
                lat2=df['latitude'].iloc[j]
                radius2=df['radius'].iloc[j]
                if(get_intersections(lat1,lon1,radius1,lat2,lon2,radius2) != None):
                    x1,y1,x2,y2 = get_intersections(lat1,lon1,radius1,lat2,lon2,radius2)
                    p1 = [x1,y1]
                    p2= [x2,y2]
                    df_distance_data1.loc[rowcounter] = [df['origin_place_name'].iloc[i]
                                                         ,df['Place_ID'].iloc[i]
                                                         ,lon
                                                         ,lat
                                                         ,df['reference_place_name'].iloc[i]
                                                         ,df['reference_place_id'].iloc[i]
                                                         ,df['reference_place_name'].iloc[j]
                                                         ,df['reference_place_id'].iloc[j]
                                                         ,x1
                                                         ,y1
                                                         ,math.dist(placepoint,p1)]
                    df_distance_data1.loc[rowcounter+1] = [df['origin_place_name'].iloc[i]
                                                         ,df['Place_ID'].iloc[i]
                                                         ,lon
                                                         ,lat
                                                         ,df['reference_place_name'].iloc[i]
                                                         ,df['reference_place_id'].iloc[i]
                                                         ,df['reference_place_name'].iloc[j]
                                                         ,df['reference_place_id'].iloc[j]
                                                         ,x2
                                                         ,y2
                                                         ,math.dist(placepoint,p2)]
                    rowcounter += 2
    return df_distance_data1

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

Yaqut_PlcaeTypeGeo = pd.read_excel(r"Yaqut-PlcaeTypeGeo - Copy.xlsx")
Distances = pd.read_excel(r"Distances.xlsx")

places_with_point = get_places_with_point(Yaqut_PlcaeTypeGeo)

df_distance_data = pd.DataFrame()  

Yaqut_PlcaeTypeGeo = pd.read_excel(r"Yaqut-PlcaeTypeGeo - Copy.xlsx")
Distances = pd.read_excel(r"Distances.xlsx")

places_with_point = get_places_with_point(Yaqut_PlcaeTypeGeo)

df_distance_data = pd.DataFrame()  

df_distance_data.to_pickle("../Data/Distances_between_place_point_and_intersection_points.pkl") 
df_distance_data