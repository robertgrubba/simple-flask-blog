from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import helpers as admin_helpers
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user, Security, SQLAlchemyUserDatastore, UserMixin 
import dateutil.parser

app = Flask(__name__,static_url_path='/wp-content')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

app.config['SECRET_KEY'] = 'secretkey'
app.config['SECURITY_PASSWORD_SALT'] = 'none'
# Configure application to route to the Flask-Admin index view upon login
app.config['SECURITY_POST_LOGIN_VIEW'] = '/admin/'
# Configure application to route to the Flask-Admin index view upon logout
app.config['SECURITY_POST_LOGOUT_VIEW'] = '/admin/'
# Configure application to route to the Flask-Admin index view upon registering
app.config['SECURITY_POST_REGISTER_VIEW'] = '/admin/'
app.config['SECURITY_REGISTERABLE'] = True
# Configure application to not send an email upon registration
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False


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

@app.template_filter('xmltime')
def xmltime(date, fmt=None):
    date = dateutil.parser.parse(str(date))
    native = date.replace(tzinfo=None)
    format='%a, %d %b %Y %H:%M:%S %z'
    return native.strftime(format) 

@app.template_filter('startswith')
def starts_with(field):
    if field.startswith('<div class="entry-content">'):
            return True
    return False

db = SQLAlchemy(app)
from models import Page, Tag, Category,Roles, Users
migrate = Migrate(app,db)

# Create a datastore and instantiate Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, Users, Roles)
security = Security(app, user_datastore)

# Create the tables for the users and roles and add a user to the user table
# This decorator registers a function to be run before the first request to the app
#  i.e. calling localhost:5000 from the browser
#@app.before_first_request
#def create_user():
#    db.drop_all()
#    db.create_all()
#    user_datastore.create_user(email='admin', password='admin')
#    db.session.commit()



admin = Admin(app, name='Panel Administracyjny',base_template='my_master.html', template_mode='bootstrap4')
class UserModelView(ModelView):
    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated)

    def _handle_view(self, name):
        if not self.is_accessible():
            return redirect(url_for('security.login'))

#    column_list = ['email', 'password']

class PostEditView(ModelView):

    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated)

    def _handle_view(self, name):
        if not self.is_accessible():
            return redirect(url_for('security.login'))

    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_widget_args = dict(content={'class': 'form-control ckeditor'})
    column_exclude_list = ['content','modified']

# Add administrative views to Flask-Admin
admin.add_view(UserModelView(Users, db.session))
admin.add_view(UserModelView(Roles, db.session))
admin.add_view(PostEditView(Page,db.session))
admin.add_view(UserModelView(Category,db.session))
admin.add_view(UserModelView(Tag,db.session))


# Add the context processor
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template = admin.base_template,
        admin_view = admin.index_view,
        get_url = url_for,
        h = admin_helpers
    )


from core.views import core_bp
app.register_blueprint(core_bp)
