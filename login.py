from flask import Flask, render_template, request, jsonify, g
import jwt
from datetime import datetime,timedelta,timezone
from functools import wraps

app = Flask(__name__)
secret_key = 'my-very-secret-key'
jwt_expiry = 30
users = {}

def generate_token(username):
    payload = {
        'user_id' : username,
        'exp' : datetime.now(timezone.utc) + timedelta(minutes=jwt_expiry)
    }
    token = jwt.encode(payload,secret_key,algorithm='HS256')
    return token
def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization',None)
        if not token:
            return jsonify({'success': False, 'message': 'Token is missing'}), 401
        try:
            decoded = jwt.decode(token, secret_key, algorithms=['HS256'])
            g.user_id = decoded['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'success': False, 'message': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'success': False, 'message': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def login_page():
    return render_template('login.html')
@app.route('/register')
def register_page():
    return render_template('register.html')
@app.route('/forgot')
def forgot_page():
    return render_template('forgot.html')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'success': False, 'message': 'All fields are required'})
    if username not in users or users[username] != password:
        return jsonify({'success': False, 'message': 'Invalid username or password'})
    token = generate_token(username)
    return jsonify({'success': True, 'token' : token})
@app.route('/register-user', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    confirm = data.get('confirm')
    if not username or not password or not confirm:
        return jsonify({'success': False, 'message': 'All fields are required'})
    if password != confirm:
        return jsonify({'success': False, 'message': 'Passwords do not match'})
    if len(password) < 8:
        return jsonify({'success': False, 'message': 'Password must be at least 8 characters long'})
    if username in users:
        return jsonify({'success': False, 'message': 'User already exists'})
    users[username] = password
    return jsonify({'success': True, 'message': 'Registration successful'})
@app.route('/forgot-send', methods=['POST'])
def forgot():
    data = request.json
    username = data.get('username')
    if not username:
        return jsonify({'success': False, 'message': 'Email is required'})
    if username not in users:
        return jsonify({'success': False, 'message': 'Email not found'})
    return jsonify({'success': True, 'message': 'Password reset link sent to your email'})

if __name__ == '__main__':
    app.run(debug=True)