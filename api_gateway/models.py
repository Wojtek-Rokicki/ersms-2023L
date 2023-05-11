from api_gateway import db, login
from flask_login import UserMixin # includes generic implementations for flask_login compatible model

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(64), nullable=False)
    surname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True, index=True)
    profile_pic = db.Column(db.String(128), nullable=False)
    
    def __repr__(self):
            return '<User {}>'.format(self.email)
    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))