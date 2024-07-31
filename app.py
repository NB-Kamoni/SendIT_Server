import os
from dotenv import load_dotenv
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from models import db, User, Parcel, DeliveryStatus

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load appropriate configuration based on FLASK_ENV
if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object('config.ProductionConfig')
elif os.getenv('FLASK_ENV') == 'testing':
    app.config.from_object('config.TestingConfig')
else:
    app.config.from_object('config.DevelopmentConfig')

# Configure SQLAlchemy database URI based on environment variables
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

# Set the Flask app secret key from environment variable
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Initialize SQLAlchemy with the Flask app
db.init_app(app)

# Create the app context
with app.app_context():
    # Create the database tables if they don't exist
    db.create_all()

# Set up Flask-Restful API
api = Api(app)

# ---------------------Define resource endpoints---------------------------------------------
# -------------------------USER RESOURCES-------------------------------------------------

class UserResource(Resource):
    def get(self):
        """
        Fetches either all users or a specific user by user_id, email, or name.
        """
        user_id = request.args.get('user_id')
        email = request.args.get('email')
        name = request.args.get('name')

        if user_id:
            user = User.query.filter_by(user_id=user_id).first()
            if user:
                return {'user': user.to_dict()}
            else:
                return {'message': 'User not found'}, 404

        elif email:
            user = User.query.filter_by(email=email).first()
            if user:
                return {'user': user.to_dict()}
            else:
                return {'message': 'User not found'}, 404

        elif name:
            users = User.query.filter(User.name.ilike(f'%{name}%')).all()
            if users:
                return {'users': [user.to_dict() for user in users]}
            else:
                return {'message': 'User not found'}, 404

        else:
            users = User.query.all()
            return {'users': [user.to_dict() for user in users]}

    def post(self):
        """
        Registers a new user.
        """
        data = request.get_json()
        new_user = User(
            name=data.get('name'),
            email=data.get('email'),
            password=data.get('password'),
            # Add other fields if necessary
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user.to_dict(), 201

    def put(self, user_id):
        """
        Updates information for a specific user identified by user_id.
        """
        data = request.get_json()
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        # Update user fields based on data provided
        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            user.email = data['email']
        if 'password' in data:
            user.password = data['password']

        db.session.commit()
        return user.to_dict()

    def delete(self, user_id):
        """
        Deletes a specific user identified by user_id.
        """
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted'}, 204

# Add resource endpoints to API
api.add_resource(UserResource, '/users', '/users/<int:user_id>')

# View all users:        GET /users
# Add new user:          POST /users
# Change user data:      PUT /users/<user_id>
# Delete users:          DELETE /users/<user_id>
# Search user by id:     GET /users?user_id=<user_id>
# Search user by email:  GET /users?email=<email>
# Search user by name:   GET /users?name=<name>

# -------------------------PARCEL RESOURCES-------------------------------------------------

class ParcelResource(Resource):
    def get(self):
        """
        Fetches either all parcels or a specific parcel by parcel_id or user_id.
        """
        parcel_id = request.args.get('parcel_id')
        user_id = request.args.get('user_id')

        if parcel_id:
            parcel = Parcel.query.filter_by(parcel_id=parcel_id).first()
            if parcel:
                return {'parcel': parcel.to_dict()}
            else:
                return {'message': 'Parcel not found'}, 404

        elif user_id:
            parcels = Parcel.query.filter_by(user_id=user_id).all()
            if parcels:
                return {'parcels': [parcel.to_dict() for parcel in parcels]}
            else:
                return {'message': 'No parcels found for this user'}, 404

        else:
            parcels = Parcel.query.all()
            return {'parcels': [parcel.to_dict() for parcel in parcels]}

    def post(self):
        """
        Creates a new parcel.
        """
        data = request.get_json()
        new_parcel = Parcel(
            user_id=data.get('user_id'),
            origin=data.get('origin'),
            destination=data.get('destination'),
            weight=data.get('weight'),
            status=data.get('status'),
            # Add other fields if necessary
        )
        db.session.add(new_parcel)
        db.session.commit()
        return new_parcel.to_dict(), 201

    def put(self, parcel_id):
        """
        Updates information for a specific parcel identified by parcel_id.
        """
        data = request.get_json()
        parcel = Parcel.query.get(parcel_id)
        if not parcel:
            return {'message': 'Parcel not found'}, 404

        # Update parcel fields based on data provided
        if 'origin' in data:
            parcel.origin = data['origin']
        if 'destination' in data:
            parcel.destination = data['destination']
        if 'weight' in data:
            parcel.weight = data['weight']
        if 'status' in data:
            parcel.status = data['status']

        db.session.commit()
        return parcel.to_dict()

    def delete(self, parcel_id):
        """
        Deletes a specific parcel identified by parcel_id.
        """
        parcel = Parcel.query.get(parcel_id)
        if not parcel:
            return {'message': 'Parcel not found'}, 404

        db.session.delete(parcel)
        db.session.commit()
        return {'message': 'Parcel deleted'}, 204

# Add resource endpoints to API
api.add_resource(ParcelResource, '/parcels', '/parcels/<int:parcel_id>')

# View all parcels:       GET /parcels
# Add new parcel:         POST /parcels
# Change parcel data:     PUT /parcels/<parcel_id>
# Delete parcels:         DELETE /parcels/<parcel_id>
# Search parcel by id:    GET /parcels?parcel_id=<parcel_id>
# Search parcels by user: GET /parcels?user_id=<user_id>

# -------------------------DELIVERY STATUS RESOURCES-------------------------------------------------

class DeliveryStatusResource(Resource):
    def get(self, parcel_id):
        """
        Fetches the delivery status of a specific parcel identified by parcel_id.
        """
        delivery_status = DeliveryStatus.query.filter_by(parcel_id=parcel_id).first()
        if delivery_status:
            return delivery_status.to_dict()
        else:
            return {'message': 'Delivery status not found'}, 404

    def post(self, parcel_id):
        """
        Creates a new delivery status for the parcel identified by parcel_id.
        """
        data = request.get_json()
        new_status = DeliveryStatus(
            parcel_id=parcel_id,
            status=data.get('status'),
            location=data.get('location'),
            timestamp=data.get('timestamp')
        )
        db.session.add(new_status)
        db.session.commit()
        return new_status.to_dict(), 201

    def put(self, parcel_id):
        """
        Updates the delivery status of the parcel identified by parcel_id.
        """
        data = request.get_json()
        delivery_status = DeliveryStatus.query.filter_by(parcel_id=parcel_id).first()
        if not delivery_status:
            return {'message': 'Delivery status not found'}, 404

        # Update status fields based on data provided
        if 'status' in data:
            delivery_status.status = data['status']
        if 'location' in data:
            delivery_status.location = data['location']
        if 'timestamp' in data:
            delivery_status.timestamp = data['timestamp']

        db.session.commit()
        return delivery_status.to_dict()

    def delete(self, parcel_id):
        """
        Deletes the delivery status of the parcel identified by parcel_id.
        """
        delivery_status = DeliveryStatus.query.filter_by(parcel_id=parcel_id).first()
        if not delivery_status:
            return {'message': 'Delivery status not found'}, 404

        db.session.delete(delivery_status)
        db.session.commit()
        return {'message': 'Delivery status deleted'}, 204

# Add resource endpoints to API
api.add_resource(DeliveryStatusResource, '/parcels/<int:parcel_id>/status')

# Fetch delivery status:  GET /parcels/<parcel_id>/status
# Create new status:      POST /parcels/<parcel_id>/status
# Update status:          PUT /parcels/<parcel_id>/status
# Delete status:          DELETE /parcels/<parcel_id>/status

# Main entry point for the application
if __name__ == '__main__':
    app.run(port=os.getenv('FLASK_RUN_PORT', 5555), debug=app.config['DEBUG'])
