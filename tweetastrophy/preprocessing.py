import pandas as pd
import numpy as np
import en_core_web_sm

# download before use
#!python -m spacy download en_core_web_sm

import locationtagger
from geopy.geocoders import Nominatim





def extract_location(text):

    place_entity = locationtagger.find_locations(text = text)

    dic = {'region':place_entity.regions,
        'country':place_entity.countries,
        'city': place_entity.cities,
        'place': place_entity.other}
    if len(dic['country']) == 0:
        dic['country'] = [country for country in place_entity.country_cities.keys()]
        if len(dic['country']) == 0:
            dic['country'] = [country for country in place_entity.country_regions.keys()]


    for k in dic.keys():
        if len(dic[k]) == 0:
              dic[k] = ['Unknown']
    return dic



def extract_gps(country, city):

    loc  = Nominatim(user_agent="tweetastrophy")


    if city != 'Unknown':
        getLoc = loc.geocode(city, exactly_one=True, timeout=10)
        return getLoc.latitude, getLoc.longitude

    elif country != 'Unknown':
        getLoc = loc.geocode(country, exactly_one=True, timeout=10)
        return getLoc.latitude, getLoc.longitude
    else:
        return 0,0


def creat_location(file_path):

    with open(file_path) as file:
        lines = [line.strip() for line in file.readlines() if len(line.strip())>0]

    df = pd.DataFrame(lines, columns=['text'])

    ls = ['region','country','city']
    for k in ls:
        df[k] = df['text'].apply(lambda x: extract_location(x)[k][0])

    df['lat'] = np.nan
    df['lon'] = np.nan
    for x, y in df.iterrows():
        df['lat'].iloc[x], df['lon'].iloc[x] = (extract_gps(y['country'],y['city']))

    return df
