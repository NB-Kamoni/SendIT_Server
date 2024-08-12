from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask_cors import CORS
from firebase_admin import auth, initialize_app, credentials
import os
import base64
import json
from models import db, User, Parcel

# Initialize the Flask application
app = Flask(__name__)
CORS(app)

# Load configuration from environment variables or set defaults
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///sendit.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key')

# Initialize SQLAlchemy, Migrate, and API
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

# Decode Firebase credentials from environment variable
firebase_credentials_base64 = os.getenv('FIREBASE_CREDENTIALS_BASE64')
if not firebase_credentials_base64:
    raise Exception("Firebase credentials not found in environment variables")

firebase_credentials_json = base64.b64decode(firebase_credentials_base64)
firebase_credentials = json.loads(firebase_credentials_json)

# Initialize Firebase Admin SDK
cred = credentials.Certificate(firebase_credentials)
initialize_app(cred)

# Firebase authentication decorator
def firebase_required(f):
    def decorator(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return make_response(jsonify({'message': 'Missing or invalid authorization header'}), 401)
        
        token = auth_header.split(' ')[1]
        try:
            decoded_token = auth.verify_id_token(token)
            request.user = decoded_token
        except Exception as e:
            app.logger.error(f"Firebase authentication error: {e}")
            return make_response(jsonify({'message': 'Invalid token', 'error': str(e)}), 401)
        
        return f(*args, **kwargs)
    
    decorator.__name__ = f.__name__
    return decorator

# API Resources
class UserResource(Resource):
    # @firebase_required
    def get(self, user_id=None):
        try:
            if user_id:
                user = User.query.get_or_404(user_id)
                return jsonify(user.to_dict())
            else:
                users = User.query.all()
                return jsonify([user.to_dict() for user in users])
        except Exception as e:
            app.logger.error(f"Error fetching users: {e}")
            return make_response(jsonify({'message': 'Internal server error'}), 500)

    # @firebase_required
    def post(self, user_id=None):
        if user_id:
            return make_response(jsonify({'message': 'User ID should not be provided for POST'}), 400)

        try:
            data = request.json

            user = User(
                email=data.get('email', ''),
                firebase_uid=data.get('firebase_uid', ''),
                first_name=data.get('first_name', ''),
                last_name=data.get('last_name', ''),
                company_name=data.get('company_name', ''),
                phone_number=data.get('phone_number', ''),
                address=data.get('address', ''),
                role=data.get('role', ''),
                profile_photo_url=data.get('profile_photo_url', ''),
                account_balance=data.get('account_balance', 0.0),
                gps_location=data.get('gps_location', None),
                country=data.get('country', ''),
                user_status=data.get('user_status', ''),
                mode_of_transport=data.get('mode_of_transport', '')
            )
            db.session.add(user)
            db.session.commit()
            return jsonify(user.to_dict()), 201
        except Exception as e:
            db.session.rollback()  # Rollback on error
            app.logger.error(f"Error creating user: {e}")
            return make_response(jsonify({'message': 'Internal server error'}), 500)

    # @firebase_required
    def put(self, user_id):
        try:
            user = User.query.get_or_404(user_id)
            data = request.json
            user.email = data.get('email', user.email)
            user.first_name = data.get('first_name', user.first_name)
            user.last_name = data.get('last_name', user.last_name)
            user.company_name = data.get('company_name', user.company_name)
            user.phone_number = data.get('phone_number', user.phone_number)
            user.address = data.get('address', user.address)
            user.role = data.get('role', user.role)
            user.profile_photo_url = data.get('profile_photo_url', user.profile_photo_url)
            user.account_balance = data.get('account_balance', user.account_balance)
            user.gps_location = data.get('gps_location', user.gps_location)
            user.country = data.get('country', user.country)
            user.user_status = data.get('user_status', user.user_status)
            user.mode_of_transport = data.get('mode_of_transport', user.mode_of_transport)
            db.session.commit()
            return jsonify(user.to_dict())
        except Exception as e:
            db.session.rollback()  # Rollback on error
            app.logger.error(f"Error updating user: {e}")
            return make_response(jsonify({'message': 'Internal server error'}), 500)

    # @firebase_required
    def delete(self, user_id):
        try:
            user = User.query.get_or_404(user_id)
            db.session.delete(user)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()  # Rollback on error
            app.logger.error(f"Error deleting user: {e}")
            return make_response(jsonify({'message': 'Internal server error'}), 500)

class ParcelResource(Resource):
    # @firebase_required
    def get(self, parcel_id=None):
        try:
            if parcel_id:
                parcel = Parcel.query.get_or_404(parcel_id)
                return jsonify(parcel.to_dict())
            else:
                parcels = Parcel.query.all()
                return jsonify([parcel.to_dict() for parcel in parcels])
        except Exception as e:
            app.logger.error(f"Error fetching parcels: {e}")
            return make_response(jsonify({'message': 'Internal server error'}), 500)

    # @firebase_required
    def post(self, parcel_id=None):
        if parcel_id:
            return make_response(jsonify({'message': 'Parcel ID should not be provided for POST'}), 400)

        try:
            data = request.json

            parcel = Parcel(
                weight=data.get('weight', 0),
                length=data.get('length', 0),
                width=data.get('width', 0),
                height=data.get('height', 0),
                value=data.get('value', 0),
                pickup_location=data.get('pickup_location', ''),
                drop_off_location=data.get('drop_off_location', ''),
                sender_id=data.get('sender_id', None),
                recipient_id=data.get('recipient_id', None),
                courier_id=data.get('courier_id', None),
                delivery_status=data.get('delivery_status', 'pending'),
                shipping_cost=data.get('shipping_cost', 0),
                distance=data.get('distance', 0)
            )
            db.session.add(parcel)
            db.session.commit()
            return jsonify(parcel.to_dict()), 201
        except Exception as e:
            db.session.rollback()  # Rollback on error
            app.logger.error(f"Error creating parcel: {e}")
            return make_response(jsonify({'message': 'Internal server error'}), 500)

    # @firebase_required
    def put(self, parcel_id):
        try:
            parcel = Parcel.query.get_or_404(parcel_id)
            data = request.json
            parcel.weight = data.get('weight', parcel.weight)
            parcel.length = data.get('length', parcel.length)
            parcel.width = data.get('width', parcel.width)
            parcel.height = data.get('height', parcel.height)
            parcel.value = data.get('value', parcel.value)
            parcel.pickup_location = data.get('pickup_location', parcel.pickup_location)
            parcel.drop_off_location = data.get('drop_off_location', parcel.drop_off_location)
            parcel.sender_id = data.get('sender_id', parcel.sender_id)
            parcel.recipient_id = data.get('recipient_id', parcel.recipient_id)
            parcel.courier_id = data.get('courier_id', parcel.courier_id)
            parcel.delivery_status = data.get('delivery_status', parcel.delivery_status)
            parcel.shipping_cost = data.get('shipping_cost', parcel.shipping_cost)
            parcel.distance = data.get('distance', parcel.distance)
            db.session.commit()
            return jsonify(parcel.to_dict())
        except Exception as e:
            db.session.rollback()  # Rollback on error
            app.logger.error(f"Error updating parcel: {e}")
            return make_response(jsonify({'message': 'Internal server error'}), 500)

    # @firebase_required
    def delete(self, parcel_id):
        try:
            parcel = Parcel.query.get_or_404(parcel_id)
            db.session.delete(parcel)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()  # Rollback on error
            app.logger.error(f"Error deleting parcel: {e}")
            return make_response(jsonify({'message': 'Internal server error'}), 500)

# Register API resources
api.add_resource(UserResource, '/users', '/users/<int:user_id>')
api.add_resource(ParcelResource, '/parcels', '/parcels/<int:parcel_id>')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
