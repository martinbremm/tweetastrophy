import numpy as np
import pandas as pd
import streamlit as st

import spacy
try:
    assert spacy.util.is_package("en_core_web_sm")
except AssertionError:
    spacy.cli.download("en_core_web_sm")

import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

import locationtagger
from geopy.geocoders import Nominatim

from bs4 import BeautifulSoup
import requests
import string
import re

from streamlit_folium import st_folium


def extract_location(text):

    place_entity = locationtagger.find_locations(text = text)

    dic = {'region':place_entity.regions,
        'country':place_entity.countries,
        'city': place_entity.cities,
        'place': place_entity.other}

    # alternative country data
    if place_entity.country_cities:
        dic.update({'country': list(place_entity.country_cities.keys())[0]})
    elif place_entity.country_regions:
        dic.update({'country': list(place_entity.country_regions.keys())[0]})

    for k, v in dic.items():
        # checking if api does not return anything
        if v == []:
            dic[k] = "Unknown"
        # removing lists
        elif type(v) == list:
            dic[k] = v[0]

    return dic


def extract_gps(country, city):

    loc  = Nominatim(user_agent="tweetastrophy")

    # getting location of city
    if city != 'Unknown':
        getLoc = loc.geocode(city, exactly_one=True, timeout=10)
        return getLoc.latitude, getLoc.longitude

    # getting location of country
    elif country != 'Unknown':
        getLoc = loc.geocode(country, exactly_one=True, timeout=10)
        return getLoc.latitude, getLoc.longitude

    # returning default if there is no data on country nor city
    else:
        return 0,0


def get_area(city):
    url = f"https://en.wikipedia.org/wiki/{city}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find('table', {'class': 'infobox'})
    try:
        for th in table:
            res = re.search('km' , th.text)
            if res != None:
                span = res.span()
                num = th.text[span[0]-15:span[1]]
                num = ''.join(digit for digit in num if digit in string.digits)
                return int(num)
            else:
                return 'NotFound'
    except:
        return 'NotFound'


@st.experimental_memo(suppress_st_warning=True)
def create_location(text_df):

    df_dict = text_df.to_dict("records")

    dictionary_list = []
    for row in df_dict:
        ### creating list of location details

        # adding geo info
        dic = extract_location(row["text"])

        # adding gps
        dic['lat'], dic['lon'] = extract_gps(dic['country'],dic['city'])

        # adding area size to the dictionary
        if dic['city'] == 'Unknown' and dic['country'] != 'Unknown':
            dic['size'] = get_area(dic['country'])
        else:
            dic['size'] = get_area(dic['city'])

        if dic['city'] != 'Unknown' and dic['country'] != 'Unknown' and dic['size'] == 'NotFound':
            dic['size'] = get_area(dic['country'])

        dictionary_list.append(dic)

    locations_df = pd.DataFrame.from_dict(data=dictionary_list)

    return locations_df
