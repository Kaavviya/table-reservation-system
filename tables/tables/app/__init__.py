from flask import Flask 
app = Flask(__name__)

app.config['SECRET_KEY'] = 'c397abab4de4fc6daece5814b4afd0cf'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

from app import views 