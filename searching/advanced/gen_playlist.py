'''
Script to generate playlist of songs using the 
advanced search option wherein the user provides
a set of paramters based on which the search results
are produced
'''

import json
import pandas as pd
import numpy as np
from scipy.spatial import distance
import multiprocessing 
import time 
import os
import sys
import time 
import requests 
from functools import partial

import pickle
from pickle import load

from config import *
from mood import * 
from positive import *
from negative import *
from field import *
from api_songs import *


def compute_emb(filename, query_id):

    with open(directory+filename, 'r') as f:
        
        song = f.readline()
        while song:
            song = song.strip().split(':')
            song_id = song[0]
            
            song_features = np.array(song[1].split(" ")).astype(np.float)


            if song_id == query_id:
                return song_features

            song = f.readline()

    return ""


# Find appropriate network embedding for query
def get_embeddings(query_id):
    pool0 = multiprocessing.Pool() 
    pool0 = multiprocessing.Pool() 
    files = [filename for filename in os.listdir(directory)]   
    compute = partial(compute_emb, query_id = query_id)
    outputs0 = pool0.map(compute, files)
    query_features = [item for sublist in outputs0 for item in sublist]

    if ("".join(map(str, query_features)) == ""):
        print("Getting spotify features ...")
        query_features = get_from_api(query_id)

    return query_features


def set_subtraction(pos, neg, field):
    
    pos_neg = [i for i in pos + neg if i not in pos or i not in neg]
    final   = [i for i in pos_neg + field if i not in pos_neg or i not in field]

    return final


while (1):

    res_songs      = []
    positive_songs = []
    negative_songs = []
    field_songs    = []
    mood_file = ""

    print("\n\n*************** SONGIFY *******************")
    print("> 'r' to reset")
    print("> 'q' to quit")
    print("> any key to continue\n")
    inp = input("Choice :")
    if inp == "q":
        break
    if inp == 'r':
        search_space.clear()

    mood_type = input("Enter a Mood: ") 
    pos_query_id = input("Enter a similarity song: ") 
    neg_query_id = input("Enter dissimilar song: ") 
    field_type = input("Enter a field : ") 
    print("***********************************\n\n")

    print("\nGenerating Playlist ... \n")


    #mood based search space
    if mood_type != "":
        mood_file = "<path to mood file>"
        mood_songs = get_mood_songs(mood_file)

    #positively related songs
    if pos_query_id != "":
        pos_query_features = get_embeddings(pos_query_id)
        positive_songs = get_positive_songs(pos_query_id, pos_query_features, mood_file)

    #negatively related songs
    if neg_query_id != "":
        neg_query_features = get_embeddings(neg_query_id)
        negative_songs = get_negative_songs(neg_query_id, neg_query_features, mood_file)


    #field based search


    #generating results as topk from mood if no other query is passed
    if pos_query_id == "" and neg_query_id == "" and field_type == "":
        res_songs = mood_songs
    
    #using set subtraction with the queries passed 
    else:
        res_songs = set_subtraction(positive_songs, negative_songs, field_songs)


    search_space = res_songs

    print(type(positive_songs), len(positive_songs), "type of pos")
    print(type(negative_songs), len(negative_songs), "type of neg")



    print("\n===================================")
    print("Your Playlist is:")
    print("===================================")

    for o in res_songs[:TOP_RES]:
        print(song_name[o[0]])

    for o in positive_songs[:TOP_RES]:
        print(song_name[o[0]])

    for o in negative_songs[:TOP_RES]:
        print(song_name[o[0]])


