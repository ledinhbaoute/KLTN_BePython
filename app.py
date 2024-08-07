from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, resources={r"/*": {"origins": "https://kltn-comic-fe.vercel.app"}})

db = SQLAlchemy(app)

from routes import *

if __name__ == "__main__":
    app.run(debug=True)
