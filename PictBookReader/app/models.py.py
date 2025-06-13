from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

class User(UserMixin, db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())) # [cite: 6]
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class BookTag(db.Model):
    book_id = db.Column(db.String(36), db.ForeignKey('book.id'), primary_key=True) # [cite: 7]
    tag = db.Column(db.String(50), primary_key=True)

class Bookmark(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    book_id = db.Column(db.String(36), db.ForeignKey('book.id'))
    page = db.Column(db.Integer)
    note = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    book = db.relationship('Book', back_populates='bookmarks')

class Book(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(100), nullable=False)
    cover_path = db.Column(db.String(255), nullable=False)
    pdf_path = db.Column(db.String(255), nullable=False)
    last_read_page = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) # [cite: 8]
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    bookmarks = db.relationship('Bookmark', back_populates='book', cascade='all, delete-orphan')
    
    @property
    def tags(self):
        return [bt.tag for bt in BookTag.query.filter_by(book_id=self.id).all()]
    
    def add_tag(self, tag):
        if tag not in self.tags:
            book_tag = BookTag(book_id=self.id, tag=tag)
            db.session.add(book_tag)
    
    def remove_tag(self, tag): # [cite: 9]
        BookTag.query.filter_by(book_id=self.id, tag=tag).delete()
    
    def add_bookmark(self, page, note=''):
        bookmark = Bookmark(book_id=self.id, page=page, note=note)
        db.session.add(bookmark)
        return bookmark
    
    def get_bookmark(self, page):
        return Bookmark.query.filter_by(book_id=self.id, page=page).first()
    
    def remove_bookmark(self, page):
        Bookmark.query.filter_by(book_id=self.id, page=page).delete()