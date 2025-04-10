from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'supersecretkey')  # for sessions

# Configure SqlLite database
MONGO_USER = "eladlevavi"
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
MONGO_CLUSTER = "cluster0.ingorqn.mongodb.net"
MONGO_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_CLUSTER}/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGO_URI)
db = client['flask_app']
messages_collection = db['messages']

# Flask login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class AdminUser(UserMixin):
	id = "admin" # single hard-coded admin

@login_manager.user_loader
def load_user(user_id):
	if (user_id == "admin"):
		return AdminUser()
	return None

# ---- Routes ----


@app.route('/')
def home():
	return render_template('index.html', message="Hello world!")


@app.route('/about')
def about():
	return render_template('about.html', title='About', description='This is a flask demo app')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
	if request.method == 'POST':
		name = request.form.get('name')
		message = request.form.get('message')
		
		# Insert into MongoDB
		messages_collection.insert_one({
			'name': name,
			'message': message
		})

		return render_template('thank_you.html', name=name, message=message)
	return render_template('contact.html')

@app.route('/admin')
@login_required
def admin():		
	all_messages = list(messages_collection.find())
	return render_template('admin.html', messages = all_messages)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		password = request.form.get('password')

		if password == 'admin123':
			user = AdminUser()
			login_user(user)
			return redirect(url_for('admin'))
		return "401, Wrong password"
	return render_template('login.html')

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))

if (__name__ == "__main__"):
	app.run(debug=True)
