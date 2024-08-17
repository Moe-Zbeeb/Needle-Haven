import functools
import os
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app as app, abort
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from .db import get_db
from flask_mail import Mail, Message
from .auth import send_store_email

bp = Blueprint('blog', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

"""The following function loads the logged-in user from the database and stores it in the g object."""
"""Object can be used to store data that might be accessed by multiple functions during the request."""
'''
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

'''
"""The following functions fetch all products from the database and render them on the index page.  
The products are fetched by joining the Product and Store tables on the store_id column. 
I render the products on the index page using the render_template function."""    

@bp.route('/index')
def index():
    return render_template('index.html')  


@bp.route('/contact_us', methods=('GET', 'POST'))
def contact_us():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        msg = request.form['message']

        db = get_db()
        error = None

        if not name:
            error = 'Name is required.'
        elif not email:
            error = 'Email is required.'
        elif not phone_number:
            error = 'Phone number is required.'
        elif not msg:
            error = 'Description is required.'

        if error is None:
            message = "Contact Us"
            message_body =  f"Name: {name}\n"+f"Store email:{email}\n"+ f"Phone_number:{phone_number}\n"+f"Message:{msg}\n"
            send_store_email(message,message_body)
            conf = "We will reply as soon as possible!!"
            flash(conf)
    return redirect(url_for('blog.index') + '#contact-form')

@bp.route('/shop')
def shop():
    return redirect(url_for('blog.category',category_name="womenswear"))

@bp.route('/category/<string:category_name>')
def category(category_name):
    if category_name == 'womenswear':
        clothing = [
            'Dresses',
            'Tops & Blouses',
            'T-shirts & Tanks',
            'Sweaters & Cardigans',
            'Jackets & Coats',
            'Pants & Leggings',
            'Skirts',
            'Shorts',
            'Jeans',
            'Suits & Blazers',
            'Activewear',
            'Swimwear'
        ]
        shoes = ['Heels', 'Flats', 'Boots', 'Sneakers', 'Sandals']
        accessories = ['Bags', 'Belts', 'Hats', 'Jewelry', 'Scarves']
        imagesnewin = [
            {
                "image": "../static/images/womenswear1-newin.jpg",
                "store": "Store Name 1",
                "item_name": "Item Name 1",
                "price": "$100.00"
            },
            {
                "image": "../static/images/womenswear2-newin.jpg",
                "store": "Store Name 2",
                "item_name": "Item Name 2",
                "price": "$120.00"
            },
            {
                "image": "../static/images/womenswear3-newin.jpg",
                "store": "Store Name 3",
                "item_name": "Item Name 3",
                "price": "$150.00"
            },
            {
                "image": "../static/images/womenswear4-newin.jpg",
                "store": "Store Name 4",
                "item_name": "Item Name 4",
                "price": "$130.00"
            }
        ]
        imagestrendingnow = [
            {
                "image": "../static/images/womenswear1-trendingnow.jpg",
                "store": "Store Name 1",
                "item_name": "Item Name 1",
                "price": "$100.00"
            },
            {
                "image": "../static/images/womenswear2-trendingnow.jpg",
                "store": "Store Name 2",
                "item_name": "Item Name 2",
                "price": "$120.00"
            },
            {
                "image": "../static/images/womenswear3-trendingnow.jpg",
                "store": "Store Name 3",
                "item_name": "Item Name 3",
                "price": "$150.00"
            },
            {
                "image": "../static/images/womenswear4-trendingnow.jpg",
                "store": "Store Name 4",
                "item_name": "Item Name 4",
                "price": "$130.00"
            }
        ]
    elif category_name == 'menswear':
        clothing = [
                'T-Shirts & Polos', 'Shirts', 'Sweaters & Hoodies', 
                'Jackets & Coats', 'Suits & Blazers', 'Pants & Chinos', 
                'Jeans', 'Shorts', 'Activewear', 'Swimwear'
            ]
        shoes = ['Boots', 'Sneakers', 'Loafers', 'Oxfords', 'Sandals']
        accessories = ['Bags', 'Belts', 'Hats', 'Watches', 'Sunglasses']
        imagesnewin = [
            {
                "image": "../static/images/menswear1-newin.jpg",
                "store": "Store Name 1",
                "item_name": "Item Name 1",
                "price": "$110.00"
            },
            {
                "image": "../static/images/menswear2-newin.jpg",
                "store": "Store Name 2",
                "item_name": "Item Name 2",
                "price": "$130.00"
            },
            {
                "image": "../static/images/menswear3-newin.jpg",
                "store": "Store Name 3",
                "item_name": "Item Name 3",
                "price": "$140.00"
            },
            {
                "image": "../static/images/menswear4-newin.jpg",
                "store": "Store Name 4",
                "item_name": "Item Name 4",
                "price": "$125.00"
            }
        ]
        imagestrendingnow = [
            {
                "image": "../static/images/menswear1-trendingnow.jpg",
                "store": "Store Name 1",
                "item_name": "Item Name 1",
                "price": "$110.00"
            },
            {
                "image": "../static/images/menswear2-trendingnow.jpg",
                "store": "Store Name 2",
                "item_name": "Item Name 2",
                "price": "$130.00"
            },
            {
                "image": "../static/images/menswear3-trendingnow.jpg",
                "store": "Store Name 3",
                "item_name": "Item Name 3",
                "price": "$140.00"
            },
            {
                "image": "../static/images/menswear4-trendingnow.jpg",
                "store": "Store Name 4",
                "item_name": "Item Name 4",
                "price": "$125.00"
            }
        ]
    else:
        clothing = ['Tops', 'Pants', 'Dresses', 'Outerwear', 'Swimwear']
        shoes = ['Boots', 'Sneakers', 'Loafers', 'Oxfords', 'Sandals']
        accessories = ['Hats', 'Bags', 'Scarves', 'Gloves']
        imagesnewin = [
            {
                "image": "../static/images/kidswear1-newin.jpg",
                "store": "Store Name 1",
                "item_name": "Kids Item 1",
                "price": "$50.00"
            },
            {
                "image": "../static/images/kidswear2-newin.jpg",
                "store": "Store Name 2",
                "item_name": "Kids Item 2",
                "price": "$60.00"
            },
            {
                "image": "../static/images/kidswear3-newin.jpg",
                "store": "Store Name 3",
                "item_name": "Kids Item 3",
                "price": "$70.00"
            },
            {
                "image": "../static/images/kidswear4-newin.jpg",
                "store": "Store Name 4",
                "item_name": "Kids Item 4",
                "price": "$55.00"
            }
        ]
        imagestrendingnow = [
            {
                "image": "../static/images/kidswear1-trendingnow.jpg",
                "store": "Store Name 1",
                "item_name": "Kids Item 1",
                "price": "$40.00"
            },
            {
                "image": "../static/images/kidswear2-trendingnow.jpg",
                "store": "Store Name 2",
                "item_name": "Kids Item 2",
                "price": "$45.00"
            },
            {
                "image": "../static/images/kidswear3-trendingnow.jpg",
                "store": "Store Name 3",
                "item_name": "Kids Item 3",
                "price": "$50.00"
            },
            {
                "image": "../static/images/kidswear4-trendingnow.jpg",
                "store": "Store Name 4",
                "item_name": "Kids Item 4",
                "price": "$55.00"
            }
        ]
    return render_template('shop.html',category_name = category_name,clothing=clothing,shoes=shoes,accessories=accessories,imagesnewin=imagesnewin,imagestrendingnow=imagestrendingnow)

@bp.route('/shop/category/<string:category_name>/subcategory/<string:subcategory>/type/<string:type>', methods=['GET'])
def filter_products(category_name, subcategory,type):
    db = get_db()
    
    # Query to get products based on category and subcategory
    if type == "":
        products = db.execute(
            'SELECT * FROM Product WHERE category = ? AND subcategory = ?',
            (category_name, subcategory)
        ).fetchall()
    else:
        products = db.execute(
        'SELECT * FROM Product WHERE category = ? AND subcategory = ? AND type = ?',
        (category_name, subcategory, type)
        ).fetchall()
    return render_template('product.html', category_name=category_name, subcategory=subcategory, products=products)


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

def user_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not session.get('user_id'):
            flash('User login required.')
            return redirect(url_for('auth.user_login'))
        return view(**kwargs)
    return wrapped_view

def store_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not session.get('store_id'):
            flash('Store login required.')
            return redirect(url_for('auth.store_login'))
        return view(**kwargs)
    return wrapped_view


@bp.route('/upload_product', methods=('GET', 'POST'))
@store_required
def upload_product():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        subcategory = request.form['subcategory']
        type = request.form['type']
        color = request.form['color']
        description = request.form['description']
        price = request.form['price']
        date_of_release = request.form['date_of_release']
        store_id = session.get('store_id')

        # Fetch the store's name based on the store_id from the session
        db = get_db()
        store = db.execute('SELECT name FROM Store WHERE id = ?', (store_id,)).fetchone()
        store_name = store['name'] if store else None

        # Handle the uploaded image
        image = request.files['image']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)

            error = None

            if not name:
                error = 'Product name is required.'
            elif not category:
                error = 'Category is required.'
            elif not subcategory:
                error = 'Subcategory is required.'
            elif not type:
                error = 'Type is required.'
            elif not color:
                error = 'Color is required.'
            elif not description:
                error = 'Description is required.'
            elif not price:
                error = 'Price is required.'
            elif not date_of_release:
                error = 'Date of release is required.'
            elif not store_name:
                error = 'Store could not be found.'

            if error is None:
                try:
                    # Insert the product along with the store's name into the Product table
                    db.execute(
                        'INSERT INTO Product (name, category, subcategory, store, store_id, type, description, price, color, date_of_release, image_path) '
                        'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                        (name, category, subcategory, store_name, store_id, type, description, price, color, date_of_release, image_path)
                    )
                    db.commit()

                    flash('Product successfully uploaded.')
                    return redirect(url_for('blog.index'))
                except db.IntegrityError:
                    error = f"Product {name} already exists."

            flash(error)
    return render_template('upload_product.html')

"""delete product function"""  
@bp.route('/delete_product/<int:product_id>', methods=('POST',))
@store_required
def delete_product(product_id):
    db = get_db()
    store_id = session.get('store_id')

    # Ensure the product belongs to the logged-in store
    product = db.execute(
        'SELECT id FROM Product WHERE id = ? AND store_id = ?', (product_id, store_id)
    ).fetchone()

    if product is None:
        flash('Product not found or you do not have permission to delete this product.')
        return redirect(url_for('blog.index'))

    # Delete the product
    db.execute('DELETE FROM Product WHERE id = ? AND store_id = ?', (product_id, store_id))
    db.commit()

    flash('Product successfully deleted.')
    return redirect(url_for('blog.index'))


"""edit product function"""  
@bp.route('/edit_product/<int:product_id>', methods=('GET', 'POST'))
@store_required
def edit_product(product_id):
    db = get_db()
    store_id = session.get('store_id')

    # Fetch the product to be edited
    product = db.execute(
        'SELECT * FROM Product WHERE id = ? AND store_id = ?', (product_id, store_id)
    ).fetchone()

    if product is None:
        flash('Product not found or you do not have permission to edit this product.')
        return redirect(url_for('blog.index'))

    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        subcategory = request.form['subcategory']
        type = request.form['type']
        description = request.form['description']
        price = request.form['price']
        color = request.form['color']
        date_of_release = request.form['date_of_release']

        # Handle the uploaded image
        image = request.files['image']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
        else:
            image_path = product['image_path']  # Keep the current image if none is uploaded

        error = None

        if not name:
            error = 'Product name is required.'
        elif not category:
            error = 'Category is required.'
        elif not subcategory:
            error = 'Subcategory is required.'
        elif not type:
            error = 'Brand is required.'
        elif not description:
            error = 'Description is required.'
        elif not price:
            error = 'Price is required.'
        elif not color:
            error = 'Color is required.'
        elif not date_of_release:
            error = 'Date of release is required.'

        if error is None:
            try:
                # Update the product in the database
                db.execute(
                    'UPDATE Product SET name = ?, category = ?, subcategory = ?, type= ?, description = ?, price = ?, color = ?, date_of_release = ?, image_path = ? '
                    'WHERE id = ? AND store_id = ?',
                    (name, category, subcategory, type, description, price, color, date_of_release, image_path, product_id, store_id)
                )
                db.commit()
                flash('Product successfully updated.')
                return redirect(url_for('blog.index'))
            except db.IntegrityError:
                error = f"Product {name} already exists."

        flash(error)

    return render_template('edit_product.html', product=product)

@bp.route('/profile')
def profile():
    if session.get('user_id'):
        return redirect(url_for('blog.user_home'))  # Redirect to the user's profile
    elif session.get('store_id'):
        return redirect(url_for('blog.store_home'))  # Redirect to the store's profile
    else:
        flash('Login required.')
        return redirect(url_for('auth.login'))  # Redirect to the login page


@bp.route('/user_profile')
def user_home():
    # Ensure the user is logged in
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('auth.login'))

    # Query the database for the user's details
    db = get_db()
    user = db.execute(
        'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()

    if user is None:
        return redirect(url_for('auth.login'))

    # Pass the user's details to the template
    return render_template('myprofile_user.html', user=user)

@bp.route('/store_profile')
def store_home():
    return render_template('myprofile_store.html')

@bp.route('/change_password',methods=['GET','POST'])
def change_password():
    if request.method == 'POST':
        current_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        db = get_db()
        error = None

        # Check if the passwords match
        if new_password != confirm_password:
            error = 'New passwords do not match.'

        if session.get('user_id'):
            user_id = session['user_id']
            user = db.execute(
                'SELECT * FROM user WHERE id = ?', (user_id,)
            ).fetchone()

            # Verify if the old password is correct
            if user is None or not check_password_hash(user['password_hash'], current_password):
                error = 'Incorrect current password.'

            if error is None:
                db.execute(
                    'UPDATE user SET password_hash = ? WHERE id = ?',
                    (generate_password_hash(new_password), user_id)
                )
                db.commit()
                flash('Your password has been updated.')
            if error != None:
                flash(error)
            return redirect(url_for('blog.user_home'))

        elif session.get('store_id'):
            store_id = session['store_id']
            store = db.execute(
                'SELECT * FROM store WHERE id = ?', (store_id,)
            ).fetchone()

            # Verify if the old password is correct
            if store is None or not check_password_hash(store['password_hash'], current_password):
                error = 'Incorrect current password.'

            if error is None:
                db.execute(
                    'UPDATE store SET password_hash = ? WHERE id = ?',
                    (generate_password_hash(new_password), store_id)
                )
                db.commit()
                flash('Your password has been updated.')
            if error != None:
                flash(error)
            return redirect(url_for('blog.store_home'))

        else:
            error = 'You need to be logged in to change your password.'

        if error:
            flash(error)

    return render_template('myprofile_user.html') 

@bp.route('/GPT/<int:i>', methods=['GET', 'POST'])
def gpt(i):
    gpt = GPT() 
    
    if request.method == 'POST':
        query = request.form.get('query')
        
        if i == 1: 
            response1 = gpt.general_search(query)
            return response1 
        elif i == 2: 
            wiki_response = gpt.wiki_search(query)
            return wiki_response
        elif i == 3:
            stores_response = gpt.stores_search(query)
            return stores_response    
        else: 
            return "Invalid request"

    # Render the HTML form if the request method is GET
    return render_template('gpt_form.html')   


@bp.route('/stylist', methods=['GET', 'POST'])
def stylist():
    if request.method == 'POST':
        gender = request.form.get('gender')
        itemname = request.form.get('itemname')
        path = request.form.get('path')
        size = request.form.get('size')
        
        generator = ImageGenerator(region_name="us-east-1", model_id="amazon.titan-image-generator-v2:0")
        generator.generate_image(
            model=gender, 
            item=itemname,
            image_path=path,  
            size=size 
        )
        
        return f"Image generated successfully with {gender}, {itemname}, {path}, {size}"
    
    return render_template('stylist_form.html')
