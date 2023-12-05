from setup import db, ma
from datetime import datetime

class Educator(db.Model):
    __tablename__ = "educators"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    name = db.Column(db.String, nullable=False)
    d_o_b = db.Column(db.Date, default="")
    phone_number = db.Column(db.String(), nullable=False, unique=True)
    is_admin = db.Column(db.Boolean(), default=False)

class EducatorSchema(ma.Schema):
    class Meta:
        fields = ("id", "email", "password", "name", "d_o_b", "phone_number", "is_admin" )
