import sys,os
import hashlib
from flaskapp import app,db,bcrypt
from flask import Flask, render_template,request,url_for,redirect,session,flash,jsonify,request,Response
from flask_login import login_user,login_required, logout_user, current_user
from flaskapp.models import *
from werkzeug.utils import secure_filename
import random
import math
from sqlalchemy.orm import load_only
import json

def encrypt_string(hash_string):
	sha_signature = \
		hashlib.sha256(hash_string.encode()).hexdigest()
	return sha_signature.upper()


@app.route("/", methods=['GET'])
def index():
	# creating a map in the view
	#Pass users lat,long to center the map for them
	return render_template('map.html')


@app.route("/login" , methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		email = request.form.get('email')
		password = request.form.get('password')
		user = User.query.filter_by(email=email).first()
		print(user,file=sys.stderr)
		if not user or not user.password == encrypt_string(password):
			print(user.password,encrypt_string(password),file=sys.stderr)
			flash("Invalid username/password","error")
			return redirect(url_for('login'))
		login_user(user)
		print(current_user.is_authenticated,file=sys.stderr)
		return render_template('map.html')
	
	return render_template('login.html')

@app.route("/signup" , methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		username = request.form.get('username')
		email = request.form.get('email')
		password = request.form.get('password')
		usernameExists = User.query.filter_by(username=username).first()
		userExists = User.query.filter_by(email=email).first()

		print(username,file=sys.stderr)

		if userExists:
			flash("Email already registered, Please Login Instead", "warning")
			return redirect(url_for('signup'))
		if usernameExists:
			flash("Username already taken!","warning")
			return redirect(url_for('signup'))	

		new_user = User(username=username,email=email,password=encrypt_string(password))
		db.session.add(new_user)
		db.session.commit()	
		flash("Registered successfully! Please Login now.","info")
		return render_template('login.html')
		
	return render_template('signup.html')		

@app.route("/home")
@login_required
def home():
	return render_template('article.html')

@app.route("/logout")
@login_required
def logout():
	logout_user()
	return render_template('map.html')

@app.route("/mapmarkers")
@login_required
def mapmarkers():
	# data = {'latitude':50,'longitude':50}

	fields = ['latitude','longitude']
	posts = db.session.query(Posts).options(load_only(*fields)).all()
	# print(posts,file=sys.stderr)

	locations = []
	for post in posts:
		latitude = post.latitude
		longitude = post.longitude
		latlongDict = {
		"lat":float(latitude),
		"lng":float(longitude)
		}
		locations.append(latlongDict)

	print(locations, file=sys.stderr)

	return render_template('mapwithmarkers.html', data = locations)

# @app.route('/postmethod', methods = ['POST'])
# def get_post_javascript_data():
#     jsdata = request.form['javascript_data']
#     print("106" + str(jsdata), file=sys.stderr)
#     return json.loads(jsdata)[0]

@app.route("/path", methods=['GET', 'POST'])
def path():
	data = request.data

	ab = str(data)

	latitude = float(ab.split('&')[0].split("=")[1].rstrip("\'"))
	longitude = float(ab.split('&')[1].split("=")[1].rstrip("\'"))

	print("latitude:" + str(latitude),file=sys.stderr)
	print("longitude:" + str(longitude),file=sys.stderr)

	post = Posts.query.filter_by(latitude = latitude, longitude = longitude).first()

	filename = post.name

	path = url_for('static',filename='upload/' + filename)
	print(path,file=sys.stderr)

	return jsonify(dict(redirect=path))
	# return Response(post.media,mimetype=post.img_type)
	# return render_template("result.html",image_path=image_path)

# @app.route("/showimage", methods=['GET', 'POST'])
# @login_required
# def showimage(filename):
# 	print(filename,file=sys.stderr)
# 	return render_template("result.html",image_path=filename)

@app.route("/showimage", methods=['GET', 'POST'])
@login_required
def showimage():
	img = Posts.query.filter_by(postid = '110').first() # Just to test
	print(img,file=sys.stderr)
	return Response(img.media,mimetype=img.img_type)


@app.route("/result", methods=['GET', 'POST'])
def result():
	return render_template('result.html')

@app.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
	if request.method == 'POST':
		pic = request.files['input-file']
		filename = pic.filename
		filename = secure_filename(pic.filename)
		mimetype = pic.mimetype
	
		content = request.form.get('caption')

		if not pic:
			return 'No picture uploaded', 400

		# filename = secure_filename(pic.filename)
		# mimetype = pic.mimetype

		# media = pic.read()

		# import exifread
		# from PIL import Image

		pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

		# tags = {}

		# with open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as f: 
		# 	tags = exifread.process_file(f, details=False)
		# 	print(tags,file=sys.stderr)
		# if "Image Orientation" in tags.keys():
		# 	orientation = tags["Image Orientation"]
		# 	print(orientation,file=sys.stderr)

		latitude = 52.6344285817945
		longitude = -2.1388551306876435

		# 52.6344285817945, -1.1388551306876435

		# dec_lat = random.randrange(0,99)
		# dec_lon = random.randrange(0,999)

		# latitude = latitude + dec_lat
		# longitude = longitude + dec_lon

		img = Posts(content = content, name=filename, latitude = latitude, longitude = longitude)
		db.session.add(img)
		db.session.commit()	
		return redirect(url_for('mapmarkers'))
	else:
		return render_template('upload.html')	

@app.after_request
def add_header(r):
	"""
	Add headers to both force latest IE rendering engine or Chrome Frame,
	and also to cache the rendered page for 10 minutes.
	"""
	r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	r.headers["Pragma"] = "no-cache" 
	r.headers["Expires"] = "0"
	r.headers['Cache-Control'] = 'public, max-age=0'
	return r