from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask_cors import CORS
from firebase_admin import auth, initialize_app, credentials
import os

# Initialize the Flask application
app = Flask(__name__)
CORS(app)

# Load configuration from environment variables or set defaults
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///sendit.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key')

# Initialize SQLAlchemy, Migrate, and API
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

# Initialize Firebase Admin SDK
cred = credentials.Certificate("firebase-adminsdk.json")
initialize_app(cred)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    firebase_uid = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20))
    address = db.Column(db.Text)
    role = db.Column(db.String(20))
    profile_photo_url = db.Column(db.Text)
    account_balance = db.Column(db.Float, default=0.0, nullable=False)  # New field

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'firebase_uid': self.firebase_uid,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number,
            'address': self.address,
            'role': self.role,
            'profile_photo_url': self.profile_photo_url,
            'account_balance': self.account_balance  # New field
        }

class Parcel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float, nullable=False)
    length = db.Column(db.Float, nullable=False)
    width = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    value = db.Column(db.Float, nullable=False)
    pickup_location = db.Column(db.Text, nullable=False)
    drop_off_location = db.Column(db.Text, nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    courier_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    delivery_status = db.Column(db.String(20), default='pending')
    shipping_cost = db.Column(db.Float, nullable=False)  # New field
    distance = db.Column(db.Float, nullable=False)  # New field

    def to_dict(self):
        return {
            'id': self.id,
            'weight': self.weight,
            'length': self.length,
            'width': self.width,
            'height': self.height,
            'value': self.value,
            'pickup_location': self.pickup_location,
            'drop_off_location': self.drop_off_location,
            'sender_id': self.sender_id,
            'recipient_id': self.recipient_id,
            'courier_id': self.courier_id,
            'delivery_status': self.delivery_status,
            'shipping_cost': self.shipping_cost,  # New field
            'distance': self.distance  # New field
        }

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
            return make_response(jsonify({'message': 'Invalid token', 'error': str(e)}), 401)
        
        return f(*args, **kwargs)
    
    decorator.__name__ = f.__name__
    return decorator

# API Resources
class UserListResource(Resource):
    # @firebase_required
    def get(self):
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])

    @firebase_required
    def post(self):
        data = request.json
        email = request.user.get('email')
        firebase_uid = request.user.get('uid')

        user = User(
            email=email,
            firebase_uid=firebase_uid,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            phone_number=data.get('phone_number'),
            address=data.get('address'),
            role=data['role'],
            profile_photo_url=data.get('profile_photo_url'),
            account_balance=data.get('account_balance', 0.0)  # New field
        )
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict()), 201

class UserResource(Resource):
    # @firebase_required
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return jsonify(user.to_dict())

    # @firebase_required
    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        data = request.json
        user.email = data.get('email', user.email)
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.phone_number = data.get('phone_number', user.phone_number)
        user.address = data.get('address', user.address)
        user.role = data.get('role', user.role)
        user.profile_photo_url = data.get('profile_photo_url', user.profile_photo_url)
        user.account_balance = data.get('account_balance', user.account_balance)  # New field
        db.session.commit()
        return jsonify(user.to_dict())

    # @firebase_required
    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

class ParcelListResource(Resource):
    # @firebase_required
    def get(self):
        parcels = Parcel.query.all()
        return jsonify([parcel.to_dict() for parcel in parcels])

    # @firebase_required
    def post(self):
        data = request.json

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
            courier_id=data.get('courier_id'),
            delivery_status=data.get('delivery_status', 'pending'),
            shipping_cost=data['shipping_cost'],  # New field
            distance=data['distance']  # New field
        )
        db.session.add(parcel)
        db.session.commit()
        return jsonify(parcel.to_dict()), 201

class ParcelResource(Resource):
    # @firebase_required
    def get(self, parcel_id):
        parcel = Parcel.query.get_or_404(parcel_id)
        return jsonify(parcel.to_dict())

    # @firebase_required
    def put(self, parcel_id):
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
        parcel.shipping_cost = data.get('shipping_cost', parcel.shipping_cost)  # New field
        parcel.distance = data.get('distance', parcel.distance)  # New field
        db.session.commit()
        return jsonify(parcel.to_dict())

    # @firebase_required
    def delete(self, parcel_id):
        parcel = Parcel.query.get_or_404(parcel_id)
        db.session.delete(parcel)
        db.session.commit()
        return '', 204

# Register API resources
api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(ParcelListResource, '/parcels')
api.add_resource(ParcelResource, '/parcels/<int:parcel_id>')

if __name__ == '__main__':
    app.run(debug=True)
