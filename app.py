import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy import inspect

# -----------------------------
# App setup
# -----------------------------
app = Flask(__name__)
app.secret_key = "supersecret"   # change in production

# Database
database_url = os.environ.get("DATABASE_URL")
if not database_url:
    raise RuntimeError("DATABASE_URL not set")

if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# -----------------------------
# Flask-Login setup
# -----------------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# -----------------------------
# Import models + routes
# -----------------------------
from models import User, Company
from routes import *   # 👈 this loads all the route functions

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# -----------------------------
# Utility routes
# -----------------------------
@app.route("/")
def home():
    return "Mezano App ✅ — Go to /signup or /login"

@app.route("/check_db")
def check_db():
    inspector = inspect(db.engine)
    return {"tables": inspector.get_table_names()}

@app.route("/init_db")
def init_db():
    with app.app_context():
        db.create_all()
    return "Database tables created ✅"

# -----------------------------
# Run locally
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)