from flask import Flask, redirect, render_template, request, url_for, flash, session
from config import dbname, dbhost, dbport
import json
import psycopg2
from functools import wraps
import sys
app = Flask(__name__)
app.secret_key = "thisisakey"

def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash("login required")
			return redirect(url_for('login'))
	return wrap

@app.route("/dashboard")
@login_required
def dashboard():
        conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
        cur = conn.cursor()
        
        if session['role'] == 'Facility Officer':
            cur.execute("SELECT request_pk, username, f1.common_name, f2.common_name, request_data  FROM requests JOIN users ON requester_fk=user_pk JOIN facilities f1 ON source_fk=f1.facility_pk JOIN facilities f2 ON destination_fk=f2.facility_pk WHERE request_pk NOT IN(SELECT request_fk FROM transit);")
            data = cur.fetchall()
            header = "Request"
            rows = ["Request ID","Requester","Source", "Destination", "Request Date"]
            url = "/approve_req"
        else:
            cur.execute("SELECT request_fk, load_time, unload_time FROM transit WHERE load_time IS Null AND unload_time IS Null")
            data = cur.fetchall()
            header = "Transit"
            rows = ["Request ID", "Load Time", "Unload Time"]
            url = "/update_transit"
            conn.commit()
        conn.close()
        return render_template("dashboard.html", data=data, header=header, rows=rows, url=url)

@app.route("/revoke_user", methods=['POST'])
def revoke_user():
    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cur = conn.cursor()
    if request.method == 'POST' and 'arguments' in request.form:
        req = json.loads(request.form['arguments'])

    data = {}
    data['result'] = "success"
    data['input'] = req
    try:
        cur.execute("SELECT * FROM users WHERE username='"+req['username']+"';")
        result = cur.fetchall()
        if len(result) > 0:
            cur.execute("UPDATE users SET active=FalseIWHERE username='"+req['username']+"';")
        else:
            data['result'] = 'user does not exist'
        conn.commit()
    except Exception as e:
        data['result'] = 'failure'
    data = json.dumps(data)
    return data

@app.route("/activate_user", methods=['POST'])
def activate_user():
    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cur = conn.cursor()
        
    if request.method == 'POST' and 'arguments' in request.form:
        req = json.loads(request.form['arguments'])

    data = {}
    data['result'] = 'success'
    facilityOfficer = None
    if req['role'] == 'facofc':
        facilityOfficer = True
    elif req['role'] == 'logofc':
        facilityOfficer = False
    else:
        data['result'] = 'failure'

    if facilityOfficer != None:
        try:
            cur.execute("SELECT * FROM users WHERE username='"+req['username']+"';")
            result = cur.fetchall()
            if len(result) > 0:
                cur.execute("UPDATE users SET active=TRUE, password='"+req['password']+"' WHERE username='"+req['username']+"';")        
            else:
                role = 1 if facilityOfficer else 2
                cur.execute("INSERT INTO users (username, password, role_fk, active) VALUES ('"+req['username']+"','"+req['password']+"',"+str(role)+", TRUE);")
            conn.commit()
        except Exception as e:
            data['result'] = 'failure: ' + str(e)

    data = json.dumps(data)
    conn.close()
    return data
                
@app.route("/add_facility", methods=['GET', 'POST'])
def add_facility():
    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cur = conn.cursor()
    
    cur.execute("SELECT common_name FROM facilities")
    facilities = cur.fetchall()

    if request.method == 'POST':
        name = request.form['name']
        code = request.form['code']
        cur.execute("SELECT common_name FROM facilities WHERE common_name='"+name+"';")
        results = cur.fetchall()
        if len(results) == 0:
            cur.execute("INSERT INTO facilities (common_name, code) VALUES ('"+name+"', '"+code+"');")
            conn.commit()
            flash("Facility successfully inserted into database")
        else:
            flash("Facility already in database")
        return redirect(url_for("add_facility"))
    conn.close()
    return render_template("addFacility.html", facilities=facilities)


@app.route("/add_asset", methods=['GET', 'POST'])
def add_asset():
    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cur = conn.cursor()
    cur.execute("SELECT common_name FROM facilities")
    facilities = cur.fetchall()
    cur.execute("SELECT asset_tag FROM assets")
    assets = cur.fetchall()
    if request.method == 'POST':
        asset_tag = request.form['asset_tag']
        description = request.form['description']
        facility = request.form['facility']
        date = request.form['date']
        cur.execute("SELECT asset_tag FROM assets WHERE asset_tag='"+asset_tag+"';")
        results = cur.fetchall()
        if len(results) == 0:
            cur.execute("INSERT INTO assets (asset_tag, description) VALUES ('"+asset_tag+"', '"+description+"');")
            cur.execute("SELECT asset_pk FROM assets WHERE asset_tag='"+asset_tag+"';")
            asset_pk = cur.fetchall()
            cur.execute("SELECT facility_pk FROM facilities WHERE common_name='"+facility+"';")
            facility_pk = cur.fetchall()
            facility_pk = facility_pk[0]
            asset_pk = asset_pk[0]
            cur.execute("INSERT INTO asset_at (asset_fk, facility_fk, arrive_dt, disposed) VALUES ("+str(asset_pk[0])+", "+str(facility_pk[0])+", '"+date+"', False);")
            conn.commit()
            flash("Asset successfully inserted into database")
        else:
            flash("Asset already in database")
        conn.close()
        return redirect(url_for("add_asset"))
    conn.close()
    return render_template("addAsset.html", facilities=facilities, assets=assets)

@app.route("/")
def welcome():
    return render_template("welcome.html", dbname=dbname, dbhost=dbhost, dbport=dbport)

@app.route("/login", methods=['GET', 'POST'])
def login():
    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cur = conn.cursor()
	
    error = ''
    if request.method == 'POST':
        cur.execute("SELECT password, active from users WHERE username='" + request.form['name'] + "';")
        result = cur.fetchall()
        if len(result) == 0:
            error = "User doesn't exist"
        else:
            tmp = False
            password = result[0]
            password = password[0]
            if password == request.form['password']:
                tmp = True
            if not tmp:
                error = "Invalid password"
            else:
                active = result[0]
                active = active[1]
                if not active:
                    error = "User is not active"

                else:   
                    cur.execute("SELECT rolename FROM roles r JOIN users u ON r.role_pk=u.role_fk WHERE u.username='"+request.form['name']+"';")
                    role = cur.fetchone()
                    session['name'] = request.form['name']
                    session['logged_in'] = True
                    session['role'] = role[0]
                    conn.close()
                    return redirect(url_for('dashboard'))
	
    return render_template('login.html', error=error)

@app.route("/dispose_asset", methods=['GET', 'POST'])
@login_required
def disposeAsset():
    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cur = conn.cursor()
    cur.execute("SELECT asset_tag FROM assets")
    assets = cur.fetchall()

    if session['role'] == 'Logistics Officer':
        if request.method == 'POST':
            asset_tag = request.form['asset_tag']
            date = request.form['date']
            cur.execute("SELECT asset_pk FROM  assets WHERE asset_tag='"+asset_tag+"';")
            result = cur.fetchall()
            if len(result) == 0:
                flash("asset does not exist")
            else:
                cur.execute("SELECT * FROM assets JOIN asset_at ON asset_pk=asset_fk WHERE depart_dt is not null AND asset_tag='"+asset_tag+"';")
                stuff = cur.fetchall()
                if len(stuff) > 0:
                    flash("Asset Already Disposed")
                else:
                    asset_pk = result[0]
                    cur.execute("UPDATE asset_at SET depart_dt='"+date+"' WHERE asset_fk="+str(asset_pk[0])+";")
                    cur.execute("UPDATE assets SET disposed=TRUE WHERE asset_pk="+str(asset_pk[0])+";")
                    conn.commit()
                    conn.close()
                    flash("asset_tag disposed")
                return redirect(url_for("dashboard"))
        conn.close()
        return render_template("disposeAsset.html", assets=assets)


    flash("Only logistics officers can dispose of assets")
    return render_template("welcome.html")

@app.route("/asset_report", methods=['GET', 'POST'])
@login_required
def assetReport():
    data = ""
    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cur = conn.cursor()
    cur.execute("SELECT common_name FROM facilities")
    facilities = cur.fetchall()

    if request.method == 'POST':
        facility = request.form['facility']
        date = request.form['date']
        try:
            cur.execute("SELECT asset_tag, common_name, arrive_dt, depart_dt FROM assets a JOIN asset_at aa ON asset_pk=asset_fk JOIN facilities ON facility_fk=facility_pk WHERE facilities.common_name LIKE '%"+facility+"%' AND aa.arrive_dt <= '"+date+"' AND (aa.depart_dt >= '"+date+"' OR aa.depart_dt is null);")
            data = cur.fetchall()
        except Exception as e:
            flash('Please enter a Date')
    conn.close()
    flash(data)
    return render_template("assetReport.html", facilities=facilities, data=data)

@app.route("/transfer_req", methods=['GET', 'POST'])
@login_required
def transferReq():
    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cur = conn.cursor()
    cur.execute("SELECT common_name FROM facilities;")
    facilities = cur.fetchall()
    cur.execute("SELECT asset_tag FROM assets;")
    assets = cur.fetchall()

    error = ''
    if session['role'] == 'Logistics Officer':
        if request.method == 'POST':
            if "asset_tag" not in request.form or "source" not in request.form or "destination" not in request.form or "date" not in request.form:
                flash("missing values")
            else:
                asset_tag = request.form['asset_tag']
                source = request.form['source']
                destination = request.form['destination']
                date = request.form['date']
                cur.execute("SELECT asset_pk FROM assets WHERE asset_tag='"+asset_tag+"';")
                asset_fk = cur.fetchall()
                if len(asset_fk) >= 0:
                    cur.execute("SELECT user_pk from users WHERE username='"+session['name']+"';")
                    user_pk = cur.fetchone()
                    cur.execute("SELECT facility_pk from facilities WHERE common_name='"+source+"';")
                    source_fk = cur.fetchone()
                    cur.execute("SELECT facility_pk from facilities WHERE common_name='"+destination+"';")
                    destination_fk = cur.fetchone()
                    
                    cur.execute("INSERT INTO requests (requester_fk, request_data, source_fk, destination_fk, assset_fk) VALUES ("+str(user_pk[0])+",'"+date+"',"+str(source_fk[0])+","+str(destination_fk[0])+","+str(asset_fk[0][0])+");")
                    flash("Asset Transfer Request is Successful!")
                else:
                    flash("Asset not exist")
                conn.commit()
                conn.close()
                return redirect(url_for("dashboard"))
                
            error = "Asset Tag does not exist"
        return render_template("transferReq.html", error=error, facilities=facilities, assets=assets)
    
    flash("Only Logistics officers can request transfers")
    conn.close()
    return redirect(url_for('dashboard'))

@app.route("/approve_req", methods=['GET', 'POST'])
@login_required
def approveReq():
    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cur = conn.cursor()
    cur.execute("SELECT request_pk, username, asset_tag, f1.common_name, f2.common_name, request_data  FROM requests JOIN users ON requester_fk=user_pk JOIN facilities f1 ON source_fk=f1.facility_pk JOIN facilities f2 ON destination_fk=f2.facility_pk JOIN assets ON assset_fk=asset_pk WHERE request_pk NOT IN(SELECT request_fk FROM transit);")
    requests = cur.fetchall()

    error = ''
    if session['role'] == 'Facility Officer':
        if request.method == 'POST':
            approval = request.form.getlist("approval")
            deny = request.form.getlist("deny")
            request_pk = request.form["request_pk"]

            cur.execute("SELECT user_pk FROM users WHERE username='"+session['name']+"';")
            approved_by = cur.fetchall();
            approved_by = approved_by[0]
            if len(approval) != 0:
                flash("APPROVED")  
                cur.execute("INSERT INTO transit (request_fk) VALUES ('"+request_pk+"');")
                cur.execute("UPDATE requests SET approve_by='"+str(approved_by[0])+"' WHERE request_pk='"+request_pk+"';")
            
            else:
                flash("Request has been removed")
                cur.execute("DELETE FROM requests WHERE request_pk='"+request_pk+"';")
            conn.commit()
            conn.close()
            
            return redirect(url_for("dashboard"))

        return render_template("approveReq.html", requests=requests)
    flash("Only Facilities Officers can approve request")
    return redirect(url_for("dashboard"))

@app.route("/update_transit", methods=['GET', 'POST'])
def transferReport():
    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cur = conn.cursor()
    cur.execute("SELECT * FROM transit WHERE load_time IS Null AND unload_time IS Null")
    transit = cur.fetchall()
    if session['role'] == 'Logistics Officer':
        if request.method == 'POST':
            load_time = request.form['load']
            unload_time = request.form['unload']
            transit_pk = request.form["transit_pk"]
            cur.execute("UPDATE transit SET load_time='"+load_time+"', unload_time='"+unload_time+"' WHERE transit_pk='"+transit_pk+"';")
            
            cur.execute("SELECT unload_time, assset_fk, destination_fk FROM transit JOIN requests ON request_fk=request_pk WHERE transit_pk='"+transit_pk+"';")
            result = cur.fetchall()
            result = result[0]
            cur.execute("INSERT INTO asset_at (asset_fk, facility_fk, arrive_dt) VALUES ('"+str(result[1])+"','"+str(result[2])+"','"+str(result[0])+"');")

            conn.commit()
            flash("Updated load/unload times")
            conn.close()
            return redirect(url_for('dashboard'))
        conn.close()
        return render_template("update_transit.html", transit=transit)
    flash("Only Logistics Officer can update tracking information.")
    conn.close()
    return redirect(url_for("dashboard"))


@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for('welcome'))

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=8080, debug=True)
        

