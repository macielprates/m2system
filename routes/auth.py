from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models.usuario import Usuario
from datetime import datetime

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        login_input = request.form.get('login', '').strip().upper()
        senha = request.form.get('senha', '')

        usuario = Usuario.query.filter_by(login=login_input, ativo=True).first()

        if usuario and usuario.verificar_senha(senha):
            usuario.dt_ultimo_acesso = datetime.now()
            from app import db
            db.session.commit()
            login_user(usuario, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard.index'))

        flash('Usuario ou senha incorretos.', 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
