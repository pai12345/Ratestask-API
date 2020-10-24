from flask import Flask
from src.ratestask.api.routes.routes import router
from src.ratestask.helper.helper import helper

app = Flask(__name__)
app.register_blueprint(router, url_prefix='/')


@app.route("/", methods=['GET'])
def welcome():
    try:
        return "<h1>Welcome to Xeneta - ratestask<h1>"
    except (BaseException) as error:
        raise error


app.run()
