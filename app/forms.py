import os

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, FileField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email
from werkzeug.utils import secure_filename

from app.models import Filmes, User
from app import db, bcrypt, app

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

    def login(self):
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, self.password.data):
                return user
            else:
                raise Exception('Incorrect Password')
        else:
            raise Exception('User not found')

class UserForm(FlaskForm):
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    nickname = StringField('Nickname', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Salvar')

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('Username já utilizado, favor utilize outro!!!')

    def save(self):
        password = bcrypt.generate_password_hash(self.password.data.encode('utf-8'))
        user = User(
            email = self.email.data,
            username = self.username.data,
            name = self.name.data,
            nickname = self.nickname.data,
            password = password,
        )
        db.session.add(user)
        db.session.commit()

        return user

    def get_user(self):
        self.save()
        return User.query.filter_by(username=self.username.data).first()

class FilmeForm(FlaskForm):
    titulo = StringField('Titulo', validators=[DataRequired()])
    ano = StringField('Ano', validators=[DataRequired()])
    resumo = TextAreaField('Resumo', validators=[DataRequired()])
    image = FileField('Imagem', validators=[DataRequired()])
    submit = SubmitField('Salvar')

    def validate_titulo(self, titulo):
        if Filmes.query.filter_by(titulo=titulo.data).first():
            raise ValidationError('Este Filme já foi incluso!!!')

    def save(self):
        file = self.image.data
        safe_name = secure_filename(file.filename)
        path_way = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),     # Recupera o caminho absoluto onde o arquivo routes.py está armazenado
            app.config['UPLOAD_FOLDER'],                    # Define a pasta de Upload que criamos
            'filmes',                                       # Define a pasta de Filmes que criamos para organizar nossos arquivos
            safe_name                                       # Define o nome seguro para o caminho
        )
        filme = Filmes(
            titulo = self.titulo.data,
            ano = self.ano.data,
            resumo = self.resumo.data,
            image=safe_name
        )
        os.makedirs(os.path.dirname(path_way), exist_ok=True)
        file.save(path_way)
        db.session.add(filme)
        db.session.commit()