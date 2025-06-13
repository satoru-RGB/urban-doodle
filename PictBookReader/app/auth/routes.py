from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user
from flask_babel import gettext as _
from app import db
from app.auth import bp
from app.models import User
from app.auth.forms import LoginForm, RegistrationForm

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('ユーザー名またはパスワードが間違っています'), 'danger') # [cite: 11]
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('main.index')
        return redirect(next_page)
    
    return render_template('auth/login.html', title=_('ログイン'), form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index')) # [cite: 12]

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('アカウントの登録が完了しました！'), 'success') # [cite: 12]
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title=_('新規登録'), form=form)
