from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

today_data = {}

@app.route('/api/update-today', methods=['POST'])
def update_today():
    global today_data
    today_data = request.get_json()
    print("Received from extension:", today_data)
    return jsonify({"status": "ok", "received": today_data})

# @app.route('/api/today')
@app.route('/')
def get_today():
    return jsonify(today_data)

if __name__ == '__main__':
    app.run(debug=True)
