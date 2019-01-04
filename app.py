from flask import Flask, render_template, request
from models import Team, League
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
debug = DebugToolbarExtension(app)


@app.route('/', methods=['GET'])
def show_homepage():
    return render_template()