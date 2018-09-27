#webserver
from flask import Flask, render_template, request, redirect, session, flash
import random
import datetime
import re
from mysqlconnection import connectToMySQL
import json
from flask_bcrypt import Bcrypt   

app = Flask(__name__)
app.secret_key = 'ThisIsSecret'
mysql = connectToMySQL('retake_python_quotesdb')
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
LETTER_REGEX = re.compile(r'^[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*\d)(?=.*[A-Z]).*$')

@app.route('/')
def index():
    

    return render_template('index.html')


# registration
@app.route("/register", methods=["POST"])
def register():


    # for retention
    session['first_name']=request.form['first_name']
    session['last_name']=request.form['last_name']
    session['email']=request.form['email']

    if len(request.form['first_name']) < 1: 
        flash("This field is required.", 'first_name')
    elif len(request.form['first_name']) < 2 or not LETTER_REGEX.match(request.form['first_name']):
        flash("Must contain at least two letters and contain only letters.", 'first_name')
    
    if len(request.form['last_name']) < 1: 
        flash("This field is required.", 'last_name')
    elif len(request.form['last_name']) < 2 or not LETTER_REGEX.match(request.form['last_name']):
        flash("Must contain at least two letters and contain only letters.", 'last_name')

    mysql = connectToMySQL('retake_python_quotesdb')
    query = "SELECT email FROM users WHERE email = %(email)s;"
    data = { 'email' : request.form['email'] }
    result = mysql.query_db(query, data)
    if len(request.form['email']) < 1: 
        flash("This field is required.", 'email')
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address.", 'email')
    elif result:
        flash("Email was already taken.", 'email')

    if len(request.form['password']) < 1:
        flash("This field is required.", 'password')
    elif  len(request.form['password']) < 8 or len(request.form['password']) > 15 or not PASSWORD_REGEX.match(request.form['password']):
        flash("Must contain a number, a capital letter, and be between 8-15 characters.",'password')

    if len(request.form['confirm_password']) < 1:
        flash("This field is required.", 'confirm_password')
    elif request.form['password'] != request.form['confirm_password']:
        flash("Password must match.", 'confirm_password')

    if '_flashes' in session.keys():
        # debugHelp('REGISTER FAILED METHOD')
        return redirect('/')
    else:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])  
        mysql = connectToMySQL('retake_python_quotesdb')
        query = "INSERT INTO users (first_name, last_name, email, password_hash, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password_hash)s,NOW(), NOW()) ;"
        data ={
            'first_name': request.form['first_name'],
            'last_name':  request.form['last_name'],
            'email': request.form['email'],
            'password_hash': pw_hash,
        }
        mysql.query_db(query, data)

        # debugHelp('REGISTERED METHOD')
        session.clear()
        mysql = connectToMySQL('retake_python_quotesdb')
        query = "SELECT id, first_name FROM users WHERE email = %(email)s;"
        data = { 
            'email' : request.form['email'],
            }
        result = mysql.query_db(query, data)
        session['user_id'] = result[0]['id']
        session['first_name']=request.form['first_name']
        session['logged_in'] = True
        

      
        return redirect('/quotes')
        #  return redirect('/wishes')

# login
@app.route("/login", methods=['POST'])
def login():

    mysql = connectToMySQL('retake_python_quotesdb')
    query = "SELECT id, first_name, last_name, password_hash FROM users WHERE email = %(email)s;"
    data = { 
        'email' : request.form['lemail'],
        }
    result = mysql.query_db(query, data)
    if result:
        # assuming we only have one user with this username, the user would be first in the list we get back
        # of course, we should have some logic to prevent duplicates of usernames when we create users
        # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form
        if bcrypt.check_password_hash(result[0]['password_hash'], request.form['lpassword']):
            # if we get True after checking the password, we may put the user id in session
            session['user_id'] = result[0]['id']
            session['first_name'] = result[0]['first_name']
            session['logged_in'] = True
            # never render on a post, always redirect!
            # print("+++++++++++++++++++++++++++")
            # print(session['level_id'])
            return redirect('/quotes')
            # return redirect('/wishes')
    # if we didn't find anything in the database by searching by username or if the passwords don't match,
    # flash an error message and redirect back to a safe route
    flash("You could not be logged in", 'cannot')
    return redirect("/")


@app.route('/quotes')
def quotes():
    
    if session.get('logged_in') is None:
        flash("You must logged in to enter this website", "logout")
        return redirect('/')
    else:
        
        mysql = connectToMySQL('retake_python_quotesdb')
        query = "SELECT quotes.id AS quote_id, quotes.user_id , users.first_name, users.last_name, quotes.message , quotes.author, quotes.created_at, count(likes.quote_id) AS count FROM quotes LEFT JOIN likes ON likes.quote_id = quotes.id JOIN users ON users.id = quotes.user_id GROUP by quotes.id ORDER BY  quotes.created_at DESC;"
        # data = {
        #     'user_id': session['user_id']
        # }
        quotes = mysql.query_db(query)

        return render_template('dash.html', quotes = quotes)


@app.route("/add_new_quotes", methods=["POST"])
def add_new_quotes():

    # for retention
    session['author']=request.form['author']
    session['quote']=request.form['quote']

    if len(request.form['author']) < 4:
        flash("Author must contain more than 3 characters", 'add_quote')
    
    if len(request.form['quote']) < 11:
        flash("Quote must contain more than 10 characters", 'add_quote')
   
    if '_flashes' in session.keys():
        # debugHelp('REGISTER FAILED METHOD')
        return redirect('/quotes')
    else:

       
        mysql = connectToMySQL('retake_python_quotesdb')
        query = "INSERT INTO quotes (user_id, message, author, created_at, updated_at) VALUES (%(user_id)s, %(message)s, %(author)s, NOW(), NOW()) ;"
        data ={
            'user_id': session['user_id'],
            'message': request.form['quote'],
            'author': request.form['author'],
        }
        mysql.query_db(query, data)


        return redirect('/quotes') 


@app.route("/add_likes/<id>")
def add_likes(id):

   
    

    mysql = connectToMySQL('retake_python_quotesdb')
    query = "SELECT user_id FROM likes WHERE quote_id = %(id)s and user_id = %(user_id)s;"
    data = { 
        'id' : id,
        'user_id': session['user_id']
        }
    for_checklike = mysql.query_db(query, data)
    print("======",for_checklike)
    # print(for_checklike[0]['user_id'])
    # print(for_checklike[0]['gift_id'])
    print(len(for_checklike))
    if len(for_checklike)  == 0:
    
        mysql = connectToMySQL('retake_python_quotesdb')
        query = "INSERT INTO likes (user_id, quote_id, created_at, updated_at) VALUES (%(user_id)s, %(quote_id)s, NOW(), NOW()) ;"
        
        data ={
            'quote_id': id,
            'user_id': session["user_id"]
        }
        mysql.query_db(query, data)
        return redirect('/quotes') 

    return redirect('/quotes') 


@app.route("/remove/<id>")
def remove_quote(id):
       
    mysql = connectToMySQL('retake_python_quotesdb')
    query = "DELETE FROM quotes WHERE id = %(id)s AND user_id = %(user_id)s;"
    datas = {
                'id':  id,
                'user_id': session['user_id']
            }
    mysql.query_db(query, datas)
    
        
    return redirect('/quotes') 


@app.route('/myaccount/<id>')
def myaccount_id(id):
    if session.get('logged_in') is None:
        flash("You must logged in to enter this website", "logout")
        return redirect('/')
    else:

        mysql = connectToMySQL('retake_python_quotesdb')
        query = "SELECT first_name, last_name, email FROM users WHERE id = %(id)s;"
        data = { 
            'id' : id,
            }

        for_edit = mysql.query_db(query, data)
        print(for_edit, '----------------------------------')

        return render_template('edit.html', for_edit = for_edit[0])

@app.route("/edit", methods=["POST"])
def edit():


    # for retention
    session['efirst_name']=request.form['efirst_name']
    session['elast_name']=request.form['elast_name']
    session['eemail']=request.form['eemail']

    if len(request.form['efirst_name']) < 1: 
        flash("This field is required.", 'efirst_name')
    elif len(request.form['efirst_name']) < 2 or not LETTER_REGEX.match(request.form['efirst_name']):
        flash("Must contain at least two letters and contain only letters.", 'efirst_name')
    
    if len(request.form['elast_name']) < 1: 
        flash("This field is required.", 'elast_name')
    elif len(request.form['elast_name']) < 2 or not LETTER_REGEX.match(request.form['elast_name']):
        flash("Must contain at least two letters and contain only letters.", 'elast_name')

    mysql = connectToMySQL('retake_python_quotesdb')
    query = "SELECT email FROM users WHERE id = %(id)s;"
    data = { 'id' : session["user_id"] }
    email_check = mysql.query_db(query, data)



    mysql = connectToMySQL('retake_python_quotesdb')
    query = "SELECT email FROM users WHERE email = %(email)s;"
    data = { 'email' : request.form['eemail'] }
    result = mysql.query_db(query, data)


    if len(request.form['eemail']) < 1: 
        flash("This field is required.", 'eemail')
    elif not EMAIL_REGEX.match(request.form['eemail']):
        flash("Invalid Email Address.", 'eemail')
        
    elif result and email_check != result :
        flash("Email was already taken.", 'eemail')


    mysql = connectToMySQL('retake_python_quotesdb')
    query = "SELECT id FROM users WHERE email = %(email)s;"
    userid = mysql.query_db(query)


    print(userid)
   
    id = session["user_id"]

    # print(int(id))
    # print(session.get["user_id"])
    if '_flashes' in session.keys():
        # debugHelp('REGISTER FAILED METHOD')
        return redirect('/myaccount/'+ str(id))
    else:

        mysql = connectToMySQL('retake_python_quotesdb')
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id  = %(id)s ;"
        data ={
            'id': session["user_id"],
            'first_name' : request.form['efirst_name'],
            'last_name' : request.form['elast_name'],
            'email' : request.form['eemail']
            
        }
        mysql.query_db(query, data)


        return redirect('/myaccount/'+ str(id))
       

@app.route('/user/<id>')
def user_id(id):
    if session.get('logged_in') is None:
        flash("You must logged in to enter this website", "logout")
        return redirect('/')
    else:

        mysql = connectToMySQL('retake_python_quotesdb')
        query = "SELECT first_name, last_name FROM users WHERE id = %(id)s;"
        data = { 
            'id' : id,
            }

        user= mysql.query_db(query, data)

        mysql = connectToMySQL('retake_python_quotesdb')
        query = "SELECT quotes.author, quotes.message, users.first_name, users.last_name FROM quotes JOIN users ON users.id = quotes.user_id WHERE users.id = %(id)s;"
        data = { 
            'id' : id,
            }

        user_quotes = mysql.query_db(query, data)
        print(user_quotes)
        return render_template('user.html', user_quotes = user_quotes, user = user[0])





# logout
@app.route('/logout')
def logout():

    session.clear()
    flash("You have been logged out", "logout")
    return redirect('/')




if __name__ == "__main__":
    app.run(debug=True)
