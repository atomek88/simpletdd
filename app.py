# app.py for flask tdd test
import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
from flask_sqlalchemy import SQLAlchemy

#get folder for this file
basedir = os.path.abspath(os.path.dirname(__file__))

# database config
DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = "my_precious"
USERNAME = 'admin'
PASSWORD = 'admin'

#defile full path for db
DATABASE_PATH = os.path.join(basedir, DATABASE)

# db config
SQLALCHEMY_DATABASE_URI = 'sqlite:///'+DATABASE_PATH
SQLALCHEMY_TRACK_MODIFICATIONS = False

# create and init app
app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)
''' add db connections
def connect_db():
    """connects to db"""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv
'''
import models
'''create db
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# open db connection
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db
#close db
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite.db'):
        g.sqlite_db.close()

'''
@app.route('/')
def index():
    """ Searches db for entries, displays them"""
    entries = db.session.query(models.Flaskr)
    return render_template('index.html', entries=entries)

def hello():
    return "Hello, cruel world!"

@app.route('/login', methods=['GET','POST'])
def login():
    "user login/auth session management"""
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = "Invalid username"
        elif request.form['password'] != app.config['PASSWORD']:
            error = "Invalid password"
        else:
            session['logged_in'] = True
            flash("You were logged in")
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    """User logout/auth/sess mgmt"""
    session.pop('logged_in', None)
    flash("You were logged out")
    return redirect(url_for('index'))

@app.route('/add', methods=['POST'])
def add_entry():
    """Add new post to database"""
    if not session.get('logged_in'):
        abort(401)
    new_entry = models.Flaskr(request.form['title'], request.form['text'])
    db.session.add(new_entry)
    db.session.commit()
    flash("New entry was successfully posted")
    return redirect(url_for('index'))

@app.route('/delete/<post_id>', methods=['GET'])
def delete_entry(post_id):
    '''Delete post from db'''
    result = {'status': 0, 'message': 'Error'}
    try:
        new_id = post_id
        db.session.query(models.Flaskr).filter_by(post_id=new_id).delete()
        db.session.commit()
        result = {'status': 1, 'message': "Post Deleted"}
        flash("The entry was deleted.")
    except Exception as e:
        result = {'status': 0, 'message': repr(e)}
    return jsonify(result)
@app.route('/search/', methods=['GET'])
def search():
    query = request.args.get("query")
    entries = db.session.query(models.Flaskr)
    if query:
        return render_template('search.html', entries=entries, query=query)
    return render_template('search.html')
    
if __name__ == '__main__':

    app.run()
