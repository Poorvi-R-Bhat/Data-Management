from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = '8f56c23ff56a4afd586221a436f715b6acf76f2b9376e82191f1ba656405825a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/site.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes
