from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import declarative_base,sessionmaker
from flask import Flask,render_template,url_for,request,redirect,jsonify
Base = declarative_base()
class Student(Base):
    __tablename__ = 'students'
    id  = Column(Integer,primary_key=True)
    name = Column(String(50))
    age = Column(Integer)
engine = create_engine("mysql+mysqlconnector://root:abcd@localhost/students",echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('db.html')
@app.route('/students/create',methods=['GET','POST'])
def create():
    if request.method == 'POST':
        sid = request.form.get('sid')
        name = request.form.get('name')
        age = request.form.get('age')
        session = Session()
        s = Student(id=sid,name=name,age=age)
        session.add(s)
        session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')
@app.route('/students/get',methods=['GET'])
def get():
    session = Session()
    students = session.query(Student).all()
    return render_template('get.html', students=students)
@app.route('/students/update/<int:sid>',methods=['GET','POST'])
def update(sid):
    session = Session()
    s = session.get(Student,sid)
    if not s:
        return jsonify({'message':'Student not found'}),404
    if request.method=='POST':
        name = request.form.get('name')
        age = request.form.get('age')
        if name:
            s.name = name
        if age:
            s.age = age
        session.commit()
        return redirect(url_for('index'))
    return render_template('update.html',student = s)
@app.route('/students/delete/<int:sid>',methods=['GET'])
def delete(sid):
    session = Session()
    st = session.get(Student,sid)
    if not st:
        return jsonify({'message':'Student not found'}),404
    session.delete(st)
    session.commit()
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True)