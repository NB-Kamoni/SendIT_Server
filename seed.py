from app import app, db
from app import User, Parcel

# Clear existing data in tables
def clear_data():
    db.session.query(Parcel).delete()
    db.session.query(User).delete()
    db.session.commit()

# Create seed data
def seed_data():
    # Create users
    users = [
        User(
            email="user1@example.com",
            firebase_uid="uid1",
            first_name="John",
            last_name="Doe",
            phone_number="1234567890",
            address="123 Main St, Anytown, USA",
            role="client",
            profile_photo_url="http://example.com/photo1.jpg"
        ),
        User(
            email="user2@example.com",
            firebase_uid="uid2",
            first_name="Jane",
            last_name="Smith",
            phone_number="0987654321",
            address="456 Elm St, Othertown, USA",
            role="courier",
            profile_photo_url="http://example.com/photo2.jpg"
        ),
        User(
            email="user3@example.com",
            firebase_uid="uid3",
            first_name="Alice",
            last_name="Brown",
            phone_number="1122334455",
            address="789 Oak St, Anycity, USA",
            role="admin",
            profile_photo_url="http://example.com/photo3.jpg"
        )
    ]

    # Add users to the session
    db.session.add_all(users)
    db.session.commit()

    # Create parcels
    parcels = [
        Parcel(
            weight=2.5,
            length=30.0,
            width=20.0,
            height=10.0,
            value=100.00,
            pickup_location="123 Main St, Anytown, USA",
            drop_off_location="789 Oak St, Anycity, USA",
            sender_id=users[0].id,
            recipient_id=users[2].id,
            courier_id=users[1].id,
            delivery_status="pending"
        ),
        Parcel(
            weight=5.0,
            length=50.0,
            width=30.0,
            height=15.0,
            value=250.00,
            pickup_location="456 Elm St, Othertown, USA",
            drop_off_location="789 Oak St, Anycity, USA",
            sender_id=users[2].id,
            recipient_id=users[0].id,
            courier_id=users[1].id,
            delivery_status="shipped"
        )
    ]

    # Add parcels to the session
    db.session.add_all(parcels)
    db.session.commit()

# Seed the database
if __name__ == '__main__':
    with app.app_context():  # Ensure the operations are within the app context
        # Clear existing data
        clear_data()

        # Seed the data
        seed_data()

    print("Database seeded successfully!")
