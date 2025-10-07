# import os 'not utilized in local version'
# from dotenv import load_dotenv 'not utilized in local version'
# import psycopg ' not utilized in local version'
import sqlite3
# from datetime import datetime 'not utilized in local version'

from flask import Flask, request, session, jsonify, render_template, redirect, url_for
# from flask_mail import Mail, Message 'not implemented in local version'
from werkzeug.security import generate_password_hash, check_password_hash
# from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired 'not implemented in local version'

# load_dotenv() 'not implemented in local version'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'local_version'
# app.config['MAIL_SERVER'] = 'not implemented in local version'
# app.config['MAIL_PORT'] = 'not implemented in local version'
# app.config['MAIL_USE_TLS'] = 'not implemented in local version'
# app.config['MAIL_USERNAME'] = 'not implemented in local version'
# app.config['MAIL_PASSWORD'] = 'not implemented in local version'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
# mail = Mail(app)

# internal_url = 'not implemented in local version'
# external_url = 'not implemented in local version'

def generate_confirmation_token(email, secret_key):
    '''
    serializer = URLSafeTimedSerializer(secret_key)
    return serializer.dumps(email, 'email-confirmation-salt')
    '''
    print('Generate_confirmation_token not implemented in local version.')
    
def send_email_verify(email):
    '''
    first_confirmation = False

    with sqlite3.connect("users.db") as conn:
        cur = conn.cursor()
        cur.execute('SELECT last_confirmation_sent FROM users WHERE email = ?', (email,))
        row = cur.fetchone()

    # with psycopg.connect(external_url) as conn:
    #     with conn.cursor() as cur:
    #         cur.execute('SELECT last_confirmation_sent FROM users WHERE email = %s', (email,))
    #         row = cur.fetchone()

    if row and row[-1]:
        last_sent_time = row[0]
        current_time = datetime.now()
    elif row and not row[-1]:
        last_sent_time = datetime.now()
        current_time = datetime.now()
        first_confirmation = True
    else:
        return False

    if current_time.hour != last_sent_time.hour or current_time.date() != last_sent_time.date() or first_confirmation:
        return True
    else:
        return False
    '''
    print('Email sending not implemented in local version!')

def send_email(email, token):
    '''
    send = send_email_verify(email)

    if send:
        confirm_url = url_for('verify_email', email=email, token=token, _external=True)
        msg = Message(subject='Confirm your email',
                    sender=app.config['MAIL_USERNAME'],
                    recipients=[email],
                    body=f'Please confirm your email: {confirm_url}')
        mail.send(msg)

        time_sent = datetime.now()

        with sqlite3.connect('users.db') as conn:
            with conn.cursor() as curr:
                curr.execute('UPDATE users SET last_confirmation_sent = ? WHERE email = ?', (time_sent, email,))

        return True
    else:
        return False
    '''
    print('Email sending not implemented in local version!')
 
@app.route('/')
def index():
    return redirect(url_for('home')) 

@app.route('/register', methods=['GET', 'POST'])
def register():
    session.clear()
    if request.method == 'POST':
        data = request.get_json()
        email = data['email']
        password = data['password']
        hashed_password = generate_password_hash(password)

        # Check if email is in database 
        with sqlite3.connect('users.db') as conn:
            cur = conn.cursor()
            cur.execute('SELECT email FROM users WHERE email = ?', (email,))
            row = cur.fetchone()

            # If it is not insert it, Else if it is  return already registered
            if not row: 
                '''
                # Insert new user into database
                cur.execute('INSERT INTO users (email, password, confirmed) VALUES (?, ?, ?)', (email, hashed_password, 0,))
                conn.commit()

                # Verify email
                token = generate_confirmation_token(email, app.secret_key)
                if send_email(email, token):
                    return jsonify({"data": "Confirmation email sent."})
                else:
                    return jsonify({"data": "Confirmation email still active. Check your inbox and/or spam folder."})
                '''
                cur.execute('INSERT INTO users (email, password_hash, confirmed) VALUES (?, ?, ?)', (email, hashed_password, 1,))
                conn.commit()
                return jsonify({"data": "Email registered."})
            else:
                return jsonify({"data": "Email already registered. Please enter a new email."})

    return render_template('register.html')

@app.route('/verify/<email>/<token>')
def verify_email(email, token):
    '''
    # verify token
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        verified = serializer.loads(token, max_age=3600, salt='email-confirmation-salt')
    except SignatureExpired:
        verified = False
        # error = 'signature expired'
    except BadSignature:
        verified = False
        # error = 'bad signature'

    if verified:
        with sqlite3.connect('users.db') as conn:
            cur = conn.cursor()
            cur.execute('UPDATE users SET confirmed = 1 WHERE email = ?', (email,))
            cur.execute('SELECT id FROM users WHERE email = ?', (email,))
            id = cur.fetchone()[0]
        
        session['email'] = email
        session['user_id'] = id
        session['confirmed'] = 1

        return redirect(url_for('home'))
    else:
        if send_email(email, generate_confirmation_token(email, app.config['SECRET_KEY'])):
            return jsonify({"data": "Something went wrong. A new confirmation email was sent."})
        else:
            return jsonify({"data": "Something went wrong. Your confirmation email is still active. Check your inbox and/or spam folder and verify to login."})
    '''
    print('Verify email function is not implemented in local version.')
            
@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == 'POST':
        data = request.get_json()

        email = data['email']
        password = data['pass']

        # check if email is in users db
        with sqlite3.connect('users.db') as conn:
            cur = conn.cursor()
            cur.execute('SELECT id, password_hash, confirmed FROM users WHERE email = ?', (email,))
            user_info = cur.fetchone()

        # if not, prompt to enter email again
        if not user_info:
            return jsonify({"success": False, "notice": "Invalid email or password. Please try again."})

        # if it is, check that their password is valid
        passwords_match = check_password_hash(user_info[1], password)
        if not passwords_match:
            return jsonify({"success": False, "notice": "Invalid email or password. Please try again."})

        # confirm that account is verified. If not, resend confirmation email
        if user_info[2] != 1:
            if send_email(email, generate_confirmation_token(email, app.config['SECRET_KEY'])):
                return jsonify({"success": False, "notice": "You must verify your account before logging in. A confirmation email has been sent."})
            else:
                return jsonify({"success": False, "notice": "You must verify your account before logging in. An active confirmation email should still be in your inbox or spam folder."})

        # return according to if password was inputted successfully
        if passwords_match and user_info[2] == 1:
            session['user_id'] = user_info[0]
            session['email'] = email
            session['confirmed'] = 1
            return jsonify({"success": True, "redirect": url_for('home')})
        # if not, prompt them to enter password again
        else:
            return jsonify({"success": False, "notice": "Invalid email or password. Please try again."})
    
    return render_template('login.html')

@app.route('/home')
def home():
    if 'email' in session and session['confirmed'] == 1:
        return render_template('home.html')
    
    return redirect(url_for('login'))

@app.route('/load_accounts')
def load_accounts():
    with sqlite3.connect('users.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT account FROM passwords WHERE user_id = ? ORDER BY account ASC', (session['user_id'],))
        rows = cur.fetchall()

    accounts = []
    for row in rows:
        account = row[0]
        accounts.append(account)

    return accounts

@app.route('/get_account')
def get_account():
    account = request.args.get('account')

    with sqlite3.connect('users.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM passwords WHERE user_id = ? AND account = ?', (session['user_id'], account))
        account_info_tup = cur.fetchone()
        account_info = account_info_tup + ("",)

    if account_info:
        return jsonify({"arr": True, "info": account_info})
    else:
        return jsonify({"arr": False, "notice": "Account does not exist."})

@app.route('/add_account', methods=['POST'])
def add_account():    
    data = request.get_json()

    with sqlite3.connect('users.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM passwords WHERE account = ?', (data['account'],))
        account = cur.fetchone()

    if account:
        return jsonify({"success": False, "notice": "Account already exists."})
    else:
        with sqlite3.connect('users.db') as conn:
            cur = conn.cursor()
            cur.execute('INSERT INTO passwords (user_id, account, username, email, encrypted_password) VALUES (?, ?, ?, ?, ?)', (session['user_id'], data['account'], data['username'], data['email'], data['password']))
            conn.commit()

        return jsonify({"success": True})

if __name__ == '__main__':
    app.run(port=3000)