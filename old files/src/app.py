from flask import Flask, render_template, flash, request, url_for, redirect, session
from functools import wraps
import psycopg2
import sys
import json
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
@app.route('/rest')
def rest():
    return render_template('rest.html')

@app.route('/rest/lost_key', methods=['POST'])
def lost_key():
    dat = dict()
    dat['timestamp']=req['timestamp']
    dat['result']='OK'
    data = json.dumps(dat)
    return data

@app.route('/rest/activate_user/<name>', methods=['POST'])
def activate_user(name):
    try:
        flash("inserting into database")
        cur.execute("INSERT INTO users (username) VALUES ('" + name + "');")
        conn.commit();
        return 'OK'
    except Exception as e:
        return 'FAIL'

@app.route('/rest/suspend_user', methods=['POST'])
def suspend_user():
    return "nothing"

@app.route('/rest/list_products', methods=['POST'])
def list_products():
    return "nothing"

@app.route('/rest/add_products/<vendor>/<description>', methods=['POST'])
def add_products(vendor, description):
    try:
        cur.execute("INSERT INTO products (vendor, description) VALUES ('"+vendor+"','"+description+"');")
        conn.commit();
        return 'OK'
    except Exception as e:
        return 'FAIL'

@app.route('/rest/add_asset/<asset_tag>/<description>', methods=['POST'])
def add_asset(asset_tag, description):
    try:
        cur.execute("INSERT INTO assets (asset_tag, description) VALUES ('"+asset_tag+"','"+description+"');")
        conn.commit();
        return 'OK'
    except Exception as e:
        return 'FAIL'

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    data =[]
    flash(request)
    if request.method == 'POST':
        arg = request.form['arg']
        #if arg == "active_user":
         #   name = request.form['name']
          #  
           # data = url_for('activate_user', name=name)
            #flash('test')
       # elif arg == "add_products":
        #    vendor = request.form['vendor']
         #   description = request.form['description']
          #  data = url_for('add_products', vendor=vendor, description=description)
        #elif arg == "add_asset":
         #   asset_tag = request.form['asset_tag']
          #  description = request.form['description']
           # data = url_for('add_asset', asset_tag=asset_tag, description=description)

@app.route('/rest/lost_key', methods=('POST',))
def lost_key():
    # Try to handle as plaintext
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])

    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['result'] = 'OK'
    data = json.dumps(dat)
    return data

@app.route('/rest/activate_user', methods=('POST',))
#not finished
def activate_user():
    # Try to handle as plaintext
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])

    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['result'] = 'OK'
    data = json.dumps(dat)
    return data

@app.route('/rest/suspend_user', methods=('POST',))
def suspend_user():
    # Try to handle as plaintext
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])

    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['result'] = 'OK'
    data = json.dumps(dat)
    return data


@app.route('/rest/list_products', methods=('POST',))
def list_products():
    """This function is huge... much of it should be broken out into other supporting
        functions"""
    
    # Check maybe process as plaintext
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])
    # Unmatched, take the user somewhere else
    else:
        redirect('rest')
    
    # Setup a connection to the database
    conn = psycopg2.connect(dbname=dbname,host=dbhost,port=dbport)
    cur  = conn.cursor()
    
    # If execution gets here we have request json to work with
    # Do I need to handle compartments in this query?
    if len(req['compartments'])==0:
        print("have not compartment")
        # Just handle vendor and description
        SQLstart = """select vendor,description,string_agg(c.abbrv||':'||l.abbrv,',')
from products p
left join security_tags t on p.product_pk=t.product_fk
left join sec_compartments c on t.compartment_fk=c.compartment_pk
left join sec_levels l on t.level_fk=l.level_pk"""
        if req['vendor']=='' and req['description']=='':
            # No filters, add the group by and query is ready to go
            SQLstart += " group by vendor,description"
            cur.execute(SQLstart)
        else:
            if not req['vendor']=='' and not req['description']=='':
                req['vendor']="%"+req['vendor']+"%"
                req['description']="%"+req['description']+"%"
                SQLstart += " where description ilike %s and vendor ilike %s group by vendor,description"
                cur.execute(SQLstart,(req['description'],req['vendor']))
            elif req['vendor']=='':
                req['description']="%"+req['description']+"%"
                SQLstart += " where description ilike %s group by vendor,description"
                cur.execute(SQLstart,(req['description'],))
            elif req['description']=='':
                req['vendor']="%"+req['vendor']+"%"
                SQLstart += " where vendor ilike %s group by vendor,description"
                cur.execute(SQLstart,(req['vendor'],))
    else:
        print("have compartment %s"%len(req['compartments']))
        # Need to handle compartments too
        SQLstart = """select vendor,description,string_agg(c.abbrv||':'||l.abbrv,',')
from security_tags t
left join compartments c on t.compartment_fk=c.compartment_pk
left join levels l on t.level_fk=l.level_pk
left join products p on t.product_fk=p.product_pk
where product_fk is not NULL and c.abbrv||':'||l.abbrv = ANY(%s)"""
        if req['vendor']=='' and req['description']=='':
            # No filters, add the group by and query is ready to go
            SQLstart += " group by vendor,description,product_fk having count(*)=%s"
            cur.execute(SQLstart,(req['compartments'],len(req['compartments'])))
        else:
            if not req['vendor']=='' and not req['description']=='':
                req['vendor']="%"+req['vendor']+"%"
                req['description']="%"+req['description']+"%"
                SQLstart += " and description ilike %s and vendor ilike %s group by vendor,description,product_fk having count(*)=%s"
                cur.execute(SQLstart,(req['compartments'],req['description'],req['vendor'],len(req['compartments'])))
            elif req['vendor']=='':
                req['description']="%"+req['description']+"%"
                SQLstart += " and description ilike %s group by vendor,description,product_fk having count(*)=%s"
                cur.execute(SQLstart,(req['compartments'],req['description'],len(req['compartments'])))
            elif req['description']=='':
                req['vendor']="%"+req['vendor']+"%"
                SQLstart += " and vendor ilike %s group by vendor,description,product_fk having count(*)=%s"
                cur.execute(SQLstart,(req['compartments'],req['vendor'],len(req['compartments'])))
    
    # One of the 8 cases should've run... process the results
    dbres = cur.fetchall()
    listing = list()
    for row in dbres:
        e = dict()
        e['vendor'] = row[0]
        e['description'] = row[1]
        if row[2] is None:
            e['compartments'] = list()
        else:
            e['compartments'] = row[2].split(',')
        listing.append(e)
    
    # Prepare the response
    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['listing'] = listing
    data = json.dumps(dat)
    
    conn.close()
    return data
 
@app.route('/rest/add_products', methods=('POST',))
def add_products():
        # Try to handle as plaintext
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])

    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['result'] = 'OK'
    data = json.dumps(dat)
    return data


@app.route('/rest/add_asset', methods=('POST',))
def add_asset():
        # Try to handle as plaintext
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])

    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['result'] = 'OK'
    data = json.dumps(dat)
    return data
    
@app.route('/goodbye')
def goodbye():
    if request.method=='GET' and 'mytext' in request.args:
        return render_template('rest.html',data=request.args.get('mytext'))

    # request.form is only populated for POST messages
    if request.method=='POST' and 'mytext' in request.form:
        return render_template('rest.html',data=request.form['mytext'])
    return render_template('rest.html')eturn render_template("insert.html", data=data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)



