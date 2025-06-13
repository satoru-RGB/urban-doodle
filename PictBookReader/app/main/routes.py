from flask import render_template, flash, redirect, url_for, request, current_app, jsonify, session
from flask_login import login_required, current_user
from flask_babel import gettext as _
from app import db
from app.main import bp
from app.models import Book, Bookmark, BookTag
from app.main.forms import SearchForm

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    search_form = SearchForm()
    selected_tag = request.args.get('tag')
    search_query = request.args.get('query', '')
    
    # Get all available tags [cite: 15]
    tags_query = db.session.query(BookTag.tag).distinct().all()
    all_tags = [tag[0] for tag in tags_query]
    
    # Filter books by search query and tag [cite: 15]
    books_query = Book.query
    if search_query:
        books_query = books_query.filter(Book.title.contains(search_query))
    
    if selected_tag:
        book_ids_query = [bt.book_id for bt in BookTag.query.filter_by(tag=selected_tag).all()]
        books_query = books_query.filter(Book.id.in_(book_ids_query))
    
    books = books_query.all() # [cite: 16]
    
    return render_template('main/index.html', 
                          title=_('マイ絵本ライブラリ'),
                          books=books, 
                          search_form=search_form,
                          all_tags=all_tags, # [cite: 17]
                          selected_tag=selected_tag,
                          search_query=search_query)

@bp.route('/book/<string:id>')
@login_required
def book_detail(id):
    book = Book.query.get_or_404(id)
    return render_template('main/book_detail.html', title=book.title, book=book)

@bp.route('/book/<string:id>/read')
@login_required
def read_book(id):
    book = Book.query.get_or_404(id)
    return render_template('main/read_book.html', title=_('読む: {}').format(book.title), book=book)

@bp.route('/api/book/<string:id>/last-page', methods=['POST']) # [cite: 18]
@login_required
def update_last_page(id):
    book = Book.query.get_or_404(id)
    page = request.json.get('page', 0)
    book.last_read_page = page
    db.session.commit()
    return jsonify({'success': True})

@bp.route('/api/book/<string:id>/bookmark', methods=['POST', 'DELETE'])
@login_required
def manage_bookmark(id):
    book = Book.query.get_or_404(id)
    
    if request.method == 'POST':
        page = request.json.get('page', 0)
        note = request.json.get('note', '')
        
        # Check if bookmark already exists [cite: 19]
        existing = book.get_bookmark(page)
        if existing:
            existing.note = note
        else:
            book.add_bookmark(page, note)
        
        db.session.commit()
        return jsonify({'success': True})
    
    elif request.method == 'DELETE':
        page = request.json.get('page', 0)
        book.remove_bookmark(page) # [cite: 20]
        db.session.commit()
        return jsonify({'success': True})

@bp.route('/api/book/<string:id>/bookmarks')
@login_required
def get_bookmarks(id):
    book = Book.query.get_or_404(id)
    bookmarks = [{'page': b.page, 'note': b.note} for b in book.bookmarks]
    return jsonify(bookmarks)

@bp.route('/set_language/<language>')
def set_language(language=None):
    if language in current_app.config['LANGUAGES']:
        session['language'] = language
    next_url = request.args.get('next') or url_for('main.index')
    return redirect(next_url)
