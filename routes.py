from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Customer, Invoice

# 🔑 This line defines the Blueprint so @routes.route works
routes = Blueprint("routes", __name__)

# ==========================
# Dashboard
# ==========================
@routes.route("/")
def index():
    customer_count = Customer.query.count()
    invoice_count = Invoice.query.count()
    total_revenue = db.session.query(db.func.sum(Invoice.amount)).scalar() or 0

    # latest 5 invoices
    recent_invoices = Invoice.query.order_by(Invoice.id.desc()).limit(5).all()
    customers = {c.id: c.name for c in Customer.query.all()}

    return render_template(
        "index.html",
        customer_count=customer_count,
        invoice_count=invoice_count,
        total_revenue=total_revenue,
        recent_invoices=recent_invoices,
        customers=customers,
        active_page="dashboard",
    )

# ==========================
# Customers
# ==========================
@routes.route("/customers")
def customers_page():
    customers = Customer.query.all()
    return render_template("customers.html", customers=customers, active_page="customers")


@routes.route("/add_customer", methods=["GET", "POST"])
def add_customer():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        address = request.form.get("address")

        new_customer = Customer(
            name=name,
            email=email,
            phone=phone,
            address=address
        )
        db.session.add(new_customer)
        db.session.commit()

        return redirect(url_for("routes.customers_page"))

    return render_template("add_customer.html", active_page="customers")

# ==========================
# Invoices
# ==========================
@routes.route("/invoices")
def invoices_page():
    invoices = Invoice.query.all()
    customers = {c.id: c.name for c in Customer.query.all()}
    return render_template("invoices.html", invoices=invoices, customers=customers, active_page="invoices")


@routes.route("/add_invoice", methods=["GET", "POST"])
def add_invoice():
    if request.method == "POST":
        customer_id = request.form.get("customer_id")
        description = request.form.get("description")
        amount = request.form.get("amount")
        status = request.form.get("status")

        new_invoice = Invoice(
            customer_id=customer_id,
            description=description,
            amount=float(amount),
            status=status,
        )
        db.session.add(new_invoice)
        db.session.commit()

        return redirect(url_for("routes.invoices_page"))

    customers = Customer.query.all()
    return render_template("add_invoice.html", customers=customers, active_page="invoices")

# ==========================
# Reports
# ==========================
@routes.route("/reports")
def reports_page():
    customer_count = Customer.query.count()
    invoice_count = Invoice.query.count()
    total_revenue = db.session.query(db.func.sum(Invoice.amount)).scalar() or 0
    return render_template(
        "reports.html",
        customer_count=customer_count,
        invoice_count=invoice_count,
        total_revenue=total_revenue,
        active_page="reports",
    )