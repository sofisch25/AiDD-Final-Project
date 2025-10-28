"""
Database models for Campus Resource Hub
Defines the SQLAlchemy models for users, resources, bookings, messages, and reviews.
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication and user management."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), default='student')  # student, staff, admin
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    owned_resources = db.relationship('Resource', backref='owner', lazy='dynamic')
    bookings = db.relationship('Booking', backref='user', lazy='dynamic')
    reviews = db.relationship('Review', backref='user', lazy='dynamic')
    sent_messages = db.relationship('Message', backref='sender', lazy='dynamic')
    
    def set_password(self, password):
        """Set password hash."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash."""
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f'<User {self.email}>'

class Resource(db.Model):
    """Resource model for campus resources (rooms, equipment, spaces)."""
    
    __tablename__ = 'resources'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    resource_type = db.Column(db.String(50), nullable=False)  # room, equipment, space
    location = db.Column(db.String(100))
    capacity = db.Column(db.Integer, default=1)
    hourly_rate = db.Column(db.Numeric(10, 2), default=0.00)
    is_available = db.Column(db.Boolean, default=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('Booking', backref='resource', lazy='dynamic')
    reviews = db.relationship('Review', backref='resource', lazy='dynamic')
    
    def get_availability_status(self):
        """Get current availability status."""
        if not self.is_available:
            return 'unavailable'
        
        now = datetime.utcnow()
        active_booking = Booking.query.filter(
            Booking.resource_id == self.id,
            Booking.status == 'confirmed',
            Booking.start_time <= now,
            Booking.end_time >= now
        ).first()
        
        return 'occupied' if active_booking else 'available'
    
    def get_upcoming_bookings(self, limit=5):
        """Get upcoming bookings for this resource."""
        return Booking.query.filter(
            Booking.resource_id == self.id,
            Booking.status == 'confirmed',
            Booking.start_time > datetime.utcnow()
        ).order_by(Booking.start_time).limit(limit).all()
    
    def get_average_rating(self):
        """Get average rating for this resource."""
        reviews = Review.query.filter_by(resource_id=self.id).all()
        if not reviews:
            return 0
        return sum(review.rating for review in reviews) / len(reviews)
    
    def __repr__(self):
        return f'<Resource {self.name}>'

class Booking(db.Model):
    """Booking model for resource reservations."""
    
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey('resources.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, cancelled, completed
    purpose = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    messages = db.relationship('Message', backref='booking', lazy='dynamic')
    
    def get_duration(self):
        """Get booking duration in hours."""
        duration = self.end_time - self.start_time
        return duration.total_seconds() / 3600
    
    def is_active(self):
        """Check if booking is currently active."""
        now = datetime.utcnow()
        return (self.status == 'confirmed' and 
                self.start_time <= now <= self.end_time)
    
    def is_upcoming(self):
        """Check if booking is upcoming."""
        return (self.status == 'confirmed' and 
                self.start_time > datetime.utcnow())
    
    def is_past(self):
        """Check if booking is in the past."""
        return self.end_time < datetime.utcnow()
    
    def can_be_cancelled(self):
        """Check if booking can be cancelled."""
        return (self.status in ['pending', 'confirmed'] and 
                self.start_time > datetime.utcnow())
    
    def __repr__(self):
        return f'<Booking {self.id}: {self.resource.name} by {self.user.email}>'

class Message(db.Model):
    """Message model for communication threads."""
    
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Message {self.id}: {self.content[:50]}...>'

class Review(db.Model):
    """Review model for resource ratings and feedback."""
    
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey('resources.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Ensure one review per user per resource
    __table_args__ = (db.UniqueConstraint('user_id', 'resource_id'),)
    
    def __repr__(self):
        return f'<Review {self.id}: {self.rating} stars for {self.resource.name}>'

# Database initialization function
def init_db():
    """Initialize database with sample data."""
    from app import app
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if data already exists
        if User.query.first():
            print("Database already initialized.")
            return
        
        # Create sample users
        admin = User(
            email='admin@campus.edu',
            first_name='Admin',
            last_name='User',
            role='admin'
        )
        admin.set_password('admin123')
        
        staff = User(
            email='staff@campus.edu',
            first_name='Staff',
            last_name='Member',
            role='staff'
        )
        staff.set_password('staff123')
        
        student = User(
            email='student@campus.edu',
            first_name='Student',
            last_name='User',
            role='student'
        )
        student.set_password('student123')
        
        db.session.add_all([admin, staff, student])
        db.session.commit()
        
        # Create sample resources
        resources = [
            Resource(
                name='Conference Room A',
                description='Large conference room with projector, whiteboard, and seating for 20 people.',
                resource_type='room',
                location='Building 1, Floor 2, Room 201',
                capacity=20,
                owner_id=staff.id
            ),
            Resource(
                name='Study Room 101',
                description='Quiet study space with individual desks and power outlets.',
                resource_type='room',
                location='Library, Floor 1, Room 101',
                capacity=4,
                owner_id=staff.id
            ),
            Resource(
                name='Laptop Cart',
                description='Mobile laptop cart with 20 Dell laptops and charging station.',
                resource_type='equipment',
                location='IT Department',
                capacity=20,
                owner_id=staff.id
            ),
            Resource(
                name='3D Printer',
                description='Ultimaker 3D printer for prototyping and educational projects.',
                resource_type='equipment',
                location='Engineering Lab, Room 305',
                capacity=1,
                owner_id=staff.id
            ),
            Resource(
                name='Outdoor Pavilion',
                description='Covered outdoor space with picnic tables and power outlets.',
                resource_type='space',
                location='Central Quad',
                capacity=50,
                owner_id=staff.id
            ),
            Resource(
                name='Recording Studio',
                description='Professional recording studio with audio equipment and soundproofing.',
                resource_type='room',
                location='Media Center, Floor 2',
                capacity=6,
                owner_id=staff.id
            )
        ]
        
        db.session.add_all(resources)
        db.session.commit()
        
        # Create sample bookings
        bookings = [
            Booking(
                user_id=student.id,
                resource_id=resources[1].id,  # Study Room 101
                start_time=datetime.utcnow().replace(hour=14, minute=0, second=0, microsecond=0),
                end_time=datetime.utcnow().replace(hour=16, minute=0, second=0, microsecond=0),
                status='confirmed',
                purpose='Group study session for Calculus exam'
            ),
            Booking(
                user_id=student.id,
                resource_id=resources[0].id,  # Conference Room A
                start_time=datetime.utcnow().replace(hour=10, minute=0, second=0, microsecond=0) + 
                          datetime.timedelta(days=1),
                end_time=datetime.utcnow().replace(hour=12, minute=0, second=0, microsecond=0) + 
                         datetime.timedelta(days=1),
                status='pending',
                purpose='Project presentation rehearsal'
            )
        ]
        
        db.session.add_all(bookings)
        db.session.commit()
        
        # Create sample reviews
        reviews = [
            Review(
                user_id=student.id,
                resource_id=resources[1].id,  # Study Room 101
                rating=5,
                comment='Perfect quiet space for studying. Great lighting and comfortable chairs.'
            ),
            Review(
                user_id=student.id,
                resource_id=resources[0].id,  # Conference Room A
                rating=4,
                comment='Excellent facilities, but the projector sometimes has connectivity issues.'
            )
        ]
        
        db.session.add_all(reviews)
        db.session.commit()
        
        print("Database initialized with sample data!")
        print("Sample users created:")
        print("- admin@campus.edu (password: admin123)")
        print("- staff@campus.edu (password: staff123)")
        print("- student@campus.edu (password: student123)")

if __name__ == '__main__':
    init_db()
