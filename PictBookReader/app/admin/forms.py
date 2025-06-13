from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField # Removed FileRequired as it's used inline
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask_babel import lazy_gettext as _l
from app.models import User

class AddUserForm(FlaskForm):
    username = StringField(_l('ユーザー名'), validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField(_l('パスワード'), validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField( # [cite: 29]
        _l('パスワード（確認用）'), validators=[DataRequired(), EqualTo('password')])
    is_admin = BooleanField(_l('管理者権限')) # [cite: 29]
    submit = SubmitField(_l('追加')) # [cite: 29]
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_l('このユーザー名は既に使用されています。別のユーザー名を選択してください。')) # [cite: 29]

class AddBookForm(FlaskForm):
    title = StringField(_l('タイトル'), validators=[DataRequired(), Length(max=100)])
    tags = StringField(_l('タグ（カンマ区切り）'))
    pdf_file = FileField(_l('PDFファイル'), validators=[
        DataRequired(message=_l('PDFファイルを選択してください。')), # Replaced FileRequired with DataRequired for consistency with message
        FileAllowed(['pdf'], _l('PDFファイルのみアップロード可能です')) # [cite: 30]
    ])
    cover_file = FileField(_l('カバー画像（任意）'), validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], _l('画像ファイルのみアップロード可能です')) # [cite: 30]
    ])
    submit = SubmitField(_l('追加'))
