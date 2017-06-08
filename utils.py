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


def get_naver_movie_info(title):
    if title:
        response = requests.get(
            NAVER_MOVIE_API+ '?query=' + title,
            headers={
                'X-Naver-Client-Id': NAVER_CLIENT_ID,
                'X-Naver-Client-Secret': NAVER_CLIENT_SECRET,
            }
        )
        json_data = json.loads(response.text)
        if json_data['total'] > 0:
            title = json_data['items'][0]['title']
            title = re.sub('<b>|</b>', '', title) # <b>, </b> 태그 제거
            naver_link = json_data['items'][0]['link']
            movie_info = '{title} : {naver_link}'.format(
                    title=title,
                    naver_link=naver_link
            )
            return movie_info 
    return ''
