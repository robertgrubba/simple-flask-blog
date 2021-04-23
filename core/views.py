from flask import Blueprint, render_template, make_response, send_from_directory, url_for, redirect
from models import Page,Category,Tag
from sqlalchemy import extract
from bs4 import BeautifulSoup
import datetime

core_bp = Blueprint('core_bp',__name__,template_folder='templates')

@core_bp.route('/')
@core_bp.route('/page/<int:page>')
def index(page=1):
    per_page=5
    posts = Page.query.filter_by(published=True).order_by(Page.created.desc()).paginate(page,per_page,error_out=False)
    recent_posts = Page.query.filter_by(published=True).order_by(Page.created.desc()).limit(5)
    archives = Page.query.filter_by(published=True).group_by(extract('year',Page.created),extract('month',Page.created)).order_by(Page.created.desc()).all()
    categories = Category.query.all()
    referer = "index"
    return render_template('core/index.html',posts=posts,recent_posts=recent_posts,archives=archives,categories=categories, ref=referer)

@core_bp.route('/category/<string:slug>/')
@core_bp.route('/category/<string:slug>/<int:page>')
def category(slug,page=1):
    per_page=5
    posts = Page.query.join(Category.pages).filter(Category.slug==slug,Page.published==True).order_by(Page.created.desc()).paginate(page,per_page,error_out=False)
    recent_posts = Page.query.filter_by(published=True).order_by(Page.created.desc()).limit(5)
    archives = Page.query.filter_by(published=True).group_by(extract('year',Page.created),extract('month',Page.created)).order_by(Page.created.desc()).all()
    categories = Category.query.all()
    return render_template('core/category.html',posts=posts,recent_posts=recent_posts,categories=categories,archives=archives,slug=slug)

@core_bp.route('/tag/<string:slug>/')
@core_bp.route('/tag/<string:slug>/<int:page>')
def tag(slug,page=1):
    per_page=5
    posts = Page.query.join(Tag.pages).filter(Tag.slug==slug,Page.published==True).order_by(Page.created.desc()).paginate(page,per_page,error_out=False)
    recent_posts = Page.query.filter_by(published=True).order_by(Page.created.desc()).limit(5)
    archives = Page.query.filter_by(published=True).group_by(extract('year',Page.created),extract('month',Page.created)).order_by(Page.created.desc()).all()
    categories = Category.query.all()
    return render_template('core/tag.html',posts=posts,recent_posts=recent_posts,categories=categories,archives=archives,slug=slug)

@core_bp.route('/<string:slug>/')
def page(slug):
    requested_post = Page.query.filter_by(slug=slug,published=True).first_or_404()
    if post:
        return render_template('core/post.html',post=requested_post,date=datetime.datetime.strftime(requested_post.created, "%d %B %Y"),short=BeautifulSoup(requested_post.content,"html.parser").text.lstrip().rstrip()[0:52])
    else:
        return render_template('index.html')

@core_bp.route('/<int:year>/<int:month>/<string:slug>/')
def post(year,month,slug):
    requested_post = Page.query.filter(extract('year',Page.created)==year,extract('month',Page.created)==month).filter_by(slug=slug,published=True).first_or_404()
    if post:
        return render_template('core/post.html',post=requested_post,date=datetime.datetime.strftime(requested_post.created, "%d %B %Y"),short=BeautifulSoup(requested_post.content,"html.parser").text.lstrip().rstrip()[0:52])
    else:
        return render_template('index.html')

@core_bp.route('/<int:year>/<int:month>/')
def month(year,month,page=1):
    per_page=5
    posts = Page.query.filter(extract('year',Page.created)==year,extract('month',Page.created)==month).filter_by(published=True).order_by(Page.created.desc()).paginate(page,per_page,error_out=False)
    if posts:
        return render_template('core/month.html',posts=posts,year=year,month=month)
    else:
        return render_template('index.html')

@core_bp.route('/p/<int:postid>/')
def post_by_id(postid):
    requested_post = Page.query.filter_by(id=postid,published=True).first_or_404()
    if post:
        return render_template('core/post.html',post=requested_post,date=datetime.datetime.strftime(requested_post.created, "%d %B %Y"),short=BeautifulSoup(requested_post.content,"html.parser").text.lstrip().rstrip()[0:52])
    else:
        return render_template('index.html')

@core_bp.route('/category/<string:slug>/feed/')
def category_feed(slug):
    pages = Page.query.filter_by(published=True).order_by(Page.created.desc()).limit(10)
    for page in pages:
        page.content = page.content.replace('&oacute;','ó').replace('&ndash;',' ').replace('&nbsp;',' ')
    template = render_template('core/feed.html',pages=pages,slug=slug)
    response = make_response(template)
    response.headers['Content-Type'] = 'application/xml'
    return response

@core_bp.route('/feed/')
def main_feed():
    pages = Page.query.filter_by(published=True).order_by(Page.created.desc()).limit(20)
    for page in pages:
        page.content = page.content.replace('&oacute;','ó').replace('&ndash;',' ').replace('&nbsp;',' ')
    template = render_template('core/feed.html',pages=pages)
    response = make_response(template)
    response.headers['Content-Type'] = 'application/xml'
    return response


@core_bp.route('/raport_klifowy.pdf')
def raport_klifowy():
    return redirect(url_for('static',filename='raport_klifowy.pdf'))

@core_bp.route('/raport_sudety.pdf')
def raport_sudety():
    return redirect(url_for('static',filename='raport_sudety.pdf'))

@core_bp.route('/raport_beskidwyspowy.pdf')
def raport_beskid_wyspowy():
    return redirect(url_for('static',filename='raport_beskidwyspowy.pdf'))

@core_bp.route('/weather_forecast.pdf')
def raport_beskid_wyspowy():
    return redirect(url_for('static',filename='weather_forecast.pdf'))
