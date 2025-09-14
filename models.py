from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# -------------------------
# Customer Model
# -------------------------
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(200), nullable=True)

    invoices = db.relationship("Invoice", backref="customer", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
        }


# -------------------------
# Invoice Model
# -------------------------
class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    description = db.Column(db.String(200))
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="unpaid")  # unpaid / paid

    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "description": self.description,
            "amount": self.amount,
            "status": self.status,
        }
        from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)