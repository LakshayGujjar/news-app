import sqlite3
from flask import Flask,render_template,url_for,redirect,request
from flask import session
from scraper import get_data 

app = Flask(__name__)
app.secret_key = 'codecraze1000' #defined for session
#session data should be cleared when user is loged out


@app.route('/')
def home():
	return redirect(url_for("login_user"))

@app.route('/login/',methods = ["POST","GET"])
def login_user():
	check = [1,1]
	if request.method == "POST":
		user_email = request.form['user_email']
		user_password = request.form["user_password"]

		with sqlite3.connect('users.db') as con:
			cur = con.cursor()
			query = 'SELECT name FROM users WHERE email_id='+"'"+user_email+"'"
			cur.execute(query)
			temp = cur.fetchall()
			if len(temp)>0:
				#correct email is entered
				query ='SELECT name FROM users WHERE email_id='+"'"+user_email+"'"+' and password='+"'"+user_password+"'"
				cur.execute(query)
				temp = cur.fetchall()
				if len(temp)>0:
					#password is also correct

					#---------------------SESSION CREATED WHEN LOGIN SUCCESSFULLY ------------------
					session['user_email_data'] = user_email

					return redirect(url_for("my_profile",name=temp[0][0]))
				else:
					#wrong password
					check[1] = 0
					return render_template("login.html",check = check)
			else:
				#wrong email is entered
				check[0] = 0
				return render_template("login.html",check = check)
				
	return render_template("login.html",check =check) 




@app.route('/signup/',methods = ["POST","GET"])
def signup_user():
	temp = 0
	if request.method == "POST":
		user_email = request.form['user_email']

		serial_id = 0
		with sqlite3.connect("users.db") as con:
				cur = con.cursor()
				query = 'SELECT MAX(id) from users'
				cur.execute(query)

				serial_id = cur.fetchall()[0][0]
				serial_id = serial_id + 1
		con.close()

		data = (user_email,request.form['user_name'],request.form['user_password'],request.form['gender'],serial_id)

		try :
			with sqlite3.connect("users.db") as con:
				cur = con.cursor()
				cur.execute("INSERT INTO users(email_id,name,password,gender,id) VALUES(?,?,?,?,?)",data)
				
				con.commit()

		except :
			con.rollback()

			query = 'SELECT email_id FROM users WHERE email_id = ' + "'" +user_email + "'"
			with sqlite3.connect("users.db") as con:
				cur = con.cursor()
				cur.execute(query)
				temp = len(cur.fetchall())
			return render_template("signup.html",temp = temp)

		#--------------SESSION IS CREATED HERE FOR SUCCESSFUL SIGNUP --------------------------
		session['user_email_data'] = user_email
		return redirect(url_for("my_profile",name=request.form['user_name']))

	return render_template("signup.html",temp = temp)

@app.route('/')

@app.route('/profile/<name>')
def my_profile(name):
	if not('user_email_data' in session):
		return redirect(url_for("login_user"))
	#else =>user its login so we want to restrict him to login to other accounts
	else:
		with sqlite3.connect('users.db') as con:
			cur = con.cursor()
			query ='SELECT name from users WHERE email_id = ' + "'" + session['user_email_data'] + "'"
			cur.execute(query)

			if (name == cur.fetchall()[0][0]):
				query ='SELECT * FROM users WHERE email_id=' +"'"+session['user_email_data']+"'"
				cur.execute(query)
				data = cur.fetchall()
				print(data)
				return render_template("profile.html",data = data)
			else :
				return '<h1> you tried to go to invalid link </h1>'

@app.route('/logout_user/')
def logout_user():
	if 'user_email_data' in session:
		session.pop('user_email_data',None)
	
	return redirect(url_for("login_user"))


@app.route('/read_news/<page_no>')
def news(page_no):
	if not('user_email_data' in session):
		return redirect(url_for("login_user"))

	news_data = get_data(page_no)
	return render_template("news.html",data = news_data,num=int(page_no))

app.debug = True
app.run()

