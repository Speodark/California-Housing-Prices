import vaex 
import pandas as pd
import numpy as np
df = vaex.open('data.hdf5')

df_pd = pd.read_csv('data.csv', encoding='unicode_escape')
df_pd = df_pd.drop_duplicates()
df_pd = df_pd.replace(r'^\s*$', np.nan, regex=True)
df_pd = df_pd.dropna()

# convert to numeric
df_pd['livingRoom'] = pd.to_numeric(df_pd['livingRoom'])
df_pd['drawingRoom'] = pd.to_numeric(df_pd['drawingRoom'])
df_pd['bathRoom'] = pd.to_numeric(df_pd['bathRoom'])

# extract only numbers from floor and convert to numeric
df_pd['floor'] = df_pd['floor'].str.extract('(\d+)', expand=False)
df_pd['floor'] = pd.to_numeric(df_pd['floor'])

# same to constructionTime
df_pd['constructionTime'] = df_pd['constructionTime'].str.extract('(\d+)', expand=False)
df_pd['constructionTime'] = pd.to_numeric(df_pd['constructionTime'])

# drop url
df_pd = df_pd.drop(['url'], axis=1)

# convert tradeTime to datetime
df_pd['tradeTime'] = pd.to_datetime(df_pd['tradeTime'])
print(df_pd.constructionTime.unique())
print(df_pd.info())

df_pd.to_hdf('data.hdf5', key='df', mode='w') 
df_pd.to_csv('data.csv',index=False)

# the vaex part
vaex_df = vaex.from_csv('data.csv',convert=True, chunk_size=5_000)

df = vaex.open('data.csv.hdf5')