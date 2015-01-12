from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask import request
import sqlite3 as lite
import os
from functools import wraps
import sqlite3
from app import app
def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('you need to login first.')
			return redirect(url_for('login'))
	return wrap
app.secret_key = os.urandom(24)
app.database='test.db'
conn=sqlite3.connect('test.db')

@app.route('/welcome')
@login_required
def welcome():
	return render_template('index.html')
@app.route('/')
@app.route('/index')
def index():
	header = {'h1': 'STUDENT DETAILS !!!'} # fake user
	return render_template('index.html', title='Home', header=header)

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
	      	if request.form['username'] != 'siva' or request.form['pasword'] != 'siva':
			error = 'invalid authentication'
		else:
			session['logged_in']=True
			return redirect(url_for('details'))
			flash('!Logged in!!')
	return render_template('login.html', error = error)
@app.route('/details')
def details():
	head = {'hd': 'ENTER DETAILS!!!'}
	return render_template('details.html', title = 'Details', head = head)

@app.route('/is_logged_in/')
def is_logged_in():
  return 'user' in session
@app.route('/insert', methods = ['GET','POST'])
def insert():
	fname = request.form['fname']
	sname = request.form['sname']
	email = request.form['email']
	sex = request.form['sex']
	con = lite.connect('test.db')
	with con:
		cur = con.cursor()
		cur.execute('insert into Student (fname,sname,email,sex) values (?,?,?,?)',[fname,sname,email,sex])
	return "data inserted"
@app.route('/display', methods = ['GET','POST'])
def display():
	head = {'h3': 'STUDENT DETAILS'}
	con = lite.connect('test.db')
	with con:
		cur = con.cursor()
		cursor = cur.execute("SELECT * FROM Student")
		rows = []
		for row in cursor:
			rows.append(row)
		return render_template('display.html',title = 'Display',head = head,rows = rows)
@app.route('/logout')
#@login_required
def logout():
	session.pop('logged_in', None)
	flash('logged out')
	return redirect(url_for('login'))
@app.route('/delete', methods = ['GET','POST'])
@login_required
def delete():
	head = {'h3': 'STUDENT DETAILS'}
	fname = request.form['fname']
	con = lite.connect('test.db')
	with con:
		cur = con.cursor()
		cur.execute("DELETE FROM Student \
				WHERE fname =(?)", ((request.form['fname'])))
		rows = []
		cursor = cur.execute("SELECT * FROM Student")
		for row in cursor:
			rows.append(row)
		return render_template('delete.html',title = 'Display',head = head,rows = rows)

