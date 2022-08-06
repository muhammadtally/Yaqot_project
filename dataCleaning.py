import pandas as pd
from shapely.geometry import Point, Polygon

#func that get point(long,lat)
#return true if the point inside the area
def point_inside_area(long,lat,coords):
    polygon = Polygon(coords)
    p = Point(long,lat)
    return p.within(polygon)

#func that get a dataframe and delete all the places that thier type1en = Continent
#return a new dataframe
def delete_Continents(df):
    counter = 0
    rowcounter=0
    new_df = pd.DataFrame(data=None, columns= ['item','placename','PlaceEng','placeHeb','LONG','LAT'
                                         ,'ProveID','ProvName','DistID','DistName','mtro_id','mtro_name'
                                         ,'type1id','type1ar','type1en','type2id','type2en'])
    for row in df.iterrows():
        if(df['type1id'].iloc[counter] != 115): 
            new_df.loc[rowcounter] = [df['item'].iloc[counter],df['placename'].iloc[counter],df['placeEng'].iloc[counter],
                                     df['placeHeb'].iloc[counter],df['LONG'].iloc[counter],df['LAT'].iloc[counter],
                                     df['prov_id'].iloc[counter],df['prov_name'].iloc[counter],df['dist_id'].iloc[counter],
                                      df['dist_name'].iloc[counter],df['mtro_id'].iloc[counter],df['mtro_name'].iloc[counter],
                                    df['type1id'].iloc[counter],df['type1ar'].iloc[counter],
                                     df['type1en'].iloc[counter],df['type2id'].iloc[counter],df['type2en'].iloc[counter]]
            rowcounter += 1
        counter += 1
    return new_df
        

#func that get a dataframe and check for places that have prov
#return provs list
def get_prov_name(df):
    provs = []
    counter = 0
    for row in df.iterrows():
        if(df['ProveID'].iloc[counter] != 0):
            provs.append(df['ProvName'].iloc[counter])
        counter += 1
    return provs

#func that get a dataframe and delete all the places that outside the area
#return a new dataframe
def delete_places_outside_area(df ,coords):
    counter = 0
    rowcounter=0
    new_df = pd.DataFrame(data=None, columns= ['item','placename','PlaceEng','placeHeb','LONG','LAT'
                                         ,'ProveID','ProvName','DistID','DistName','mtro_id','mtro_name'
                                         ,'type1id','type1ar','type1en','type2id','type2en'])
    for row in df.iterrows():
        long = df['LONG'].iloc[counter]
        lat = df['LAT'].iloc[counter]
        if((point_inside_area(long,lat,coords)) or ((df['LONG'].iloc[counter] == 0) and df['LAT'].iloc[counter] == 0)):
            new_df.loc[rowcounter] = [df['item'].iloc[counter],df['placename'].iloc[counter],df['PlaceEng'].iloc[counter],
                                     df['placeHeb'].iloc[counter],df['LONG'].iloc[counter],df['LAT'].iloc[counter],
                                     df['ProveID'].iloc[counter],df['ProvName'].iloc[counter],df['DistID'].iloc[counter],
                                      df['DistName'].iloc[counter],df['mtro_id'].iloc[counter],df['mtro_name'].iloc[counter],
                                    df['type1id'].iloc[counter],df['type1ar'].iloc[counter],
                                     df['type1en'].iloc[counter],df['type2id'].iloc[counter],df['type2en'].iloc[counter]]
            rowcounter +=1
        counter +=1
    return new_df

#function that gets a dataframe and deleted the rows where original_place = reference_place
#return a updated dataframe
def clean_duplicated(df):
    labels = []
    counter = 0
    for row in df.iterrows():
        if(df['orig_place_id'].iloc[counter] == df['reference_place_id'].iloc[counter]):
            labels.append(counter)
        counter += 1
    return df.drop(labels=labels, axis=0)


Yaqut_PlcaeTypeGeo = pd.read_excel(r"Yaqut-PlcaeTypeGeo.xlsx")
Distances = pd.read_excel(r"Distances.xlsx")
Distances = Distances.fillna(0)
Yaqut_PlcaeTypeGeo = Yaqut_PlcaeTypeGeo.fillna(0)
area_coords = [(48.283698, -25.326321),(-38.064795, -18.646634),(-34.379086, 76.099459),(4.829015, 78.033053),
                          (9.536497, 115.826022),(42.618349, 134.634615),(56.704922, 116.177584),(55.329576, -14.779446)]


Yaqut_PlcaeTypeGeo_witout_Continents = delete_Continents(Yaqut_PlcaeTypeGeo)
Yaqut_PlcaeTypeGeo_witout_Continents =Yaqut_PlcaeTypeGeo_witout_Continents.fillna(0)
Yaqut_PlcaeTypeGeo_witout_Continents_and_area = delete_places_outside_area(Yaqut_PlcaeTypeGeo_witout_Continents,area_coords)
Yaqut_PlcaeTypeGeo_witout_Continents_and_area = Yaqut_PlcaeTypeGeo_witout_Continents_and_area.fillna(0)

prov_list = get_prov_name(Yaqut_PlcaeTypeGeo_witout_Continents_and_area)
prov_list = list(dict.fromkeys(prov_list))
Distances = clean_duplicated(Distances)
Distances = Distances.fillna(0)

#func that get a datafreame and check if in a row there is a lang/lat point and the point is placed in the prov area
#return a updated dataframe
def delete_sdup_by_prov(df):
    rowcounter=0
    counter = 0
    dup_counter = 1
    check_counter = 0
    df_size = df.shape[0]
    new_df = pd.DataFrame(data=None, columns= ['item','placename','PlaceEng','placeHeb','LONG','LAT'
                                         ,'ProveID','ProvName','DistID','DistName','mtro_id','mtro_name'
                                         ,'type1id','type1ar','type1en','type2id','type2en'])
    while(counter < df_size):
        if(dup_counter < df_size and df['ProvName'].iloc[counter] != 0 and df['placename'].iloc[counter] == df['placename'].iloc[dup_counter] and 
           df['LONG'].iloc[counter] != 0 and df['LAT'].iloc[counter]):
            while(df['placename'].iloc[counter] == df['placename'].iloc[dup_counter]):
                    check_counter += 1
                    dup_counter += 1
            for i in range (0, check_counter):
                prove_name = df['ProvName'].iloc[counter + i]
                if(prove_name == "واسط"):
                    wast_coords = [(32.118134,43.0671294),(33.002312,45.512848),(32.284181,46.743066),(31.289825,45.143027)]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,wast_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],
                                              df['placename'].iloc[counter+ i],df['PlaceEng'].iloc[counter+ i],
                                              df['placeHeb'].iloc[counter+ i],0,0,df['ProveID'].iloc[counter+ i],
                                              df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                              df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],
                                              df['mtro_name'].iloc[counter+ i],df['type1id'].iloc[counter+ i],
                                              df['type1ar'].iloc[counter+ i],df['type1en'].iloc[counter+ i],
                                              df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                elif(prove_name == "سجستان"):
                    sajstan_coords = [(92.636313,57.805380),(26.577050,59.633872),(28.380083,62.386905),
                                          (30.503834,63.772659),(39.530008,61.894335),(34.598913,55.803825)]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,sajstan_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],df['LONG'].iloc[counter+ i],df['LAT'].iloc[counter+ i],
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                elif(prove_name == "جرجان"):
                    jarjan_coords = [(36.615793, 54.799223),(36.590087, 54.617773),(36.448552, 53.966685),
                                     (36.786946, 53.923991),(36.897958, 54.078337)]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,jarjan_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],df['LONG'].iloc[counter+ i],df['LAT'].iloc[counter+ i],
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                elif(prove_name == "أذربيجان"):
                    azerbaycan_coords = [(39.711686, 47.975957),(38.869929, 47.997929),(38.449566, 48.854863),
                                         (40.334255, 50.370976),(41.841186, 48.569218),(41.816627, 46.547734),
                                         (41.775674, 46.196172),(41.298712, 44.998662),(39.990020, 45.602910),
                                         (38.929779, 46.448857)]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,azerbaycan_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],df['LONG'].iloc[counter+ i],df['LAT'].iloc[counter+ i],
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                elif(prove_name == "الأندلس"):
                    andlus_coords = [(37.038150, -8.960748),(38.851332, -11.338582),(40.955775, -9.875300),
                                     (43.357261, -1.827248),(42.419184, 3.581670),(37.632233, -0.140772),
                                     (36.105127, -4.098063),(36.313841, -10.786639),(38.947257, -9.899756)]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,andlus_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],df['LONG'].iloc[counter+ i],df['LAT'].iloc[counter+ i],
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                elif(prove_name == "البحرين"):
                    bahreen_coords = [(26.329172, 50.329100),(26.038996, 50.286639),(25.745158, 50.378094),
                                      (25.786340, 50.779843),(26.358443, 50.841902),(26.367222, 50.371562)]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,bahreen_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],df['LONG'].iloc[counter+ i],df['LAT'].iloc[counter+ i],
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                elif(prove_name == "خراسان"):
                    kharasan_coords = [(38.158818, 52.543218),(39.177786, 73.424965),(29.284762, 72.306300),
                                       (30.416685, 53.413291)]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,kharasan_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],df['LONG'].iloc[counter+ i],df['LAT'].iloc[counter+ i],
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                elif(prove_name == "كرمان"):
                    karman_coords = [(25.802553, 61.331573),(26.315763, 57.244659),(29.346453, 55.157256),
                                     (32.140912, 55.003448),(32.419562, 60.474639),(26.355147, 61.683135)]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,karman_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],df['LONG'].iloc[counter+ i],df['LAT'].iloc[counter+ i],
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                elif(prove_name == "اليمن"):
                    yaman_coords = [(15.969493, 54.259524),(19.499071, 52.101700),(17.791328, 41.921847),
                                    (14.106310, 42.251867),(12.475762, 43.140383),(12.822542, 49.055360)]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,yaman_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],df['LONG'].iloc[counter+ i],df['LAT'].iloc[counter+ i],
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                elif(prove_name == "الشام"):
                    alsham_coords = [(31.300329, 32.051070),(27.486196, 33.289011),(28.090989, 35.432311),
                                     (30.693782, 46.658640),(39.426783, 44.297014),(35.380353, 29.940812)]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,alsham_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],df['LONG'].iloc[counter+ i],df['LAT'].iloc[counter+ i],
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                elif(prove_name == "مصر"):
                    masr_coords = [(21.188579, 37.035981),(21.645691, 23.339118),(32.667266, 23.634745),
                                   (31.598244, 34.250634),(21.429064, 38.583506)]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,masr_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],df['LONG'].iloc[counter+ i],df['LAT'].iloc[counter+ i],
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                elif(prove_name == "إفريقية"):
                    efricia_coords = [(37.029840, 7.500458), (30.091877, 8.780830), (32.767011, 13.876188),
                                      (38.188040, 10.814263)]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,efricia_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],df['LONG'].iloc[counter+ i],df['LAT'].iloc[counter+ i],
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                elif(prove_name == "ما وراء النهر"):
                    alnahar_coords = [(45.823576, 81.754287),(43.898661, 84.717248),(46.586836, 86.182268),
                                      (46.913916, 81.968279)]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,alnahar_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],df['LONG'].iloc[counter+ i],df['LAT'].iloc[counter+ i],
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                elif(prove_name == "خزر"):
                    kharaz_coords = [(45.227933, 36.684448),(43.463470, 39.943539),(42.200222, 45.716785),
                                     (41.854375, 48.510291),(45.652612, 48.370616),(48.412537, 49.394902),
                                     (48.843350, 42.876720),(47.319385, 38.313994)]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,kharaz_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],df['LONG'].iloc[counter+ i],df['LAT'].iloc[counter+ i],
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                elif(prove_name == "خوزستان"):
                    khozstan_coords = [(29.804309, 48.617994), (30.248720, 50.812543),(31.816739, 50.663760),
                                       (33.153293, 49.302396),(32.916305, 46.802842),(29.623401, 48.052619)]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,khozstan_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],df['LONG'].iloc[counter+ i],df['LAT'].iloc[counter+ i],
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                elif(prove_name == "السند"):
                    alsend_coords = [(24.689011, 66.167141),(28.690300, 66.900359),(28.745596, 71.503156),
                                     (23.887281, 72.180965),(22.787325, 67.057989)]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,alsend_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],df['LONG'].iloc[counter+ i],df['LAT'].iloc[counter+ i],
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                elif(prove_name == "الري"):
                    alray_coords = [(35.603162, 51.396769),(35.532750, 51.416029),(35.566156, 51.522275),
                                    (35.600581, 51.504074),(35.607981, 51.422167)]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,alray_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],df['LONG'].iloc[counter+ i],df['LAT'].iloc[counter+ i],
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                elif(prove_name == "فارس"):
                    fares_coords = [(31.389609, 51.573681),(31.576990, 54.781689),(27.389667, 56.715283),
                                    (26.232675, 52.804150),(29.342294, 49.024853)]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,fares_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],df['LONG'].iloc[counter+ i],df['LAT'].iloc[counter+ i],
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                elif(prove_name == "الحجاز"):
                    hejaz_coords = [(29.344214, 33.954924),(17.321438, 40.563147),(20.378826, 45.050830),(30.228136, 39.198892)]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,hejaz_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],df['LONG'].iloc[counter+ i],df['LAT'].iloc[counter+ i],
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                elif(prove_name == "المغرب"):
                    morocco_coords = [(20.174736, -18.323937),(25.272142, -19.329178),(36.689524, -7.338089),
                                      (36.516598, 0.273021),(31.825962, 0.344824),(19.431619, -13.943958)]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,morocco_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],df['LONG'].iloc[counter+ i],df['LAT'].iloc[counter+ i],
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                elif(prove_name == "عمان"):
                    uman_coords = [(19.449731, 50.856591), (16.102528, 52.768212),(19.904899, 60.810204),(23.879532, 60.260888),
                                   (25.476726, 56.547509,(24.540850, 53.691063))]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,uman_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],df['LONG'].iloc[counter+ i],df['LAT'].iloc[counter+ i],
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                elif(prove_name == "صقلية"):
                    sicilia_coords = [(37.861243, 11.029567),(38.940256, 14.530497),(38.046399, 16.280963),
                                      (36.577859, 15.448424),(35.620594, 11.563245)]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,sicilia_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],df['LONG'].iloc[counter+ i],df['LAT'].iloc[counter+ i],
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                elif(prove_name == "أرمن" or prove_name == "أرمينية"):
                    armenia_coords = [(40.308609, 43.310954),(39.922129, 43.530680),(39.567340, 44.684245),
                                      (39.389261, 45.376383),(38.903608, 45.887248),(38.715268, 46.370646),
                                      (39.151113, 46.969401),(39.842039, 46.469523),(40.475958, 45.914713),
                                      (41.112226, 45.667521),(41.479535, 44.925944),(41.318834, 43.915202),
                                      (41.178412, 43.217570)]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,armenia_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],df['LONG'].iloc[counter+ i],df['LAT'].iloc[counter+ i],
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                elif(prove_name == "الأهواز"):
                    ahwaz_coords = [(31.239039, 48.527083),(31.220250, 48.722091),(31.283647, 48.867660),
                                    (31.452497, 48.781829),(31.533297, 48.654113),(31.501688, 48.512664),
                                    (31.287168, 48.510604)]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,ahwaz_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],df['LONG'].iloc[counter+ i],df['LAT'].iloc[counter+ i],
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                elif(prove_name == "خوارزم"):
                    khwarzem_coords = [(39.984277, 55.200449),(39.375499, 51.333261),(42.170326, 40.874277),
                                       (38.486706, 40.786386),(28.698780, 55.815683),(24.615560, 70.229745),
                                       (32.702725, 90.796151),(48.697125, 85.962167),(53.212437, 70.982759),
                                       (46.774952, 53.109812)]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,khwarzem_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],df['LONG'].iloc[counter+ i],df['LAT'].iloc[counter+ i],
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                elif(prove_name == "طبرستان"):
                    tabrstan_coords = [(38.191405, 49.360232),(37.983878, 47.734255),(35.017232, 49.799685),
                                       (36.831986, 56.215700),(38.398343, 55.248904)]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,tabrstan_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],df['LONG'].iloc[counter+ i],df['LAT'].iloc[counter+ i],
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                elif(prove_name == "همذان" or prove_name == "همدان"):
                    hamdan_coords = [(34.816234, 48.453030),(34.762099, 48.448910),(34.735079, 48.474271),
                                     (34.740341, 48.546682),(34.792542, 48.601853),(34.849965, 48.570820),
                                     (34.873813, 48.592001),(34.877046, 48.525008),(34.845114, 48.470823),
                                     (34.828538, 48.434864)]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,hamdan_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],df['LONG'].iloc[counter+ i],df['LAT'].iloc[counter+ i],
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                elif(prove_name == "الصين"):
                    china_coords = [(44.432156, 103.330916),(51.479966, 115.899275),(55.302843, 119.063338),
                                    (48.892120, 136.289900),(40.812088, 130.752791),(36.419453, 123.369978),
                                    (27.174446, 123.633650),(19.101500, 111.856307),(17.349958, 110.336769),
                                    (18.080680, 107.421775),(20.733286, 107.626336),(20.350178, 101.233804),
                                    (22.728400, 96.273200),(26.676425, 93.153644),(29.119165, 80.640273),
                                    (35.423518, 70.845245),(40.801583, 72.244534),(49.342106, 80.173843),
                                    (52.192627, 88.569581)]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,china_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],df['LONG'].iloc[counter+ i],df['LAT'].iloc[counter+ i],
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                elif(prove_name == "العراق"):
                    iraq_coords = [(33.880151, 37.869661),(31.513626, 38.440950),(28.024153, 46.241242),(29.907970, 49.756867),
                                   (38.143779, 46.966340),(37.327077, 39.693391),(35.093550, 37.452180)]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,iraq_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],df['LONG'].iloc[counter+ i],df['LAT'].iloc[counter+ i],
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                elif(prove_name == "عدوان"):
                    adwan_coords = [(32.829782, 35.996876),(32.826717, 36.008635),(32.820298, 36.011252),
                                    (32.813878, 36.002154),(32.813337, 35.989838),(32.816908, 35.984688),
                                    (32.827258, 35.988293)]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,adwan_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],df['LONG'].iloc[counter+ i],df['LAT'].iloc[counter+ i],
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                elif(prove_name == "الطائف"):
                    altaef_coords = [(21.696242, 40.669316),(21.619661, 40.779179),(21.480437, 40.923375),
                                     (21.273269, 40.652836),(21.114499, 40.677555),(21.105531, 40.418003),
                                     (21.163172, 40.229863),(21.436981, 40.302647),(21.693690, 40.438603)]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,altaef_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],df['LONG'].iloc[counter+ i],df['LAT'].iloc[counter+ i],
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                elif(prove_name == "تهامة"):
                    tohama_coords = [(27.393675, 35.239693),(27.715100, 35.986763),(14.761558, 44.990059),(13.675299, 42.529122)]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,tohama_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],df['LONG'].iloc[counter+ i],df['LAT'].iloc[counter+ i],
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                elif(prove_name == "نوبة"):
                    noba_coords = [(24.538160, 35.111837),(22.279979, 28.959494),(14.616574, 23.422384),
                                   (9.157451, 30.058126),(17.404144, 40.517111)]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,noba_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],df['LONG'].iloc[counter+ i],df['LAT'].iloc[counter+ i],
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                elif(prove_name == "زنج"):
                    zonj_coords = [(12.809219, 13.663702),(3.949299, 4.523077),(-16.722921, 7.687140),
                                   (-17.227287, 27.198858),(-32.623100, 30.011358),(-19.727834, 60.773077),
                                   (-0.266319, 41.437139),(-0.266319, 41.437139),(3.247565, 29.835577)]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,zonj_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],df['LONG'].iloc[counter+ i],df['LAT'].iloc[counter+ i],
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                elif(prove_name == "هند"):
                    india_coords =[(20.946978, 89.783779),(27.084467, 88.641201),
                                   (31.278418, 80.595774),(33.477636, 77.735258),
                                   (32.852203, 74.148939),(28.390124, 69.708734),
                                   (23.712542, 66.976300),(7.576254, 71.331116),
                                   (7.470437, 78.781267),(9.875997, 79.549764),(11.836933, 80.614354)]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,india_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],df['LONG'].iloc[counter+ i],df['LAT'].iloc[counter+ i],
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                elif(prove_name == "جيلان"):
                    jilan_coords =[(37.090995, 50.702858),(37.499279, 50.308068),(38.541143, 48.992098),
                                   (38.520554, 48.274895),(37.206376, 48.511769),(36.463843, 49.419788),
                                   (36.432086, 50.554812),(37.143463, 50.873934)]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,jilan_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],df['LONG'].iloc[counter+ i],df['LAT'].iloc[counter+ i],
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                elif(prove_name == "مكران"):
                    makran_coords = [(36.679867, 53.033726),(34.383615, 60.506917),(23.909542, 62.336020),
                                     (20.229635, 64.269643),(24.386409, 71.795094),(39.516927, 72.474475)]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,makran_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],df['LONG'].iloc[counter+ i],df['LAT'].iloc[counter+ i],
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                elif(prove_name == "دوس"):
                    dous_coords = [(19.619749, 39.738335),(20.662346, 41.704621),(19.576670, 42.632237),(18.861137, 40.737809)]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,dous_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],df['LONG'].iloc[counter+ i],df['LAT'].iloc[counter+ i],
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                elif(prove_name == "غفار"):
                    ghafar_coords = [(26.849947, 42.159251),(26.828426, 42.143201),(26.822605, 42.145604),
                                     (26.819924, 42.156247),(26.841906, 42.178305),(26.852550, 42.168006)]
                    long = df['LONG'].iloc[counter + i]
                    lat = df['LAT'].iloc[counter + i]
                    if(point_inside_area(long,lat,ghafar_coords)):
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],df['LONG'].iloc[counter+ i],df['LAT'].iloc[counter+ i],
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                    else:
                        new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                        rowcounter += 1
                else:
                    new_df.loc[rowcounter] = [df['item'].iloc[counter + i],df['placename'].iloc[counter+ i],
                                                  df['PlaceEng'].iloc[counter+ i],
                                     df['placeHeb'].iloc[counter+ i],0,0,
                                     df['ProveID'].iloc[counter+ i],df['ProvName'].iloc[counter+ i],df['DistID'].iloc[counter+ i],
                                      df['DistName'].iloc[counter+ i],df['mtro_id'].iloc[counter+ i],df['mtro_name'].iloc[counter+ i],
                                    df['type1id'].iloc[counter+ i],df['type1ar'].iloc[counter+ i],
                                     df['type1en'].iloc[counter+ i],df['type2id'].iloc[counter+ i],df['type2en'].iloc[counter+ i]]
                    rowcounter += 1
            counter += check_counter
            dup_counter = counter + 1
            check_counter = 0
                    
        else:
            new_df.loc[rowcounter] = [df['item'].iloc[counter],df['placename'].iloc[counter],
                                                  df['PlaceEng'].iloc[counter],
                                     df['placeHeb'].iloc[counter],df['LONG'].iloc[counter],df['LAT'].iloc[counter],
                                     df['ProveID'].iloc[counter],df['ProvName'].iloc[counter],df['DistID'].iloc[counter],
                                      df['DistName'].iloc[counter],df['mtro_id'].iloc[counter],df['mtro_name'].iloc[counter],
                                    df['type1id'].iloc[counter],df['type1ar'].iloc[counter],
                                     df['type1en'].iloc[counter],df['type2id'].iloc[counter],df['type2en'].iloc[counter]]
            rowcounter += 1
            counter += 1
    return new_df

final_yaqut = delete_sdup_by_prov(Yaqut_PlcaeTypeGeo_witout_Continents_and_area)
#get Distances datframe
# return the data frame without ref long/lat
def clean_dis_df(df):
    counter = 0
    for row in df.iterrows():
        if(df['reference_lat'].iloc[counter] !=0 and df['reference_long'].iloc[counter] !=0 ):
            df['reference_lat'].iloc[counter] =0
            df['reference_long'].iloc[counter] =0
        counter += 1
    return df

#get Distances and yaqut datframe
#fill ref lang/lat of distances dataframe according to yaqut
def fill_disDF(Ydf,Ddf):
    counter = 0
    df2_counter = 0
    lenY = len(Ydf)
    for row in Ddf.iterrows():
        place_id = Ddf['reference_place_id'].iloc[counter]
        for row2 in Ydf.iterrows():
            if(df2_counter < lenY):
                ref_id = Ydf['item'].iloc[df2_counter]
                if(place_id == ref_id):
                    if(Ydf['LONG'].iloc[df2_counter] != 0 and Ydf['LAT'].iloc[df2_counter] != 0):
                        Ddf['reference_long'].iloc[counter] = Ydf['LONG'].iloc[df2_counter]
                        Ddf['reference_lat'].iloc[counter] = Ydf['LAT'].iloc[df2_counter]
                df2_counter += 1
        counter += 1
    return Ddf

Distances = clean_dis_df(Distances)
Distances.fillna(0)
Distances = fill_disDF(final_yaqut,Distances)
Distances.fillna(0)