# import mysql.connector
# db = mysql.connector.connect(host = "localhost",user = "root",passwd = "abcd",)
# cursor = db.cursor()
# cursor.execute("CREATE DATABASE students")
from sqlalchemy import create_engine,Column,String,Integer
from sqlalchemy.orm import declarative_base,sessionmaker
from flask import Flask,request,jsonify
Base = declarative_base()
class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer,primary_key=True)
    name = Column(String(50))
    age = Column(Integer)
engine = create_engine("mysql+mysqlconnector://root:abcd@localhost/students",echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
app=Flask(__name__)
@app.route('/')
def home():
    return "API is running."
@app.route('/api/students',methods=['POST'])
def create():
    data = request.get_json()
    session = Session()
    s1 = Student(name=data['name'],age=data['age'])
    session.add(s1)
    session.commit()
    return jsonify({'message':'Student created','id':s1.id})
@app.route('/api/students',methods=['GET'])
def select():
    session = Session()
    students = session.query(Student).all()
    return jsonify([{'id':s.id,'name':s.name,'age':s.age} for s in students])
@app.route('/api/students/<int:sid>',methods=['PUT'])
def update(sid):
    session = Session()
    data = request.get_json()
    stud = session.query(Student).get(sid)
    if not stud:
        return jsonify({'message':'Student not found'}),404
    stud.name = data.get('name',stud.name)
    stud.age = data.get('age',stud.age)
    session.commit()
    return jsonify({'message':'Updated'})
@app.route('/api/students/<int:sid>',methods=['DELETE'])
def delete(sid):
    session = Session()
    stud = session.get(Student,sid)
    if not stud:
        return jsonify({'message':'Student not found'}),404
    session.delete(stud)
    session.commit()
    return jsonify({'message':'Deleted'})
if __name__ == '__main__':
    app.run(debug=True)