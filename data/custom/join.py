'''
Script to perform a join on the two sets of features
musical features and the extra features

NOTE : Merge mini files before using the script.
'''

import pandas as pd

musicalf = './musical-features.csv'
musicaldf = pd.read_csv(musicalf)

extraf = './extra-features.csv'
extradf = pd.read_csv(extraf)

musicaldf.sort_index(inplace=True)
extradf.sort_index(inplace=True)

musicaldf.loc[musicaldf.id.isin(extradf.id), ['name', 'artists','popularity','year']] = extradf[['name', 'artists','popularity','year']]

musicaldf.to_csv('./combined-features.csv') 
