from flask import Flask
import time
app = Flask(__name__)

@app.route('/')
def hello_world():
    time.sleep(70)
    return 'Hello, World!'       

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
