from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from datetime import datetime
from werkzeug.utils import secure_filename

# =====================================================
# APP CONFIGURATION
# =====================================================

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # change this to something secure

# Database connection (same as before)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/inventory_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# =====================================================
# UPLOAD SETTINGS
# =====================================================

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# =====================================================
# INITIALIZE EXTENSIONS
# =====================================================

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


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
    name = db.Column(db.String(100))
    stock = db.Column(db.Integer)  # renamed from quantity
    price = db.Column(db.Float)
    image = db.Column(db.String(255), nullable=True)
    date_added = db.Column(db.Date)
    time_added = db.Column(db.Time)


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
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
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
    return render_template('admin_dashboard.html', username=session['username'])


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

    products = Product.query.all()
    return render_template('index.html', products=products)


@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if 'role' not in session or session['role'] != 'admin':
        flash('Access denied: Admins only', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form['name']
        stock = request.form['stock']
        price = request.form['price']

        # Optional image upload
        image_file = request.files.get('image')
        filename = None
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Add timestamp
        now = datetime.now()

        new_product = Product(
            name=name,
            stock=stock,
            price=price,
            image=filename,
            date_added=now.date(),
            time_added=now.time()
        )
        db.session.add(new_product)
        db.session.commit()

        flash('Footwear item added successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('add_product.html')



@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    if 'role' not in session or session['role'] != 'admin':
        flash('Access denied: Admins only', 'danger')
        return redirect(url_for('index'))

    product = Product.query.get_or_404(id)

    if request.method == 'POST':
        product.name = request.form['name']
        product.stock = request.form['stock']   # ✅ corrected name
        product.price = request.form['price']

        # Optional: update image if admin uploads a new one
        image_file = request.files.get('image')
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            product.image = filename

        db.session.commit()
        flash('Footwear updated successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('edit_product.html', product=product)



@app.route('/delete/<int:id>')
def delete_product(id):
    if 'role' not in session or session['role'] != 'admin':
        flash("Access denied: Admins only.", "danger")
        return redirect(url_for('index'))

    product = Product.query.get_or_404(id)
    db.session.delete(product)
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
# RUN APP
# =====================================================
if __name__ == '__main__':
    app.run(debug=True)
