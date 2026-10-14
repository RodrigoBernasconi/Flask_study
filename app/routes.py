from flask import render_template, url_for, jsonify, redirect
from flask_login import login_required, login_user, logout_user

from app import app
from app.forms import FilmeForm, UserForm, LoginForm
from app.models import Filmes

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.login()
        login_user(user, remember=True)
        return redirect(url_for('homepage'))
    return render_template('login.html', form=form)

@app.route('/new_user', methods=['GET', 'POST'])
def newUser():
    form = UserForm()
    if form.validate_on_submit():
        user = form.get_user()
        login_user(user, remember=True)
        return redirect(url_for('homepage'))
    return render_template('new_user.html', form=form)

@app.route('/calcular/<int:valor>')
def calcular(valor):
    context = {
        'valor': valor,
        'valor_dobro': valor * 2
    }
    return render_template('calcular.html', context=context)

@app.route('/api/dados')
def dados():
    dados = {'mensagem': 'Dados do back-end'}
    return jsonify(dados)

@app.route('/filmes/novo', methods=['GET', 'POST'])
@login_required
def novoFilme():
    form = FilmeForm()
    if form.validate_on_submit():
        form.save()
        return redirect(url_for('homepage'))
    
    return render_template('filme_novo.html', form=form)

@app.route('/filme/lista')
def listaFilme():
    filmes = Filmes.query.order_by(Filmes.titulo.desc()).all()
    return render_template('filme_lista.html', objects=filmes)

@app.route('/filme/<int:id>')
def detailFilme(id):
    filme = Filmes.query.get(id)
    return render_template('filme_detail.html', object=filme)

@app.route('/')
def homepage():
    context = {
        'usuario': 'Rodrigo',
        'idade': 24
    }
    return render_template('index.html', context=context)