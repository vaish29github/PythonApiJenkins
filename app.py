from flask import Flask,jsonify
app = Flask(__name__)
@app.route('/')
def hello():
    return jsonify({'message': 'Hello from Python API!'})
@app.route('/api/health')
def health():
    return jsonify({"status": 'API is running!'})

if __name__ =='__main__':
    app.run(host='0.0.0.0', port=5000)
