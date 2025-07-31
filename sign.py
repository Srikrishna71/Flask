from flask import Flask,request,render_template,redirect,url_for,session
import random
import string
app = Flask(__name__)
app.secret_key = 'my-very-secret-key'
otp_generated = {}
@app.route('/')
def index():
    return render_template('sign.html')
@app.route('/signin',methods=['POST'])
def signin():
    email = request.form.get('email')
    if email:
        otp = ''.join(random.choices(string.digits,k=6))
        otp_generated[email] = otp
        session['email'] = email
        return render_template('verify.html',otp=otp)
    return "Email is required",400
@app.route('/verify',methods=['GET','POST'])
def verify():
    if request.method == 'POST':
        input_otp = request.form.get('otp')
        email = session.get('email')
        if email and otp_generated.get(email) == input_otp:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        return "Invalid OTP",403
    return render_template('verify.html', otp=None)
@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    return "You are logged in successfully"
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True)