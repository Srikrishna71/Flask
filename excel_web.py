from flask import Flask,render_template,request
from excel import generate_row,generate_column
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('api.html')
@app.route('/download-row',methods=['POST'])
def download_excel_row():
    data={
        'email' : request.form['email'],
        'password' : request.form['password'],
        'emp_name' : request.form['emp_name'],
        'emp_id' : request.form['emp_id']
    }
    return generate_row(data)
@app.route('/download-column',methods=['POST'])
def download_excel_column():
    data={
        'email' : request.form['email'],
        'password' : request.form['password'],
        'emp_name' : request.form['emp_name'],
        'emp_id' : request.form['emp_id']
    }
    return generate_column(data)
if __name__ == "__main__":
    app.run(debug=True)