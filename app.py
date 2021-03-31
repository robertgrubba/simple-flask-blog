from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.template_filter('month_name')
def month_name(month_number):
    miesiace = {
            1:"Styczeń",
            2:"Luty",
            3:"Marzec",
            4:"Kwiecień",
            5:"Maj",
            6:"Czerwiec",
            7:"Lipiec",
            8:"Sierpień",
            9:"Wrzesień",
            10:"Październik",
            11:"Listopad",
            12:"Grudzień"
    }
    return miesiace[month_number]

@app.template_filter('show_all_attrs')
def show_all_attrs(value):
    res = []
    for k in dir(value):
        res.append('%r %r\n' % (k, getattr(value, k)))
    return '\n'.join(res)

db = SQLAlchemy(app)
from models import Page, Tag, Category
migrate = Migrate(app,db)

from core.views import core_bp
app.register_blueprint(core_bp)
