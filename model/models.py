from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    user_role = db.Column(db.String(80), nullable=False)
    password = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    company = db.relationship('Company', backref="user")
    employee = db.relationship('Employee', backref="user")
    super_admin = db.relationship('Super_Admin', backref="user")
    com_user = db.relationship('com_user', backref="user")

    def __repr__(self) -> str:
        return 'User>>> {self.username}'



class Company(db.Model):
    __tablename__ = 'Company'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    company_name = db.Column(db.String(100))
    tax_number = db.Column(db.String(20), unique=True)
    industry = db.Column(db.String(100))
    company_size = db.Column(db.Integer)
    company_tel = db.Column(db.String(100))
    company_email = db.Column(db.String(100))
    company_gps = db.Column(db.String(100))
    company_address = db.Column(db.String(200))
    managed_by  = db.Column(db.String(200))
    manager_role = db.Column(db.String(200))
    manager_tel = db.Column(db.String(200))
    manager_email = db.Column(db.String(200))
    image = db.Column(db.String(255))  # New attribute for user image
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    employee = db.relationship('Employee', backref="company")
    visitor = db.relationship('Visitor', backref="company")
    Vehicle = db.relationship('Vehicle', backref="company")
    com_user = db.relationship('com_user', backref="company")

    def __repr__(self) -> str:
        return 'company>>> {self.tax_number}'


class Employee(db.Model):  # Ensure StaffUser inherits from User
    __tablename__ = 'Employee'  # Specify the table name explicitly

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    com_id = db.Column(db.Integer, db.ForeignKey('Company.id'))
    full_name = db.Column(db.String(200))
    staff_email = db.Column(db.String(200))
    staff_social_link = db.Column(db.String(200))
    staff_role = db.Column(db.String(200))
    staff_home_address = db.Column(db.String(200))
    staff_department = db.Column(db.String(200))
    image = db.Column(db.String(255))  # New attribute for user image
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __repr__(self) -> str:
        return 'Company>>> {self.tax_number}'
    


class Super_Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    full_name = db.Column(db.String(200))
    image = db.Column(db.String(255))  # New attribute for user image
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __repr__(self) -> str:
        return 'Super_Admin>>> {self.email}'

class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    com_id = db.Column(db.Integer, db.ForeignKey('Company.id'))
    full_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    contact_details = db.Column(db.String(50), nullable=False)
    purpose_of_visit = db.Column(db.String(200), nullable=False)
    time_in = db.Column(db.DateTime, nullable=False)
    badge_issued = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())



    def __repr__(self) -> str:
        return 'Visitor>>> {self.id}'


class Visitor_card(Visitor):
    surname = db.Column(db.String(100))
    given_name = db.Column(db.String(100))
    dob = db.Column(db.Date)
    pob = db.Column(db.String(100))
    sex = db.Column(db.String(100))
    proff = db.Column(db.String(100))
    id_card_number = db.Column(db.Integer)
    

    def __repr__(self) -> str:
        return 'Visitor_card>>> {self.id_card_number}'


class com_user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    com_id = db.Column(db.Integer, db.ForeignKey('Company.id'))
    full_name = db.Column(db.String(200))
    work_role = db.Column(db.String(200))
    image = db.Column(db.String(255))  # New attribute for user image
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __repr__(self) -> str:
        return 'Visitor_card>>> {self.email}'


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    com_id = db.Column(db.Integer, db.ForeignKey('Company.id'))
    plate_number = db.Column(db.String(20), nullable=False)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(20), nullable=False)
    owner_details = db.Column(db.String(100), nullable=False)
    entry_time = db.Column(db.DateTime, nullable=False)
    exit_time = db.Column(db.DateTime)
    flagged_as_suspicious = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())


    def __repr__(self) -> str:
        return 'Visitor>>> {self.plate_number}'



def init_db():
    # Create all tables
    db.create_all()
    print("Database tables created successfully.")