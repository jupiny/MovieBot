import os

from flask import Flask, request, jsonify
 
 
app = Flask(__name__)
 
 
@app.route('/keyboard')
def Keyboard():
 
    dataSend = {
        "type" : "buttons",
        "buttons" : ["시작하기", "도움말"]
    }
 
    return jsonify(dataSend)


@app.route('/message', methods=['POST'])
def Message():
    
    dataReceive = request.get_json()
    content = dataReceive['content']
 
    if content == "시작하기":
        dataSend = {
            "message": {
                "text": "시작하기"
            }
        }
    elif content == "도움말":
        dataSend = {
            "message": {
                "text": "도움말"
            }
        }
    return jsonify(dataSend)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 5000)
