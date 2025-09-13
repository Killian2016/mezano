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