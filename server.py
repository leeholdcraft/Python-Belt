from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
app= Flask(__name__)
app.secret_key = 'My super secret key'
bcrypt = Bcrypt(app)

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def begin():
    return render_template("login.html")

@app.route('/adduser', methods=['POST'])
def register():
    is_valid = True
    if len(request.form['first_name']) < 2:
        is_valid = False
        flash("Please enter a first name")
    if len(request.form['last_name']) < 2:
        is_valid = False
        flash("Please enter a last name")
    if not EMAIL_REGEX.match(request.form['email']):
        is_valid= False
        flash("Invalid email address!")
    if len(request.form['password']) < 8:
        is_valid = False
        flash("Please enter a password with at least 8 characters")
    if request.form['password'] != request.form['confirm']:
        is_valid = False
        flash("Passwords must match")
    mysql = connectToMySQL("belt")
    query = "SELECT * FROM users WHERE email= %(email)s;"
    data = {
        "email": request.form["email"],
        }
    result = mysql.query_db(query, data)
    if len(result) > 0:
        is_valid=False
        flash("Email already used")
    if not is_valid:
        return redirect("/")

    else:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        mysql = connectToMySQL("belt")
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password_hash)s);"
        data = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form["email"],
            "password_hash": pw_hash ,
            }
        newuser = mysql.query_db(query, data)
        print (newuser)
        flash("You have successfully registered!")
        return redirect('/welcome')

@app.route('/login', methods=['POST'])
def login():
    mysql = connectToMySQL("belt")
    query = "SELECT * FROM users WHERE email = %(email)s;"
    data = { "email" : request.form["email"] }
    result = mysql.query_db(query, data)
    if len(result) > 0:
        if bcrypt.check_password_hash(result[0]['password'], request.form['password']):
            session['userid'] = result[0]['id']
            session['username'] = result[0]['first_name']
            return redirect('/welcome')
        else:
            flash('Invalid email/password combination')
    else:
        flash("Email not in database")
        return redirect("/")

@app.route('/welcome/')
def success():
    if 'userid' not in session:
        flash('Must be logged in to acces this page')
        return redirect('/')
    user_id = session['userid']
    mysql = connectToMySQL("belt")
    users = mysql.query_db('SELECT * FROM users')
    mysql = connectToMySQL("belt")
    likes = mysql.query_db('SELECT * FROM likes')
    mysql = connectToMySQL("belt")
    content= mysql.query_db("SELECT * FROM thoughts JOIN users ON users.id = thoughts.users_id;")
    return render_template("index.html", users=users, thoughts=content, likes=likes)

@app.route('/add_thought', methods=['POST'])
def new_thoughts():
    is_valid = True
    if len(request.form['text']) < 5:
        is_valid = False
        flash("Thoughts must be at least 5 characters!")
    if not is_valid:
        return redirect("/welcome")
    else:
        mysql = connectToMySQL("belt")
        query="INSERT INTO thoughts (text, users_id) VALUES (%(text)s, %(user)s);"
        data={
            "text": request.form['text'],
            "user": session['userid']
        }
        mysql.query_db(query, data)
        return redirect('/welcome')
    
@app.route('/like/<users_id>', methods=['POST'])
def like(users_id):
    mysql = connectToMySQL("belt")
    query = "INSERT INTO likes (users_id, thoughts_id) VALUES (%(who)s, %(text)s);"
    data = {
        "who": session['userid'],
        "text": users_id
    }
    like=mysql.query_db(query,data)
    return redirect('/welcome')

@app.route('/unlike/<users_id>', methods=['POST'])
def unlike(users_id):
    mysql = connectToMySQL("belt")
    query = "DELETE FROM likes WHERE thoughts_id = %(who)s;"
    data = {
        "who": users_id 
    }
    unlike=mysql.query_db(query,data)
    return redirect('/welcome')


@app.route("/show/<users_id>")
def show(users_id):
    mysql = connectToMySQL("belt")
    query = "SELECT * FROM thoughts JOIN users on users.id= users_id WHERE users_id= %(content_id)s;"
    data = {
        "content_id": users_id
    }
    content=mysql.query_db(query,data)
    print(content)
    return render_template("view.html", thoughts=content)


@app.route('/thoughts/<user_id>/delete', methods=['POST'])
def delete(user_id):
    mysql = connectToMySQL("belt")
    query="DELETE FROM thoughts WHERE id = %(thought)s"
    data={
        "thought": user_id
    }
    mysql.query_db(query, data)
    return redirect('/welcome')

@app.route('/logout', methods=["POST"])
def logout():
    session.clear()
    return render_template("logout.html")


if __name__== "__main__":
    app.run(debug= True)