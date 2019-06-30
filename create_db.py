# create db py file

from app import db
from models import Flaskr

db.create_all()

db.session.commit()
# create and commit all changes
