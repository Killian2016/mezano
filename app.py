from flask import Flask
from routes import routes
from models import db

app = Flask(__name__, template_folder="templates")

# Database config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mezano.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize db WITH this app
db.init_app(app)

# Register routes
app.register_blueprint(routes)

@app.route("/")
def home():
    return "👷 Welcome to Mezano Construction Accounting App"

@app.route("/hello")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()   # create tables
    app.run(debug=True)
    import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database connection from environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Example Model (add your real models here)
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

# Create tables when the server starts
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return "Mezano is connected to Postgres!"