from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit
from mailer import MAIL
from os import environ as env
from flask_session import Session
from replit import db
import hashlib

app = Flask(__name__, static_url_path='/assets/',static_folder='assets/')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = env['SECRET_KEY']
Session(app)
wss = SocketIO(app, manage_session=False, logger=True, cors_allowed_origins=['https://d25e6da8-5e02-4157-94b1-8b6d856f1b60.id.repl.co', 'https://patriot-point-manager.hpms-services.repl.co'])

def hash(strh):
	h = hashlib.new('sha256')
	h.update(strh.encode())
	return h.hexdigest()

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/teacher/login')
def teacher_login():
	if session.get('loggedin', False):
		if session['type'] == 'teacher':
			return render_template('redirect.html', url='/teacher/portal')
		else:
			return render_template('redirect.html', url='/student/portal')
	else:
		return render_template('teacherlogin.html')

@app.route('/student/login')
def student_login():
	if session.get('loggedin', False):
		if session['type'] == 'student':
			return render_template('redirect.html', url='/student/portal')
		else:
			return render_template('redirect.html', url='/teacher/portal')
	else:
		return render_template('studentlogin.html')

@app.route('/teacher/signup')
def teacher_signup():
	if session.get('loggedin', False):
		if session['type'] == 'teacher':
			return render_template('redirect.html', url='/teacher/portal')
		else:
			return render_template('redirect.html', url='/student/portal')
	else:
		return render_template('teachersignup.html')

@app.route('/student/signup')
def student_signup():
	if session.get('loggedin', False):
		if session['type'] == 'student':
			return render_template('redirect.html', url='/student/portal')
		else:
			return render_template('redirect.html', url='/teacher/portal')
	else:
		return render_template('studentsignup.html')


@app.route('/teacher/portal')
def teacher_portal():
	if session.get('loggedin', False):
		if session['type'] == 'teacher':
			return render_template('teacherportal.html', loggedin=session['username'])
		else:
			return render_template('redirect.html', url='/student/portal')
	else:
		return render_template('redirect.html', url='/teacher/login')

@app.route('/student/portal')
def student_portal():
	if session.get('loggedin', False):
		if session['type'] == 'student':
			return render_template('studentportal.html', loggedin=session['username'], pp=db['students'][session['username']]['patriotpoints'])
		else:
			return render_template('redirect.html', url='/teacher/portal')
	else:
		return render_template('redirect.html', url='/student/login')
		
#check
@app.route('/teacher/')
def teacher():
	return render_template('teacher.html')

@app.route('/student/')
def student():
	return render_template('student.html')

@app.route('/logout')
def logout():
	session.clear()
	return render_template('redirect.html', url='/')


@app.route('/patriotpoints')
def patriotpoints():
	return render_template('point.html')


@app.route('/referral')
def student_refer():
	return render_template('refer.html')

#check
@wss.on('teacher_login')
def ws_teacher_login(data):
	print('teacher login')
	if data['username'] in db['teachers'].keys():
		if hash(data['password']) == db['teachers'][data['username']]['password']:
			emit('login_successful', to=request.sid)
			session['loggedin'] = True
			session['username'] = db['teachers'][data['username']]['username']
			session['type'] = 'teacher'
			print('logged in')
		else:
			emit('login_failed', {
				'message': 'Incorrect password!'
			}, to=request.sid)
			print('wrong pass')
	else:
		emit('login_failed', {
			'message': 'Username not found! Try <a href="/teacher/signup">signing up</a> instead.'
		}, to=request.sid)
		print('fail')

@wss.on('teacher_signup')
def ws_teacher_signup(data):
	print('teacher signup')
	if data['username'] not in db['teachers'].keys():
		if data['email'] not in db['usedemails']:
			if data['email'] in env['WHITELISTED_EMAILS'].split(','):
				db['teachers'][data['username']] = {
					'username': data['username'],
					'password': hash(data['password']),
					'type': 'teacher'
				}
				session['loggedin'] = True
				session['type'] = 'teacher'
				session['username'] = data['username']
				emit('signup_success', {})
				db['usedemails'].append(data['email'])
			else:
				MAIL(data['username'], data['email'])
				emit('signup_awaiting_conf', {})
		else:
			emit('signup_fail', {
				'message': 'That email is taken! Try <a href="/teacher/login">logging in</a> instead.'
			})
	else:
		emit('signup_fail', {
			'message': 'That username is taken! Try <a href="/teacher/login">logging in</a> instead.'
		})

@wss.on('patriot_points_update')
def ws_pp_update(data):
	if data['username'] in db['students'].keys():
		db['students'][data['username']]['patriotpoints'] += data['amount']
		emit('patriot_points_update_success', {
			'amount_requested': data['amount'],
			'new_amount': db[data['username']]['patriotpoints']
		})
	else:
		emit('patriot_point_update_fail', {
			'message': 'Student not found!'
		})

@wss.on('student_login')
def ws_student_login(data):
	if data['username'] in db['students'].keys():
		if hash(data['password']) == db['students'][data['username']]['password']:
			session['type'] = 'student'
			session['username'] = data['username']
			session['loggedin'] = True
			emit('login_success', {})
		else:
			emit('login_fail', {
				'message': 'Incorrect password!'
			})
	else:
		emit('login_fail', {
			'message': 'Username not found. Try <a href="/student/signup">signing up</a> instead.'
		})

@wss.on('student_signup')
def ws_student_signup(data):
	if data['username'] not in db['students'].keys():
		db['students'][data['username']] = {
			'patriotpoints': 0,
			'password': hash(data['password'])
		}
		session['type'] = 'student'
		session['loggedin'] = True
		session['username'] = data['username']
		emit('signup_success', {})
	else:
		emit('signup_fail', {
			'message': 'Username taken! Try <a href="">logging in</a> instead.'
		})

wss.run(app, host='0.0.0.0', port=69+420+48+21+911+666+71+13)