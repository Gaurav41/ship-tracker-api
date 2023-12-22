

from flask import Blueprint, jsonify, render_template
from flask_cors import cross_origin


home = Blueprint("home",__name__)


@home.route("/", methods=['GET'])
@cross_origin()
def get_ships():
    """ GET API 
        Return welcome message
    """
    # return jsonify({"message":"Welcome"})
    return render_template("index.html")

