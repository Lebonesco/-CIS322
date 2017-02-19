from flask import Flask, render_template, request, url_for, flash
from config import dbname, dbhost, dbport
import json
import psycopg2
from functools import wraps

conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
cur = conn.cursor()

app = Flask(__name__)
app.secret_key = "thisisakey"

def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in sessiion:
			return f(*args, **kwargs)
		else:
			flash("login required")
			return redirect(url_for('login_page'))
	return wrap

@app.route("/dashboard")
@login_required
def dashboard():
	return session['name']

@app.route("/create_user", methods=['GET', 'POST'])
def create_user():
	
	if request.method == 'POST':
		name = request.form['name']
		password = request.form['password']
		cur.execute("SELECT name FROM users WHERE name='" + name + "';")
		results = cur.fetchall()
		if results == None:
			cur.execute("INSERT INTO users (name) VALUES ('" + name + "');")
			conn.commit()
			flash("User successfully inserted into database")
		else:
			flash("User already has this name")	
	return render_template("login.html", title="Create User")

@app.route("/")
@app.route("/login", methods=['GET', 'POST'])
def login():
	error = ''
	try:
		if request.method == 'POST':
			session['logged_in'] = True
			session['name'] = requst.form['name']
			return redirect(url_for('dashboard'))
	except Exception as e:
		error = 'Invalid credentials. Try again.'
	return render_template('login.html', error=error, title="Login")



if __name__ == '__main__':
	app.run(host="0.0.0.0", port=8080, debug=True)
        

