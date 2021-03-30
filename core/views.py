from flask import Blueprint, render_template
from models import Page,Category
from sqlalchemy import extract
from bs4 import BeautifulSoup
import datetime

core_bp = Blueprint('core_bp',__name__,template_folder='templates')

@core_bp.route('/')
@core_bp.route('/page/<int:page>')
def index(page=1):
    per_page=5
    posts = Page.query.order_by(Page.created.desc()).paginate(page,per_page,error_out=False)
    recent_posts = Page.query.order_by(Page.created.desc()).limit(5)
    archives = Page.query.group_by(extract('year',Page.created),extract('month',Page.created)).order_by(Page.created.desc()).all()
    referer = "index"
    return render_template('core/index.html',posts=posts,recent_posts=recent_posts,archives=archives, ref=referer)

@core_bp.route('/category/<string:cat>/')
def category(cat):
    posts = Page.query.join(Category.pages).filter(Category.name==cat).all()
    recent_posts = Page.query.order_by(Page.created.desc()).limit(5)
    archives = Page.query.group_by(extract('year',Page.created),extract('month',Page.created)).order_by(Page.created.desc()).all()
    return render_template('core/category.html',posts=posts,recent_posts=recent_posts,archives=archives)

@core_bp.route('/<int:year>/<int:month>/<string:slug>/')
def post(year,month,slug):
    requested_post = Page.query.filter(extract('year',Page.created)==year,extract('month',Page.created)==month).filter_by(slug=slug).first_or_404()
    if post:
        return render_template('core/post.html',post=requested_post,date=datetime.datetime.strftime(requested_post.created, "%d %B %Y"),short=BeautifulSoup(requested_post.content,"html.parser").text.lstrip().rstrip()[0:52])
    else:
        return render_template('index.html')

@core_bp.route('/<int:year>/<int:month>/')
def month(year,month,page=1):
    per_page=5
    posts = Page.query.filter(extract('year',Page.created)==year,extract('month',Page.created)==month).order_by(Page.created.desc()).paginate(page,per_page,error_out=False)
    if posts:
        return render_template('core/month.html',posts=posts,year=year,month=month)
    else:
        return render_template('index.html')

@core_bp.route('/p/<int:postid>/')
def post_by_id(postid):
    requested_post = Page.query.filter_by(id=postid).first_or_404()
    if post:
        return render_template('core/post.html',post=requested_post,date=datetime.datetime.strftime(requested_post.created, "%d %B %Y"),short=BeautifulSoup(requested_post.content,"html.parser").text.lstrip().rstrip()[0:52])
    else:
        return render_template('index.html')
