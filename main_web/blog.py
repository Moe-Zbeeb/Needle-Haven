import functools
import os
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app as app, abort
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from main_web.db import get_db
from flask_mail import Mail, Message
from main_web import mail

bp = Blueprint('blog', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

"""The following function loads the logged-in user from the database and stores it in the g object."""
"""Object can be used to store data that might be accessed by multiple functions during the request."""
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

        # Assuming user table does not have store_id, fetching it based on some relationship
        store = get_db().execute(
            'SELECT * FROM Store WHERE id = (SELECT store_id FROM some_user_store_relationship WHERE user_id = ?)',
            (user_id,)
        ).fetchone()

        if store:
            g.user['store_id'] = store['id']
        else:
            g.user['store_id'] = None

"""The following functions fetch all products from the database and render them on the index page.  
The products are fetched by joining the Product and Store tables on the store_id column. 
I render the products on the index page using the render_template function."""    

@bp.route('/')
def index():
    return render_template('index.html')  

"""The following function fetches a single product from the database and renders it on the product page.
The product is fetched by joining the Product, Store, and ProductImages tables on the store_id and product_id columns.
I render the product on the product page using the render_template function.""" 
@bp.route('/product/<int:product_id>')
def product(product_id):
    db = get_db()
    product = db.execute(
        'SELECT p.id, p.name, p.description, p.price, p.rating, s.name AS store_name, pi.image_path FROM Product p'
        ' JOIN Store s ON p.store_id = s.id'
        ' LEFT JOIN ProductImages pi ON p.id = pi.product_id'
        ' WHERE p.id = ?',
        (product_id,)
    ).fetchone()
    if product is None:
        abort(404, f"Product id {product_id} doesn't exist.")
    return render_template('blog/product.html', product=product)

"""login as shop and add product"""  
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

def store_owner_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None or not g.user.get('is_store_owner', False):
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

@bp.route('/add_product', methods=('GET', 'POST'))
@login_required
@store_owner_required
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        rating = request.form['rating']
        store_id = g.user.get('store_id')  # Get store_id from logged-in user

        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['image']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            db = get_db()
            error = None

            if not name:
                error = 'Product name is required.'
            elif not description:
                error = 'Description is required.'
            elif not price:
                error = 'Price is required.'
            elif not rating:
                error = 'Rating is required.'
            elif not store_id:
                error = 'Store ID is required.'

            if error is None:
                try:
                    db.execute(
                        'INSERT INTO Product (name, description, price, rating, store_id) VALUES (?, ?, ?, ?, ?)',
                        (name, description, price, rating, store_id)
                    )
                    db.commit()
                    product_id = db.execute(
                        'SELECT id FROM Product WHERE name = ? AND store_id = ?',
                        (name, store_id)
                    ).fetchone()['id']
                    db.execute(
                        'INSERT INTO ProductImages (product_id, image_path) VALUES (?, ?)',
                        (product_id, file_path)
                    )
                    db.commit()
                    return redirect(url_for('blog.index'))
                except db.IntegrityError:
                    error = f"Product {name} already exists."

            flash(error)

    return render_template('add_product.html') 

"""delete product function"""  
@bp.route('/delete_product/<int:product_id>', methods=('POST',)) 
@login_required 
@store_owner_required 
def delete_product(product_id):
    db = get_db()
    db.execute('DELETE FROM Product WHERE id = ?', (product_id,))
    db.commit()
    return redirect(url_for('blog.index'))  

"""edit product function"""  
@bp.route('/edit_product/<int:product_id>', methods=('GET', 'POST')) 
@login_required 
@store_owner_required 
def edit_product(product_id):
    db = get_db()
    product = db.execute(
        'SELECT * FROM Product WHERE id = ?', (product_id,)
    ).fetchone()

    if product is None:
        abort(404, f"Product id {product_id} doesn't exist.")

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        rating = request.form['rating']

        if not name:
            flash('Product name is required.')
        elif not description:
            flash('Description is required.')
        elif not price:
            flash('Price is required.')
        elif not rating:
            flash('Rating is required.')
        else:
            db.execute(
                'UPDATE Product SET name = ?, description = ?, price = ?, rating = ?'
                ' WHERE id = ?',
                (name, description, price, rating, product_id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('edit_product.html', product=product)
