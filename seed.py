from app import app, db
from models import Customer, Invoice


def seed_data():
    with app.app_context():
        # Reset database (drop + create tables fresh)
        db.drop_all()
        db.create_all()

        # Example Customers
        c1 = Customer(name="Acme Construction", email="info@acme.com", phone="123-456-7890", address="123 Main St")
        c2 = Customer(name="BuildRight Ltd.", email="contact@buildright.com", phone="555-987-6543", address="456 Oak Ave")

        db.session.add_all([c1, c2])
        db.session.commit()

        # Example Invoices
        i1 = Invoice(customer_id=c1.id, description="Concrete Foundation Work", amount=5000.0, status="paid")
        i2 = Invoice(customer_id=c2.id, description="Roof Installation", amount=12000.0, status="unpaid")

        db.session.add_all([i1, i2])
        db.session.commit()

        print("✅ Database seeded with sample customers + invoices!")


if __name__ == "__main__":
    seed_data()