from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Привет! Это мой первый магазин на Flask!</h1>"

if __name__ == '__main__':
    app.run(debug=True)