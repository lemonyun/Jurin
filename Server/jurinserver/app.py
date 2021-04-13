from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import make_response
from sqlalchemy import func
from flask_restx import Api, Resource

import os
import json
import time
from collections import defaultdict
from datetime import datetime, date, timedelta

migrate = Migrate()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:\\Jurin\\Server\\jurinserver.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False

api = Api(app)
db = SQLAlchemy(app)

from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler(daemon=True)
scheduler.start()

def dbUpdate():
    os.system("python ../setupdb.py")
## 스케줄링으로 setupdb.py가 실행되는 도중에는 trend rank가 표시되지 않음

scheduler.add_job(dbUpdate, trigger="cron", hour='08', minute='55')
scheduler.add_job(dbUpdate, trigger="cron", hour='12', minute='00')
scheduler.add_job(dbUpdate, trigger="cron", hour='15', minute='00')
scheduler.add_job(dbUpdate, trigger="cron", hour='18', minute='00')
scheduler.add_job(dbUpdate, trigger="cron", hour='23', minute='55')


class TodayRank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(200), nullable=False)

class WeekRank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(200), nullable=False)

class Title(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())

@api.route('/todaytrend')
class Todaytrend(Resource):
    def get(self):
        # today = time.strftime("%y-%m-%d", time.localtime(time.time()))
        keyword_list = TodayRank.query.filter(func.date(Title.date) == date.today()).all()

        jsondict = defaultdict(list)

        for keyword in keyword_list:
            jsondict['trend'].append({'name':keyword.keyword,'count':keyword.id})

        a = dict(jsondict)

        b = json.dumps(a, ensure_ascii=False, indent=4)
        res = make_response(b)
        return res

@api.route('/weektrend')
class Weektrend(Resource):
    def get(self):
        today = time.strftime("%y-%m-%d", time.localtime(time.time()))
        print(type(today))
        keyword_list = WeekRank.query.filter(Title.date.between(datetime.now() + timedelta(days=-6), datetime.now()))

        jsondict = defaultdict(list)

        for keyword in keyword_list:
            jsondict['trend'].append({'name': keyword.keyword, 'count': keyword.id})

        a = dict(jsondict)

        b = json.dumps(a, ensure_ascii=False, indent=4)
        res = make_response(b)
        return res

@api.route('/title/<keyword>')
class News(Resource):
    def get(self, keyword):

        title_list = Title.query.filter(Title.title.like('%'+keyword+'%')).order_by(Title.id.desc())

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

