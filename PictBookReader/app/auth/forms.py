from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask_babel import lazy_gettext as _l # lazy_gettext for forms
from app.models import User

class LoginForm(FlaskForm):
    username = StringField(_l('ユーザー名'), validators=[DataRequired()]) # [cite: 13]
    password = PasswordField(_l('パスワード'), validators=[DataRequired()]) # [cite: 13]
    remember_me = BooleanField(_l('ログイン状態を保持')) # [cite: 13]
    submit = SubmitField(_l('ログイン')) # [cite: 13]

class RegistrationForm(FlaskForm):
    username = StringField(_l('ユーザー名'), validators=[DataRequired(), Length(min=3, max=20)]) # [cite: 13]
    password = PasswordField(_l('パスワード'), validators=[DataRequired(), Length(min=6)]) # [cite: 13]
    password2 = PasswordField(
        _l('パスワード（確認用）'), validators=[DataRequired(), EqualTo('password')]) # [cite: 13]
    submit = SubmitField(_l('登録')) # [cite: 13]
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first() # [cite: 14]
        if user is not None:
            raise ValidationError(_l('このユーザー名は既に使用されています。別のユーザー名を選択してください。')) # [cite: 14]
