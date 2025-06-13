
import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///picture_book_reader.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    PDF_FOLDER = os.path.join(UPLOAD_FOLDER, 'pdf')
    COVER_FOLDER = os.path.join(UPLOAD_FOLDER, 'covers')
    THUMBNAIL_SIZE = (400, 600)
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    LANGUAGES = ['ja', 'en', 'km']  # 対応言語: 日本語, 英語, クメール語 [cite: 2]
    BABEL_DEFAULT_LOCALE = 'ja'     # デフォルト言語 [cite: 2, 3]
    BABEL_DEFAULT_TIMEZONE = 'UTC'  # デフォルトタイムゾーン (必要に応じて変更) [cite: 3]
