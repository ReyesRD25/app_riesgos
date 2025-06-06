import numpy as np
import pandas as pd
import pickle

from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import Binarizer
from sklearn.preprocessing import MinMaxScaler

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingRegressor

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline

def calidad_datos(temp):
    temp['antigüedad_empleo'] = temp['antigüedad_empleo'].fillna('desconocido')
    for column in temp.select_dtypes('number').columns:
        temp[column] = temp[column].fillna(0)
    return temp

def creacion_variables(df):
    temp = df.copy()
    temp.vivienda = temp.vivienda.replace(['ANY','NONE','OTHER'],'MORTGAGE')
    temp.finalidad = temp.finalidad.replace(['wedding','educational','renewable_energy'],'otros')
    return(temp)

def ejecutar_modelos(df):
   #5. Calidad y creacion de variables
   x_pd = creacion_variables(calidad_datos(df.copy()))
   x_ead = creacion_variables(calidad_datos(df.copy()))
   x_lgd = creacion_variables(calidad_datos(df.copy()))

   with open('pe_pd.pickle', mode='rb') as file:
      pipe_ejecucion_pd = pickle.load(file)

   with open('pe_ead.pickle', mode='rb') as file:
      pipe_ejecucion_ead = pickle.load(file)

   with open('pe_lgd.pickle', mode='rb') as file:
      pipe_ejecucion_lgd = pickle.load(file)

   #7. Ejecucion
   scoring_pd = pipe_ejecucion_pd.predict_proba(x_pd)[:, 1]
   ead = pipe_ejecucion_ead.predict(x_ead)
   lgd = pipe_ejecucion_lgd.predict(x_lgd)

   #8.Resultados
   principal = x_pd.principal
   EL = pd.DataFrame({'principal':principal,
                      'pd':scoring_pd,
                      'ead':ead,
                      'lgd':lgd})

   EL['perdida_esperada'] = round(EL.pd * EL.principal * EL.ead * EL.lgd,2)

   return(EL)
