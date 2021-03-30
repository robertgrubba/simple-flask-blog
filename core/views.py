from flask import Blueprint, render_template
from models import Page
from sqlalchemy import extract
from bs4 import BeautifulSoup
import datetime

core_bp = Blueprint('core_bp',__name__,template_folder='templates')

@core_bp.route('/')
@core_bp.route('/page/<int:page>')
def index(page=1):
    per_page=5
    posts = Page.query.order_by(Page.created.desc()).paginate(page,per_page,error_out=False)
    return render_template('core/index.html',posts=posts)

@core_bp.route('/<int:year>/<int:month>/<string:slug>/')
def post(year,month,slug):
    requested_post = Page.query.filter(extract('year',Page.created)==year,extract('month',Page.created)==month).filter_by(slug=slug).first_or_404()
    if post:
        return render_template('core/post.html',post=requested_post,date=datetime.datetime.strftime(requested_post.created, "%d %B %Y"),short=BeautifulSoup(requested_post.content,"html.parser").text.lstrip().rstrip()[0:52])
    else:
        return render_template('index.html')

@core_bp.route('/p/<int:postid>/')
def post_by_id(postid):
    requested_post = Page.query.filter_by(id=postid).first_or_404()
    if post:
        return render_template('core/post.html',post=requested_post,date=datetime.datetime.strftime(requested_post.created, "%d %B %Y"),short=BeautifulSoup(requested_post.content,"html.parser").text.lstrip().rstrip()[0:52])
    else:
        return render_template('index.html')
