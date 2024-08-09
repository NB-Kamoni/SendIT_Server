from app import db, User, Parcel, app  # Import 'app' from your Flask application

def seed_data():
    with app.app_context():  # Create an application context
        db.create_all()

        # Create users
        user1 = User(email='client@example.com', firebase_uid='client_uid', first_name='Client', last_name='User', role='client', account_balance=100.0)
        user2 = User(email='courier@example.com', firebase_uid='courier_uid', first_name='Courier', last_name='User', role='individual_courier', account_balance=50.0)
        user3 = User(email='admin@example.com', firebase_uid='admin_uid', first_name='Admin', last_name='User', role='admin', account_balance=500.0)
        
        # Add users to the session
        db.session.add_all([user1, user2, user3])
        
        # Create parcels
        parcel1 = Parcel(weight=10.0, length=20.0, width=30.0, height=40.0, value=100.0, pickup_location='Location A', drop_off_location='Location B', sender_id=1, recipient_id=2, shipping_cost=25.0, distance=15.0)
        parcel2 = Parcel(weight=5.0, length=10.0, width=15.0, height=20.0, value=50.0, pickup_location='Location C', drop_off_location='Location D', sender_id=2, recipient_id=1, shipping_cost=15.0, distance=10.0)
        
        # Add parcels to the session
        db.session.add_all([parcel1, parcel2])
        
        # Commit the session
        db.session.commit()

if __name__ == '__main__':
    seed_data()
