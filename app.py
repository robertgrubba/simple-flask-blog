from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import calendar

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.template_filter('month_name')
def month_name(month_number):
   return calendar.month_name[month_number]

db = SQLAlchemy(app)
from models import Page, Tag, Category
migrate = Migrate(app,db)

from core.views import core_bp
app.register_blueprint(core_bp)
