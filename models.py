from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, func
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
import uuid
from sqlalchemy.orm import aliased

# Define a naming convention for the metadata
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)

#--------------------------------------------
# Define the User model
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-password', '-sent_parcels_list.sender', '-received_parcels_list.recipient', '-assigned_parcels_list.courier')

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    firebase_uid = db.Column(db.String(120), unique=True, nullable=True)
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

    # Relationships with explicit back_populates
    sent_parcels_list = db.relationship('Parcel', foreign_keys='Parcel.sender_id', back_populates='sender_user', lazy='dynamic')
    received_parcels_list = db.relationship('Parcel', foreign_keys='Parcel.recipient_id', back_populates='recipient_user', lazy='dynamic')
    assigned_parcels_list = db.relationship('Parcel', foreign_keys='Parcel.courier_id', back_populates='courier_user', lazy='dynamic')

    # Association proxy for easy access to all parcels related to the user
    parcels = association_proxy('sent_parcels_list', 'id')

    def __repr__(self):
        return f'<User id={self.id} email={self.email} role={self.role}>'
    
    @staticmethod
    def create_user(firebase_uid, email, role='client', status='active'):
        """Create a new user with the provided Firebase UID, email, role, and status."""
        new_user = User(
            firebase_uid=firebase_uid,
            email=email,
            role=role,
            user_status=status
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user 
    
    @staticmethod
    def update_profile(user_id, data):
        """
        Update the user's profile with the provided data.
        Only updates fields that are present in the data.
        """
        user = User.query.get(user_id)
        if not user:
            return False, "User not found."

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

        # Commit the changes to the database
        try:
            db.session.commit()
            return True, "User profile updated successfully."
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def get_couriers_by_status(status):
        """Return a list of couriers based on their user_status"""
        return User.query.filter(User.role.in_(['individual_courier', 'corporate_courier']), User.user_status == status).all()

    @staticmethod
    def get_all_parcels():
        """Return a list of all parcels along with their associated sender, recipient, and courier"""
        return Parcel.query.all()

    @staticmethod
    def get_users_by_role(role):
        """Return a list of users based on their role"""
        return User.query.filter_by(role=role).all()
   

    @staticmethod
    def get_all_users():
        """Return a list of all users"""
        return User.query.all()

    @staticmethod
    def get_users_by_status(status):
        """Return a list of users based on their status"""
        return User.query.filter_by(user_status=status).all()

#--------------------------------------------
# Define the Parcel model
class Parcel(db.Model, SerializerMixin):
    __tablename__ = 'parcels'

    serialize_rules = ('-sender_user', '-recipient_user', '-courier_user')

    id = db.Column(db.Integer, primary_key=True)
    tracking_number = db.Column(db.String(50), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    weight = db.Column(db.Float, nullable=False)
    length = db.Column(db.Float, nullable=False)
    width = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    value = db.Column(db.Float, nullable=False)
    pickup_location = db.Column(db.String(255), nullable=False)
    drop_off_location = db.Column(db.String(255), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    courier_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    delivery_status = db.Column(db.String(50), default='pending')
    shipping_cost = db.Column(db.Float, nullable=False)
    distance = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, onupdate=func.now())

    # Define relationships with back_populates
    sender_user = db.relationship('User', foreign_keys=[sender_id], back_populates='sent_parcels_list')
    recipient_user = db.relationship('User', foreign_keys=[recipient_id], back_populates='received_parcels_list')
    courier_user = db.relationship('User', foreign_keys=[courier_id], back_populates='assigned_parcels_list')

    def __repr__(self):
        return f'<Parcel id={self.id} tracking_number={self.tracking_number} status={self.delivery_status}>'

    @staticmethod
    def get_parcels_by_client(client_id):
        """Return all parcels where the client is either the sender or the recipient"""
        return Parcel.query.filter((Parcel.sender_id == client_id) | (Parcel.recipient_id == client_id)).all()

    @staticmethod
    def get_parcel_by_tracking_number(tracking_number):
        """Return the parcel details by tracking number"""
        return Parcel.query.filter_by(tracking_number=tracking_number).first()

    @staticmethod
    def get_parcels_by_status(status):
        """Return all parcels by delivery status"""
        return Parcel.query.filter_by(delivery_status=status).all()

    @staticmethod
    def get_parcels_with_details():
        """Return all parcels along with their sender, recipient, and courier details."""
        # Aliases for the User table
        sender_alias = aliased(User, name='sender')
        recipient_alias = aliased(User, name='recipient')
        courier_alias = aliased(User, name='courier')
        
        query = db.session.query(
            Parcel,
            sender_alias,
            recipient_alias,
            courier_alias
        ).join(sender_alias, Parcel.sender_id == sender_alias.id) \
         .join(recipient_alias, Parcel.recipient_id == recipient_alias.id) \
         .join(courier_alias, Parcel.courier_id == courier_alias.id)
         
        return query.all()

