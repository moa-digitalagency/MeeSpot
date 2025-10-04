import os
import bcrypt
from app import app, db, User

def create_admin():
    with app.app_context():
        db.create_all()
        
        email = input("Enter admin email: ")
        
        existing = User.query.filter_by(email=email).first()
        if existing:
            print(f"User with email {email} already exists.")
            make_admin = input("Make this user an admin? (yes/no): ")
            if make_admin.lower() == 'yes':
                existing.role = 'admin'
                db.session.commit()
                print(f"User {email} is now an admin!")
            return
        
        name = input("Enter admin name: ")
        password = input("Enter admin password: ")
        
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        admin = User(
            email=email,
            password_hash=password_hash,
            name=name,
            role='admin',
            gender='other',
            age=30,
            orientation='other'
        )
        
        db.session.add(admin)
        db.session.commit()
        
        print(f"Admin user created successfully!")
        print(f"Email: {email}")
        print(f"Name: {name}")
        print(f"Role: admin")

if __name__ == '__main__':
    create_admin()
