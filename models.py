from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)

class Client(db.Model, SerializerMixin):
    __tablename__ = 'client'
    
    ClientID = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String, index=True, unique=True)
    State = db.Column(db.String)
    City = db.Column(db.String)
    Address = db.Column(db.String)
    PhoneNumber = db.Column(db.String)
    FirstName = db.Column(db.String)
    LastName = db.Column(db.String)
    ProfilePicture = db.Column(db.String)

    # Relationships
    sent_parcels = db.relationship('Parcel', foreign_keys='Parcel.SenderID', backref='sender', lazy=True)
    received_parcels = db.relationship('Parcel', foreign_keys='Parcel.RecipientID', backref='recipient', lazy=True)

    serialize_rules = ('-sent_parcels', '-received_parcels')  # Exclude parcels relationships during serialization

    def __repr__(self):
        return (f'<Client(ClientID={self.ClientID}, Email={self.Email}, '
                f'FirstName={self.FirstName}, LastName={self.LastName})>')

class Admin(db.Model, SerializerMixin):
    __tablename__ = 'admin'
    
    AdminID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String)
    SecondName = db.Column(db.String)
    City = db.Column(db.String)
    State = db.Column(db.String)
    BranchCode = db.Column(db.String)
    ProfilePicture = db.Column(db.String)

    # Relationships
    allocations = db.relationship('AdminDeliveryGuyAllocation', backref='admin', lazy=True)

    serialize_rules = ('-allocations',)  # Exclude allocations relationship during serialization

    def __repr__(self):
        return (f'<Admin(AdminID={self.AdminID}, FirstName={self.FirstName}, '
                f'SecondName={self.SecondName}, BranchCode={self.BranchCode})>')

class ParcelStatus(db.Model, SerializerMixin):
    __tablename__ = 'parcel_status'
    
    StatusID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String, unique=True)
    cancelled = db.Column(db.Boolean, default=False)
    delivered = db.Column(db.Boolean, default=False)
    posted = db.Column(db.Boolean, default=False)
    en_route = db.Column(db.Boolean, default=False)

    # Relationships
    parcels = db.relationship('Parcel', backref='status', lazy=True)

    serialize_rules = ('-parcels',)  # Exclude parcels relationship during serialization

    def __repr__(self):
        return f'<ParcelStatus(Name={self.Name})>'

class DeliveryGuy(db.Model, SerializerMixin):
    __tablename__ = 'delivery_guy'
    
    DeliveryGuyID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String)
    SecondName = db.Column(db.String)
    Address = db.Column(db.String)
    City = db.Column(db.String)
    State = db.Column(db.String)
    PhoneNumber = db.Column(db.String)
    Mode = db.Column(db.String)
    LiveLocation = db.Column(db.String)
    ProfilePictureURL = db.Column(db.String)

    # Relationships
    parcels = db.relationship('Parcel', backref='delivery_guy', lazy=True)
    allocations = db.relationship('AdminDeliveryGuyAllocation', backref='delivery_guy', lazy=True)

    serialize_rules = ('-parcels', '-allocations') 

    def __repr__(self):
        return (f'<DeliveryGuy(DeliveryGuyID={self.DeliveryGuyID}, '
                f'FirstName={self.FirstName}, LastName={self.SecondName})>')

class Parcel(db.Model, SerializerMixin):
    __tablename__ = 'parcel'
    
    ParcelID = db.Column(db.Integer, primary_key=True)
    Weight = db.Column(db.Float)
    Origin = db.Column(db.String)
    Destination = db.Column(db.String)
    SenderID = db.Column(db.Integer, db.ForeignKey('client.ClientID'))
    RecipientID = db.Column(db.Integer, db.ForeignKey('client.ClientID'))
    StatusID = db.Column(db.Integer, db.ForeignKey('parcel_status.StatusID'))
    DeliveryGuyID = db.Column(db.Integer, db.ForeignKey('delivery_guy.DeliveryGuyID'))

    serialize_rules = ('-sender', '-recipient', '-status', '-delivery_guy')  

    def __repr__(self):
        return (f'<Parcel(ParcelID={self.ParcelID}, Weight={self.Weight}, '
                f'Origin={self.Origin}, Destination={self.Destination})>')

class AdminDeliveryGuyAllocation(db.Model, SerializerMixin):
    __tablename__ = 'admin_delivery_guy_allocation'
    
    AllocationID = db.Column(db.Integer, primary_key=True)
    AdminID = db.Column(db.Integer, db.ForeignKey('admin.AdminID'))
    DeliveryGuyID = db.Column(db.Integer, db.ForeignKey('delivery_guy.DeliveryGuyID'))
    ParcelID = db.Column(db.Integer, db.ForeignKey('parcel.ParcelID'))
    AllocatedAt = db.Column(db.DateTime, default=datetime.utcnow)
    PickUpLocation = db.Column(db.String)
    DropOffLocation = db.Column(db.String)

    serialize_rules = ('-admin', '-delivery_guy', '-parcel') 
    def __repr__(self):
        return (f'<AdminDeliveryGuyAllocation(AllocationID={self.AllocationID}, '
                f'AdminID={self.AdminID}, DeliveryGuyID={self.DeliveryGuyID})>')
