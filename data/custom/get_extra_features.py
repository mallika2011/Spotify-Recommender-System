'''
Script to extract all the extra features : popularity, artist URI,
and year associated with each unique song ID.
Uses Spotify API endpoints
'''

import requests 
import json
import pandas as pd


#API endpoint 
URL = "https://api.spotify.com/v1/tracks"

TOKEN = "BQBHckONOf5kX1qmhdLakJt-YEWs-NWTgqcCUgvaqQWIRuU1ZJOdWq48VuxVNAnaXgo04amYf23K4ynhxjfWMvXW_45mLD8S1aqqhyL0AEFI0LArYQwh132BiwpntrciGO0clWmQoEFEBd-ejB4hfmQ_pP9M5jF5tATtmDo0IIXVbtzFti40F0lHDBYWic5nF3So_OCzhp4qMCloOVI3vJYXgYRx0y0yHWqGOSY9JGj4nzokPCYV033JRPt7qBYhao7WB2HWPoTl6opNvBMMZycT2JHGdLai0NY"
kaggle_file = './kaggle-data.csv'
kaggle = pd.read_csv(kaggle_file)

columns = ['id','name','artists','year', 'popularity']

final = pd.DataFrame(columns = columns)

total_nulls = 0
null_el = []
id_count = 0
i = 0
id_list = []
kaggle_count = 0
api_count = 0


def api_get():

    global null_el
    global final

    PARAMS = {'ids':','.join(id_list)} 
    r = requests.get(url = URL, params = PARAMS, headers={'Authorization': 'Bearer '+TOKEN})

    # extracting data in json format 
    data = r.json()

    if ('error' in data) and (data['error']['status']==401) :
        print("Token expired :( ")
        exit(0)
    
    if 'tracks' not in data:
        print(data)
        print(id_list)


    if not data['tracks'] :
        print(data)
        print(id_list)

    
    #get all nulls indices
    nulls_ind = [i for i in range(len(data['tracks'])) if data['tracks'][i] == None]

    if nulls_ind :

        null_el += [id_list[i] for i in nulls_ind]

    data['tracks'] = list(filter(None, data['tracks'])) 

    all_tracks = []
    for track in data['tracks']:
        artists = []
        for art in track['artists'] :
            artists.append(art['uri'].split(':')[2])
        
        all_tracks.append({"id":track['id'],"name":track['name'],"artists":artists, "year":track['album']['release_date'][0:4], "popularity":track['popularity']})

    try:
        df = pd.DataFrame.from_records(all_tracks)

    except:
        print("Nones found!")
        print(data)
        print(id_list)
        exit(0)

    #append to final datafram
    final = final.append(df, ignore_index = True) 

    


with open('../../../../spotify-uncommit/subfiles/part4.txt','r') as f:

    ID = f.readline().strip('\n')

    while (ID):

        i+=1

        #unique id tracker
        if i%1000 == 0:
            print("songs read = ", i)

        if ID in kaggle['id'].values :
            kaggle_count+=1

        api_count+=1
        id_count+=1
        id_list.append(ID)

        # make a GET request in bunches of 50
        if id_count == 50 :
            api_get()    

            #reset values
            id_count = 0
            id_list.clear()


        ID = f.readline().strip('\n')


#get features for residual API songs
if id_list :
    api_get()

    #reset values
    id_count = 0
    id_list.clear()



# print(final)
print("\nNULL SIZE = ", len(null_el))
with open('null4e.txt', 'w') as f:
    for item in null_el:
        f.write("%s\n" % item)

print("======= All done  ============")
print("Kaggle songs = ", kaggle_count)
print("API songs =", api_count)
final.to_csv('./extra-features4.csv') 