import os

from flask import Flask, request, jsonify
 
 
app = Flask(__name__)
 
 
@app.route('/keyboard')
def keyboard():
 
    dataSend = {
        "type" : "text",
    }
 
    return jsonify(dataSend)


@app.route('/message', methods=['POST'])
def message():
    
    dataReceive = request.get_json()
    content = dataReceive['content']
 
    dataSend = {
        "message": {
            "text": content,
        }
    }

    return jsonify(dataSend)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8090)
