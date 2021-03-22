from flask import Blueprint, render_template
from models import Page
from sqlalchemy import extract

post_bp = Blueprint('core_bp',__name__,template_folder='templates')

@post_bp.route('/')
def index():
        return render_template('index.html')

@post_bp.route('/<int:year>/<int:month>/<string:slug>/')
def post(year,month,slug):
    requested_post = Page.query.filter(extract('year',Page.created)==year,extract('month',Page.created)==month).filter_by(slug=slug).first_or_404()
    if post:
        return render_template('post/post.html',post=requested_post)
    else:
        return render_template('index.html')
