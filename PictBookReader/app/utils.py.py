import os
import uuid
from flask import current_app
# from werkzeug.utils import secure_filename # Not used
import fitz  # PyMuPDF
from PIL import Image
from io import BytesIO

def save_pdf(pdf_file):
    """Save PDF file with unique filename"""
    filename = f"{uuid.uuid4().hex}.pdf"
    pdf_file.save(os.path.join(current_app.config['PDF_FOLDER'], filename))
    return filename

def save_cover(cover_file):
    """Save cover image with unique filename"""
    extension = cover_file.filename.rsplit('.', 1)[1].lower() # [cite: 31]
    filename = f"{uuid.uuid4().hex}.{extension}"
    cover_file.save(os.path.join(current_app.config['COVER_FOLDER'], filename))
    return filename

def generate_thumbnail(pdf_filename):
    """Generate thumbnail from first page of PDF"""
    pdf_path = os.path.join(current_app.config['PDF_FOLDER'], pdf_filename)
    thumbnail_filename = f"{pdf_filename.rsplit('.', 1)[0]}_cover.jpg"
    thumbnail_path = os.path.join(current_app.config['COVER_FOLDER'], thumbnail_filename)
    
    # Open PDF and get first page
    pdf = fitz.open(pdf_path)
    first_page = pdf[0]
    
    # Render page to image
    pix = first_page.get_pixmap()
    img_data = pix.tobytes("jpeg") # [cite: 32]
    
    # Resize image
    img = Image.open(BytesIO(img_data))
    img.thumbnail(current_app.config['THUMBNAIL_SIZE'])
    
    # Save thumbnail
    img.save(thumbnail_path, "JPEG")
    
    return thumbnail_filename

def seed_admin():
    """Create admin user if one doesn't exist"""
    from app.models import User
    from app import db
    
    admin = User.query.filter_by(is_admin=True).first()
    if admin is None:
        admin = User(username='admin', is_admin=True)
        admin.set_password('admin123') # [cite: 33]
        db.session.add(admin)
        db.session.commit()
        print("Admin user created: username='admin', password='admin123'")

def seed_sample_books():
    """Add sample books if none exist"""
    from app.models import Book
    from app import db
    
    if Book.query.count() == 0:
        # Add sample books
        # This would require sample PDF files to be in place
        pass # [cite: 34]