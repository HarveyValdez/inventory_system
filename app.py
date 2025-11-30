# =====================================================
# IMPORTS & ENVIRONMENT SETUP
# =====================================================
import os
import filetype
import csv
import re
import secrets 
from io import StringIO
from datetime import datetime, timezone, timedelta  
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask import make_response
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

# =====================================================
# APP CONFIGURATION
# =====================================================

app = Flask(__name__)

# Security Configuration 
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'fallback-dev-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'static/uploads')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))

# Session Security 
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
        stream.seek(0)  
        
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
    role = db.Column(db.String(10), nullable=False)
    must_change_password = db.Column(db.Boolean, default=False, nullable=False)
    
    # Enhanced name fields
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=False)
    
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)  # Made required
    
    # Address fields
    address = db.Column(db.Text, nullable=True)
    city = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    
    # Personal details
    birthdate = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    education_level = db.Column(db.String(50), nullable=True)
    
    department = db.Column(db.String(50), default='General')
    is_active = db.Column(db.Boolean, default=True)
    is_approved = db.Column(db.Boolean, default=False)
    terms_accepted = db.Column(db.Boolean, nullable=False, default=False)
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(tz=timezone.utc))

    @property
    def full_name(self):
        """Dynamically generate full name"""
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Float, nullable=False, default=0.0)
    image = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(tz=timezone.utc))
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
    changes = db.relationship('ProductChangeLog', backref='activity_log', lazy=True, cascade='all, delete-orphan')

class StockAlert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), unique=True)
    product_name = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    alert_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(tz=timezone.utc))

class LoginActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    username = db.Column(db.String(100), nullable=False)
    action = db.Column(db.String(50), nullable=False)
    ip_address = db.Column(db.String(45))
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(tz=timezone.utc))

class StockHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    old_stock = db.Column(db.Integer, nullable=False)
    new_stock = db.Column(db.Integer, nullable=False)
    change_reason = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    username = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(tz=timezone.utc))

class ProductChangeLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity_log_id = db.Column(db.Integer, db.ForeignKey('activity_log.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    field_name = db.Column(db.String(50), nullable=False)
    old_value = db.Column(db.Text)
    new_value = db.Column(db.Text)
    change_reason = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    username = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(tz=timezone.utc))

class Invitation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(100), unique=True, nullable=False, index=True)
    email = db.Column(db.String(100), nullable=False, index=True)
    role = db.Column(db.String(10), default='staff')
    department = db.Column(db.String(50), default='General')
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=lambda: datetime.utcnow())
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)
    used_at = db.Column(db.DateTime, nullable=True)
    
    # Relationship for creator info
    creator = db.relationship('User', backref='invitations_created')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Generate secure token if not provided
        if not self.token:
            self.token = secrets.token_urlsafe(32)
        # Set 24-hour expiry from creation time if not provided
        if not self.expires_at:
            self.expires_at = datetime.utcnow() + timedelta(hours=24)
    
    @property
    def is_expired(self):
        """Check if invitation is expired"""
        return datetime.utcnow() > self.expires_at
    
    def __repr__(self):
        return f"<Invitation {self.email} - {'Used' if self.used else 'Active'}>"
    
class UserReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    report_type = db.Column(db.String(50), nullable=False)  # 'bug', 'feature', 'help', 'other'
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='unread')  # unread, read, resolved
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(tz=timezone.utc))
    
    # Relationship
    user = db.relationship('User', backref='reports', lazy=True)
    
    def __repr__(self):
        return f"<UserReport {self.id} - {self.user.username}: {self.report_type}>"

# Add this to your models section if needed
class StaffSetupToken(db.Model):
    """Separate table for staff setup tokens to keep User model clean"""
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(100), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)
    
    user = db.relationship('User', backref='setup_token', lazy=True)

# =====================================================
# TEMPLATE FILTERS
# =====================================================

@app.template_filter('manila_time')
def manila_time_filter(utc_datetime):
    """Convert UTC datetime to Manila Time (UTC+8) for display"""
    if utc_datetime is None:
        return "N/A"
    
    
    manila_tz = timezone(timedelta(hours=8))
    
    
    if utc_datetime.tzinfo is None:
        utc_datetime = utc_datetime.replace(tzinfo=timezone.utc)
    
    local_time = utc_datetime.astimezone(manila_tz)
    
    return local_time.strftime("%Y-%m-%d %H:%M:%S")


@app.template_filter('is_expired')
def is_expired_filter(dt):
    """Check if datetime is expired (handles both naive & aware datetimes)"""
    if dt is None:
        return False
    
    # Get current time as naive UTC (matching MySQL storage)
    now = datetime.utcnow()
    
    # If datetime is aware, convert to naive for comparison
    if dt.tzinfo is not None:
        dt = dt.replace(tzinfo=None)
    
    return now > dt

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
            # CHECK PASSWORD CHANGE REQUIREMENT
            if hasattr(user, 'must_change_password') and user.must_change_password:
                session['user_id'] = user.id
                session['username'] = user.username
                session['role'] = user.role
                flash("⚠️ You must change your password before continuing.", "warning")
                return redirect(url_for('change_password'))
            
            if not user.is_approved:
                flash("❌ Account pending approval.", "warning")
                return render_template('login.html')

            # Normal login flow...
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            
            db.session.add(LoginActivity(user_id=user.id, username=user.username, action='Login'))
            db.session.commit()
            
            flash(f"Welcome, {user.username}!", "success")
            return redirect(url_for('homepage' if user.role == 'admin' else 'staff_dashboard'))
        else:
            flash("Invalid credentials", "danger")

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

    user = User.query.get_or_404(session['user_id'])
    must_change = hasattr(user, 'must_change_password') and user.must_change_password

    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if len(new_password) < 6:
            flash("❌ Password must be at least 6 characters.", "danger")
            return redirect(url_for('change_password'))

        if not bcrypt.check_password_hash(user.password, old_password):
            flash("❌ Incorrect password.", "danger")
            return redirect(url_for('change_password'))

        if new_password != confirm_password:
            flash("❌ Passwords do not match.", "danger")
            return redirect(url_for('change_password'))

        # Update password and clear flag
        user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        if hasattr(user, 'must_change_password'):
            user.must_change_password = False
        db.session.commit()

        flash("✅ Password changed successfully!", "success")
        return redirect(url_for('admin_dashboard' if user.role == 'admin' else 'staff_dashboard'))

    return render_template('change_password.html', must_change_password=must_change)


# =====================================================
# DASHBOARD ROUTES
# =====================================================

@app.route('/admin_dashboard')
@admin_only
def admin_dashboard():
    #dashboard statistics
    total_items = Product.query.count()
    low_stock_items = Product.query.filter(Product.stock < 5).all()
    low_stock_count = len(low_stock_items)

    # Manila timezone
    manila_tz = timezone(timedelta(hours=8))
    today_manila = datetime.now(tz=manila_tz).date()
    
    
    from sqlalchemy import text
    items_added_today = db.session.query(Product).filter(
        db.func.date(Product.created_at + text("INTERVAL 8 HOUR")) == today_manila
    ).count()
    
    total_staff = User.query.filter(User.role == 'staff').count()

    # 📅 DATE RANGE FILTER
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Build queries
    activities_query = ActivityLog.query
    logins_query = LoginActivity.query
    
    # date filtering
    if start_date:
        
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        start_manila = start_dt.replace(hour=0, minute=0, second=0, tzinfo=manila_tz)
        
        start_utc = start_manila.astimezone(timezone.utc)
        activities_query = activities_query.filter(ActivityLog.timestamp >= start_utc)
        logins_query = logins_query.filter(LoginActivity.timestamp >= start_utc)
    
    if end_date:
        
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        end_manila = end_dt.replace(hour=23, minute=59, second=59, tzinfo=manila_tz)
        
        end_utc = end_manila.astimezone(timezone.utc)
        activities_query = activities_query.filter(ActivityLog.timestamp <= end_utc)
        logins_query = logins_query.filter(LoginActivity.timestamp <= end_utc)

    recent_activities = activities_query.order_by(ActivityLog.timestamp.desc()).limit(20).all()
    recent_logins = logins_query.order_by(LoginActivity.timestamp.desc()).limit(20).all()

    # 📊 CHART DATA: Stock 
    from sqlalchemy import func
    chart_data = db.session.query(
        Product.category,
        func.sum(Product.stock).label('total_stock')
    ).filter(
        Product.category.isnot(None),
        Product.category != ''
    ).group_by(Product.category).all()
    
    chart_categories = [row.category for row in chart_data]
    chart_stocks = [row.total_stock for row in chart_data]

    return render_template(
        'admin_dashboard.html',
        username=session['username'],
        total_items=total_items,
        low_stock_items=low_stock_items,
        low_stock_count=low_stock_count,
        items_added_today=items_added_today,
        total_staff=total_staff,
        recent_activities=recent_activities,
        recent_logins=recent_logins,
        chart_categories=chart_categories,
        chart_stocks=chart_stocks,
        start_date=start_date,
        end_date=end_date
    )

@app.route('/staff_dashboard')
def staff_dashboard():
    if session.get('role') != 'staff':
        flash("Access denied: Staff only.", "danger")
        return redirect(url_for('login'))
    
    # Get chart data
    from sqlalchemy import func
    chart_data = db.session.query(
        Product.category,
        func.sum(Product.stock).label('total_stock')
    ).filter(
        Product.category.isnot(None),
        Product.category != ''
    ).group_by(Product.category).all()
    
    chart_categories = [row.category for row in chart_data]
    chart_stocks = [row.total_stock for row in chart_data]
    
    # Get recent products for staff
    recent_products = Product.query.order_by(Product.created_at.desc()).limit(6).all()
    
    return render_template('staff_dashboard.html', 
        username=session['username'],
        chart_categories=chart_categories,
        chart_stocks=chart_stocks,
        recent_products=recent_products  # Add this
    )


# =====================================================
# USER MANAGEMENT ROUTES (Admin Only)
# =====================================================
@app.route('/register_staff', methods=['GET', 'POST'])
@admin_only
def register_staff():
    if request.method == 'POST':
        errors = []
        
        # Get all fields with proper defaults
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        department = request.form.get('department', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        phone = request.form.get('phone', '').strip() or "Not provided"
        
        # --- Validation Rules ---
        
        # First Name
        if not first_name:
            errors.append("First name is required")
        elif len(first_name) < 2:
            errors.append("First name must be at least 2 characters")
        elif not re.match(r'^[a-zA-Z\s\-]+$', first_name):
            errors.append("First name can only contain letters, spaces, and hyphens")
        
        # Last Name
        if not last_name:
            errors.append("Last name is required")
        elif len(last_name) < 2:
            errors.append("Last name must be at least 2 characters")
        elif not re.match(r'^[a-zA-Z\s\-]+$', last_name):
            errors.append("Last name can only contain letters, spaces, and hyphens")
        
        # Email
        if not email:
            errors.append("Email address is required")
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            errors.append("Invalid email format")
        elif User.query.filter_by(email=email).first():
            errors.append("Email is already registered")
        
        # Department
        if not department:
            errors.append("Department selection is required")
        elif department not in ['Sales', 'Inventory', 'Customer Service', 'Management', 'General']:
            errors.append("Invalid department selected")
        
        # Username
        if not username:
            errors.append("Username is required")
        elif len(username) < 3:
            errors.append("Username must be at least 3 characters")
        elif len(username) > 50:
            errors.append("Username cannot exceed 50 characters")
        elif not re.match(r'^[a-zA-Z0-9_]+$', username):
            errors.append("Username can only contain letters, numbers, and underscores")
        elif User.query.filter_by(username=username).first():
            errors.append("Username is already taken")
        
        # Password
        if not password:
            errors.append("Password is required")
        elif len(password) < 6:
            errors.append("Password must be at least 6 characters")
        elif len(password) > 128:
            errors.append("Password cannot exceed 128 characters")
        elif password != confirm_password:
            errors.append("Passwords do not match")
        
        # Confirm Password
        if not confirm_password:
            errors.append("Please confirm the password")
        
        # Phone (Optional but validated if provided)
        if phone != "Not provided":
            if not re.match(r'^[\d\-\+\(\)\s]+$', phone):
                errors.append("Invalid phone number format")
            elif len(phone) > 20:
                errors.append("Phone number cannot exceed 20 characters")
        
        # --- Handle Errors ---
        if errors:
            for error in errors:
                flash(f"❌ {error}", "danger")
            return render_template('register_staff.html')
        
        # --- Create User ---
        try:
            new_staff = User(
                username=username,
                password=bcrypt.generate_password_hash(password).decode('utf-8'),
                role='staff',
                must_change_password=True,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                department=department,
                is_active=True,
                is_approved=True,
                terms_accepted=False
            )
            
            db.session.add(new_staff)
            
            log = ActivityLog(
                user_id=session['user_id'],
                username=session['username'],
                action="Registered staff",
                product_name=f"{first_name} {last_name}"
            )
            db.session.add(log)
            db.session.commit()
            
            flash(f"✅ Staff '{username}' created successfully!", "success")
            flash(f"🔑 Temporary password: {password}", "info")
            flash("⚠️ Staff must change password on first login", "warning")
            return redirect(url_for('manage_users'))
            
        except Exception as e:
            db.session.rollback()
            flash(f"❌ Database error: {str(e)}", "danger")
            return render_template('register_staff.html')
    
    # GET request
    return render_template('register_staff.html')

# Add API endpoints for validation
@app.route('/api/check_username')
def check_username():
    """Check if username is available"""
    username = request.args.get('username', '').strip()
    
    if not username or len(username) < 3:
        return {'available': False, 'message': 'Username too short'}
    
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return {'available': False, 'message': 'Invalid characters'}
    
    if User.query.filter_by(username=username).first():
        return {'available': False, 'message': 'Username already taken'}
    
    return {'available': True, 'message': 'Username available'}

@app.route('/api/check_email')
def check_email():
    """Check if email is available"""
    email = request.args.get('email', '').strip()
    
    if not email or '@' not in email:
        return {'available': False, 'message': 'Invalid email format'}
    
    if User.query.filter_by(email=email).first():
        return {'available': False, 'message': 'Email already registered'}
    
    return {'available': True, 'message': 'Email available'}


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

@app.route('/inventory')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Get query parameters from URL
    search_query = request.args.get('query', '').strip()
    sort_by = request.args.get('sort', 'id')
    order = request.args.get('order', 'asc')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    # Validate parameters for security
    allowed_columns = ['id', 'name', 'brand', 'category', 'size', 'stock', 'price', 'created_at']
    if sort_by not in allowed_columns:
        sort_by = 'id'
    if order not in ['asc', 'desc']:
        order = 'asc'
    if per_page not in [10, 20, 50, 100]:  
        per_page = 20

    # Build base query
    query = Product.query

    # Apply search filter
    if search_query:
        query = query.filter(
            db.or_(
                Product.name.ilike(f"%{search_query}%"),
                Product.brand.ilike(f"%{search_query}%"),
                Product.category.ilike(f"%{search_query}%"),
                Product.size.ilike(f"%{search_query}%"),
                Product.size_unit.ilike(f"%{search_query}%")
            )
        )

    # Apply sorting
    sort_column = getattr(Product, sort_by)
    if order == 'desc':
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    # Apply pagination
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    products = pagination.items

    #  DYNAMIC
    unique_brands = db.session.query(Product.brand).filter(
        Product.brand.isnot(None),
        Product.brand != ''
    ).distinct().order_by(Product.brand).all()
    unique_brands = [brand[0] for brand in unique_brands if brand[0]]

    return render_template('index.html', 
                         products=products, 
                         pagination=pagination,
                         search_query=search_query,
                         sort_by=sort_by,
                         order=order,
                         per_page=per_page,
                         unique_brands=unique_brands)  

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

        # image upload
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
    
    # Store original values for comparison
    original_values = {
        'name': product.name,
        'stock': product.stock,
        'price': product.price,
        'brand': product.brand,
        'category': product.category,
        'size': product.size,
        'size_unit': product.size_unit
    }

    if request.method == 'POST':
        # Get and validate reason
        edit_reason = request.form.get('edit_reason', '').strip()
        if not edit_reason:
            flash("❌ Edit reason is required!", "danger")
            return render_template('edit_product.html', product=product)

        # Create activity log entry first
        activity_msg = f"{session['role'].capitalize()} edited product"
        log = ActivityLog(
            user_id=session['user_id'],
            username=session['username'],
            action=activity_msg,
            product_name=product.name
        )
        db.session.add(log)
        db.session.flush()  # Get log.id for foreign key

        # Track field changes
        changes = []
        fields_to_check = ['name', 'brand', 'category', 'size', 'size_unit', 'stock', 'price']
        
        for field in fields_to_check:
            new_value = request.form.get(field)
            if field in ['stock', 'price']:
                new_value = float(new_value) if field == 'price' else int(new_value)
            
            if str(original_values[field]) != str(new_value):
                changes.append({
                    'field': field,
                    'old': original_values[field],
                    'new': new_value
                })
                
                # Create detailed change log
                change_log = ProductChangeLog(
                    activity_log_id=log.id,
                    product_id=product.id,
                    product_name=product.name,
                    field_name=field,
                    old_value=str(original_values[field]),
                    new_value=str(new_value),
                    change_reason=edit_reason,
                    user_id=session['user_id'],
                    username=session['username']
                )
                db.session.add(change_log)

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
            product.image = image_file

        db.session.commit()

        flash(f'✅ Product updated successfully! {len(changes)} fields changed.', 'success')
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
    old_stock = product.stock
    
    try:
        added_qty = int(request.form['added_qty'])
        
        if added_qty <= 0:
            flash("Quantity must be at least 1.", "danger")
            return redirect(url_for('index'))
            
        if added_qty > 1000:
            flash("Maximum 1000 units at once.", "danger")
            return redirect(url_for('index'))

        product.stock += added_qty
        db.session.commit()

        # ✅ LOG STOCK HISTORY
        history = StockHistory(
            product_id=product.id,
            product_name=product.name,
            old_stock=old_stock,
            new_stock=product.stock,
            change_reason=f"Added {added_qty} units",
            user_id=session['user_id'],
            username=session['username']
        )
        db.session.add(history)
        
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
        flash("Invalid quantity.", "danger")
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
    old_stock = product.stock
    
    try:
        deduct_qty = int(request.form['deduct_qty'])
        
        if deduct_qty <= 0:
            flash("Quantity must be at least 1.", "danger")
            return redirect(url_for('index'))
            
        if deduct_qty > product.stock:
            flash(f"Cannot deduct {deduct_qty}. Only {product.stock} in stock.", "danger")
            return redirect(url_for('index'))

        product.stock -= deduct_qty
        db.session.commit()

        # ✅ LOG STOCK HISTORY
        history = StockHistory(
            product_id=product.id,
            product_name=product.name,
            old_stock=old_stock,
            new_stock=product.stock,
            change_reason=f"Deducted {deduct_qty} units",
            user_id=session['user_id'],
            username=session['username']
        )
        db.session.add(history)
        
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
        flash("Invalid quantity.", "danger")
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
    users = User.query
    
    if query:
        users = users.filter(
            db.or_(
                User.username.ilike(f"%{query}%"),
                User.full_name.ilike(f"%{query}%"),
                User.email.ilike(f"%{query}%"),
                User.department.ilike(f"%{query}%")
            )
        )
    
    users = users.filter(User.role != 'admin').all()
    return render_template('manage_users.html', users=users, search_query=query)


# =====================================================
# ACTIVITY LOGS
# =====================================================

@app.route('/activity_logs')
@admin_only
def activity_logs():
    """Activity logs with date filtering, search, and pagination"""
    
    # Get filter parameters
    search_query = request.args.get('query', '').strip()
    start_date = request.args.get('start_date', '').strip()
    end_date = request.args.get('end_date', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Validate pagination
    if per_page not in [10, 20, 50, 100]:
        per_page = 20
    
    
    query = ActivityLog.query.options(db.joinedload(ActivityLog.changes))
    
    # Apply search filter
    if search_query:
        query = query.filter(
            db.or_(
                ActivityLog.username.ilike(f"%{search_query}%"),
                ActivityLog.action.ilike(f"%{search_query}%"),
                ActivityLog.product_name.ilike(f"%{search_query}%")
            )
        )
    
    # Apply date filters
    if start_date or end_date:
        from sqlalchemy import text
        
        # Manila timezone conversion
        manila_tz = timezone(timedelta(hours=8))
        
        if start_date:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            start_manila = start_dt.replace(hour=0, minute=0, second=0, tzinfo=manila_tz)
            start_utc = start_manila.astimezone(timezone.utc)
            query = query.filter(ActivityLog.timestamp >= start_utc)
        
        if end_date:
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            end_manila = end_dt.replace(hour=23, minute=59, second=59, tzinfo=manila_tz)
            end_utc = end_manila.astimezone(timezone.utc)
            query = query.filter(ActivityLog.timestamp <= end_utc)
    
    # Apply sorting
    query = query.order_by(ActivityLog.timestamp.desc())
    
    # Paginate
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    logs = pagination.items
    
    
    total_logs = query.count()
    unique_users = db.session.query(ActivityLog.username).distinct().count()
    
    return render_template('activity_logs.html', 
                         logs=logs,
                         pagination=pagination,
                         search_query=search_query,
                         start_date=start_date,
                         end_date=end_date,
                         per_page=per_page,
                         total_logs=total_logs,
                         unique_users=unique_users)


@app.context_processor
def inject_admin_alerts():
    """Make low stock count and active users available in templates"""
    low_stock_products = Product.query.filter(Product.stock < 5).all()
    
    # Only count approved active users
    active_users = User.query.filter(
        User.is_active == True, 
        User.is_approved == True
    ).count()
    
    return {
        'low_stock_products': low_stock_products,
        'low_stock_count': len(low_stock_products),
        'active_users': active_users
    }

@app.context_processor
def inject_invitation_count():
    """Make pending invitation count available"""
    def get_count():
        return Invitation.query.filter_by(used=False).count()
    return {'pending_invitations_count': get_count}


@app.context_processor
def inject_report_alerts():
    """Make unread report count available in all templates"""
    def get_unread_report_count():
        return UserReport.query.filter_by(status='unread').count()
    

    return {
        'UserReport': UserReport, 
        'unread_reports_count': get_unread_report_count
    }

# =====================================================
# HOMEPAGE ROUTE
# =====================================================

@app.route('/')
def homepage():
    
    total_products = Product.query.count()
    low_stock_count = Product.query.filter(Product.stock < 5).count()
    active_users = User.query.filter(User.is_active == True).count()
    
    
    recent_products = []
    if session.get('role') == 'admin':
        recent_products = Product.query.order_by(Product.created_at.desc()).limit(6).all()
    
    return render_template('homepage.html',
                         total_products=total_products,
                         low_stock_count=low_stock_count,
                         active_users=active_users,
                         recent_products=recent_products)

# =====================================================
# CLI COMMANDS
# =====================================================

@app.cli.command('create-admin')
def create_admin():
    """Create a full admin profile from the command line"""
    
    # Username
    username = input('Enter admin username: ').strip()
    if User.query.filter_by(username=username).first():
        print(f"❌ Username '{username}' already exists!")
        return
    
    # Password
    password = input('Enter admin password: ')
    if len(password) < 6:
        print("❌ Password must be at least 6 characters")
        return
    
    # Full Name
    full_name = input('Enter full name: ').strip()
    if len(full_name) < 3:
        print("❌ Full name must be at least 3 characters")
        return
    
    # Email
    email = input('Enter email address: ').strip()
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        print("❌ Invalid email format")
        return
    if User.query.filter_by(email=email).first():
        print(f"❌ Email '{email}' is already registered")
        return
    
    # Phone (optional)
    phone = input('Enter phone number (optional): ').strip()
    phone = phone if phone else None
    
    # Department (optional)
    department = input('Enter department (default: Management): ').strip()
    department = department if department else 'Management'
    
    # Create admin
    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    new_admin = User(
        username=username,
        password=hashed_pw,
        role='admin',
        full_name=full_name,
        email=email,
        phone=phone,
        department=department,
        is_active=True
    )
    db.session.add(new_admin)
    db.session.commit()
    
    print(f'✅ Admin "{full_name}" created successfully!')
    print(f'   Username: {username}')
    print(f'   Email: {email}')
    print(f'   Department: {department}')

# =====================================================
# EXPORT INVENTORY TO CSV
# =====================================================
@app.route('/export_csv')
def export_csv():
    """Export CSV with customizable columns and advanced filters including Brand"""
    if 'username' not in session or session.get('role') not in ['admin', 'staff']:
        flash("Access denied.", "danger")
        return redirect(url_for('login'))
    
    # Get column selection
    columns = request.args.getlist('columns')
    include_headers = request.args.get('include_headers') == 'true'
    
    # Get filters
    brand_filter = request.args.get('brand_filter', '').strip()
    category_filter = request.args.get('category_filter', '').strip()
    size_min = request.args.get('size_min', '').strip()
    size_max = request.args.get('size_max', '').strip()
    stock_min = request.args.get('stock_min', type=int)
    stock_max = request.args.get('stock_max', type=int)
    price_min = request.args.get('price_min', type=float)
    price_max = request.args.get('price_max', type=float)
    date_start = request.args.get('date_start', '').strip()
    date_end = request.args.get('date_end', '').strip()
    
    # Validate columns
    if not columns:
        flash("❌ Please select at least one column to export.", "warning")
        return redirect(url_for('index'))
    
    # Map column names to headers
    column_headers = {
        'name': 'Product Name',
        'brand': 'Brand',
        'category': 'Category',
        'size': 'Size',
        'stock': 'Stock',
        'price': 'Price (₱)',
        'created_at': 'Created Date'
    }
    
    # Build base query
    query = Product.query
    
    # Apply filters dynamically
    filters_applied = []
    
    #  NEW: Brand filter
    if brand_filter:
        query = query.filter(Product.brand.ilike(f"%{brand_filter}%"))
        filters_applied.append(f"Brand: {brand_filter}")
    
    if category_filter:
        query = query.filter(Product.category == category_filter)
        filters_applied.append(f"Category: {category_filter}")
    
    if size_min or size_max:
        if size_min and size_max:
            query = query.filter(Product.size.between(size_min, size_max))
            filters_applied.append(f"Size: {size_min} - {size_max}")
        elif size_min:
            query = query.filter(Product.size >= size_min)
            filters_applied.append(f"Size ≥ {size_min}")
        elif size_max:
            query = query.filter(Product.size <= size_max)
            filters_applied.append(f"Size ≤ {size_max}")
    
    if stock_min is not None or stock_max is not None:
        if stock_min is not None and stock_max is not None:
            query = query.filter(Product.stock.between(stock_min, stock_max))
            filters_applied.append(f"Stock: {stock_min} - {stock_max}")
        elif stock_min is not None:
            query = query.filter(Product.stock >= stock_min)
            filters_applied.append(f"Stock ≥ {stock_min}")
        elif stock_max is not None:
            query = query.filter(Product.stock <= stock_max)
            filters_applied.append(f"Stock ≤ {stock_max}")
    
    if price_min is not None or price_max is not None:
        if price_min is not None and price_max is not None:
            query = query.filter(Product.price.between(price_min, price_max))
            filters_applied.append(f"Price: ₱{price_min:.2f} - ₱{price_max:.2f}")
        elif price_min is not None:
            query = query.filter(Product.price >= price_min)
            filters_applied.append(f"Price ≥ ₱{price_min:.2f}")
        elif price_max is not None:
            query = query.filter(Product.price <= price_max)
            filters_applied.append(f"Price ≤ ₱{price_max:.2f}")
    
    if date_start or date_end:
        if date_start:
            start_date = datetime.strptime(date_start, '%Y-%m-%d')
            query = query.filter(Product.created_at >= start_date)
        if date_end:
            end_date = datetime.strptime(date_end, '%Y-%m-%d') + timedelta(days=1)
            query = query.filter(Product.created_at < end_date)
        filters_applied.append(f"Date: {date_start or 'Start'} to {date_end or 'End'}")
    
    # Apply search 
    search_query = request.args.get('query', '').strip()
    if search_query:
        query = query.filter(
            db.or_(
                Product.name.ilike(f"%{search_query}%"),
                Product.brand.ilike(f"%{search_query}%"),
                Product.category.ilike(f"%{search_query}%"),
                Product.size.ilike(f"%{search_query}%")
            )
        )
        filters_applied.append(f"Search: '{search_query}'")
    
    # Sort by name
    products = query.order_by(Product.name.asc()).all()
    
    if not products:
        flash("⚠️ No products found matching your filters.", "warning")
        return redirect(url_for('index'))
    
    # Create CSV
    output = StringIO()
    writer = csv.writer(output)
    
    # Write filters comment
    if filters_applied:
        writer.writerow([f"Filters Applied: {' | '.join(filters_applied)}"])
    
    # Write headers
    if include_headers:
        headers = [column_headers.get(col, col) for col in columns]
        writer.writerow(headers)
    
    # Write data rows
    for product in products:
        row = []
        for col in columns:
            if col == 'name':
                row.append(product.name or 'N/A')
            elif col == 'brand':
                row.append(product.brand or 'N/A')
            elif col == 'category':
                row.append(product.category or 'N/A')
            elif col == 'size':
                size_str = f"{product.size} {product.size_unit}" if product.size and product.size_unit else product.size or 'N/A'
                row.append(size_str)
            elif col == 'stock':
                row.append(str(product.stock or 0))
            elif col == 'price':
                row.append(f"{product.price:.2f}" if product.price else '0.00')
            elif col == 'created_at':
                row.append(product.created_at.strftime("%Y-%m-%d %H:%M:%S") if product.created_at else 'N/A')
            else:
                row.append('N/A')
        writer.writerow(row)
    
    # Prepare response
    response = make_response(output.getvalue())
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filter_text = "_filtered" if filters_applied else "_all"
    filename = f"inventory{filter_text}_{timestamp}.csv"
    
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    response.headers["X-Content-Type-Options"] = "nosniff"
    
    return response

# =====================================================
# STOCK HISTORY ROUTE
# =====================================================

@app.route('/product_history/<int:product_id>')
def product_history(product_id):
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))
    
    if session.get('role') not in ['admin', 'staff']:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('index'))
    
    product = Product.query.get_or_404(product_id)
    histories = StockHistory.query.filter_by(product_id=product_id).order_by(StockHistory.timestamp.desc()).all()
    
    return render_template('product_history.html', product=product, histories=histories)

@app.route('/debug')
def debug_homepage():
    total = Product.query.count()
    low_stock = Product.query.filter(Product.stock < 5).count()
    active = User.query.filter(User.is_active == True).count()
    
 
    print(f"DEBUG: total_products={total}, low_stock={low_stock}, active_users={active}")
    

    return {
        "total_products": total,
        "low_stock_count": low_stock,
        "active_users": active,
        "db_url": app.config['SQLALCHEMY_DATABASE_URI']
    }

# =====================================================
# INVITATION MANAGEMENT ROUTES
# =====================================================

@app.route('/create_invitation', methods=['GET', 'POST'])
@admin_only
def create_invitation():
    """
    Generate a secure, time-limited invitation link for staff registration.
    Uses naive UTC datetimes for MySQL compatibility.
    """
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        department = request.form.get('department', 'General')
        
       
        errors = []
        
        # Email format validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not email:
            errors.append("Email address is required.")
        elif not re.match(email_pattern, email):
            errors.append("Invalid email format.")
        
        # for existing invitation 
        existing = Invitation.query.filter(
            Invitation.email == email,
            Invitation.used == False,
            Invitation.expires_at > datetime.utcnow()
        ).first()
        
        if existing:
            errors.append(f"Active invitation already exists for {email}")
        
        # if user already exists
        if User.query.filter_by(email=email).first():
            errors.append(f"User with email {email} already exists")
        
        if errors:
            for error in errors:
                flash(f"❌ {error}", "danger")
            return render_template('create_invitation.html', 
                                   email=email, 
                                   department=department)
        
        try:
            #  CREATE INVITATION
            invitation = Invitation(
                email=email,
                department=department,
                created_by=session['user_id']
            )
            db.session.add(invitation)
            db.session.flush()  
            
            # Generate URL 
            registration_url = url_for('register_with_invite', 
                                       token=invitation.token, 
                                       _external=True)
            
            # Log activity
            log = ActivityLog(
                user_id=session['user_id'],
                username=session['username'],
                action=f"Admin created invitation for {email}",
                product_name=f"{department} Department"
            )
            db.session.add(log)
            db.session.commit()
            
            # Store in session
            session['invite_link'] = registration_url
            session['invite_email'] = email
            
            flash(f"✅ Invitation created successfully!", "success")
            return redirect(url_for('view_invitations'))
            
        except Exception as e:
            db.session.rollback()
            flash(f"❌ Error creating invitation: {str(e)}", "danger")
            return render_template('create_invitation.html')
    
    # GET request
    return render_template('create_invitation.html')


@app.route('/view_invitations')
@admin_only
def view_invitations():
    """View all active (unused and not expired) invitations"""
    active_invites = Invitation.query.filter(
        Invitation.used == False,
        Invitation.expires_at > datetime.utcnow()
    ).order_by(Invitation.created_at.desc()).all()
    
    return render_template('view_invitations.html', invitations=active_invites)


@app.route('/cancel_invitation/<int:invite_id>')
@admin_only
def cancel_invitation(invite_id):
    """Cancel an unused invitation"""
    invite = Invitation.query.get_or_404(invite_id)
    
    if invite.used:
        flash("❌ Cannot cancel used invitation", "warning")
    else:
        db.session.delete(invite)
        db.session.commit()
        flash(f"✅ Invitation for {invite.email} cancelled", "success")
    
    return redirect(url_for('view_invitations'))

# =====================================================
# INVITATION-BASED REGISTRATION
# =====================================================
@app.route('/register/<token>', methods=['GET', 'POST'])
def register_with_invite(token):
    """
    Enhanced registration with comprehensive user details
    """
    invitation = Invitation.query.filter_by(token=token).first()
    
    if not invitation or invitation.used:
        flash("❌ Invalid or already used invitation link", "danger")
        return redirect(url_for('login'))
    
    # Check expiry
    now = datetime.utcnow() 
    expires_at = invitation.expires_at
    if expires_at.tzinfo is not None:
        expires_at = expires_at.replace(tzinfo=None)
    
    if now > expires_at:
        flash("❌ This invitation has expired", "danger")
        return redirect(url_for('login'))
    
    if request.method == 'GET':
        return render_template('register_with_invite.html', 
                               token=token, 
                               email=invitation.email,
                               department=invitation.department)
    
    # ==== SERVER-SIDE VALIDATION ====
    errors = []
    
    # Required fields
    required_fields = ['username', 'password', 'confirm_password', 
                       'first_name', 'last_name', 'phone', 'birthdate']
    
    for field in required_fields:
        if not request.form.get(field):
            errors.append(f"{field.replace('_', ' ').title()} is required.")
    
    # Username validation
    username = request.form['username'].strip()
    if len(username) < 3:
        errors.append("Username must be at least 3 characters.")
    if User.query.filter_by(username=username).first():
        errors.append(f"Username '{username}' already exists.")
    
    # Password validation
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    if len(password) < 6:
        errors.append("Password must be at least 6 characters.")
    if password != confirm_password:
        errors.append("Passwords do not match.")
    
    # Name validation
    if len(request.form['first_name']) < 2:
        errors.append("First name must be at least 2 characters.")
    if len(request.form['last_name']) < 2:
        errors.append("Last name must be at least 2 characters.")
    
    # Date validation
    try:
        birthdate = datetime.strptime(request.form['birthdate'], '%Y-%m-%d').date()
        today = datetime.now().date()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        if age < 18:
            errors.append("You must be at least 18 years old to register.")
    except ValueError:
        errors.append("Invalid birthdate format.")
    
   
    phone = request.form['phone'].strip()
    if not re.match(r'^[\d\-\+\(\)\s]+$', phone):
        errors.append("Invalid phone number format.")
    
    
    if not request.form.get('terms_accepted'):
        errors.append("You must accept the Terms and Conditions.")
    
    # Display errors
    if errors:
        for error in errors:
            flash(f"❌ {error}", "danger")
        return render_template('register_with_invite.html', 
                               token=token, 
                               email=invitation.email,
                               department=invitation.department,
                               form_data=request.form)
    
    try:
        # Create user with enhanced details
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(
            username=username,
            password=hashed_pw,
            role=invitation.role,
            first_name=request.form['first_name'].strip(),
            middle_name=request.form.get('middle_name', '').strip() or None,
            last_name=request.form['last_name'].strip(),
            email=invitation.email,
            phone=phone,
            department=invitation.department,
            birthdate=birthdate,
            address=request.form.get('address', '').strip() or None,
            city=request.form.get('city', '').strip() or None,
            country=request.form.get('country', '').strip() or None,
            gender=request.form.get('gender') or None,
            education_level=request.form.get('education_level') or None,
            is_active=True,
            is_approved=True,
            terms_accepted=True
        )
        db.session.add(new_user)
        
        
        invitation.used = True
        invitation.used_at = datetime.utcnow()
        
        # Log activity
        log = ActivityLog(
            user_id=None,
            username="System",
            action=f"Staff registered via invitation",
            product_name=f"{new_user.full_name} ({invitation.email})"
        )
        db.session.add(log)
        db.session.commit()
        
        flash(f"✅ Registration successful! Welcome {new_user.full_name}. You can now log in.", "success")
        return redirect(url_for('login'))
        
    except Exception as e:
        db.session.rollback()
        flash(f"❌ Registration failed: {str(e)}", "danger")
        return render_template('register_with_invite.html', 
                               token=token, 
                               email=invitation.email,
                               department=invitation.department,
                               form_data=request.form)

# =====================================================
# ACCOUNT MANAGEMENT ROUTES
# =====================================================

@app.route('/account')
def account():
    """Display user account details"""
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))
    
    user = User.query.get_or_404(session['user_id'])
    return render_template('account.html', user=user)


@app.route('/delete_account/<int:id>', methods=['POST'])
def delete_account(id):
    """Allow user to delete their own account"""
    if 'user_id' not in session or session['user_id'] != id:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('login'))
    
    user = User.query.get_or_404(id)
    
    # Prevent admin self-deletion
    if user.role == 'admin':
        flash("Admin accounts cannot be self-deleted. Contact another admin.", "danger")
        return redirect(url_for('account'))
    
    try:
        # Log the deletion
        log = ActivityLog(
            user_id=session['user_id'],
            username=session['username'],
            action="User deleted their own account",
            product_name=f"{user.full_name} ({user.email})"
        )
        db.session.add(log)
        

        UserReport.query.filter_by(user_id=user.id).delete()
        
        db.session.delete(user)
        db.session.commit()
        
        session.clear()
        return {"success": True, "message": "Account deleted successfully"}
        
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": str(e)}, 500


# =====================================================
# REPORTING SYSTEM ROUTES
# =====================================================

@app.route('/submit_report', methods=['POST'])
def submit_report():
    """Submit a user report/issue"""
    if 'user_id' not in session:
        return {"success": False, "message": "Not logged in"}, 401
    
    data = request.get_json()
    
    # Validate
    if not data.get('message') or len(data['message'].strip()) < 10:
        return {"success": False, "message": "Message must be at least 10 characters"}, 400
    
    if not data.get('report_type'):
        return {"success": False, "message": "Please select an issue type"}, 400
    
    try:
        report = UserReport(
            user_id=session['user_id'],
            report_type=data['report_type'],
            message=data['message'].strip(),
            status='unread'
        )
        db.session.add(report)
        db.session.commit()
        

        
        return {"success": True, "message": "Report submitted successfully"}
        
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": str(e)}, 500


@app.route('/api/unread_reports')
@admin_only
def api_unread_reports():
    """API endpoint for unread report count (polling)"""
    count = UserReport.query.filter_by(status='unread').count()
    return {"count": count}


@app.route('/admin/reports')
@admin_only
def admin_reports():
    """Admin page to view and manage user reports"""
    reports = UserReport.query.order_by(UserReport.created_at.desc()).all()
    return render_template('manage_reports.html', reports=reports)


@app.route('/admin/report_action/<int:report_id>', methods=['POST'])
@admin_only
def report_action(report_id):
    """Mark report as read/resolved"""
    report = UserReport.query.get_or_404(report_id)
    action = request.json.get('action')
    
    if action == 'mark_read':
        report.status = 'read'
    elif action == 'resolve':
        report.status = 'resolved'
    elif action == 'delete':
        db.session.delete(report)
    
    db.session.commit()
    return {"success": True}


# =====================================================
# API: Get Current User Details
# =====================================================

@app.context_processor
def inject_user_details():
    """Make current user available in all templates"""
    if 'user_id' in session:
        return {'current_user': User.query.get(session['user_id'])}
    return {'current_user': None}



@app.context_processor
def inject_user_utils():
    """Safe utility functions for templates (not filters)"""
    
    def get_last_login(user_id):
        """Get formatted last login time for a user"""
        last_login = LoginActivity.query.filter_by(
            user_id=user_id, 
            action='Login'
        ).order_by(LoginActivity.timestamp.desc()).first()
        
        if not last_login or not last_login.timestamp:
            return 'First time'
        
        
        return manila_time_filter(last_login.timestamp)
    
    def format_date_value(value, format='%B %d, %Y'):
        """Format a date value (not a filter)"""
        if not value:
            return 'N/A'
        try:
            return value.strftime(format)
        except:
            return str(value)
    
   
    return {
        'get_last_login': get_last_login,
        'format_date_value': format_date_value,
    }
# =====================================================
# RUN APPLICATION
# =====================================================

if __name__ == '__main__':
    # Create tables 
    with app.app_context():
        db.create_all()
    
    app.run(host='0.0.0.0', port=5000, debug=(os.getenv('FLASK_DEBUG', 'True') == 'True'))