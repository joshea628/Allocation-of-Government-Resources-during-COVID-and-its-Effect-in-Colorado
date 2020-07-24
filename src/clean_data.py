import pandas as pd
import numpy as np

#import data
df = pd.read_csv('../.gitignore/PPP_data_to_150k.csv')
counties = pd.read_csv('../data/zip_code_database.csv')
demographics = pd.read_csv('../data/counties.csv')

#filter out all unanswered ethnicities
df2 = df[~df.RaceEthnicity.str.contains("Unanswered")]

#drop nonprofit column
df2.drop('NonProfit', axis=1,inplace=True)

#drop row with Nebraska Zip code
df2.drop([71479],axis=0, inplace=True)

#filter zip code database for Colorado, drop unnecessary columns
co_counties = counties[counties['state']=='CO']
co_counties_1 = co_counties.drop(['decommissioned', 'acceptable_cities', 'unacceptable_cities','timezone','area_codes','world_region','country','irs_estimated_population_2015','primary_city','state'],axis=1)

#merge counties onto dataframe 
df_with_counties = pd.merge(df2,co_counties_1, left_on='Zip', right_on='zip')

#only include 2018 demographic data
demographics_18 = demographics[demographics['YEAR']==2018]
demographics_18 = demographics_18.iloc[:,:11]


if __name__ == '__main__':

    