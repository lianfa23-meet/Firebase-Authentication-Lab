from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase


firebaseConfig = {
  'apiKey': "AIzaSyBL4mdrq-C5NG1o4Bws1S_Vzi0soNGD_ec",
  'authDomain': "fir-lab1-efb11.firebaseapp.com",
  'projectId': "fir-lab1-efb11",
  'storageBucket': "fir-lab1-efb11.appspot.com",
  'messagingSenderId': "206261278642",
  'appId': "1:206261278642:web:fced1ba71bfbb2df54b6ab",
  'measurementId': "G-L2HQFSQ76Q",
  "databaseURL": ""

}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    error=''
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, pwd)
            return render_template('add_tweet.html')
        except:
            error = 'Authentication failed'
            print(error)
            print(login_session['user'])
            return render_template('signin.html')
    else:
        return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['password']
        
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, pwd)

            return render_template('signin.html')
        except:
            error = 'Authentication failed'
            return render_template("signup.html")
    else:
        return render_template("signup.html")

@app.route('/logout')
def logout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")


if __name__ == '__main__':
    app.run(debug=True)