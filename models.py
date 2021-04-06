import datetime
from flask_security import current_user, Security, SQLAlchemyUserDatastore, UserMixin
from app import db
from sqlalchemy.sql import func

#db=SQLAlchemy()

tags = db.Table('tags', db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True), db.Column('page_id', db.Integer, db.ForeignKey('page.id'), primary_key=True))
categories = db.Table('categories', db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True),db.Column('page_id', db.Integer, db.ForeignKey('page.id'), primary_key=True))

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120),unique=True)
    slug = db.Column(db.String(255),unique=True)

    def __repr__(self):
        return '<Tag %r>' % self.name

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255),nullable=False)
    slug = db.Column(db.String(255),nullable=False)
    content = db.Column(db.Text)
    created = db.Column(db.DateTime,nullable=False,default=func.now())
    modified = db.Column(db.DateTime,onupdate=func.now())
    tags = db.relationship('Tag', secondary=tags, lazy='subquery', backref=db.backref('pages', lazy=True))
    categories = db.relationship('Category', secondary=categories, lazy='subquery', backref=db.backref('pages', lazy=True))

    def __repr__(self):
        return '<Page %r>' % self.slug

class Category(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(120),unique=True)
    slug = db.Column(db.String(255),unique=True)

    def __repr__(self):
        return '<Cagegory %r>' % self.name

roles_users_table = db.Table('roles_users',
                            db.Column('users_id', db.Integer(), db.ForeignKey('users.id')),
                            db.Column('roles_id', db.Integer(), db.ForeignKey('roles.id')))

class Roles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(80))
    active = db.Column(db.Boolean())

    roles = db.relationship('Roles', secondary=roles_users_table, backref='user', lazy=True)

