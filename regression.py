import boto3
from boto3.dynamodb.conditions import Key, Attr

from sklearn import metrics
from sklearn.base import TransformerMixin
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import BayesianRidge
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn.feature_extraction import DictVectorizer
import numpy as np

import math

features = ['Budget', 'Runtime', 'vote_average', 'Popularity', 'vote_count']
complex_features = ['Genres']

class DenseTransformer(TransformerMixin):
    def transform(self, X, y=None, **fit_params):
        return X.todense()

    def fit_transform(self, X, y=None, **fit_params):
        self.fit(X, y, **fit_params)
        return self.transform(X)

    def fit(self, X, y=None, **fit_params):
        return self

def pre_process(data):
    X = []
    Y = []
    for movie in data:
        #print(movie['original_title'])
        x = {}
        for f in features:
            x[f] = movie[f]

        for cf in complex_features:
            simp= cleaner(movie, cf, 'Name')

            for s in simp:
                x[s] = True

        Y.append(movie['Revenue'])
        X.append(x)

    return X, Y

def extractor(response, dictList, attribute):
    ### example: extractor(table.scan()['Items'], 'Genres', 'Name')

    s = set([])
    for movie in response:
        for g in movie[dictList] if movie[dictList] != None else []:
            s.add(g[attribute])

    return list(s)

def cleaner(movie, dictList, attribute):
    ### example: extractor(movie, 'Genres', 'Name')

    s = set([])
    for g in movie[dictList] if movie[dictList] != None else []:
        s.add(g[attribute])

    return list(s)


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('movies')
rows = table.scan(FilterExpression=Attr('Budget').gt(1000))['Items']
data,target = pre_process(rows)

reg = make_pipeline(DictVectorizer(), DenseTransformer(), LinearRegression())
scores = cross_val_score(reg, data, target, cv=10)


print(scores)
print(np.mean(np.array(scores)))