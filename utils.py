import json
import random
import re

import requests


MY_OPENAPI_SERVER = 'http://155.230.25.63:8080'
MAX_DISPLAY_NUM = 5


def get_title_of_movies(title='', genre=''):
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
