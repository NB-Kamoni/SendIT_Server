from datetime import date
from app import app, db
from models import Admin

with app.app_context():
    # Drop all tables and create them again
    db.drop_all()
    db.create_all()

    ad1 = Admin(first_name="John", last_name="Doe", city="Nairobi", state="Kenya", branch_code="57hg", profile_pic="https://media.istockphoto.com/id/1327592506/vector/default-avatar-photo-placeholder-icon-grey-profile-picture-business-man.jpg?s=1024x1024&w=is&k=20&c=er-yFBCv5wYO_curZ-MILgW0ECSjt0DDg5OlwpsAgZM=")
    ad2 = Admin(first_name="Jane", last_name="Doe", city="Nairobi", state="Kenya", branch_code="57hg", profile_pic="https://media.istockphoto.com/id/1327592506/vector/default-avatar-photo-placeholder-icon-grey-profile-picture-business-man.jpg?s=1024x1024&w=is&k=20&c=er-yFBCv5wYO_curZ-MILgW0ECSjt0DDg5OlwpsAgZM=")


    db.session.add_all([ad1,ad2])
    db.session.commit()

    print("Database seeded successfully!")