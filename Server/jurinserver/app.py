from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from collections import defaultdict
from flask import make_response

from flask_restx import Api, Resource

import json

migrate = Migrate()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:\\Jurin\\Server\\jurinserver.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False

api = Api(app)
db = SQLAlchemy(app)

class rank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(200), nullable=False)

class title(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)

@api.route('/trend')
class Trend(Resource):
    def get(self):
        keyword_list = rank.query.all()

        jsondict = defaultdict(list)

        for keyword in keyword_list:
            jsondict['trend'].append({'name':keyword.keyword,'count':keyword.id})

        a = dict(jsondict)

        bb = json.dumps(a, ensure_ascii=False, indent=4)
        res = make_response(bb)
        return res


if __name__ == "__main__":
    db.init_app(app)
    migrate.init_app(app, db)
    app.run(host='0.0.0.0', port=5000)

