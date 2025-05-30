from flask import Flask
from flask_cors import CORS
from models import db
from routes import bp
from config import DATABASE_URL, SECRET_KEY

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Drop and recreate all tables
with app.app_context():
    db.drop_all()  # Be careful with this in production!
    db.create_all()

app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True)