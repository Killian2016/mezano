from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from models import User, Company

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
        db.session.flush()

        # Create user linked to company
        user = User(email=email, company_id=company.id)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
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