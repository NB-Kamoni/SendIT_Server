import os
from dotenv import load_dotenv
from models import db, Admin, DeliveryGuy, Courier, Client
from flask import Flask, request, make_response, jsonify
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_migrate import Migrate
from werkzeug.exceptions import NotFound
from flask_cors import CORS



# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)


# Load configuration
if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object('config.ProductionConfig')
elif os.getenv('FLASK_ENV') == 'testing':
    app.config.from_object('config.TestingConfig')
else:
    app.config.from_object('config.DevelopmentConfig')

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_EXTERNAL_URL")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config['DEBUG'] = os.getenv('DEBUG', 'False') == 'True'

# Initialize SQLAlchemy and Migrate

migrate = Migrate(app, db)
db.init_app(app)

# Initialize Flask-CORS
CORS(app)

# Set up Flask-Restful API
api = Api(app)

# Models
# class Admin(db.Model):
#     __tablename__ = 'admins'
#     admin_id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String)
#     last_name = db.Column(db.String)
#     city = db.Column(db.String)
#     state = db.Column(db.String)
#     branch_code = db.Column(db.String(100))
#     profile_pic = db.Column(db.String, nullable=True)

#     def to_dict(self):
#         return {
#             'admin_id': self.admin_id,
#             'first_name': self.first_name,
#             'last_name': self.last_name,
#             'city': self.city,
#             'state': self.state,
#             'branch_code': self.branch_code,
#             'profile_pic': self.profile_pic
#         }

# class DeliveryGuy(db.Model):
#     __tablename__ = 'delivery_guys'
#     delivery_guy_id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String, nullable=False)
#     second_name = db.Column(db.String, nullable=False)
#     address = db.Column(db.String, nullable=False)
#     city = db.Column(db.String, nullable=False)
#     state = db.Column(db.String, nullable=False)
#     phone_number = db.Column(db.String(15), nullable=False)
#     mode = db.Column(db.String, nullable=False)
#     live_location = db.Column(db.String, nullable=True)
#     profile_picture = db.Column(db.String, nullable=True)

#     def to_dict(self):
#         return {
#             'delivery_guy_id': self.delivery_guy_id,
#             'first_name': self.first_name,
#             'second_name': self.second_name,
#             'address': self.address,
#             'city': self.city,
#             'state': self.state,
#             'phone_number': self.phone_number,
#             'mode': self.mode,
#             'live_location': self.live_location,
#             'profile_picture': self.profile_picture
#         }

# class Courier(db.Model):
#     __tablename__ = 'couriers'
#     courier_id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False)
#     address = db.Column(db.String(120), nullable=False)
#     city = db.Column(db.String(50), nullable=False)
#     state = db.Column(db.String(50), nullable=False)
#     phone_number = db.Column(db.String(20), nullable=False)
#     email = db.Column(db.String(120), nullable=False)

#     def to_dict(self):
#         return {
#             'courier_id': self.courier_id,
#             'name': self.name,
#             'address': self.address,
#             'city': self.city,
#             'state': self.state,
#             'phone_number': self.phone_number,
#             'email': self.email,
#         }

# Resources
class Admins(Resource):
    def get(self):
        admins_dict_list = [admin.to_dict() for admin in Admin.query.all()]
        return make_response(admins_dict_list, 200)
    
    def post(self):
        data = request.get_json()
        new_admin = Admin(
            first_name=data["first_name"],
            last_name=data["last_name"],
            city=data["city"],
            state=data["state"],
            branch_code=data["branch_code"],
            profile_pic=data.get("profile_pic")
        )
        db.session.add(new_admin)
        db.session.commit()
        return make_response(new_admin.to_dict(), 201)

class AdminById(Resource):
    def get(self, id):
        admin = Admin.query.get_or_404(id)
        return make_response(admin.to_dict(), 200)
    
    def patch(self, id):
        admin = Admin.query.get_or_404(id)
        data = request.get_json()
        for attr, value in data.items():
            setattr(admin, attr, value)
        db.session.commit()
        return make_response(admin.to_dict(), 200)
    
    def delete(self, id):
        admin = Admin.query.get_or_404(id)
        db.session.delete(admin)
        db.session.commit()
        return make_response({"message": "Admin deleted successfully"}, 200)

class DeliveryGuys(Resource):
    def get(self):
        delivery_guys_dict_list = [dg.to_dict() for dg in DeliveryGuy.query.all()]
        return make_response(delivery_guys_dict_list, 200)

    def post(self):
        data = request.get_json()
        new_delivery_guy = DeliveryGuy(
            first_name=data["first_name"],
            second_name=data["second_name"],
            address=data["address"],
            city=data["city"],
            state=data["state"],
            phone_number=data["phone_number"],
            mode=data["mode"],
            live_location=data.get("live_location"),
            profile_picture=data.get("profile_picture")
        )
        db.session.add(new_delivery_guy)
        db.session.commit()
        return make_response(new_delivery_guy.to_dict(), 201)

class DeliveryGuyById(Resource):
    def get(self, id):
        delivery_guy = DeliveryGuy.query.get_or_404(id)
        return make_response(delivery_guy.to_dict(), 200)
    
    def put(self, id):
        delivery_guy = DeliveryGuy.query.get_or_404(id)
        data = request.get_json()
        for attr, value in data.items():
            setattr(delivery_guy, attr, value)
        db.session.commit()
        return make_response(delivery_guy.to_dict(), 200)
    
    def delete(self, id):
        delivery_guy = DeliveryGuy.query.get_or_404(id)
        db.session.delete(delivery_guy)
        db.session.commit()
        return make_response({"message": "Delivery guy deleted successfully"}, 200)

class Couriers(Resource):
    def get(self):
        couriers_dict_list = [courier.to_dict() for courier in Courier.query.all()]
        return make_response(couriers_dict_list, 200)

    def post(self):
        data = request.get_json()
        new_courier = Courier(
            name=data["name"],
            address=data["address"],
            city=data["city"],
            state=data["state"],
            phone_number=data["phone_number"],
            email=data["email"]
            
        )
        db.session.add(new_courier)
        db.session.commit()
        return make_response(new_courier.to_dict(), 201)

class CourierById(Resource):
    def get(self, id):
        courier = Courier.query.get_or_404(id)
        return make_response(courier.to_dict(), 200)
    
    def put(self, id):
        courier = Courier.query.get_or_404(id)
        data = request.get_json()
        for attr, value in data.items():
            setattr(courier, attr, value)
        db.session.commit()
        return make_response(courier.to_dict(), 200)
    
    def delete(self, id):
        courier = Courier.query.get_or_404(id)
        db.session.delete(courier)
        db.session.commit()
        return make_response({"message": "Courier deleted successfully"}, 200)
    

class Clients(Resource):
    def get(self):
        clients_dict_list = [client.to_dict() for client in Client.query.all()]
        return make_response(clients_dict_list, 200)
    
    def post(self):
        data = request.get_json()
        new_client = Client(
            first_name=data["first_name"],
            last_name=data["last_name"],
            city=data["city"],
            state=data["state"],
            address=data["address"],
            email=data["email"],
            phone_no=data["phone_no"],
            profile_pic=data.get("profile_pic")
        )
        db.session.add(new_client)
        db.session.commit()
        return make_response(new_client.to_dict(), 201)


class ClientById(Resource):
    def get(self, id):
        client = Client.query.get_or_404(id)
        return make_response(client.to_dict(), 200)
    
    def patch(self, id):
        client = Client.query.get_or_404(id)
        data = request.get_json()
        for attr, value in data.items():
            setattr(client, attr, value)
        db.session.commit()
        return make_response(client.to_dict(), 200)
    
    def delete(self, id):
        client = Client.query.get_or_404(id)
        db.session.delete(client)
        db.session.commit()
        return make_response({"message": "Client deleted successfully"}, 200)



# Register resources
api.add_resource(Admins, '/admins')
api.add_resource(AdminById, '/admins/<int:id>')
api.add_resource(DeliveryGuys, '/delivery_guys')
api.add_resource(DeliveryGuyById, '/delivery_guys/<int:id>')
api.add_resource(Couriers, '/couriers')
api.add_resource(CourierById, '/couriers/<int:id>')
api.add_resource(Clients, '/clients')
api.add_resource(ClientById, '/clients/<int:id>')


if __name__ == '__main__':
    app.run(port=os.getenv('FLASK_RUN_PORT', 5555), debug=app.config['DEBUG'])
