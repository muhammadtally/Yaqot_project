import pandas as pd

#get dataframe. and update the long\lat for places
#return updated dataframe
def update_long_lat(file):
    file = file.fillna(0)
    rowcounter = 0
    for i in range(0,len(file)):
        if(file['reference_place_name'].iloc[rowcounter] == "مكة"):
            file['reference_lat'].iloc[rowcounter] = 21.42251
            file['reference_long'].iloc[rowcounter] = 39.826168
            rowcounter += 1
        elif(file['reference_place_name'].iloc[rowcounter] == "صنعاء"):
            file['reference_lat'].iloc[rowcounter] = 15.35
            file['reference_long'].iloc[rowcounter] = 44.2
            rowcounter += 1
        elif(file['reference_place_name'].iloc[rowcounter] == "الري"):
            file['reference_lat'].iloc[rowcounter] = 35.583333
            file['reference_long'].iloc[rowcounter] = 51.433333
            rowcounter += 1
        elif(file['reference_place_name'].iloc[rowcounter] == "شيراز"):
            file['reference_lat'].iloc[rowcounter] = 29.61
            file['reference_long'].iloc[rowcounter] = 52.5425
            rowcounter += 1
        elif(file['reference_place_name'].iloc[rowcounter] == "المقدس"):
            file['reference_lat'].iloc[rowcounter] = 31.778889
            file['reference_long'].iloc[rowcounter] = 35.225556
            rowcounter += 1
        elif(file['reference_place_name'].iloc[rowcounter] == "تبريز"):
            file['reference_lat'].iloc[rowcounter] = 38.073889
            file['reference_long'].iloc[rowcounter] = 46.296111
            rowcounter += 1
        elif(file['reference_place_name'].iloc[rowcounter] == "فيد"):
            file['reference_lat'].iloc[rowcounter] = 27.1203
            file['reference_long'].iloc[rowcounter] = 42.5225
            rowcounter += 1
        elif(file['reference_place_name'].iloc[rowcounter] == "الموصل"):
            file['reference_lat'].iloc[rowcounter] = 36.34
            file['reference_long'].iloc[rowcounter] = 43.13
            rowcounter += 1
        elif(file['reference_place_name'].iloc[rowcounter] == "فاس"):
            file['reference_lat'].iloc[rowcounter] = 34.043333
            file['reference_long'].iloc[rowcounter] = -5.003333
            rowcounter += 1
        elif(file['reference_place_name'].iloc[rowcounter] == "نهاوند"):
            file['reference_lat'].iloc[rowcounter] = 34.188611
            file['reference_long'].iloc[rowcounter] = 48.376944
            rowcounter += 1
        elif(file['reference_place_name'].iloc[rowcounter] == "بسطام"):
            file['reference_lat'].iloc[rowcounter] = 36.485278
            file['reference_long'].iloc[rowcounter] = 54.999722
            rowcounter += 1
        elif(file['reference_place_name'].iloc[rowcounter] == "باب الأبواب"):
            file['reference_lat'].iloc[rowcounter] = 42.05
            file['reference_long'].iloc[rowcounter] = 48.3
            rowcounter += 1
        elif(file['reference_place_name'].iloc[rowcounter] == "السيرجان"):
            file['reference_lat'].iloc[rowcounter] = 29.451944
            file['reference_long'].iloc[rowcounter] = 55.681389
            rowcounter += 1
        else:
            rowcounter += 1
    return file

Distances = pd.read_excel(r"Distances.xlsx")
file = update_long_lat(Distances)
file.to_excel("distance2.xlsx")