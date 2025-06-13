import os
from flask import Flask, request, g, session # request, g, session をインポート [cite: 3]
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_babel import Babel, gettext as _ # Babel と gettext (エイリアスとして _) をインポート [cite: 3]
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
# login_manager.login_message = 'このページにアクセスするにはログインが必要です。' # ← これはBabelで翻訳するため削除またはコメントアウト [cite: 3]
login_manager.login_message_category = 'info'
babel = Babel() # Babelオブジェクトを作成 [cite: 3]

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    os.makedirs(app.config['PDF_FOLDER'], exist_ok=True)
    os.makedirs(app.config['COVER_FOLDER'], exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db) # [cite: 4]
    login_manager.init_app(app)
    babel.init_app(app) # Babelをアプリに初期化 [cite: 4]


    @babel.localeselector
    def get_locale():
        # ユーザーが言語を選択していればそれを使用 (セッション経由など、後のステップで実装) [cite: 4]
        if 'language' in session and session['language'] in app.config['LANGUAGES']:
            return session['language']
        # それ以外の場合は、ブラウザの言語設定から最適なものを選択 [cite: 4]
        return request.accept_languages.best_match(app.config['LANGUAGES'])

    @app.before_request
    def before_request():
        # 選択されたロケールをグローバル変数 g に保存し、テンプレートで参照できるようにする [cite: 4, 5]
        g.locale = str(get_locale())
        # Flask-Loginのメッセージも翻訳対象にする [cite: 5]
        login_manager.login_message = _('このページにアクセスするにはログインが必要です。')
 

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app
