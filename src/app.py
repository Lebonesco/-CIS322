from flask import Flask, render_template, flash, request, url_for, redirect, session
from functools import wraps
import psycopg2
import sys

conn = psycopg2.connect(dbname='lost', host='localhost', port=5432, user='osnapdev', password='secret')
cur = conn.cursor()

app = Flask(__name__)
app.secret_key='thisisakey'




@app.route('/')
def index():
    #return 'goodbye'
    return render_template('index.html')


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("login required")
            return redirect(url_for('login_page'))
    return wrap

@app.route('/filter')
@login_required
def filter():
    return render_template("reportFilter.html")


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    data = []
    #cur.execute("SELECT fcode, asset_pk, asset_tag, arrive_dt, depart_dt FROM assets a JOIN asset_at aa ON a.asset_pk=aa.asset_fk JOIN facilities f ON facility_pk=aa.facility_fk;")
    if True:
        flash(request.args['date'])
        report_type = request.args['report_type']
        filter_type = request.args['filter_type']
        filter = request.args['filter']
        if report_type == "asset":
            if filter_type == "facility":
                cur.execute("SELECT fcode, a.asset_tag, description, c.arrive_dt, c.depart_dt FROM assets a JOIN asset_at aa ON a.asset_pk=aa.asset_fk JOIN facilities f ON f.facility_pk=aa.facility_fk JOIN asset_on ao ON a.asset_pk=ao.asset_fk JOIN convoys c ON ao.convoy_fk=c.convoy_pk WHERE f.fcode LIKE '%" + filter + "%';")
            elif filter_type == "date":
                cur.execute("SELECT common_name, a.asset_tag, description, c.arrive_dt, c.depart_dt FROM assets a JOIN asset_at aa ON a.asset_pk=aa.asset_fk JOIN facilities f ON f.facility_pk=aa.facility_fk JOIN asset_on ao ON a.asset_pk=ao.asset_fk JOIN convoys c ON ao.convoy_fk=c.convoy_pk WHERE'"+ request.args['date'] + "'<= c.depart_dt OR '" + request.args['date'] + "' >= c.arrive_dt;")
            data = cur.fetchall()
            return render_template('dashboard.html', data=data)
        else:
            if filter_type == "date":
                if len(request.args['date']) > 2:
                    cur.execute("SELECT source_fk, dest_fk, depart_dt, arrive_dt FROM convoys c JOIN asset_on ao ON c.convoy_pk=ao.convoy_fk JOIN assets a ON a.asset_pk=ao.asset_fk WHERE '"+ request.args['date'] + "'>= c.depart_dt AND '" + request.args['date'] + "' <= c.arrive_dt;")
                else:
                    cur.execute("SELECT source_fk, dest_fk, depart_dt, arrive_dt FROM convoys c JOIN asset_on ao ON c.convoy_pk=ao.convoy_fk JOIN assets a ON a.asset_pk=ao.asset_fk;")
            if filter_type == "facility":
                cur.execute("SELECT source_fk, dest_fk, depart_dt, arrive_dt FROM convoys c JOIN asset_on ao ON c.convoy_pk=ao.convoy_fk JOIN assets a ON a.asset_pk=ao.asset_fk;")

            data = cur.fetchall()
            flash(request.args['date'])
            return render_template('transit.html', data=data)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    error = ''
    
    try:
        if request.method == 'POST':
            session['logged_in'] = True
            session['username'] = request.form['username']
            return redirect(url_for('filter'))

    except Exception as e:
        error = 'Invalid credentials. Try again.'
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('dashboard'))

# API calls are here
@api.route('/insert', methods=['GET', 'POST'])
def insert():
    data =[]
    if request.method == 'POST':
        


    return render_template("insert.html", data)


@app.route('/rest')
def rest():
    return render_template('rest.html')

@app.route('/rest/lost_key', methods=['POST'])
def lost_key():
    return "nothing"

@app.route('/rest/activate_user/<input>', methods=['POST'])
def activate_user(input="result"):
    try:
        cursor.execute("INSERT INTO users (username) VALUES (" + input +");")
        conn.commit();
    except Exception as e:
        pass
    return 'nothing'

@app.route('/rest/suspend_user', methods=['POST'])
def suspend_user():
    return "nothing"

@app.route('/rest/list_products', methods=['POST'])
def list_products():
    return "nothing"

@app.route('/rest/add_products', methods=['POST'])
def add_products():
    try:
        cursor.execute("INSERT INTO users (username) VALUES (" + input +");")
        conn.commit();
    except Exception as e:
        pass
    return 'nothing'

@app.route('/rest/add_asset', methods=['POST'])
def add_asset():
    try:
        cursor.execute("INSERT INTO users (username) VALUES (" + input +");")
        conn.commit();
    except Exception as e:
        pass
    return 'nothing'
























if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)



