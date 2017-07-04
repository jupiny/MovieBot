import re
import requests
from bs4 import BeautifulSoup

from database import add_movie
from exceptions import NaverMoviePageAcessDeniedError


NAVER_RATED_MOVIE_URL = 'http://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20170702'  # 20170702 기준 영화 평점
NAVER_MOVIE_DETAIL_URL = 'http://movie.naver.com/movie/bi/mi/basic.nhn?code={code}'
LAST_PAGE = 40


def get_rated_movie_code_list():
    print('네이버 평점순 영화 코드 크롤링 시작')
    rated_movie_code_list  = []
    for i in range(1, LAST_PAGE+1):
        response = requests.get(NAVER_RATED_MOVIE_URL + '&page=' + str(i))
        soup = BeautifulSoup(response.text, 'html.parser')
        table_element = soup.find('table', class_='list_ranking')
        link_elements = table_element.select('td.title div.tit5 a')
        for link_element in link_elements:
            link = link_element.get('href')
            match = re.search(r"\d{4,6}$", link)
            movie_code = match.group()
            rated_movie_code_list.append(movie_code)
        print(str(i) + ' 페이지 저장완료')
    print('네이버 평점순 영화 코드 크롤링 종료')
    return rated_movie_code_list


def get_movie_info(movie_code):
    response = requests.get(NAVER_MOVIE_DETAIL_URL.format(code=movie_code))
    soup = BeautifulSoup(response.text, 'html.parser')

    movie_info_element = soup.find('div', class_='mv_info')
    if not movie_info_element:
        raise NaverMoviePageAcessDeniedError()

    kor_title = movie_info_element.select_one('h3.h_movie a').text

    eng_title = movie_info_element.select_one('strong.h_movie2').text
    eng_title = eng_title.replace('\t', '').replace('\n', '').replace('\r', '')
    eng_title = re.sub(r', \d{4}$', '', eng_title)


    dl_element = soup.find('dl', class_='info_spec')

    genre_elements = dl_element.select('dd')[0].p.span.select('a')
    genre = '|'.join([
        genre_element.text
        for genre_element in genre_elements
    ])

    director_elements  = dl_element.select('dd')[1].p.select('a')
    director = '|'.join([
        director_element.text
        for director_element in director_elements
    ])

    actor_elements  = dl_element.select('dd')[2].p.select('a')
    actor = '|'.join([
        actor_element.text
        for actor_element in actor_elements
    ])
    return kor_title, eng_title, genre, director, actor


def crawl_rated_movies():
    rated_movie_code_list = get_rated_movie_code_list()
    print('데이터베이스 저장 시작')
    for movie_code in rated_movie_code_list:
        try:
            add_movie(movie_code, *get_movie_info(movie_code))
            print(movie_code + ' 영화 정보 데이터베이스 저장 완료')
        except NaverMoviePageAcessDeniedError:
            print(movie_code + ' 영화 정보 페이지 접근 불가')
            pass
    print('데이터베이스 저장 완료')


if __name__ == "__main__":
    crawl_rated_movies()
