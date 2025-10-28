"""
Database initialization script for Campus Resource Hub
Creates database tables and populates with sample data.
"""

import os
import sys
from datetime import datetime, timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Initialize Flask app for database operations
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///campus_hub.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Import models first
from models import User, Resource, Booking, Message, Review, db

# Initialize db with app
db.init_app(app)

def create_tables():
    """Create all database tables."""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

def create_sample_data():
    """Create sample data for testing and development."""
    with app.app_context():
        # Check if data already exists
        if User.query.first():
            print("Sample data already exists. Skipping data creation.")
            return
        
        print("Creating sample users...")
        
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
        
        student1 = User(
            email='student@campus.edu',
            first_name='Student',
            last_name='User',
            role='student'
        )
        student1.set_password('student123')
        
        student2 = User(
            email='john.doe@campus.edu',
            first_name='John',
            last_name='Doe',
            role='student'
        )
        student2.set_password('password123')
        
        db.session.add_all([admin, staff, student1, student2])
        db.session.commit()
        
        print("Creating sample resources...")
        
        # Create sample resources
        resources = [
            Resource(
                name='Conference Room A',
                description='Large conference room with projector, whiteboard, and seating for 20 people. Perfect for presentations and meetings.',
                resource_type='room',
                location='Building 1, Floor 2, Room 201',
                capacity=20,
                hourly_rate=0.00,
                owner_id=staff.id
            ),
            Resource(
                name='Study Room 101',
                description='Quiet study space with individual desks, power outlets, and whiteboard. Ideal for focused studying.',
                resource_type='room',
                location='Library, Floor 1, Room 101',
                capacity=4,
                hourly_rate=0.00,
                owner_id=staff.id
            ),
            Resource(
                name='Study Room 102',
                description='Group study room with large table and presentation screen.',
                resource_type='room',
                location='Library, Floor 1, Room 102',
                capacity=8,
                hourly_rate=0.00,
                owner_id=staff.id
            ),
            Resource(
                name='Laptop Cart',
                description='Mobile laptop cart with 20 Dell laptops, charging station, and WiFi hotspot.',
                resource_type='equipment',
                location='IT Department',
                capacity=20,
                hourly_rate=0.00,
                owner_id=staff.id
            ),
            Resource(
                name='3D Printer',
                description='Ultimaker 3D printer for prototyping and educational projects. Includes PLA filament.',
                resource_type='equipment',
                location='Engineering Lab, Room 305',
                capacity=1,
                hourly_rate=5.00,
                owner_id=staff.id
            ),
            Resource(
                name='Outdoor Pavilion',
                description='Covered outdoor space with picnic tables, power outlets, and WiFi access.',
                resource_type='space',
                location='Central Quad',
                capacity=50,
                hourly_rate=0.00,
                owner_id=staff.id
            ),
            Resource(
                name='Recording Studio',
                description='Professional recording studio with audio equipment, microphones, and soundproofing.',
                resource_type='room',
                location='Media Center, Floor 2',
                capacity=6,
                hourly_rate=10.00,
                owner_id=staff.id
            ),
            Resource(
                name='Computer Lab 1',
                description='Computer lab with 25 workstations, projector, and printing facilities.',
                resource_type='room',
                location='Computer Science Building, Floor 1',
                capacity=25,
                hourly_rate=0.00,
                owner_id=staff.id
            ),
            Resource(
                name='VR Headset Set',
                description='Set of 4 VR headsets with controllers and gaming PC setup.',
                resource_type='equipment',
                location='Gaming Lab, Room 205',
                capacity=4,
                hourly_rate=15.00,
                owner_id=staff.id
            ),
            Resource(
                name='Art Studio',
                description='Art studio with easels, supplies, and natural lighting.',
                resource_type='room',
                location='Fine Arts Building, Floor 2',
                capacity=12,
                hourly_rate=0.00,
                owner_id=staff.id
            )
        ]
        
        db.session.add_all(resources)
        db.session.commit()
        
        print("Creating sample bookings...")
        
        # Create sample bookings
        now = datetime.utcnow()
        bookings = [
            Booking(
                user_id=student1.id,
                resource_id=resources[1].id,  # Study Room 101
                start_time=now.replace(hour=14, minute=0, second=0, microsecond=0),
                end_time=now.replace(hour=16, minute=0, second=0, microsecond=0),
                status='confirmed',
                purpose='Group study session for Calculus exam'
            ),
            Booking(
                user_id=student1.id,
                resource_id=resources[0].id,  # Conference Room A
                start_time=now.replace(hour=10, minute=0, second=0, microsecond=0) + timedelta(days=1),
                end_time=now.replace(hour=12, minute=0, second=0, microsecond=0) + timedelta(days=1),
                status='pending',
                purpose='Project presentation rehearsal'
            ),
            Booking(
                user_id=student2.id,
                resource_id=resources[2].id,  # Study Room 102
                start_time=now.replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days=2),
                end_time=now.replace(hour=11, minute=0, second=0, microsecond=0) + timedelta(days=2),
                status='confirmed',
                purpose='Team project meeting'
            ),
            Booking(
                user_id=student2.id,
                resource_id=resources[4].id,  # 3D Printer
                start_time=now.replace(hour=13, minute=0, second=0, microsecond=0) + timedelta(days=3),
                end_time=now.replace(hour=15, minute=0, second=0, microsecond=0) + timedelta(days=3),
                status='pending',
                purpose='Prototype printing for engineering project'
            )
        ]
        
        db.session.add_all(bookings)
        db.session.commit()
        
        print("Creating sample reviews...")
        
        # Create sample reviews
        reviews = [
            Review(
                user_id=student1.id,
                resource_id=resources[1].id,  # Study Room 101
                rating=5,
                comment='Perfect quiet space for studying. Great lighting and comfortable chairs. Highly recommended!'
            ),
            Review(
                user_id=student1.id,
                resource_id=resources[0].id,  # Conference Room A
                rating=4,
                comment='Excellent facilities and equipment. The projector sometimes has connectivity issues, but overall great for presentations.'
            ),
            Review(
                user_id=student2.id,
                resource_id=resources[2].id,  # Study Room 102
                rating=5,
                comment='Spacious room perfect for group work. The presentation screen is very helpful for collaborative projects.'
            ),
            Review(
                user_id=student2.id,
                resource_id=resources[4].id,  # 3D Printer
                rating=4,
                comment='Great 3D printer with good quality output. The staff is very helpful with setup and troubleshooting.'
            )
        ]
        
        db.session.add_all(reviews)
        db.session.commit()
        
        print("Creating sample messages...")
        
        # Create sample messages
        messages = [
            Message(
                booking_id=bookings[1].id,  # Pending booking
                sender_id=student1.id,
                content='Hi, I would like to request this room for our project presentation rehearsal. We need the projector and whiteboard.'
            ),
            Message(
                booking_id=bookings[1].id,
                sender_id=staff.id,
                content='Approved! The room is available and all equipment is working properly. Have a great presentation!'
            ),
            Message(
                booking_id=bookings[3].id,  # 3D Printer booking
                sender_id=student2.id,
                content='I need to print a prototype for my engineering project. Could you please confirm the booking?'
            )
        ]
        
        db.session.add_all(messages)
        db.session.commit()
        
        print("\n" + "="*50)
        print("DATABASE INITIALIZATION COMPLETE!")
        print("="*50)
        print("\nSample users created:")
        print("• admin@campus.edu (password: admin123) - Admin")
        print("• staff@campus.edu (password: staff123) - Staff")
        print("• student@campus.edu (password: student123) - Student")
        print("• john.doe@campus.edu (password: password123) - Student")
        print(f"\nSample resources created: {len(resources)}")
        print(f"Sample bookings created: {len(bookings)}")
        print(f"Sample reviews created: {len(reviews)}")
        print(f"Sample messages created: {len(messages)}")
        print("\nYou can now run the Flask application with: python app.py")

def reset_database():
    """Reset the database (drop all tables and recreate)."""
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()
        print("Creating all tables...")
        db.create_all()
        print("Database reset complete!")

def main():
    """Main function to initialize the database."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Initialize Campus Resource Hub database')
    parser.add_argument('--reset', action='store_true', help='Reset database (drop all tables)')
    parser.add_argument('--no-data', action='store_true', help='Create tables only, no sample data')
    
    args = parser.parse_args()
    
    if args.reset:
        reset_database()
    
    create_tables()
    
    if not args.no_data:
        create_sample_data()

if __name__ == '__main__':
    main()
