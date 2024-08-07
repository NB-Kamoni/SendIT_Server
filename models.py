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

class Admin(db.Model, SerializerMixin):
    __tablename__ = 'admins'
    admin_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    branch_code = db.Column(db.String(20))
    profile_pic = db.Column(db.String, nullable=True)  

    #Relationships
    delGuys= db.relationship('DeliveryGuy', back_populates="admin", cascade='all, delete-orphan')

    # add serialization rules
    serialize_rules = ('-delGuys.admin',)

    deliveryGuys = association_proxy('delGuys', 'deliveryGuy')


    def __repr__(self):
        return f'<Admin {self.first_name}, city {self.city}>'
    

class DeliveryGuy(db.Model, SerializerMixin):
    __tablename__ = 'delivery_guys'
    delivery_guy_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)  # Updated length
    second_name = db.Column(db.String(50), nullable=False)  # Updated length
    address = db.Column(db.String(255), nullable=False)  # Updated length
    city = db.Column(db.String(50), nullable=False)  # Updated length
    state = db.Column(db.String(50), nullable=False)  # Updated length
    phone_number = db.Column(db.String(20), nullable=False)
    mode = db.Column(db.String(50), nullable=False)  # Updated length
    live_location = db.Column(db.String(255), nullable=True)
    profile_picture = db.Column(db.String, nullable=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.admin_id'))

    #Relationships
    admin = db.relationship('Admin', back_populates="delGuys")

    # add serialization rules
    serialize_rules = ('-admin.deliveryGuy',)
     


    def __repr__(self):
        return f'<DeliveryGuy {self.first_name} {self.second_name}, city {self.city}>'

class Courier(db.Model):
    __tablename__ = 'couriers' 
    courier_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
  

    def to_dict(self):
        return {
            'courier_id': self.courier_id,
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'phone_number': self.phone_number,
            'email': self.email,
        }