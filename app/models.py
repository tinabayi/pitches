from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
    @property
    def password(self):
            raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
            self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
            return check_password_hash(self.pass_secure,password)
   
    def __repr__(self):
        return f'User {self.username}'

    @login_manager.user_loader
    def load_user(user_id):
            return User.query.get(int(user_id))
   

class Pitch(db.Model):
    __tablename__ = 'pitches'

    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    description = db.Column(db.String(255))
   

    
    def save_pitches(self):
        db.session.add(self)
        db.session.commit()


    @classmethod
    def clear_pitches(cls):
        Pitch.all_pitches.clear()

    @classmethod
    def get_pitches(id):
        pitches=Pitch.query.all()

        return pitches

   

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
    description = db.Column(db.String(255))
    

    @classmethod
    def get_comments(id):
        comments=Comment.query.all()

        return comments

   

