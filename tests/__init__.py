import pytest
from flask_sqlalchemy import SQLAlchemy
from app import app

DB_CONN = 'sqlite://'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONN
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model): # pylint: disable=too-few-public-methods
    """todo class representing task list item"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
