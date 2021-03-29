from flask import Blueprint, render_template
from jurinserver.models import title, rank

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'

@bp.route('/')
def index():
    rank_list = rank.query.order_by(rank.id.asc())
    return render_template('index.html', rank_list=rank_list)



@bp.route('/<string:keyword>/')
def detail(keyword):
    title_list = title.query.filter(title.title.like('%' + keyword + '%')).all()
    return render_template('keyword_detail.html', title_list=title_list)