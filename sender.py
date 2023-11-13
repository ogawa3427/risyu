from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/example', methods=['GET'])
def get_example():
    data = {"message": "Hello, World!"}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
