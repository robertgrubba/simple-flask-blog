from flask import Blueprint, render_template
from models import Page
from sqlalchemy import extract
from bs4 import BeautifulSoup
import datetime

post_bp = Blueprint('core_bp',__name__,template_folder='templates')

@post_bp.route('/')
def index():
        return render_template('index.html')

@post_bp.route('/<int:year>/<int:month>/<string:slug>/')
def post(year,month,slug):
    requested_post = Page.query.filter(extract('year',Page.created)==year,extract('month',Page.created)==month).filter_by(slug=slug).first_or_404()
    if post:
        return render_template('post/post.html',post=requested_post,date=datetime.datetime.strftime(requested_post.created, "%d %B %Y"),short=BeautifulSoup(requested_post.content,"html.parser").text.lstrip().rstrip()[0:52])
    else:
        return render_template('index.html')

@post_bp.route('/p/<int:postid>/')
def post_by_id(postid):
    requested_post = Page.query.filter_by(id=postid).first_or_404()
    if post:
        return render_template('post/post.html',post=requested_post,date=datetime.datetime.strftime(requested_post.created, "%d %B %Y"),short=BeautifulSoup(requested_post.content,"html.parser").text.lstrip().rstrip()[0:52])
    else:
        return render_template('index.html')
