# Required Imports
import pandas as pd 
import numpy as np
import json
import operator


# functions
def wrapDecodeJSON(str):
    return json.loads('{"temp":'+str+'}')['temp']

# vars
dir = './tmdb-5000-movie-dataset/'


# Read in data files
movies = pd.read_csv(dir+'movies.csv')
credits = pd.read_csv(dir+'credits.csv')

# Lets get some metrics on the multilabel values
def multilabelMetrics(array,column,attr,top):
    print('==========='+column.upper()+'==========')
    movie_cols = array[column]
    unique_cols = dict()
    count_cols = dict()
    attr1 = attr[0]
    attr2 = attr[1]
    for movie_col in movie_cols:
        cols = wrapDecodeJSON(movie_col)
        for col in cols:
            unique_cols[col[attr1]] = col[attr2]
            try:
                count_cols[col[attr1]]+=1
            except:
                count_cols[col[attr1]]=0
    print("Number of unique values for " +column+": " + str(len(unique_cols.keys())) + ".")
    x = []
    y = []
    print("Top " + str(top) + " values are:")
    for i in range(top):
        idx = max(count_cols.items(), key=operator.itemgetter(1))[0]
        x.append(idx)
        y.append(count_cols[idx])
        print(str(i+1)+". " + unique_cols[idx]+ ' with '+ str(count_cols[idx]) +' counts.')
        count_cols[idx] = -99

def multilabelSingleMetrics(array,column,value,attr,top):
    print('==========='+value[1].upper()+'==========')
    movie_cols = array[column]
    unique_cols = dict()
    count_cols = dict()
    attr1 = attr[0]
    attr2 = attr[1]
    for movie_col in movie_cols:
        cols = wrapDecodeJSON(movie_col)
        for col in cols:
            if (col[value[0]] == value[1]):
                unique_cols[col[attr1]] = col[attr2]
                try:
                    count_cols[col[attr1]]+=1
                except:
                    count_cols[col[attr1]]=0
    print("Number of unique values for " +value[1]+": " + str(len(unique_cols.keys())) + ".")
    x = []
    y = []
    print("Top " + str(top) + " values are:")
    for i in range(top):
        idx = max(count_cols.items(), key=operator.itemgetter(1))[0]
        x.append(idx)
        y.append(count_cols[idx])
        print(str(i+1)+". " + unique_cols[idx]+ ' with '+ str(count_cols[idx]) +' counts.')
        count_cols[idx] = -99

multilabelMetrics(movies,'genres',['id','name'],5)
multilabelMetrics(movies,'production_companies',['id','name'],5)
multilabelMetrics(credits,'cast',['id','name'],5)
multilabelMetrics(credits,'crew',['id','name'],5)
multilabelMetrics(movies,'keywords',['id','name'],5)
multilabelSingleMetrics(credits,'crew',['job','Director'],['id','name'],5)