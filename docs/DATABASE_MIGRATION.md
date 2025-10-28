# Database Migration Guide - Campus Resource Hub

## Overview

This document outlines the database migration process for the Campus Resource Hub application. The system uses Flask-SQLAlchemy with SQLite for development and supports PostgreSQL for production.

## Database Schema

### Core Tables

#### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128),
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    role VARCHAR(20) DEFAULT 'student',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);
```

#### Resources Table
```sql
CREATE TABLE resources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    resource_type VARCHAR(50) NOT NULL,
    location VARCHAR(100),
    capacity INTEGER,
    hourly_rate DECIMAL(10,2) DEFAULT 0.00,
    is_available BOOLEAN DEFAULT TRUE,
    owner_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users (id)
);
```

#### Bookings Table
```sql
CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    resource_id INTEGER NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    purpose TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (resource_id) REFERENCES resources (id)
);
```

#### Messages Table
```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INTEGER NOT NULL,
    sender_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES bookings (id),
    FOREIGN KEY (sender_id) REFERENCES users (id)
);
```

#### Reviews Table
```sql
CREATE TABLE reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    resource_id INTEGER NOT NULL,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (resource_id) REFERENCES resources (id)
);
```

## Migration Commands

### Initial Setup

1. **Initialize Flask-Migrate**
   ```bash
   flask db init
   ```

2. **Create initial migration**
   ```bash
   flask db migrate -m "Initial migration"
   ```

3. **Apply migration**
   ```bash
   flask db upgrade
   ```

### Development Workflow

1. **Make model changes** in your Python files
2. **Generate migration**
   ```bash
   flask db migrate -m "Description of changes"
   ```
3. **Review migration file** in `migrations/versions/`
4. **Apply migration**
   ```bash
   flask db upgrade
   ```

### Rollback

```bash
# Rollback to previous version
flask db downgrade

# Rollback to specific revision
flask db downgrade <revision_id>
```

## Sample Data Migration

### Initial Data Setup

Create a `sample_data.py` file:

```python
from app import app, db
from models import User, Resource, Booking
from werkzeug.security import generate_password_hash

def create_sample_data():
    with app.app_context():
        # Create users
        admin = User(
            email='admin@campus.edu',
            password_hash=generate_password_hash('admin123'),
            first_name='Admin',
            last_name='User',
            role='admin'
        )
        
        staff = User(
            email='staff@campus.edu',
            password_hash=generate_password_hash('staff123'),
            first_name='Staff',
            last_name='Member',
            role='staff'
        )
        
        student = User(
            email='student@campus.edu',
            password_hash=generate_password_hash('student123'),
            first_name='Student',
            last_name='User',
            role='student'
        )
        
        db.session.add_all([admin, staff, student])
        
        # Create resources
        resources = [
            Resource(
                name='Conference Room A',
                description='Large conference room with projector',
                resource_type='room',
                location='Building 1, Floor 2',
                capacity=20,
                owner_id=staff.id
            ),
            Resource(
                name='Study Room 101',
                description='Quiet study space',
                resource_type='room',
                location='Library, Floor 1',
                capacity=4,
                owner_id=staff.id
            ),
            Resource(
                name='Laptop Cart',
                description='Mobile laptop cart with 20 laptops',
                resource_type='equipment',
                location='IT Department',
                capacity=20,
                owner_id=staff.id
            )
        ]
        
        db.session.add_all(resources)
        db.session.commit()
        
        print("Sample data created successfully!")

if __name__ == '__main__':
    create_sample_data()
```

### Run Sample Data Migration

```bash
python sample_data.py
```

## Production Migration

### PostgreSQL Setup

1. **Install PostgreSQL**
2. **Create database**
   ```sql
   CREATE DATABASE campus_resource_hub;
   CREATE USER campus_user WITH PASSWORD 'secure_password';
   GRANT ALL PRIVILEGES ON DATABASE campus_resource_hub TO campus_user;
   ```

3. **Update DATABASE_URL**
   ```env
   DATABASE_URL=postgresql://campus_user:secure_password@localhost/campus_resource_hub
   ```

4. **Run migrations**
   ```bash
   flask db upgrade
   ```

### Backup and Restore

```bash
# Backup SQLite database
cp campus_hub.db backup_$(date +%Y%m%d).db

# Backup PostgreSQL database
pg_dump campus_resource_hub > backup_$(date +%Y%m%d).sql

# Restore PostgreSQL database
psql campus_resource_hub < backup_20231201.sql
```

## Migration Best Practices

1. **Always backup before migration**
2. **Test migrations on development first**
3. **Use descriptive migration messages**
4. **Review auto-generated migrations**
5. **Handle data migrations separately from schema changes**
6. **Use transactions for complex migrations**

## Troubleshooting

### Common Issues

**Migration conflicts:**
```bash
# Reset migrations (development only)
rm -rf migrations/
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

**Database locked (SQLite):**
- Ensure no other processes are using the database
- Check for uncommitted transactions

**Foreign key constraint errors:**
- Ensure referenced records exist before creating dependent records
- Use proper order in data migrations

### Migration Status

```bash
# Check current migration status
flask db current

# Show migration history
flask db history

# Show pending migrations
flask db show
```

## Environment-Specific Configurations

### Development
- SQLite database (`campus_hub.db`)
- Debug mode enabled
- Detailed error messages

### Production
- PostgreSQL database
- Debug mode disabled
- Error logging to files
- SSL/HTTPS enabled

## Data Validation

### Constraints
- Email addresses must be unique
- Booking times cannot overlap for same resource
- Ratings must be between 1-5
- Resource capacity must be positive

### Indexes
```sql
-- Performance indexes
CREATE INDEX idx_bookings_resource_time ON bookings(resource_id, start_time, end_time);
CREATE INDEX idx_bookings_user ON bookings(user_id);
CREATE INDEX idx_resources_type ON resources(resource_type);
CREATE INDEX idx_users_email ON users(email);
```

This migration guide ensures smooth database operations throughout the development and deployment lifecycle of the Campus Resource Hub application.
