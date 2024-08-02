import os
from dotenv import load_dotenv
from models import db, Admin
from flask import Flask, request, make_response, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_migrate import Migrate  
from werkzeug.exceptions import NotFound 


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

# Set up database URI based on environment (use DB_EXTERNAL_URL by default)
if os.getenv('FLASK_ENV') == 'production':
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_INTERNAL_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_EXTERNAL_URL")

# Set the Flask app secret key from environment variable
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Initialize SQLAlchemy with the Flask app
migrate = Migrate(app, db)
db.init_app(app)

# with app.app_context():
#     # from app.models import *
#     db.create_all()

# Create the app context
# with app.app_context():
#     # Create the database tables if they don't exist
#     db.create_all()

# Set up Flask-Restful API
api = Api(app)

# ---------------------Define resource endpoints---------------------------------------------
# -------------------------USER RESOURCES-------------------------------------------------

#Bianca
# Error handling
@app.errorhandler(NotFound)
def handle_not_found(e):
    response = make_response(
        jsonify({'error':'Not Found','message': 'The requested resource does not exist.'}),
        404
    )
    response.headers['Content-Type'] = 'application/json'
    return response

app.register_error_handler(404, handle_not_found)

# Added routes to admin
class Admins(Resource):
    def get(self):
        admins_dict_list = [admin.to_dict() for admin in Admin.query.all()]
        response = make_response(admins_dict_list,200)
        return response
    
    def post(self):
        new_admin = Admin(
            first_name = request.get_json()["first_name"],
            last_name = request.get_json()["last_name"],
            city = request.get_json()["city"],
            state = request.get_json()["state"],
            branch_code = request.get_json()["branch_code"],
            profile_pic = request.get_json()["profile_pic"],
        )
        db.session.add(new_admin)
        db.session.commit()

        res_dict = new_admin.to_dict()
        response = make_response(res_dict,201)
        return response
    
api.add_resource(Admins, '/admins')

class AdminById(Resource):
    def get(self, id):
        admin = Admin.query.filter_by(admin_id=id).first()
        admin_dict =admin.to_dict()
        return make_response(jsonify(admin_dict), 200)
    
    def patch(self, id):
        admin = Admin.query.filter(Admin.admin_id == id).first()
        json_data = request.get_json()
        for attr ,value in json_data.items():
            setattr(admin,attr,value)
        db.session.add(admin)
        db.session.commit()

        res_dict = admin.to_dict()
        response = make_response(res_dict, 200)
        return response
    
    def delete(self, id):
        admin = Admin.query.filter(Admin.admin_id == id).first()
        db.session.delete(admin)
        db.session.commit()
        res_dict = {"message":"admin deleted successfully"}
        response = make_response(res_dict,200)
        return response
    
api.add_resource(AdminById, '/admins/<int:id>')



# Main entry point for the application
if __name__ == '__main__':
    app.run(port=os.getenv('FLASK_RUN_PORT', 5555), debug=app.config['DEBUG'])
