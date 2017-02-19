from flask import Flask, redirect, render_template, request, url_for, flash, session
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
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash("login required")
			return redirect(url_for('login_page'))
	return wrap

@app.route("/dashboard")
@login_required
def dashboard():
	return render_template("dashboard.html")

@app.route("/create_user", methods=['GET', 'POST'])
def create_user():
	
        if request.method == 'POST':
                name = request.form['name']
                password = request.form['password']
                role = request.form['role']
                cur.execute("SELECT username FROM users WHERE username='" + name + "';")
                results = cur.fetchall()
                if len(results) == 0:
                        cur.execute("SELECT role_pk FROM roles WHERE rolename='" + role + "';");
                        role_pk = cur.fetchall();
                        cur.execute("INSERT INTO users (username, password) VALUES ('" + name + "', '"+password+"', '"+role_pk+"');")
                        conn.commit()
                        flash("User successfully inserted into database")
                else:
                        flash("User already has this name")	
        return render_template("createUser.html")

@app.route("/")
def welcome():
    return render_template("welcome.html", dbname=dbname, dbhost=dbhost, dbport=dbport)

@app.route("/login", methods=['GET', 'POST'])
def login():
	error = ''
	if request.method == 'POST':
                cur.execute("SELECT password from users WHERE username='" + request.form['name'] + "';")
                result = cur.fetchall()
                if len(result) == 0:
                    error = "User doesn't exist"
                else:
                    tmp = False
                    for password in result:
                        if password[0] == request.form['password']:
                            tmp = True
                    if not tmp:
                        error = "Invalid password"
                    else:
                        session['name'] = request.form['name']
                        session['logged_in'] = True
                        return redirect(url_for('dashboard'))
	
	return render_template('login.html', error=error)

@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for('welcome'))

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=8080, debug=True)
        

