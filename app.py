from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from flask_restful import Api, Resource
from flask_migrate import Migrate
import os
from models import db, User, Parcel

app = Flask(__name__)

CORS(app)

# --------------------------configuration--------------------------------------
# Load appropriate configuration based on FLASK_ENV
if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object('config.ProductionConfig')
elif os.getenv('FLASK_ENV') == 'testing':
    app.config.from_object('config.TestingConfig')
else:
    app.config.from_object('config.DevelopmentConfig')

# Configure SQLAlchemy database URI based on environment variables
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Set up database URI based on environment (use DB_EXTERNAL_URL by default)
if os.getenv('FLASK_ENV') == 'production':
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_INTERNAL_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_EXTERNAL_URL")

# Set the Flask app secret key from environment variable
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")



# db = SQLAlchemy(app)

# Initialize SQLAlchemy with the Flask app
db.init_app(app)

# Create the app context
with app.app_context():
    # Create the database tables if they don't exist
    db.create_all()

migrate = Migrate(app, db)
api = Api(app)



#--------------------------------------------
# Admin Endpoints
class CreateUserResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        role = data.get('role')
        firebase_uid = data.get('firebase_uid')
        user_status = data.get('status', 'active')

        if not email or not role or not firebase_uid:
            return jsonify({'error': 'Email, role, and firebase_uid are required'}), 400

        # Check if the user already exists
        if User.query.filter_by(firebase_uid=firebase_uid).first():
            return jsonify({'error': 'User with this Firebase UID already exists'}), 400

        try:
            user = User(
                email=email,
                role=role,
                firebase_uid=firebase_uid,
                user_status=user_status
            )
            db.session.add(user)
            db.session.commit()
            return jsonify({'message': 'User created successfully', 'user': user.to_dict()}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400
        

class SearchUserByIdResource(Resource):
    def get(self, user_id):
        """Search user by user ID"""
        user = User.query.get(user_id)
        if not user:
            abort(404, description="User not found")
        return jsonify(user.to_dict())

class SearchUserByEmailResource(Resource):
    def get(self, email):
        """Search user by user email"""
        user = User.query.get(email)
        if not user:
            abort(404, description="User not found")
        return jsonify(user.to_dict())
        
class UpdateUserProfileResource(Resource):
    def put(self, user_id):
        data = request.get_json()

        # Fetch the user by ID
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Update user attributes if they are provided in the request data
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.company_name = data.get('company_name', user.company_name)
        user.phone_number = data.get('phone_number', user.phone_number)
        user.address = data.get('address', user.address)
        user.profile_photo_url = data.get('profile_photo_url', user.profile_photo_url)
        user.account_balance = data.get('account_balance', user.account_balance)
        user.gps_location = data.get('gps_location', user.gps_location)
        user.country = data.get('country', user.country)
        user.mode_of_transport = data.get('mode_of_transport', user.mode_of_transport)

        try:
            db.session.commit()
            return jsonify({'message': 'User profile updated successfully', 'user': user.to_dict()}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

class UserListResource(Resource):
    def get(self):
        """Admin: Get a list of all users"""
        users = User.get_all_users()
        return jsonify([user.to_dict() for user in users])

class ParcelListResource(Resource):
    def get(self):
        """Admin: Get a list of all parcels with details"""
        parcels = Parcel.get_parcels_with_details()
        return jsonify([parcel.to_dict() for parcel in parcels])

class CourierListResource(Resource):
    def get(self, status=None):
        """Admin: Get a list of couriers filtered by status"""
        if status:
            couriers = User.get_couriers_by_status(status)
        else:
            couriers = User.get_users_by_role('individual_courier') + User.get_users_by_role('corporate_courier')
        return jsonify([courier.to_dict() for courier in couriers])

class ParcelSearchByTrackingResource(Resource):
    def get(self, tracking_number):
        """Admin: Search parcels by tracking number"""
        parcel = Parcel.get_parcel_by_tracking_number(tracking_number)
        if not parcel:
            abort(404, description="Parcel not found")
        return jsonify(parcel.to_dict())

class UserSearchByStatusResource(Resource):
    def get(self, status):
        """Admin: Get a list of users filtered by status"""
        users = User.get_users_by_status(status)
        return jsonify([user.to_dict() for user in users])

#--------------------------------------------
# Client Endpoints
class ClientParcelListResource(Resource):
    def get(self, client_id):
        """Client: Get all parcels where the client is the sender or recipient"""
        parcels = Parcel.get_parcels_by_client(client_id)
        return jsonify([parcel.to_dict() for parcel in parcels])

class CreateParcelResource(Resource):
    def post(self):
        """Client: Create a new parcel"""
        data = request.json
        try:
            parcel = Parcel(
                weight=data['weight'],
                length=data['length'],
                width=data['width'],
                height=data['height'],
                value=data['value'],
                pickup_location=data['pickup_location'],
                drop_off_location=data['drop_off_location'],
                sender_id=data['sender_id'],
                recipient_id=data['recipient_id'],
                courier_id=data.get('courier_id'),  # Optional
                shipping_cost=data['shipping_cost'],
                distance=data['distance']
            )
            db.session.add(parcel)
            db.session.commit()
            return jsonify(parcel.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            abort(400, description=f"Error creating parcel: {str(e)}")

class ParcelTrackingResource(Resource):
    def get(self, tracking_number):
        """Client: Get parcel details by tracking number"""
        parcel = Parcel.get_parcel_by_tracking_number(tracking_number)
        if not parcel:
            abort(404, description="Parcel not found")
        return jsonify(parcel.to_dict())

#--------------------------------------------
# API Routes
# Admin routes
api.add_resource(UserListResource, '/admin/users')
api.add_resource(ParcelListResource, '/admin/parcels')
api.add_resource(CourierListResource, '/admin/couriers', '/admin/couriers/<string:status>')
api.add_resource(ParcelSearchByTrackingResource, '/admin/parcels/track/<string:tracking_number>')
api.add_resource(UserSearchByStatusResource, '/admin/users/status/<string:status>')

# Client routes
api.add_resource(ClientParcelListResource, '/client/<int:client_id>/parcels')
api.add_resource(CreateParcelResource, '/client/parcels')
api.add_resource(ParcelTrackingResource, '/client/parcels/track/<string:tracking_number>')

# updating user profile
api.add_resource(UpdateUserProfileResource, '/user/profiles')
# creating user
api.add_resource(CreateUserResource, '/users')

#Search user by id
api.add_resource(SearchUserByIdResource, '/users/<int:user_id>')

#Search user by email
api.add_resource(SearchUserByEmailResource, '/users/<string:email>')


#--------------------------------------------
# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
