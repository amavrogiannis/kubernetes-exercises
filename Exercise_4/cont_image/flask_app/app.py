from flask import Flask, render_template
import os

app = Flask(__name__)


@app.route('/')
def home():
    user_var = os.getenv("TV_ENV")
    return render_template('index.html', user_var=user_var)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
