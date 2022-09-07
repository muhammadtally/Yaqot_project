import pandas as pd

Distances = pd.read_excel(r"distances2.xlsx")

#func that get a dataframe
#return all the reference places without lat/long
def get_refPlaces_without_point(file):
    file = file.fillna(0)
    rowcounter = 0
    counter = 1
    rowounter2 = 0
    column_names = ["Place_Name","place_id","Counts"]
    places_df = pd.DataFrame(columns = column_names)
    for row in file.iterrows():
        if(file['reference_lat'].iloc[rowcounter] == 0 and file['reference_long'].iloc[rowcounter] == 0):
            placeName = file['reference_place_name'].iloc[rowcounter]
            placeID = file['reference_place_id'].iloc[rowcounter]
            for i in range(0, len(file)):
                if(placeName == file['reference_place_name'].iloc[i] and i != rowcounter):
                    counter += 1
            places_df.loc[rowounter2] = [placeName,placeID,counter]
            counter = 1
            rowounter2 += 1
        rowcounter += 1
    return places_df

places = get_refPlaces_without_point(Distances)
places = places.drop_duplicates(subset=None, keep='first', inplace=False, ignore_index=False)
places = places.sort_values(by=['Counts'], ascending=False)
places.to_excel("places.xlsx")