import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

app = Flask(__name__)

# -----------------------------
# Database Setup
# -----------------------------
# Render gives DATABASE_URL in environment variables
database_url = os.environ.get("DATABASE_URL")

if not database_url:
    raise RuntimeError("DATABASE_URL not set. Did you add it in Render?")

# Fix postgres:// -> postgresql:// for SQLAlchemy
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# -----------------------------
# Models
# -----------------------------
class Customer(db.Model):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# -----------------------------
# Routes
# -----------------------------

@app.route("/")
def home():
    return "Mezano is running with Postgres ✅"

@app.route("/check_db")
def check_db():
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    return jsonify(tables)

@app.route("/init_db")
def init_db():
    # Create tables if they don’t exist
    db.create_all()
    return "Database tables created ✅"

@app.route("/add_test_customer")
def add_customer():
    new_customer = Customer(name="Test User")
    db.session.add(new_customer)
    db.session.commit()
    return f"Added customer with id {new_customer.id}"

@app.route("/list_customers")
def list_customers():
    customers = Customer.query.all()
    return jsonify([{"id": c.id, "name": c.name} for c in customers])

# -----------------------------
# Run locally
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)