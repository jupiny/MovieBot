import json
import random
import re
import os

import requests


MY_OPENAPI_SERVER = 'http://155.230.25.63:8080'
MAX_DISPLAY_NUM = 5
NAVER_MOVIE_API = 'https://openapi.naver.com/v1/search/movie.json'
NAVER_CLIENT_ID = os.environ.get('NAVER_CLIENT_ID')
NAVER_CLIENT_SECRET = os.environ.get('NAVER_CLIENT_SECRET')


def get_title_list_of_movies(title='', genre=''):
    if title:
        response = requests.get(MY_OPENAPI_SERVER + '/movies/?title=' + title)
    elif genre:
        response = requests.get(MY_OPENAPI_SERVER + '/movies/?genres=' + genre)
    else:
        response = requests.get(MY_OPENAPI_SERVER + '/movies')
    json_data = json.loads(response.text)
    if len(json_data) >= MAX_DISPLAY_NUM:
        json_data = random.sample(json_data, MAX_DISPLAY_NUM)

    year_parttern = r' \(\d{4}\)$'
    movie_title_list = [re.sub(year_parttern, '', movie['title']) for movie in json_data]
    return movie_title_list


def get_naver_link_list_of_movies(title):
    naver_link_list = []
    if title:
        response = requests.get(
            NAVER_MOVIE_API+ '?query=' + title,
            headers={
                'X-Naver-Client-Id': NAVER_CLIENT_ID,
                'X-Naver-Client-Secret': NAVER_CLIENT_SECRET,
            }
        )
        json_data = json.loads(response.text)
        naver_link = json_data['items'][0]['link']
        naver_link_list.append(naver_link)
    return naver_link_list
