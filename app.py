# =====================================================
# IMPORTS & ENVIRONMENT SETUP
# =====================================================
import os
import filetype
import csv
from io import StringIO
from flask import make_response
from datetime import datetime, timezone
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from dotenv import load_dotenv


load_dotenv()

# =====================================================
# APP CONFIGURATION
# =====================================================

app = Flask(__name__)

# Security Configuration (from environment)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'fallback-dev-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'static/uploads')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))

# Session Security (enforce in production with HTTPS)
app.config['SESSION_COOKIE_SECURE'] = os.getenv('FLASK_ENV') == 'production'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Database Configuration
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Create upload directory if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'], mode=0o755)


# =====================================================
# HELPER FUNCTIONS
# =====================================================

def admin_only(f):
    """Decorator to restrict access to admin users only"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin':
            flash("Access denied: Admins only.", "danger")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


def allowed_file(filename):
    """Check if file extension is allowed"""
    allowed = os.getenv('ALLOWED_EXTENSIONS', 'png,jpg,jpeg,gif').split(',')
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed


def validate_image(stream):
    """Validate that the file is actually an image"""
    try:
        # Read a chunk of the file
        header = stream.read(512)
        stream.seek(0)  # Reset stream position
        
        # Detect file type
        kind = filetype.image(header)
        return '.' + kind.extension if kind else None
    except Exception:
        return None


def save_uploaded_file(file_storage):
    """
    Simple file upload with basic validation
    Returns: filename on success, None on failure
    """
    if not file_storage or not file_storage.filename:
        return None
    
    # Get filename
    filename = secure_filename(file_storage.filename)
    
    # Add timestamp to avoid duplicate names
    name, ext = os.path.splitext(filename)
    timestamp = int(datetime.now(tz=timezone.utc).timestamp())
    filename = f"{name}_{timestamp}{ext}"
    
    # Save file
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file_storage.save(filepath)
        return filename
    except Exception as e:
        flash(f"Error saving file: {str(e)}", "danger")
        return None

# =====================================================
# DATABASE MODELS
# =====================================================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'admin' or 'staff'


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Float, nullable=False, default=0.0)
    image = db.Column(db.String(200), nullable=True)
    date_added = db.Column(db.Date, default=lambda: datetime.now(tz=timezone.utc).date())
    time_added = db.Column(db.Time, default=lambda: datetime.now(tz=timezone.utc).time())
    size = db.Column(db.String(10))
    size_unit = db.Column(db.String(5))
    brand = db.Column(db.String(50))
    category = db.Column(db.String(50))


class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    username = db.Column(db.String(50), nullable=False)
    action = db.Column(db.String(200), nullable=False)
    product_name = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(tz=timezone.utc))


class StockAlert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), unique=True)
    product_name = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    alert_type = db.Column(db.String(50), nullable=False)  # "Low Stock" or "Out of Stock"
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(tz=timezone.utc))


class LoginActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    username = db.Column(db.String(100), nullable=False)
    action = db.Column(db.String(50), nullable=False)  # 'Login' or 'Logout'
    ip_address = db.Column(db.String(45))  # IPv4/IPv6 support
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(tz=timezone.utc))


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
            login_log = LoginActivity(
                user_id=user.id,
                username=user.username,
                action='Login',
                ip_address=request.remote_addr
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
        # Record logout activity
        logout_log = LoginActivity(
            user_id=session['user_id'],
            username=session['username'],
            action='Logout',
            ip_address=request.remote_addr
        )
        db.session.add(logout_log)
        db.session.commit()

    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))

    if session.get('role') not in ['staff', 'admin']:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('index'))

    user = User.query.get_or_404(session['user_id'])

    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        # ✅ VALIDATION: Password length (for admin & staff)
        if len(new_password) < 6:
            flash("❌ Password must be at least 6 characters.", "danger")
            return redirect(url_for('change_password'))

        # ✅ VALIDATION: New password must be different
        if new_password == old_password:
            flash("❌ New password must be different from old password.", "danger")
            return redirect(url_for('change_password'))

        # ✅ VALIDATION: Check old password
        if not bcrypt.check_password_hash(user.password, old_password):
            flash("❌ Incorrect old password.", "danger")
            return redirect(url_for('change_password'))

        # ✅ VALIDATION: Confirm password match
        if new_password != confirm_password:
            flash("❌ New passwords do not match.", "danger")
            return redirect(url_for('change_password'))

        user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        db.session.commit()

        flash("✅ Password updated successfully!", "success")
        return redirect(url_for('admin_dashboard' if user.role == 'admin' else 'staff_dashboard'))

    return render_template('change_password.html')


# =====================================================
# DASHBOARD ROUTES
# =====================================================

@app.route('/admin_dashboard')
@admin_only
def admin_dashboard():
    # Calculate dashboard statistics
    total_items = Product.query.count()
    low_stock_items = Product.query.filter(Product.stock < 5).all()
    low_stock_count = len(low_stock_items)

    today = datetime.now(tz=timezone.utc).date()
    items_added_today = Product.query.filter(db.func.date(Product.date_added) == today).count()
    total_staff = User.query.filter(User.role == 'staff').count()

    # Fetch recent activities (last 20)
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
    if session.get('role') != 'staff':
        flash("Access denied: Staff only.", "danger")
        return redirect(url_for('login'))
    return render_template('staff_dashboard.html', username=session['username'])


# =====================================================
# USER MANAGEMENT ROUTES (Admin Only)
# =====================================================

@app.route('/register_staff', methods=['GET', 'POST'])
@admin_only
def register_staff():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        # ✅ VALIDATION: Username length
        if len(username) < 3:
            flash("❌ Username must be at least 3 characters.", "danger")
            return redirect(url_for('register_staff'))

        # ✅ VALIDATION: Password length
        if len(password) < 6:
            flash("❌ Password must be at least 6 characters.", "danger")
            return redirect(url_for('register_staff'))

        # ✅ VALIDATION: Username already exists
        if User.query.filter_by(username=username).first():
            flash("❌ Username already exists!", "danger")
            return redirect(url_for('register_staff'))

        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        new_staff = User(username=username, password=hashed_pw, role='staff')
        db.session.add(new_staff)
        db.session.commit()

        flash("✅ New staff registered successfully!", "success")
        return redirect(url_for('admin_dashboard'))

    return render_template('register_staff.html')


@app.route('/manage_users')
@admin_only
def manage_users():
    users = User.query.filter(User.role != 'admin').all()
    return render_template('manage_users.html', users=users)


@app.route('/delete_user/<int:id>')
@admin_only
def delete_user(id):
    user = User.query.get_or_404(id)
    
    if user.role == 'admin':
        flash("You cannot delete another admin!", "danger")
        return redirect(url_for('manage_users'))

    db.session.delete(user)
    db.session.commit()
    flash(f"User '{user.username}' deleted successfully.", "info")
    return redirect(url_for('manage_users'))


# =====================================================
# INVENTORY ROUTES
# =====================================================

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))

    search_query = request.args.get('query', '').strip()

    if search_query:
        products = Product.query.filter(
            db.or_(
                Product.name.ilike(f"%{search_query}%"),
                Product.brand.ilike(f"%{search_query}%"),
                Product.category.ilike(f"%{search_query}%"),
                Product.size.ilike(f"%{search_query}%"),
                Product.size_unit.ilike(f"%{search_query}%")
            )
        ).all()
    else:
        products = Product.query.all()

    return render_template('index.html', products=products, search_query=search_query)


# =====================================================
# PRODUCT CRUD ROUTES
# =====================================================

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if session.get('role') not in ['admin', 'staff']:
        flash("Access denied.", "danger")
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Create new product
        new_product = Product(
            name=request.form['name'],
            stock=int(request.form['stock']),
            price=float(request.form['price']),
            brand=request.form.get('brand'),
            category=request.form.get('category'),
            size=request.form.get('size'),
            size_unit=request.form.get('size_unit')
        )

        # Handle image upload
        image_file = save_uploaded_file(request.files.get('image'))
        if image_file:
            new_product.image = image_file

        db.session.add(new_product)
        db.session.commit()

        # Log activity
        log = ActivityLog(
            user_id=session['user_id'],
            username=session['username'],
            action=f"{session['role'].capitalize()} added product",
            product_name=new_product.name
        )
        db.session.add(log)

        # Check for low stock
        if new_product.stock <= 5:
            alert = StockAlert(
                product_id=new_product.id,
                product_name=new_product.name,
                stock=new_product.stock,
                alert_type="Low Stock" if new_product.stock > 0 else "Out of Stock"
            )
            db.session.add(alert)
        
        db.session.commit()

        flash('Footwear added successfully!', 'success')
        return redirect(url_for('staff_dashboard' if session['role'] == 'staff' else 'index'))

    return render_template('add_product.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    if session.get('role') not in ['admin', 'staff']:
        flash("Access denied.", "danger")
        return redirect(url_for('login'))

    product = Product.query.get_or_404(id)

    if request.method == 'POST':
        # Update product fields
        product.name = request.form['name']
        product.brand = request.form.get('brand')
        product.category = request.form.get('category')
        product.size = request.form.get('size')
        product.size_unit = request.form.get('size_unit')
        product.stock = int(request.form['stock'])
        product.price = float(request.form['price'])

        # Handle image update
        image_file = save_uploaded_file(request.files.get('image'))
        if image_file:
            # Optionally delete old image here
            product.image = image_file

        db.session.commit()

        # Log activity
        log = ActivityLog(
            user_id=session['user_id'],
            username=session['username'],
            action=f"{session['role'].capitalize()} edited product",
            product_name=product.name
        )
        db.session.add(log)

        # Update low stock alerts
        existing_alert = StockAlert.query.filter_by(product_id=product.id).first()
        if product.stock <= 5:
            if existing_alert:
                existing_alert.stock = product.stock
                existing_alert.alert_type = "Low Stock" if product.stock > 0 else "Out of Stock"
            else:
                alert = StockAlert(
                    product_id=product.id,
                    product_name=product.name,
                    stock=product.stock,
                    alert_type="Low Stock" if product.stock > 0 else "Out of Stock"
                )
                db.session.add(alert)
        elif existing_alert:
            db.session.delete(existing_alert)
        
        db.session.commit()

        flash('Product updated successfully!', 'success')
        return redirect(url_for('staff_dashboard' if session['role'] == 'staff' else 'index'))

    return render_template('edit_product.html', product=product)


@app.route('/delete/<int:id>')
@admin_only
def delete_product(id):
    product = Product.query.get_or_404(id)
    
    # Log activity before deletion
    log = ActivityLog(
        user_id=session['user_id'],
        username=session['username'],
        action="Admin deleted product",
        product_name=product.name
    )
    db.session.add(log)
    
    # Delete product
    db.session.delete(product)
    db.session.commit()

    flash("Product deleted successfully!", "info")
    return redirect(url_for('index'))


# =====================================================
# STOCK MANAGEMENT ROUTES
# =====================================================

@app.route('/add_stock/<int:product_id>', methods=['POST'])
def add_stock(product_id):
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))

    if session.get('role') not in ['admin', 'staff']:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('index'))

    product = Product.query.get_or_404(product_id)
    
    try:
        added_qty = int(request.form['added_qty'])
        
        # VALIDATION
        if added_qty <= 0:
            flash("Quantity must be at least 1.", "danger")
            return redirect(url_for('index'))
            
        if added_qty > 1000:
            flash("Maximum 1000 units can be added at once.", "danger")
            return redirect(url_for('index'))

        product.stock += added_qty
        db.session.commit()

        # Log activity
        log = ActivityLog(
            user_id=session['user_id'],
            username=session['username'],
            action=f"Added {added_qty} units",
            product_name=product.name
        )
        db.session.add(log)
        db.session.commit()

        flash(f"✅ Added {added_qty} units to {product.name}.", "success")
        return redirect(url_for('index'))

    except (ValueError, KeyError):
        flash("Invalid quantity entered.", "danger")
        return redirect(url_for('index'))


@app.route('/deduct_stock/<int:product_id>', methods=['POST'])
def deduct_stock(product_id):
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))

    if session.get('role') not in ['admin', 'staff']:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('index'))

    product = Product.query.get_or_404(product_id)
    
    try:
        deduct_qty = int(request.form['deduct_qty'])
        
        # VALIDATION
        if deduct_qty <= 0:
            flash("Quantity must be at least 1.", "danger")
            return redirect(url_for('index'))
            
        if deduct_qty > product.stock:
            flash(f"Cannot deduct {deduct_qty} units. Only {product.stock} in stock.", "danger")
            return redirect(url_for('index'))

        product.stock -= deduct_qty
        db.session.commit()

        # Log activity
        log = ActivityLog(
            user_id=session['user_id'],
            username=session['username'],
            action=f"Deducted {deduct_qty} units",
            product_name=product.name
        )
        db.session.add(log)

        # Update low stock alerts
        existing_alert = StockAlert.query.filter_by(product_id=product.id).first()
        if product.stock <= 5:
            if existing_alert:
                existing_alert.stock = product.stock
                existing_alert.alert_type = "Low Stock" if product.stock > 0 else "Out of Stock"
            else:
                alert = StockAlert(
                    product_id=product.id,
                    product_name=product.name,
                    stock=product.stock,
                    alert_type="Low Stock" if product.stock > 0 else "Out of Stock"
                )
                db.session.add(alert)
        elif existing_alert:
            db.session.delete(existing_alert)
        
        db.session.commit()

        flash(f"➖ Deducted {deduct_qty} units from {product.name}.", "success")
        return redirect(url_for('index'))

    except (ValueError, KeyError):
        flash("Invalid quantity entered.", "danger")
        return redirect(url_for('index'))


# =====================================================
# SEARCH ROUTES
# =====================================================

@app.route('/search_inventory')
def search_inventory():
    if 'username' not in session:
        return redirect(url_for('login'))

    query = request.args.get('query', '').strip()
    if query:
        products = Product.query.filter(Product.name.ilike(f"%{query}%")).all()
    else:
        products = Product.query.all()

    return render_template('index.html', products=products, search_query=query)


@app.route('/search_users')
@admin_only
def search_users():
    query = request.args.get('query', '').strip()
    if query:
        users = User.query.filter(User.username.ilike(f"%{query}%")).all()
    else:
        users = User.query.filter(User.role != 'admin').all()

    return render_template('manage_users.html', users=users, search_query=query)


# =====================================================
# ACTIVITY LOGS
# =====================================================

@app.route('/activity_logs')
@admin_only
def activity_logs():
    logs = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).all()
    return render_template('activity_logs.html', logs=logs)


@app.context_processor
def inject_admin_alerts():
    """Make low stock count available in all templates"""
    low_stock_products = Product.query.filter(Product.stock < 5).all()
    return {
        'low_stock_products': low_stock_products,
        'low_stock_count': len(low_stock_products)
    }


# =====================================================
# CLI COMMANDS
# =====================================================

@app.cli.command('create-admin')
def create_admin():
    """Create an admin user from the command line"""
    username = input('Enter admin username: ')
    if User.query.filter_by(username=username).first():
        print(f"Error: Username '{username}' already exists!")
        return
    
    password = input('Enter admin password: ')
    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    new_admin = User(username=username, password=hashed_pw, role='admin')
    db.session.add(new_admin)
    db.session.commit()
    print('✅ Admin user created successfully!')

# =====================================================
# EXPORT INVENTORY TO CSV
# =====================================================
@app.route('/export_csv')
@admin_only
def export_csv():
    products = Product.query.all()
    
    # Create CSV in memory
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['ID', 'Name', 'Brand', 'Category', 'Size', 'Stock', 'Price'])
    
    # Write data
    for p in products:
        writer.writerow([p.id, p.name, p.brand, p.category, p.size, p.stock, p.price])
    
    # Create response
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=inventory.csv"
    response.headers["Content-type"] = "text/csv"
    return response


# =====================================================
# RUN APPLICATION
# =====================================================

if __name__ == '__main__':
    # Create tables if they don't exist (development only)
    with app.app_context():
        db.create_all()
    
    app.run(host='0.0.0.0', port=5000, debug=(os.getenv('FLASK_DEBUG', 'True') == 'True'))