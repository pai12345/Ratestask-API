""" Xeneta's Rate API task

    Application having details, functionality and information for fetcing average prices and uploading prices.
"""

from flask import Flask, Response
from src.ratestask.api.routes.routes import router

app = Flask(__name__)
app.register_blueprint(router, url_prefix='/')


@app.route("/", methods=['GET'])
def welcome():
    """ Welcome Page.

        Page with a welcome greeting.
    """
    try:
        return Response("<h1>Welcome to Xeneta's Rate task API<h1>", status=200)
    except (BaseException) as error:
        return {"status": "error", "message": f"""Encountered Error for Welcome Page: {error}"""}


app.run()
