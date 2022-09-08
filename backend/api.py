# INITIALISE DATABASE AND CREATE CONNECTION
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# initialise flask app
app = Flask(__name__)

# gets the directory of our app
basedir = os.path.abspath(os.path.dirname(__file__))
# set the path to the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + 'db.sqlite'
# required to stop some warnings in the console
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# initialise SQL Alchemy
db = SQLAlchemy(app)
# initialise Marshmallow
ma = Marshmallow(app)

# creates the database model for the table
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    course_type = db.Column(db.String(100))
    teacher_info = db.Column(db.String(100))
    requirements = db.Column(db.String(100))
    ucas_points = db.Column(db.String(100))
    topics = db.Column(db.String(100))
    course_description = db.Column(db.String(1000))
    testimonials = db.Column(db.String(500))
    exam_details = db.Column(db.String(100))
    image = db.Column(db.String(1000))
    key_ribbon = db.Column(db.String(20))

    def __init__(self, Title, CourseType, TeacherInfo, Requirements, UCASPoints, Topics, CourseDescription, Testimonials, ExamDetails, Image, KeyRibbon) -> None:
        self.title = Title
        self.course_type = CourseType
        self.teacher_info = TeacherInfo
        self.requirements = Requirements
        self.ucas_points = UCASPoints
        self.topics = Topics
        self.course_description = CourseDescription
        self.testimonials = Testimonials
        self.exam_details = ExamDetails
        self.image = Image
        self.key_ribbon = KeyRibbon

class SubjectSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'course_type', 'teacher_info', 'requirements', 'ucas_points', 'topics', 'course_description', 'testimonials', 'exam_details', 'image', 'key_ribbon')

# creates an instance of the schema
subject_schema = SubjectSchema()  # single person
subjects_schema = SubjectSchema(many=True)  # people

#C.R.U.D operations for API
#Creates a new person in the database
@app.route('/Subjects', methods=['POST'])
def add_subject():
    Title = request.json['title']
    CourseType = request.json['course_type']
    TeacherInfo = request.json['teacher_info']
    Requirements = request.json['requirements']
    UCASPoints = request.json['ucas_points']
    Topics = request.json['topics']
    CourseDescription = request.json['course_description']
    Testimonials = request.json['testimonials']
    ExamDetails = request.json['exam_details']
    Image = request.json['image']
    KeyRibbon = request.json['key_ribbon']

    new_subject = Subject(Title, CourseType, TeacherInfo, Requirements, UCASPoints, Topics, CourseDescription, Testimonials, ExamDetails, Image, KeyRibbon)
    db.session.add(new_subject)
    db.session.commit()

    return subject_schema.jsonify(new_subject)

#Gets all people in the database
@app.route('/Subjects', methods=['GET'])
def get_subjects():
    all_subject = Subject.query.all()
    result = subjects_schema.dump(all_subject)
    return jsonify(result)

#Gets a single person by ID
@app.route('/Subjects/<id>', methods=['GET'])
def get_subject(id):
    subject = Subject.query.get(id)
    return subject_schema.jsonify(subject)

#Updates a person with the ID
@app.route('/Subjects/<id>', methods=['PUT'])
def update_subject(id):
    subject = Subject.query.get(id)
    Title = request.json['title']
    CourseType = request.json['course_type']
    TeacherInfo = request.json['teacher_info']
    Requirements = request.json['requirements']
    UCASPoints = request.json['ucas_points']
    Topics = request.json['topics']
    CourseDescription = request.json['course_description']
    Testimonials = request.json['testimonials']
    ExamDetails = request.json['exam_details']
    Image = request.json['image']
    KeyRibbon = request.json['key_ribbon']

    subject.title = Title
    subject.course_type = CourseType
    subject.teacher_info = TeacherInfo
    subject.requirements = Requirements
    subject.ucas_points = UCASPoints
    subject.topics = Topics
    subject.course_description = CourseDescription
    subject.testimonials = Testimonials
    subject.exam_details = ExamDetails
    subject.image = Image
    subject.key_ribbon = KeyRibbon

    db.session.commit()
    return subject.jsonify(subject)

#Deletes the person with the ID
@app.route('/Subjects/<id>', methods=['DELETE'])
def delete_subject(id):
    subject = Subject.query.get(id)
    db.session.delete(subject)
    db.session.commit()
    return subject_schema.jsonify(subject)

db.create_all()
if __name__ =="__main__":
    app.run(debug=True)