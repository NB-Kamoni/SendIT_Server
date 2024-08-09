from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Enum, ForeignKey, Integer, String, Text, Float, DateTime, Column
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

# Define metadata with naming convention
metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

# Initialize the SQLAlchemy object with custom metadata
db = SQLAlchemy(metadata=metadata)

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    # Serialization rules to exclude certain fields
    serialize_rules = ('-sent_parcels', '-received_parcels', '-courier_parcels')

    # Define columns
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    firebase_uid = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(255))
    last_name = Column(String(255))
    phone_number = Column(String(20))
    address = Column(Text)
    role = Column(Enum('admin', 'client', 'individual_courier', 'corporate_courier', name='user_roles'), nullable=False)
    profile_photo_url = Column(Text)
    account_balance = Column(Float, default=0.0, nullable=False)  # New field

    # Define relationships
    sent_parcels = relationship('Parcel', backref='sender', foreign_keys='Parcel.sender_id', lazy=True)
    received_parcels = relationship('Parcel', backref='recipient', foreign_keys='Parcel.recipient_id', lazy=True)
    courier_parcels = relationship('Parcel', backref='courier', foreign_keys='Parcel.courier_id', lazy=True)

    def __repr__(self):
        return f'<User(id={self.id}, email={self.email}, role={self.role})>'

class Parcel(db.Model, SerializerMixin):
    __tablename__ = 'parcels'
    
    # Serialization rules to exclude certain fields
    serialize_rules = ('-sender', '-recipient', '-courier')

    # Define columns
    id = Column(Integer, primary_key=True)
    weight = Column(Float, nullable=False)
    length = Column(Float, nullable=False)
    width = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    value = Column(Float, nullable=False)
    pickup_location = Column(Text, nullable=False)
    drop_off_location = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    delivery_status = Column(Enum('pending', 'in_transit', 'delivered', 'cancelled', name='delivery_statuses'), default='pending', nullable=False)
    shipping_cost = Column(Float, nullable=False)  # New field
    distance = Column(Float, nullable=False)  # New field

    # Define foreign keys
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    recipient_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    courier_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    def __repr__(self):
        return f'<Parcel(id={self.id}, status={self.delivery_status}, sender={self.sender_id}, recipient={self.recipient_id})>'
