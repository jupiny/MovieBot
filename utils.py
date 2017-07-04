import random

from database import get_all_movies, \
                     get_movies_by_genre, \
                     get_movies_by_actor, \
                     get_movies_by_director


NAVER_MOVIE_DETAIL_URL = 'http://movie.naver.com/movie/bi/mi/basic.nhn?code={code}'
MAX_DISPLAY_NUM = 5


def get_movie_list(genre='', actor='', director=''):
    if genre:
        movie_list = get_movies_by_genre(genre)
    elif actor:
        movie_list = get_movies_by_actor(actor)
    elif director:
        movie_list = get_movies_by_director(director)
    else:
        movie_list = get_all_movies()
    if len(movie_list) >= MAX_DISPLAY_NUM:
        movie_list = random.sample(movie_list, MAX_DISPLAY_NUM)
    return movie_list


def formalize_movie(movie):
    title = movie.get('kor_title')
    naver_link = NAVER_MOVIE_DETAIL_URL.format(code=movie.get('naver_code'))
    formatted_movie = '{title} : {naver_link}'.format(
        title=title,
        naver_link=naver_link,
    )
    return formatted_movie
