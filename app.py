from flask import Flask, render_template, request, redirect, session
import mysql.connector
import re
import os 

app = Flask(__name__)
app.secret_key=os.urandom(24)
conn = mysql.connector.connect(
    host='project-12fox.criqc0wmc4yw.us-east-1.rds.amazonaws.com',
    user='vishva',
    password='Vishva2003',
    database='12Fox'
)
cursor = conn.cursor()

#Routing to the user Login page

@app.route('/login')
def login():
   return render_template("login.html")



@app.route("/login1", methods=['GET', 'POST'])
def login1():
    msg =""
    if request.method == 'POST':
        USERNAME = request.form['username']
        PASSWORD = request.form['password']

        query = "SELECT * FROM user WHERE USERNAME = %s AND PASSWORD = %s"
        cursor.execute(query, (USERNAME, PASSWORD))
        user=cursor.fetchall()
        
        if len(user)>0:
            session["USER_ID"]=user[0][0]
            return redirect("/home")
        else:
            error="Invalid username or password"
            return render_template("login.html", msg=error)
        
    return render_template('login.html')

#Routing to the user registration page

@app.route("/reg")
def reg():
    return render_template("reg.html")

@app.route("/reg1", methods=['GET', 'POST'])
def reg1():
    msg=""
    if request.method == 'POST':
        USERNAME = request.form['username']
        PASSWORD = request.form['password']
        EMAIL = request.form['email']

        # Check if account exists using MySQL
        query = "SELECT * FROM user WHERE USERNAME = %s AND PASSWORD = %s"
        cursor.execute(query, (USERNAME, PASSWORD))
        user = cursor.fetchall()
        # If account exists show error and validation checks
        if user:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', EMAIL):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', USERNAME):
            msg = 'Username must contain only characters and numbers!'
        elif not USERNAME or not PASSWORD or not EMAIL:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            query =("INSERT INTO user(USER_ID,USERNAME ,PASSWORD ,EMAIL ) VALUES (NULL, %s, %s, %s)")  
            cursor.execute(query, (USERNAME, PASSWORD,EMAIL,))
            user=conn.commit()
            msg = 'You have successfully registered!'
            return render_template('reg.html', msg=msg)
    else :
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('reg.html', msg=msg)

#Routing to the user dashboard

@app.route('/home')
def home():
   return render_template("index.html")


#Routing to the contact us

@app.route('/contact')
def contact():
   return render_template("contact.html")

@app.route('/contact1', methods=['GET', 'POST'])
def contact1():
    msg=""
    if request.method == 'POST':
        USERNAME = request.form['username']
        EMAIL = request.form['email']
        SUBJECT = request.form['subject']
        MESSAGE = request.form['message']

        
        query =("INSERT INTO contact (USERNAME ,EMAIL ,SUBJECT ,MESSAGE) VALUES (%s, %s, %s, %s)")  
        cursor.execute(query, (USERNAME,EMAIL,SUBJECT,MESSAGE))
        contact= conn.commit()
    
        return render_template('contact.html', msg="Thanks for filling in 12Fox!!")



if __name__ == "__main__":
   app.run(host='0.0.0.0',debug=True)