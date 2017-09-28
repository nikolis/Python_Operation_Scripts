#!flask/bin/python3
from flask import Flask, jsonify
import src.impl.htmlproc as htmlproc
from src.impl.htmlproc import Recipe, IngredientEntry, IngredientEntrySet
from flask_cors import CORS
import json
from flask import Flask
from flask.ext.cors import CORS, cross_origin

rest_server = Flask(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   dog'
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:port"}})


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj,'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)

app = Flask(__name__)
CORS(app)

@rest_server.route('/')
@cross_origin(origin='localhost', headers=['Content- Type','Authorization'])
def index():
    recipe = Recipe()
    recipe =  htmlproc.get_next()
    return json.dumps(recipe.reprJSON(), cls=ComplexEncoder)


if __name__ =='__main__':
    rest_server.run(debug=True)

