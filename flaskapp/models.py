from flaskapp import db,login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	__tablename__ = 'user'
	userid = db.Column(db.Integer,primary_key=True)
	email = db.Column(db.String(100), unique=True,nullable=False)
	password = db.Column(db.String(100),nullable=False)
	img_file = db.Column(db.String(100),nullable=False,default='profile.jpg')
	username = db.Column(db.String(100),unique=True,nullable=False)

	posts = db.relationship('Posts', backref='poster')

	def get_id(self):
		return (self.userid)

class Posts(db.Model):
	__tablename__ = 'posts'
	postid = db.Column(db.Integer,primary_key=True)
	content = db.Column(db.Text,nullable=False)
	media = db.Column(db.Text,unique=True, nullable=False)
	name = db.Column(db.Text, nullable=False)
	img_type = db.Column(db.Text, nullable=False)
	date_posted = db.Column(db.DateTime,nullable=False, default=datetime.utcnow)
	latitude = db.Column(db.Numeric(8,6), nullable = False)
	longitude = db.Column(db.Numeric(9,6), nullable = False)
	poster_id = db.Column(db.Integer,db.ForeignKey('user.userid'), nullable=False)		

