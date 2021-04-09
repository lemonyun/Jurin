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

class Rank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(200), nullable=False)

class Title(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)

@api.route('/trend')
class Trend(Resource):
    def get(self):
        keyword_list = Rank.query.all()

        jsondict = defaultdict(list)

        for keyword in keyword_list:
            jsondict['trend'].append({'name':keyword.keyword,'count':keyword.id})

        a = dict(jsondict)

        b = json.dumps(a, ensure_ascii=False, indent=4)
        res = make_response(b)
        return res

@api.route('/title/<keyword>')
class News(Resource):
    def get(self, keyword):

        title_list = Title.query.filter(Title.title.like('%'+keyword+'%'))

        jsondict = defaultdict(list)

        for title in title_list:
            jsondict['titles'].append({'title':title.title})
        a = dict(jsondict)
        b = json.dumps(a, ensure_ascii=False, indent=4)
        res = make_response(b)
        return res


if __name__ == "__main__":
    db.init_app(app)
    migrate.init_app(app, db)
    app.run(host='0.0.0.0', port=5000)

