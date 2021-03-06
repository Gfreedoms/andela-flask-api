
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from passlib.apps import custom_app_context as pwd_context

from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

db = SQLAlchemy()

from datetime import datetime


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]


# Create our database model
class User(db.Model):
    """This class represents the User table."""

    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(
        db.String(255), index=True, unique=False, nullable=False)
    token = db.Column(db.String(255), nullable=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = self.hash_password(password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def hash_password(self, password):
        return pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def generate_auth_token(self, expiration=10800):
        s = Serializer(
            "youll-never-know-what-it-is-coz-its-secret", expires_in=expiration)
        return s.dumps({'id': self.user_id})

    def invalidate_token(self):
        """nullify token fields"""
        self.token = None
        db.session.commit()

    def save_token(self, token):
        """nullify token fields"""
        self.token = token
        db.session.commit()

    def __repr__(self):
        return '<E-mail %r>' % self.email

    @staticmethod
    def verify_auth_token(token):
        s = Serializer("youll-never-know-what-it-is-coz-its-secret")
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user


class ShoppingList(db.Model):
    """This class represents the ShoppingList table."""

    __tablename__ = "shopping_list"

    list_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.user_id', ondelete='CASCADE'), nullable=False)
    __table_args__ = (db.UniqueConstraint(
        'name', 'user_id', name='_list_user_unique_column'),)

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
        self.date = datetime.now()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'list_id': self.list_id,
            'name': self.name,
            'date_time': dump_datetime(self.date)
        }

    @staticmethod
    def get_all(user_id, q, limit=10, page=1):
        query = ShoppingList.query.filter_by(user_id=user_id)

        if q is not None:
            query = query.filter(
                func.lower(ShoppingList.name).like("%"+q.lower().strip()+"%"))

        try:
            limit = int(limit)
            page = int(page)
        except:
            limit = None

        if limit is not None:
            return query.paginate(page, limit, False).items

        return query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<List Name %r>' % self.name


class ShoppingListItem(db.Model):
    """This class represents the ShoppingListItem table."""

    __tablename__ = "shopping_list_item"

    item_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    bought = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey(
        'shopping_list.list_id', ondelete='CASCADE'), nullable=False)
    __table_args__ = (db.UniqueConstraint(
        'name', 'list_id', name='_item_list_unique_column'),)

    def __init__(self, name, list_id, amount):
        self.name = name
        self.list_id = list_id
        self.date = datetime.now()
        self.amount = amount
        self.bought = 0

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(list_id, q, limit=10, page=1):

        query = ShoppingListItem.query.filter_by(list_id=list_id)

        if q is not None:
            query = query.filter(
                func.lower(ShoppingListItem.name).like("%"+q.lower().strip()+"%"))

        try:
            limit = int(limit)
            page = int(page)
        except:
            limit = None

        if limit is not None:
            return query.paginate(page, limit, False).items

        return query.all()

    @staticmethod
    def get_all_despite_list(user_id):
        q = ShoppingListItem.query\
            .join(ShoppingList)\
            .filter(ShoppingList.user_id == user_id)
        return q.all()

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'item_id': self.item_id,
            'list_id': self.list_id,
            'name': self.name,
            'date_time': dump_datetime(self.date),
            'amount': self.amount,
            'bought': self.bought,
        }

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Item Name %r>' % self.name
