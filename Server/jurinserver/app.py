from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from flask import jsonify

from flask_restx import Api, Resource

migrate = Migrate()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:\\Jurin\\Server\\jurinserver.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


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

        jsonstr = '{"trend"['
        for keyword in keyword_list:
            jsonstr += '{"name":' + '"' + keyword.keyword + '","count":' + str(keyword.id) + '},'

        jsonstr += ']}'

        return jsonify(jsonstr)


if __name__ == "__main__":
    db.init_app(app)
    migrate.init_app(app, db)
    app.run(host='0.0.0.0', port=5000)

