import os
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, login_user, logout_user,
    login_required, current_user, UserMixin
)
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import inspect

# -----------------------------
# App setup
# -----------------------------
app = Flask(__name__)
app.secret_key = "supersecret"   # change this in production

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
# Models
# -----------------------------
class Company(db.Model):
    __tablename__ = "company"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    users = db.relationship("User", backref="company", lazy=True)

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

# -----------------------------
# Flask-Login setup
# -----------------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# -----------------------------
# Routes
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

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        company_name = request.form["company_name"]

        if User.query.filter_by(email=email).first():
            return "Email already exists ❌"

        # Create company
        company = Company(name=company_name)
        db.session.add(company)
        db.session.flush()  # get company.id

        # Create user linked to company
        user = User(email=email, company_id=company.id)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        login_user(user)  # log in right after signup
        return redirect(url_for("dashboard"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("dashboard"))
        return "Invalid credentials ❌"

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    return f"Welcome {current_user.email} 🎉 — Company: {current_user.company.name}"
    
# -----------------------------
# Run locally
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)