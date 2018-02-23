from sklearn import metrics
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import BayesianRidge
from sklearn.model_selection import cross_val_score
from sklearn.feature_extraction import DictVectorizer

reg = make_pipeline(DictVectorizer(), BayesianRidge())
scores = cross_val_score(reg, data, target, cv=5)
print(scores)