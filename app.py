from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from functools import wraps

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 'admin':
            flash("Access denied: Admins only.", "danger")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function
# =====================================================
# APP CONFIGURATION
# =====================================================

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # change this to something secure

# Database connection 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/inventory_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# =====================================================
# UPLOAD SETTINGS
# =====================================================

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# =====================================================
# INITIALIZE EXTENSIONS
# =====================================================

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


# =====================================================
# DATABASE MODEL
# =====================================================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'admin' or 'staff'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    stock = db.Column(db.Integer)  # renamed from quantity
    price = db.Column(db.Float)
    image = db.Column(db.String(200), nullable=True)
    date_added = db.Column(db.Date)
    time_added = db.Column(db.Time)
    size = db.Column(db.String(10))
    size_unit = db.Column(db.String(5))
    brand = db.Column(db.String(50))
    category = db.Column(db.String(50))

# =====================================================
#ActivityLog and LoginActivity
# =====================================================
class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    username = db.Column(db.String(50))
    action = db.Column(db.String(100))
    product_name = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.now)


class StockAlert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product_name = db.Column(db.String(100))
    stock = db.Column(db.Integer)
    alert_type = db.Column(db.String(50))  # "Low Stock" or "Out of Stock"
    created_at = db.Column(db.DateTime, default=datetime.now)

class LoginActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    username = db.Column(db.String(100))
    action = db.Column(db.String(50))
    ip_address = db.Column(db.String(45))  # new column for IPv4/IPv6
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)



# =====================================================
# AUTHENTICATION ROUTES
# =====================================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            # Set session data
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role

            # Record login activity
            ip = request.remote_addr
            login_log = LoginActivity(
                user_id=user.id,
                username=user.username,
                action='Login',
                ip_address=ip
            )
            db.session.add(login_log)
            db.session.commit()

            flash(f"Welcome, {user.username}!", "success")

            # Redirect based on role
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'staff':
                return redirect(url_for('staff_dashboard'))
        else:
            flash("Invalid username or password", "danger")

    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'user_id' in session:
        user_id = session.get('user_id')
        username = session.get('username')
        ip = request.remote_addr

        # Record logout activity
        logout_log = LoginActivity(
            user_id=user_id,
            username=username,
            action='Logout',
            ip_address=ip
        )
        db.session.add(logout_log)
        db.session.commit()

    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

# =====================================================
# DASHBOARDS
# =====================================================
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'role' not in session or session['role'] != 'admin':
        flash("Access denied: Admins only.", "danger")
        return redirect(url_for('login'))

    # Dashboard stats
    total_items = Product.query.count()
    low_stock_items = Product.query.filter(Product.stock < 5).all()  # threshold 5
    low_stock_count = len(low_stock_items)

    today = datetime.utcnow().date()
    items_added_today = Product.query.filter(db.func.date(Product.date_added) == today).count()

    total_staff = User.query.filter(User.role == 'staff').count()

    # recent activity logs and login reports (last 20)
    recent_activities = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).limit(20).all()
    recent_logins = LoginActivity.query.order_by(LoginActivity.timestamp.desc()).limit(20).all()

    return render_template(
        'admin_dashboard.html',
        username=session['username'],
        total_items=total_items,
        low_stock_items=low_stock_items,
        low_stock_count=low_stock_count,
        items_added_today=items_added_today,
        total_staff=total_staff,
        recent_activities=recent_activities,
        recent_logins=recent_logins
    )



@app.route('/staff_dashboard')
def staff_dashboard():
    if 'role' not in session or session['role'] != 'staff':
        flash("Access denied: Staff only.", "danger")
        return redirect(url_for('login'))
    return render_template('staff_dashboard.html', username=session['username'])

# =====================================================
# STAFF REGISTRATION (Admin Only)
# =====================================================
@app.route('/register_staff', methods=['GET', 'POST'])
def register_staff():
    if 'role' not in session or session['role'] != 'admin':
        flash("Access denied: Admins only.", "danger")
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash("Username already exists!", "danger")
            return redirect(url_for('register_staff'))

        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        new_staff = User(username=username, password=hashed_pw, role='staff')
        db.session.add(new_staff)
        db.session.commit()

        flash("New staff registered successfully!", "success")
        return redirect(url_for('admin_dashboard'))

    return render_template('register_staff.html')

# =====================================================
# INVENTORY CRUD
# =====================================================
@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))

    search_query = request.args.get('query', '')

    if search_query:
        products = Product.query.filter(
            (Product.name.like(f"%{search_query}%")) |
            (Product.brand.like(f"%{search_query}%")) |
            (Product.category.like(f"%{search_query}%")) |
            (Product.size.like(f"%{search_query}%")) |
            (Product.size_unit.like(f"%{search_query}%"))
        ).all()
    else:
        products = Product.query.all()

    return render_template('index.html', products=products, search_query=search_query)



# =====================================================
# ADD PRODUCT (With Activity Log + Stock Check)
# =====================================================
@app.route('/add', methods=['GET', 'POST'])
@admin_only
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        stock = int(request.form['stock'])
        price = float(request.form['price'])
        brand = request.form.get('brand')
        category = request.form.get('category')
        size = request.form.get('size')
        size_unit = request.form.get('size_unit')

        image = request.files.get('image')
        filename = None
        if image and image.filename:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        new_product = Product(
            name=name,
            stock=stock,
            price=price,
            brand=brand,
            category=category,
            size=size,
            size_unit=size_unit,
            image=filename,
            date_added=datetime.now().date(),
            time_added=datetime.now().time()
        )
        db.session.add(new_product)
        db.session.commit()

        # 🧾 Log Activity
        log = ActivityLog(
            user_id=session['user_id'],
            username=session['username'],
            action="Added new product",
            product_name=name
        )
        db.session.add(log)
        db.session.commit()

        # 🚨 Check for Low Stock
        if stock <= 5:
            alert = StockAlert(
                product_id=new_product.id,
                product_name=new_product.name,
                stock=new_product.stock,
                alert_type="Low Stock" if stock > 0 else "Out of Stock"
            )
            db.session.add(alert)
            db.session.commit()

        flash('Footwear added successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('add_product.html')


# =====================================================
# EDIT PRODUCT (With Activity Log + Stock Update Check)
# =====================================================
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@admin_only
def edit_product(id):
    product = Product.query.get_or_404(id)

    if request.method == 'POST':
        product.name = request.form['name']
        product.brand = request.form.get('brand')
        product.category = request.form.get('category')
        product.size = request.form.get('size')
        product.size_unit = request.form.get('size_unit')
        product.stock = int(request.form['stock'])
        product.price = float(request.form['price'])

        # Handle image update
        image = request.files.get('image')
        if image and image.filename:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            product.image = filename

        db.session.commit()

        # 🧾 Log Activity
        log = ActivityLog(
            user_id=session['user_id'],
            username=session['username'],
            action="Edited product details",
            product_name=product.name
        )
        db.session.add(log)
        db.session.commit()

        # 🚨 Update Low Stock Alerts
        existing_alert = StockAlert.query.filter_by(product_id=product.id).first()
        if product.stock <= 5:
            if not existing_alert:
                alert = StockAlert(
                    product_id=product.id,
                    product_name=product.name,
                    stock=product.stock,
                    alert_type="Low Stock" if product.stock > 0 else "Out of Stock"
                )
                db.session.add(alert)
            else:
                existing_alert.stock = product.stock
                existing_alert.alert_type = "Low Stock" if product.stock > 0 else "Out of Stock"
        elif existing_alert:
            db.session.delete(existing_alert)

        db.session.commit()

        flash('Product updated successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('edit_product.html', product=product)


# =====================================================
# DELETE PRODUCT (With Activity Log)
# =====================================================
@app.route('/delete/<int:id>')
@admin_only
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()

    # 🧾 Log Activity
    log = ActivityLog(
        user_id=session['user_id'],
        username=session['username'],
        action="Deleted product",
        product_name=product.name
    )
    db.session.add(log)
    db.session.commit()

    flash("Product deleted successfully!", "info")
    return redirect(url_for('index'))

# =====================================================
# ADMIN: MANAGE USERS (DELETE STAFF)
# =====================================================
@app.route('/manage_users')
def manage_users():
    if 'role' not in session or session['role'] != 'admin':
        flash("Access denied: Admins only.", "danger")
        return redirect(url_for('index'))

    users = User.query.filter(User.role != 'admin').all()
    return render_template('manage_users.html', users=users)


@app.route('/delete_user/<int:id>')
def delete_user(id):
    if 'role' not in session or session['role'] != 'admin':
        flash("Access denied: Admins only.", "danger")
        return redirect(url_for('index'))

    user = User.query.get_or_404(id)
    if user.role == 'admin':
        flash("You cannot delete another admin!", "danger")
        return redirect(url_for('manage_users'))

    db.session.delete(user)
    db.session.commit()
    flash(f"User '{user.username}' deleted successfully.", "info")
    return redirect(url_for('manage_users'))

# =====================================================
# INITIAL ADMIN CREATION (Command Line)
# =====================================================
@app.cli.command('create-admin')
def create_admin():
    """Run this command to create an admin from terminal."""
    username = input('Enter admin username: ')
    password = input('Enter admin password: ')
    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    new_admin = User(username=username, password=hashed_pw, role='admin')
    db.session.add(new_admin)
    db.session.commit()
    print('Admin user created successfully!')

# =====================================================
# Search Function
# =====================================================
@app.route('/search_inventory', methods=['GET'])
def search_inventory():
    if 'username' not in session:
        return redirect(url_for('login'))

    query = request.args.get('query', '')
    if query:
        products = Product.query.filter(Product.name.like(f"%{query}%")).all()
    else:
        products = Product.query.all()

    return render_template('index.html', products=products, search_query=query)

# =====================================================
# Search Users
# =====================================================
@app.route('/search_users', methods=['GET'])
def search_users():
    if 'role' not in session or session['role'] != 'admin':
        flash('Access denied: Admins only', 'danger')
        return redirect(url_for('index'))

    query = request.args.get('query', '')
    if query:
        users = User.query.filter(User.username.like(f"%{query}%")).all()
    else:
        users = User.query.all()

    return render_template('manage_users.html', users=users, search_query=query)

@app.route('/activity_logs')
@admin_only
def activity_logs():
    logs = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).all()
    return render_template('activity_logs.html', logs=logs)


@app.context_processor
def inject_admin_alerts():
    low_stock_products = Product.query.filter(Product.stock < 5).all()
    low_stock_count = len(low_stock_products)

    return {
        'low_stock_products': low_stock_products,
        'low_stock_count': low_stock_count
    }


# =====================================================
# RUN APP
# =====================================================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

