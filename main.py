# Import flask standard libraries
from flask import Flask, render_template, request

# Import from Utils
from utils import *


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/')
def home():
    # Count page view
    count_pageview()

    # Render template
    return render_template('index.html')

@app.route('/search')
def search():
    # Get parameters from url
    param = str(request.args.get('param'))

    # Make request to RSS3
    data = query_address(param)

    # Count page view
    count_pageview()

    # Render template
    return render_template('search.html', data=data)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. You
    # can configure startup instructions by adding `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
