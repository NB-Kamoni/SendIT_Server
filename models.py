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
    state = db.column(db.String)
    branch_code = db.Column(db.String(100))
    profile_pic = db.Column(db.String, nullable=True)  

    def __repr__(self):
        return f'<Admin {self.first_name}, city  {self.city}>'