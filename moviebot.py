import re

from flask import Flask, request, jsonify

from utils import get_movie_list, formalize_movie
 

ALL = 0
GENRE = 1
ACTOR = 2
DIRECTOR = 3
GENRE_LIST = ['드라마', '판타지', '서부', '공포', '로맨스', '모험', '스릴러', '느와르', '컬트', '다큐멘터리',
              '코미디', '가족', '미스터리', '전쟁', '애니메이션', '범죄', '뮤지컬', 'SF', '액션', '무협',
              '에로', '서스펜스', '서사', '블랙코미디', '실험', '영화카툰', '영화음악', '영화패러디포스터',]
 
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

    with open('./log/query.log', 'a') as log_file:
        log_file.write(content + '\n')

    genre_match = re.search(r'^장르 *', content)
    actor_match = re.search(r'^배우 *', content)
    director_match = re.search(r'^감독 *', content)

    text = ''
    if content in ['시작하기', '도움말']:
        text = '[도움말]\n\n1. 전체 추천\n=> "전체"\n\n2. 장르별 추천\n=> "장르 (검색할 장르명)"\n\n3. 배우별 추천\n=> "배우 (검색할 배우명)"\n\n4. 감독별 추천\n=> "감독 (검색할 감독명)"\n\n5. 검색 가능 장르 보기\n=> "전체 장르"\n\n6. 도움말 다시 보기\n=> "도움말"'
    elif content == '전체':
        text = get_message_text(ALL)
    elif content == '전체 장르':
        text = '\n'.join(GENRE_LIST)
    elif genre_match or actor_match or director_match:
        if genre_match:
            content_match = genre_match
            search_type = GENRE
        elif actor_match:
            content_match = actor_match
            search_type = ACTOR
        elif director_match:
            content_match = director_match
            search_type = DIRECTOR
        start_index = content_match.end()
        search_word = content[start_index:].strip()
        text = get_message_text(search_type, search_word)

    data= {
        "message": {
            "text": text,
        },
        "keyboard": {
            "type": "text",
        }
    }

    return jsonify(data)


def get_message_text(search_type, search_word=''):
    if search_type == ALL:
        movie_list = get_movie_list()
    else:
        if not search_word:
            return '검색어를 입력하세요.'

        if search_type == GENRE:
            if search_word not in GENRE_LIST:
                return '존재하지 않는 장르입니다.'
            movie_list = get_movie_list(genre=search_word)
        elif search_type == ACTOR:
            movie_list = get_movie_list(actor=search_word)
        elif search_type == DIRECTOR:
            movie_list = get_movie_list(director=search_word)

    if not movie_list:
        return '검색된 영화가 없습니다.'

    formatted_movie_list = []
    for movie in movie_list:
        formatted_movie_list.append(formalize_movie(movie))
    text = '\n'.join(formatted_movie_list)
    return text


if __name__ == "__main__":
    app.run(host='0.0.0.0')
