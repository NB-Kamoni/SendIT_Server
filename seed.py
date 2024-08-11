from app import db, app  # Import 'db' and 'app' from your Flask application
from models import User, Parcel  # Import models from 'models.py'

def seed_data():
    with app.app_context():  # Create an application context
        db.create_all()

        # Create users with additional fields
        user1 = User(
            email='client@example.com', 
            firebase_uid='client_uid', 
            first_name='Client', 
            last_name='User', 
            role='client', 
            account_balance=100.0,
            gps_location='12.9716,77.5946',  # Example GPS location
            country='USA',
            user_status='active',
            company_name='Client Company',  # Example company name
            mode_of_transport='Car',  # Example mode of transport
            profile_photo_url='https://example.com/profiles/client.jpg'  # Profile photo URL
        )
        user2 = User(
            email='courier@example.com', 
            firebase_uid='courier_uid', 
            first_name='Courier', 
            last_name='User', 
            role='individual_courier', 
            account_balance=50.0,
            gps_location='13.0827,80.2707',  # Example GPS location
            country='Canada',
            user_status='active',
            company_name='Courier Services',  # Example company name
            mode_of_transport='Bike',  # Example mode of transport
            profile_photo_url='https://example.com/profiles/courier.jpg'  # Profile photo URL
        )
        user3 = User(
            email='admin@example.com', 
            firebase_uid='admin_uid', 
            first_name='Admin', 
            last_name='User', 
            role='admin', 
            account_balance=500.0,
            gps_location='51.5074,-0.1278',  # Example GPS location
            country='UK',
            user_status='active',
            company_name='Admin Corporation',  # Example company name
            mode_of_transport='Public Transport',  # Example mode of transport
            profile_photo_url='https://example.com/profiles/admin.jpg'  # Profile photo URL
        )
        
        # Add users to the session
        db.session.add_all([user1, user2, user3])
        
        # Commit the session to get user IDs
        db.session.commit()

        # Retrieve user IDs after committing
        user1 = User.query.filter_by(email='client@example.com').first()
        user2 = User.query.filter_by(email='courier@example.com').first()
        user3 = User.query.filter_by(email='admin@example.com').first()
        
        # Create parcels
        parcel1 = Parcel(
            weight=10.0, 
            length=20.0, 
            width=30.0, 
            height=40.0, 
            value=100.0, 
            pickup_location='Location A', 
            drop_off_location='Location B', 
            sender_id=user1.id, 
            recipient_id=user2.id, 
            courier_id=user2.id,  # Courier assigned to this parcel
            shipping_cost=25.0, 
            distance=15.0
        )
        parcel2 = Parcel(
            weight=5.0, 
            length=10.0, 
            width=15.0, 
            height=20.0, 
            value=50.0, 
            pickup_location='Location C', 
            drop_off_location='Location D', 
            sender_id=user2.id, 
            recipient_id=user1.id, 
            courier_id=user2.id,  # Courier assigned to this parcel
            shipping_cost=15.0, 
            distance=10.0
        )
        
        # Add parcels to the session
        db.session.add_all([parcel1, parcel2])
        
        # Commit the session
        db.session.commit()

if __name__ == '__main__':
    seed_data()
