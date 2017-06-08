import os
import re

from flask import Flask, request, jsonify

from utils import get_title_list_of_movies
from utils import get_naver_movie_info
 

TITLE = 1
GENRE = 2
GENRE_LIST = ['adventure', 'animation', 'children', 'comedy', 'fantasy', 'romance', 'drama', 'action', 'crime', 'thriller',
              'horror', 'mystery', 'sci-fi', 'documentary', 'imax', 'war', 'musical', 'film-noir', 'western',]
 
app = Flask(__name__)
 
 
@app.route('/keyboard')
def keyboard():

    data = {
        "type": "buttons",
        "buttons": ["시작하기"],
    }

    return jsonify(data)


@app.route('/message', methods=['POST'])
def message():
    json_data = request.get_json()
    content = json_data['content']
    title_match = re.search(r'^제목 ', content)
    genre_match = re.search(r'^장르 ', content)

    text = ''
    if content in ['시작하기', '도움말']:
        text = '[도움말]\n\n1. 제목으로 검색하기\n=> "제목 (검색할 제목명)"\n\n2. 장르로 검색하기\n=> "장르 (검색할 장르명)"\n\n3. 모든 장르 목록 보기\n=> "모든 장르"\n\n4. 도움말 다시 보기\n=> "도움말"'
    elif content == '모든 장르':
        text = '\n'.join(GENRE_LIST)
    elif title_match or genre_match:
        if title_match:
            content_match = title_match
            search_type = TITLE
        elif genre_match:
            content_match = genre_match
            search_type = GENRE
        start_index = content_match.end()
        search_word = content[start_index:].strip()
        text = get_message_text(search_word, search_type)

    data= {
        "message": {
            "text": text,
        },
        "keyboard": {
            "type": "text",
        }
    }

    return jsonify(data)


def get_message_text(search_word, search_type):
    if search_word:
        if search_type == TITLE:
            if len(search_word) < 2:
                return '검색할 제목은 최소 2글자 이상이어야 합니다.'
            title_list = get_title_list_of_movies(title=search_word)
        if search_type == GENRE:
            if search_word.lower() not in GENRE_LIST:
                return '존재하지 않는 장르입니다.'
            title_list = get_title_list_of_movies(genre=search_word)
        naver_movie_info_list = []
        for title in title_list:
            movie_info = get_naver_movie_info(title)
            if movie_info:
                naver_movie_info_list.append(movie_info)
        text = '\n'.join(naver_movie_info_list)
        if not text:
            return '검색된 영화가 없습니다.'
        return text
    return '검색어를 입력하세요.'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8090)
