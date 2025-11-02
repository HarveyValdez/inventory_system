from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # change this to something secure

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/inventory_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# =====================================================
# DATABASE MODELS
# =====================================================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # "admin" or "staff"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)

# =====================================================
# ROUTES: LOGIN SYSTEM
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
            flash('Welcome, ' + user.username + '!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# =====================================================
# ROUTES: INVENTORY CRUD (ROLE-PROTECTED)
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
        quantity = request.form['quantity']
        price = request.form['price']

        new_product = Product(name=name, quantity=quantity, price=price)
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully!', 'success')
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
        product.quantity = request.form['quantity']
        product.price = request.form['price']
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('edit_product.html', product=product)


@app.route('/delete/<int:id>')
def delete_product(id):
    if 'role' not in session or session['role'] != 'admin':
        flash('Access denied: Admins only', 'danger')
        return redirect(url_for('index'))

    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'info')
    return redirect(url_for('index'))

# =====================================================
# INITIAL ADMIN CREATION
# =====================================================

@app.cli.command('create-admin')
def create_admin():
    username = input('Enter admin username: ')
    password = input('Enter admin password: ')
    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    new_admin = User(username=username, password=hashed_pw, role='admin')
    db.session.add(new_admin)
    db.session.commit()
    print('Admin user created successfully!')

if __name__ == '__main__':
    app.run(debug=True)
