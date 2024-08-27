from app import db
from datetime import datetime

class Upload(db.Model): #defining Upload table
    id = db.Column(db.Integer, primary_key=True)
    upload_id = db.Column(db.String(50), unique=True, nullable=False)
    upload_timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_data = db.relationship('UserData', backref='upload', lazy=True)  #one to many relationship

class UserData(db.Model): #defining UserData table
    id = db.Column(db.Integer, primary_key=True)
    sno = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    upload_id = db.Column(db.Integer, db.ForeignKey('upload.id'), nullable=False)
