from app import app, db
from models import User, Parcel
from datetime import datetime, timedelta
import random
from sqlalchemy.exc import IntegrityError
from faker import Faker

fake = Faker()

def seed_users():
    """Seed the database with sample user data."""
    try:
        # Clear existing users
        User.query.delete()

        users = [
            {'email': 'client1@example.com', 'firebase_uid': 'firebase_uid_client1', 'role': 'client', 'first_name': 'Alice', 'last_name': 'Smith'},
            {'email': 'client2@example.com', 'firebase_uid': 'firebase_uid_client2', 'role': 'client', 'first_name': 'Bob', 'last_name': 'Johnson'},
            {'email': 'courier1@example.com', 'firebase_uid': 'firebase_uid_courier1', 'role': 'individual_courier', 'first_name': 'Charlie', 'last_name': 'Brown'},
            {'email': 'courier2@example.com', 'firebase_uid': 'firebase_uid_courier2', 'role': 'corporate_courier', 'first_name': 'Diana', 'last_name': 'Wilson'},
            {'email': 'admin@example.com', 'firebase_uid': 'firebase_uid_admin', 'role': 'admin', 'first_name': 'Eve', 'last_name': 'Davis'}
        ]

        for user_data in users:
            user = User(
                email=user_data['email'],
                firebase_uid=user_data['firebase_uid'],
                role=user_data['role'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name']
            )
            db.session.add(user)
        
        db.session.commit()
        print("Users seeded successfully.")
    except IntegrityError as e:
        db.session.rollback()
        print(f"IntegrityError: {e}")

def seed_parcels():
    """Seed the database with sample parcel data."""
    try:
        users = User.query.all()
        if len(users) < 3:
            print("Not enough users to create parcels.")
            return

        sender = users[0]
        recipient = users[1]
        courier = users[2] if len(users) > 2 else None

        now = datetime.utcnow()
        one_day = timedelta(days=1)

        parcels = [
            {
                'weight': random.uniform(1, 10),
                'length': random.uniform(10, 20),
                'width': random.uniform(5, 15),
                'height': random.uniform(5, 15),
                'value': random.uniform(100, 500),
                'pickup_location': 'Location A',
                'drop_off_location': 'Location B',
                'shipping_cost': random.uniform(10, 50),
                'distance': random.uniform(5, 20),
                'delivery_status': 'delivered',
                'created_at': now,
                'updated_at': now
            },
            {
                'weight': random.uniform(1, 10),
                'length': random.uniform(10, 20),
                'width': random.uniform(5, 15),
                'height': random.uniform(5, 15),
                'value': random.uniform(100, 500),
                'pickup_location': 'Location C',
                'drop_off_location': 'Location D',
                'shipping_cost': random.uniform(10, 50),
                'distance': random.uniform(5, 20),
                'delivery_status': 'in_progress',
                'created_at': now - one_day,
                'updated_at': now,
                
            }
        ]

        for parcel_data in parcels:
            parcel = Parcel(
                weight=parcel_data['weight'],
                length=parcel_data['length'],
                width=parcel_data['width'],
                height=parcel_data['height'],
                value=parcel_data['value'],
                pickup_location=parcel_data['pickup_location'],
                drop_off_location=parcel_data['drop_off_location'],
                sender_id=sender.id,
                recipient_id=recipient.id,
                courier_id=courier.id if courier else None,
                shipping_cost=parcel_data['shipping_cost'],
                distance=parcel_data['distance'],
                delivery_status=parcel_data['delivery_status'],
                created_at=parcel_data['created_at'],
                updated_at=parcel_data['updated_at']
            )
            try:
                db.session.add(parcel)
                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()
                print(f"Failed to add parcel with tracking number {parcel_data.get('tracking_number')}: {e}")

        print("Parcels seeded successfully.")
    except Exception as e:
        print(f"Error seeding parcels: {e}")

def seed_database():
    """Initialize the database and seed it with sample data."""
    with app.app_context():
        try:
            db.drop_all()
            db.create_all()
            seed_users()
            seed_parcels()
            print("Database seeded successfully.")
        except Exception as e:
            print(f"Error during database seeding: {e}")

if __name__ == '__main__':
    seed_database()
