import os

from flask import Flask, request, jsonify

from utils import get_title_list_of_movies
from utils import get_naver_movie_info
 
 
app = Flask(__name__)
 
 
@app.route('/keyboard')
def keyboard():
 
    dataSend = {
        "type" : "text",
    }
 
    return jsonify(dataSend)


@app.route('/message', methods=['POST'])
def message():
    json_data = request.get_json()
    content = json_data['content']
 
    title_list = get_title_list_of_movies(title=content)
    naver_movie_info_list = []
    for title in title_list:
        movie_info = get_naver_movie_info(title)
        if movie_info:
            naver_movie_info_list.append(movie_info)
    text = '\n'.join(naver_movie_info_list)
    data= {
        "message": {
            "text": text,
        }
    }

    return jsonify(data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8090)
