"""
Campus Resource Hub - Flask Application
Main application file for the campus resource management system.
"""

import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///campus_hub.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Import models and initialize db
from models import User, Resource, Booking, Message, Review, db
db.init_app(app)

# Initialize extensions
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    """Home page with featured resources and quick search."""
    featured_resources = Resource.query.filter_by(is_available=True).limit(6).all()
    return render_template('index.html', featured_resources=featured_resources)

@app.route('/resources')
def resources():
    """Browse all available resources."""
    page = request.args.get('page', 1, type=int)
    resource_type = request.args.get('type', '')
    search_query = request.args.get('search', '')
    
    query = Resource.query.filter_by(is_available=True)
    
    if resource_type:
        query = query.filter_by(resource_type=resource_type)
    
    if search_query:
        query = query.filter(Resource.name.contains(search_query) | 
                           Resource.description.contains(search_query))
    
    resources = query.paginate(
        page=page, per_page=12, error_out=False
    )
    
    return render_template('resources.html', resources=resources, 
                         resource_type=resource_type, search_query=search_query)

@app.route('/resources/<int:resource_id>')
def resource_detail(resource_id):
    """View detailed information about a specific resource."""
    resource = Resource.query.get_or_404(resource_id)
    reviews = Review.query.filter_by(resource_id=resource_id).all()
    return render_template('resource_detail.html', resource=resource, reviews=reviews)

@app.route('/bookings')
@login_required
def bookings():
    """View user's bookings."""
    user_bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.start_time.desc()).all()
    return render_template('bookings.html', bookings=user_bookings)

@app.route('/bookings/new/<int:resource_id>')
@login_required
def new_booking(resource_id):
    """Create a new booking for a resource."""
    resource = Resource.query.get_or_404(resource_id)
    return render_template('new_booking.html', resource=resource)

@app.route('/bookings/create', methods=['POST'])
@login_required
def create_booking():
    """Process new booking creation."""
    resource_id = request.form.get('resource_id')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    purpose = request.form.get('purpose', '')
    
    # Check for conflicts
    conflicting_booking = Booking.query.filter(
        Booking.resource_id == resource_id,
        Booking.status.in_(['confirmed', 'pending']),
        Booking.start_time < end_time,
        Booking.end_time > start_time
    ).first()
    
    if conflicting_booking:
        flash('This time slot conflicts with an existing booking.', 'error')
        return redirect(url_for('new_booking', resource_id=resource_id))
    
    # Create new booking
    booking = Booking(
        user_id=current_user.id,
        resource_id=resource_id,
        start_time=datetime.fromisoformat(start_time),
        end_time=datetime.fromisoformat(end_time),
        purpose=purpose,
        status='pending'
    )
    
    db.session.add(booking)
    db.session.commit()
    
    flash('Booking request submitted successfully!', 'success')
    return redirect(url_for('bookings'))

@app.route('/admin')
@login_required
def admin_dashboard():
    """Admin dashboard for managing resources and bookings."""
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    pending_bookings = Booking.query.filter_by(status='pending').all()
    all_resources = Resource.query.all()
    return render_template('admin/dashboard.html', 
                         pending_bookings=pending_bookings, 
                         resources=all_resources)

@app.route('/admin/resources/new')
@login_required
def new_resource():
    """Create a new resource (admin only)."""
    if current_user.role not in ['admin', 'staff']:
        flash('Access denied. Staff privileges required.', 'error')
        return redirect(url_for('index'))
    
    return render_template('admin/new_resource.html')

@app.route('/admin/resources/create', methods=['POST'])
@login_required
def create_resource():
    """Process new resource creation."""
    if current_user.role not in ['admin', 'staff']:
        flash('Access denied. Staff privileges required.', 'error')
        return redirect(url_for('index'))
    
    resource = Resource(
        name=request.form.get('name'),
        description=request.form.get('description'),
        resource_type=request.form.get('resource_type'),
        location=request.form.get('location'),
        capacity=int(request.form.get('capacity', 1)),
        owner_id=current_user.id
    )
    
    db.session.add(resource)
    db.session.commit()
    
    flash('Resource created successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

# Authentication routes
@app.route('/auth/register', methods=['GET', 'POST'])
def register():
    """User registration."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        role = request.form.get('role', 'student')
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return render_template('auth/register.html')
        
        # Create new user
        user = User(
            email=email,
            password_hash=generate_password_hash(password),
            first_name=first_name,
            last_name=last_name,
            role=role
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('auth/register.html')

@app.route('/auth/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('auth/login.html')

@app.route('/auth/logout')
@login_required
def logout():
    """User logout."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# API routes for AJAX requests
@app.route('/api/resources')
def api_resources():
    """API endpoint for resources."""
    resources = Resource.query.filter_by(is_available=True).all()
    return jsonify([{
        'id': r.id,
        'name': r.name,
        'description': r.description,
        'type': r.resource_type,
        'location': r.location,
        'capacity': r.capacity
    } for r in resources])

@app.route('/api/bookings/<int:resource_id>')
def api_resource_bookings(resource_id):
    """API endpoint for resource bookings."""
    bookings = Booking.query.filter_by(resource_id=resource_id, status='confirmed').all()
    return jsonify([{
        'start_time': b.start_time.isoformat(),
        'end_time': b.end_time.isoformat(),
        'purpose': b.purpose
    } for b in bookings])

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

# Context processors
@app.context_processor
def inject_user():
    return dict(current_user=current_user)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
