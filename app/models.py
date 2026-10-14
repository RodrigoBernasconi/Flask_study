from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100))
    name = db.Column(db.String(100))
    nickname = db.Column(db.String(100))
    password = db.Column(db.String(100))


class Filmes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_criacao = db.Column(db.DateTime, nullable=True, default=datetime.now())
    titulo = db.Column(db.String, nullable=True)
    ano = db.Column(db.Integer, nullable=True)
    resumo = db.Column(db.String, nullable=True)
    image = db.Column(db.String, default='default.png')
