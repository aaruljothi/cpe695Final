# Required Imports
import pandas as pd 
import numpy as np 
import json
import pickle

# functions
def binStringOr(s1,s2):
    if not (len(s1)==len(s2)): print('WARNING STRING LENGTHS DO NOT MATCH')
    sst = len(s1) if len(s1)<len(s2) else len(s2)
    fin = ''
    for idx in range(sst):
        if (s2[idx] == '1') or (s1[idx] == '1'):
            fin+='1'
        else:
            fin+='0'
    return fin

def binExtract(s,size):
    base = '0' * size
    tot = []
    if len(s) < size:
        s = '0' * (size-len(s)) + s
    for idx in range(len(s)):
        if s[idx] == '1':
            tot.append(base[0:idx]+'1'+base[idx+1:])
    return tot

def wrapDecodeJSON(str):
    return json.loads('{"temp":'+str+'}')['temp']

def extractArrDict(arr,idx):
    tot = []
    for val in arr:
        tot.append(val[idx])
    return tot

def extractDict(dic,idxs):
    tot = []
    for idx in idxs:
        tot.append(dic[idx])
    return tot

class customOneHot:
    def __init__(self):
        self.binary_d = dict()
        self.decode_d = dict()
    def fit(self, vals):
        vals = np.unique(vals)
        base= '0' * len(vals)
        count = 0
        for val in vals:
            bin_rep = base[0:count]+'1'+base[count+1:]
            self.binary_d[val] = bin_rep
            self.decode_d[int(bin_rep,2)] = val
            count+=1
    def transform(self,vals):
        rep = '0'* len(self.binary_d.keys())
        for val in vals :
            rep =binStringOr(rep,self.binary_d[val])
        return int(rep,2)
    def transform_many(self,valss):
        tot = []
        for vals in valss:
            tot.append(self.transform(vals))
        return tot
    def decode(self,val):
        bin_str = "{0:b}".format(val)
        single_bins = binExtract(bin_str,len(self.binary_d.keys()))
        tot = []
        for bin_ in single_bins:
            tot.append(self.decode_d[int(bin_,2)])
        return tot
    def decode_many(self,vals):
        tot = []
        for val in vals:
            tot.append(self.decode(val))
        return tot
    def get_dict(self):
        return self.binary_d


def catExtract(array,column,attr):
    movie_cols = array[column]
    unique_cols = dict()
    attr1 = attr[0]
    attr2 = attr[1]
    for movie_col in movie_cols:
        cols = wrapDecodeJSON(movie_col)
        for col in cols:
            unique_cols[col[attr1]] = col[attr2]
    return unique_cols

def catExtractSingle(array,column,value,attr):
    movie_cols = array[column]
    unique_cols = dict()
    attr1 = attr[0]
    attr2 = attr[1]
    for movie_col in movie_cols:
        cols = wrapDecodeJSON(movie_col)
        for col in cols:
            if (col[value[0]] == value[1]):
                unique_cols[col[attr1]] = col[attr2]
    return unique_cols



# vars
dir = './tmdb-5000-movie-dataset/'


# Read in data files
movies = pd.read_csv(dir+'movies.csv')
credits = pd.read_csv(dir+'credits.csv')

# Predictors as numbers, categorical, and extra work and where they come from
x_nums_m = ['budget','runtime']
x_cats_m = ['genres','production_companies']
x_cats_c = ['cast','crew']
x_xtra_c = ['jobs','Director']
x_xtra_m = ['release_date']

# Dictionaries to hold IDS of our cats
all_genres = catExtract(movies,'genres',['id','name'])
all_production_companies = catExtract(movies,'production_companies',['id','name'])
all_casts = catExtract(credits,'crew',['id','name'])
all_directors = catExtractSingle(credits,'crew',['job','Director'],['id','name'])

# fit our custom encouder to all this
print("Starting Encoding")
genres_enc = customOneHot()
production_companies_enc = customOneHot()
cast_enc = customOneHot()
directors_enc = customOneHot()
genres_enc.fit(list(all_genres.values()))
production_companies_enc.fit(list(all_production_companies.values()))
cast_enc.fit(list(all_casts.values()))
directors_enc.fit(all_directors.values())
print("Complete Encoding")
# pickle.dump(genres_enc,open('./encoders/genre_encoder.p','wb'))
# pickle.dump(production_companies_enc,open('./encoders/production_encoder.p','wb'))
# pickle.dump(cast_enc,open('./encoders/cast_encoder.p','wb'))
# # pickle.dump(directors_enc,open('./encoders/director_encoder.p','wb'))
# print('Saving Complete')

# Load encoders
# genres_enc = pickle.load(open('./encoders/genre_encoder.p','rb'))
# production_companies_enc=pickle.load(open('./encoders/production_encoder.p','rb'))
# cast_enc=pickle.load(open('./encoders/cast_encoder.p','rb'))
# directors_enc=pickle.load(open('./encoders/director_encoder.p','rb'))

# print(genre_enc.get_dict())
# print(genre_enc.get_dict()['Action'])
# print(binStringOr('00001101','00101001'))
# print(genres_enc.transform(['Action','Crime']))
# print(genres_enc.decode(557056))
# print(binExtract('1101',5))
# genre_enc.fit(all_genres)

# remove everything that we done need
# movies = movies[[x_nums_m+x_cats_m+x_xtra_m]]
# credits = credits[[x_cats_c]]

# Encode the cat columns
for row in range(len(movies)):
    # binary encode everything we need
    genres = wrapDecodeJSON(movies.iloc[row]['genres'])
    genres = extractArrDict(genres,'name')
    genres = genres_enc.transform(genres)
    movies.iloc[row,'genres'] = genres 
    pos = wrapDecodeJSON(movies.iloc[row]['production_companies'])
    pos = extractArrDict(pos,'name')
    pos = production_companies_enc.transform(pos)
    movies.iloc[row,'production_companies'] = pos
    
    # print
    # print(movies.iloc[row]['budget'])
    # movies.loc[row,'budget'] = 100
    # print(movies.iloc[row]['budget'])
    break