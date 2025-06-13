from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user # [cite: 21]
from flask_babel import gettext as _
from app import db
from app.admin import bp
from app.models import User, Book, BookTag
from app.admin.forms import AddUserForm, AddBookForm
from app.utils import save_pdf, save_cover, generate_thumbnail
import os

def admin_required(f):
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash(_('管理者権限が必要です'), 'danger') # [cite: 21]
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__ # to avoid overwriting endpoint name
    return decorated_function

@bp.route('/')
@admin_required
def index():
    return render_template('admin/index.html', title=_('管理パネル'))

@bp.route('/users')
@admin_required
def users(): # [cite: 22]
    users_list = User.query.all()
    return render_template('admin/users.html', title=_('ユーザー管理'), users=users_list)

@bp.route('/users/add', methods=['GET', 'POST'])
@admin_required
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, is_admin=form.is_admin.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('ユーザー「{}」を追加しました').format(form.username.data), 'success') # [cite: 22]
        return redirect(url_for('admin.users'))
    return render_template('admin/add_user.html', title=_('ユーザー追加'), form=form)

@bp.route('/users/<string:id>/delete', methods=['POST'])
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    if user.id == current_user.id: # [cite: 23]
        flash(_('自分自身を削除することはできません'), 'danger') # [cite: 23]
    else:
        db.session.delete(user)
        db.session.commit()
        flash(_('ユーザー「{}」を削除しました').format(user.username), 'success') # [cite: 23]
    return redirect(url_for('admin.users'))

@bp.route('/books')
@admin_required
def books():
    books_list = Book.query.all()
    return render_template('admin/books.html', title=_('絵本管理'), books=books_list)

@bp.route('/books/add', methods=['GET', 'POST'])
@admin_required
def add_book():
    form = AddBookForm()
    if form.validate_on_submit():
        # Save PDF file
        pdf_filename = save_pdf(form.pdf_file.data)
        pdf_path = os.path.join('uploads', 'pdf', pdf_filename) # [cite: 24]
        
        # Handle cover image
        if form.cover_file.data:
            cover_filename = save_cover(form.cover_file.data)
        else:
            # Generate cover from PDF
            cover_filename = generate_thumbnail(pdf_filename)
        
        cover_path = os.path.join('uploads', 'covers', cover_filename) # [cite: 25]
        
        # Create book
        book = Book(
            title=form.title.data,
            cover_path=cover_path,
            pdf_path=pdf_path
        )
        
        # Add tags [cite: 26]
        tags_list = [tag.strip() for tag in form.tags.data.split(',') if tag.strip()]
        
        db.session.add(book)
        db.session.flush()  # To get book.id
        
        for tag_item in tags_list:
            book.add_tag(tag_item)
        
        db.session.commit()
        flash(_('絵本「{}」を追加しました').format(form.title.data), 'success') # [cite: 26]
        return redirect(url_for('admin.books')) # [cite: 27]
    
    return render_template('admin/add_book.html', title=_('絵本追加'), form=form)

@bp.route('/books/<string:id>/delete', methods=['POST'])
@admin_required
def delete_book(id):
    book = Book.query.get_or_404(id)
    
    # Delete files from disk
    try:
        if os.path.exists(os.path.join(current_app.root_path, 'static', book.pdf_path)):
            os.remove(os.path.join(current_app.root_path, 'static', book.pdf_path))
        
        if os.path.exists(os.path.join(current_app.root_path, 'static', book.cover_path)):
            os.remove(os.path.join(current_app.root_path, 'static', book.cover_path))
    except Exception as e: # [cite: 28]
        flash(_('ファイル削除中にエラーが発生しました: {}').format(str(e)), 'warning') # [cite: 28]
    
    # Delete from database
    db.session.delete(book)
    db.session.commit()
    
    flash(_('絵本「{}」を削除しました').format(book.title), 'success') # [cite: 28]
    return redirect(url_for('admin.books'))
