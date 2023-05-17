from flask import Blueprint

#Blueprint for application
views = Blueprint('views', __name__)

@views.route("/")
def home():
    return "<h1>Test</h1>"

