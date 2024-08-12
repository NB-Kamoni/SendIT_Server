from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    firebase_uid = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    company_name = db.Column(db.String(120))
    phone_number = db.Column(db.String(20))
    address = db.Column(db.String(200))
    role = db.Column(db.String(50), default='client')
    profile_photo_url = db.Column(db.String(255))
    account_balance = db.Column(db.Float, default=0.0)
    gps_location = db.Column(db.String(255))
    country = db.Column(db.String(100))
    user_status = db.Column(db.String(50), default='active')
    mode_of_transport = db.Column(db.String(250))

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'firebase_uid': self.firebase_uid,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'company_name': self.company_name,
            'phone_number': self.phone_number,
            'address': self.address,
            'role': self.role,
            'profile_photo_url': self.profile_photo_url,
            'account_balance': self.account_balance,
            'gps_location': self.gps_location,
            'country': self.country,
            'user_status': self.user_status,
            'mode_of_transport': self.mode_of_transport,
        }

class Parcel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float, nullable=False)
    length = db.Column(db.Float, nullable=False)
    width = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    value = db.Column(db.Float, nullable=False)
    pickup_location = db.Column(db.String(255), nullable=False)
    drop_off_location = db.Column(db.String(255), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    courier_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    delivery_status = db.Column(db.String(50), default='pending')
    shipping_cost = db.Column(db.Float, nullable=False)
    distance = db.Column(db.Float, nullable=False)

    sender = db.relationship('User', foreign_keys=[sender_id])
    recipient = db.relationship('User', foreign_keys=[recipient_id])
    courier = db.relationship('User', foreign_keys=[courier_id])

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
            'shipping_cost': self.shipping_cost,
            'distance': self.distance,
        }
