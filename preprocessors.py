import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
import datetime
from feature_engine.outliers import Winsorizer
# import time


class PrintStatus(BaseEstimator, TransformerMixin):

    def __init__(self, variable):
        self.variable = variable        
        
    def fit(self, X, y=None):
        # we need the fit statement to accomodate the sklearn pipeline
        return self

    def transform(self, X):
        print(f'{self.variable} finished at {datetime.datetime.now()}')

        return X
        


class TextToDate(BaseEstimator,TransformerMixin):

    def __init__(self, variables):

        if not isinstance(variables, list):
            raise ValueError('variables should be a list')

        self.variables = variables        

    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X = X.copy()

        for feature in self.variables:
            X[feature] = pd.to_datetime(X[feature], errors='coerce')
         
        return X


class TextToNum(BaseEstimator,TransformerMixin):

    def __init__(self, variables):

        if not isinstance(variables, list):
            raise ValueError('variables should be a list')

        self.variables = variables        

    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X = X.copy()

        for feature in self.variables:
            X[feature] = X[feature].astype('float32')
         
        return X


class LowerText(BaseEstimator,TransformerMixin):

    def __init__(self, variables):

        if not isinstance(variables, list):
            raise ValueError('variables should be a list')

        self.variables = variables        

    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X = X.copy()

        for feature in self.variables:
            X[feature] = X[feature].str.lower()
         
        return X
    

class Left2Text(BaseEstimator,TransformerMixin):

    def __init__(self, variables):

        if not isinstance(variables, list):
            raise ValueError('variables should be a list')

        self.variables = variables        

    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X = X.copy()

        for feature in self.variables:
            X[feature] = X[feature].str[:2]
         
        return X


class Mapper(BaseEstimator, TransformerMixin):

    def __init__(self, variables, mappings):

        if not isinstance(variables, list):
            raise ValueError('variables should be a list')

        self.variables = variables
        self.mappings = mappings

    def fit(self, X, y=None):
        # we need the fit statement to accomodate the sklearn pipeline
        return self

    def transform(self, X):
        X = X.copy()
        for feature in self.variables:
            X[feature] = X[feature].map(self.mappings[feature])

        return X


class DateToDate(BaseEstimator,TransformerMixin):

    def __init__(self, variables, mapping):

        if not isinstance(variables, list):
            raise ValueError('variables should be a list')

        self.variables = variables      
        self.mapping = mapping  

    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X = X.copy()

        for feature in self.variables:
            X[f'{feature}_to_{self.mapping}'] = (X[self.mapping] - X[feature]).dt.days

        X = X.drop(columns=self.variables, axis=1)
         
        return X

class outlier_capper(BaseEstimator, TransformerMixin):
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        X = X.copy()

        for feature in X.columns.tolist():
            try:
                X[feature] = Winsorizer(capping_method='iqr').fit_transform(X[feature].to_numpy().reshape(-1,1))
            except:
                X[feature] = Winsorizer(capping_method='gaussian').fit_transform(X[feature].to_numpy().reshape(-1,1))
        return X
    

class Float64ToFloat32(BaseEstimator, TransformerMixin):
    # def __init__(self, variables):

    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X = X.copy()

        for feature in X.select_dtypes('float64').columns.tolist():
            X[feature] = X[feature].astype('float32')

        return X
        
class Int64ToInt32(BaseEstimator, TransformerMixin):
    # def __init__(self, variables):

    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X = X.copy()

        for feature in X.select_dtypes('int64').columns.tolist():
            X[feature] = X[feature].astype('int32')

        return X