import pandas as pd
import cartopy
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.feature as cfeature
import shapely.geometry as sgeom
import numpy as np
from cartopy.geodesic import Geodesic


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

#get float number, convert it to int + 10, and return a new float
def changeMaxValue(maxNum):
    maxNum = int(maxNum) + 10
    maxNum = float(maxNum)
    return maxNum
#get float number, convert it to int - 10,and return a new float
def changeMinValue(minNum):
    minNum = int(minNum) - 10
    minNum = float(minNum)
    return minNum


#function that gets a place name, and a dataframe of points of places related to our place
#Prints a map with circles to find intersections, to identify where the place is
def Create_Map_for_place(placename, df):
    gd = Geodesic()
    src_crs = ccrs.PlateCarree()
    lcc = ccrs.Robinson()
    fig = plt.figure(figsize=(25, 10))
    ax = plt.axes(projection=lcc)
    ax.coastlines(resolution='50m')
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAKES, alpha=0.5)
    ax.add_feature(cfeature.RIVERS)
    geoms = []
    counter = 0
    for row in df.iterrows():
        cp = gd.circle(lon=df['longitude'].iloc[counter],
                       lat=df['latitude'].iloc[counter],
                       radius=df['radius'].iloc[counter] * 1000)
        geoms.append(sgeom.Polygon(cp))
        counter += 1
    ax.add_geometries(geoms, crs=src_crs, edgecolor='r', alpha=0.5)
    
    maxlong = changeMaxValue(df['longitude'].max())
    maxlat = changeMaxValue(df['latitude'].max())
    minlong = changeMinValue(df['longitude'].min()) 
    minlat = changeMinValue(df['latitude'].min()) 
    
    ax.set_extent([minlong, maxlong, minlat, maxlat])
    plt.show()

# Load our Excel Files
#Yaqut_PlcaeTypeGeo = pd.read_excel(r"Yaqut-PlcaeTypeGeo - Copy.xlsx")
Distances = pd.read_excel(r"Distances.xlsx")

#get two arrays : 1)places with points 2)places without points
#places_with_point = get_places_with_point(Yaqut_PlcaeTypeGeo)
#places_without_point = get_places_without_point(Yaqut_PlcaeTypeGeo)

#places_with_point_len = len(places_with_point)
#intforcheck = len(places_with_point) - 1

#get a dataframe of points(latitude and longitude) and distances of places that related to the place
dfForPlace = get_places_latlong_for_place("هجر", Distances)

#Prints a map with circles to find intersections, to identify where the place is
Create_Map_for_place("هجر" , dfForPlace)