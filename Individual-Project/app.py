from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase



Config = {"apiKey": "AIzaSyDqR_yGSPt5ghxT3fN1g09IZhebDawjBMs",
  "authDomain": "layanproject-f01e1.firebaseapp.com",
  "projectId": "layanproject-f01e1",
  "storageBucket": "layanproject-f01e1.appspot.com",
  "messagingSenderId": "465695879242",
  "appId": "1:465695879242:web:f7dc800ae08b44c871b6b3",
  "measurementId": "G-C63W3J82KQ" ,
  "databaseURL": "https://layanproject-f01e1-default-rtdb.europe-west1.firebasedatabase.app/" }

firebase = pyrebase.initialize_app(Config)
auth = firebase.auth()
db =firebase.database()



app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def mainpage():
    return render_template("mainpage.html")


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error=""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_user_with_email_and_password(email,password)
            return redirect(url_for('mainpage.html'))
        except:
            error = "Authentication failed"
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error =""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user= {"email": request.form['email'],"password": request.form['password'], "phone": request.form['phonenumber']}
            login_session['user'] = auth.create_user_with_email_and_password(email,password)
            db.child("Users").child(login_session['user']['localId']).set(user)
            return redirect(url_for('mainpage'))
        except:
            error=error

    return render_template("signup.html")
    error=error



@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('mainpage'))

@app.route('/books')
def books(): 
    user =db.child("Users").child(login_session['user']['localId']).get().val()
    return render_template('books.html',user = user)

@app.route('/product', methods=['GET', 'POST'])
def product():

    users = db.child("Users").child(login_session['user']['localId']).get().val()

    return render_template("product.html",users=users, user = login_session['user'])

@app.route('/cart/<string:pic>')
def cart(pic):
    return render_template("cart.html", pic = pic)




if __name__ == "__main__":  
    app.run(debug=True) 