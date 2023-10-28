from crypt import methods
from flask import Flask,jsonify,request,Response
import json
from flask import request
from flask_restx import Api, Resource,fields, marshal, marshal_with, marshal_with_field
from flask_sqlalchemy import SQLAlchemy     #2
import os
from sqlalchemy import DateTime, ForeignKey

#from sqlalchemy import create_engine
import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref


from flask_marshmallow import Marshmallow

basedir = os.path.dirname(os.path.realpath(__file__))

#print(basedir)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'candidateprofiles.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SQLALCHEMY_ECHO']= True

ma = Marshmallow(app)

api = Api(app)

db = SQLAlchemy(app)
    

class Candidate(db.Model):
    #""" Candidate Model for storing candidate related details """
    #__tablename__ = "candidate"
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    name = db.Column(db.String(80),unique=True, nullable=False)
    qualification = db.Column(db.String(40),nullable=False)
    contact_number = db.Column(db.Integer,unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    skills= db.relationship('Skill', secondary= 'candidate_skill_map', backref='candidate')
    #skills= db.relationship('Skill', secondary= candidate_skill_map, backref='skill' , lazy=True)
    #skills= db.relationship('Skill', backref='candidate')

    created_at = db.Column(db.DateTime(timezone=True),server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True),onupdate=func.now(),server_default=func.now())
    #             
    def __repr__(self):         
        return  f'<Candidate "{self.name}">'

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    skill_name = db.Column(db.String(255),nullable=False, unique=True)

    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'))

    def __repr__(self):
        data= {'id':self.id,
               'skill_name':self.skill_name}
        result=json.dumps(data)
        lr = json.loads(result)
        return str(lr)
        #return str(result)

    # def __repr__(self):
    #     return self.skill_name

class Candidate_skill_map(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'))
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'))




# candidate_skill_map = db.Table('candidate_skill_map',
#         db.Column('id',db.Integer, primary_key=True),
#         db.Column('candidate_id',db.Integer, db.ForeignKey('candidate.id')),
#         db.Column('skill_id',db.Integer, db.ForeignKey('skill.id')))



#  1st(line).   
# export FLASK_APP=app.py   flask shell
#      2nd(line) flask shell
# next >>> db
#  Name,qualification,Contact imfor,email,skills,locations
# new_candidate=Candidate(name='rahul',qualification='be',contact_number=9663125721,email='rahul@gmail.com')
# db.session.add(new_candidate)
# >>db.session.commit()

# new_skill=Skill(skill_name='python',candidate_id=1)
# db.session.add(new_skill)

# map = candidate_skill_map(candidate_id=1,skill_id=1)
# db.session.add(map)

# db.session.commit()

# >>> from app import db,Candidate,Skill
# >>> new_candidate=Candidate(name='rahul',qualification='be',contact_number=9663125721,email='rahul@gmail.com')
# >>> new_skill=Skill(skill_name='python')
# >>> db.session.add_all([new_candidate,new_skill])
candidate_model = api.model(
                'Candidate',{
                            'id':fields.Integer(),
                            'name':fields.String(''),
                            'qualification':fields.String(''),
                            'contact_number':fields.Integer(),
                            'email': fields.String(''),
                            'skills':fields.String(''),

                            'created_at':fields.String(),
                            'updated_at':fields.String()
                            
                        })
candidate_post_model = api.model(
                'Candidate',{
                            'name':fields.String(''),
                            'qualification':fields.String(''),
                            'contact_number':fields.Integer(),
                            'email': fields.String('')})
                         
                        
skill_post_model = api.model(
                'Skills',{
                            'skill_name':fields.String(''),
                            'candidate_id': fields.Integer()})                        

skill_model2 = api.model(
                'Skill',{   'id': fields.Integer(),
                            'skill_name':fields.String('')}) 

@api.route('/candidates')
class Candidates(Resource):

    @api.marshal_with(candidate_model,envelope='candidates')
    def get(self):
        '''List all candidates'''
    
        candidates = Candidate.query.all()
        # print('--------------------',candidates)
        # candidates.forEach((val)=>{
        #    print('--------------------',candidates) 
        # })
        return candidates

    @api.expect(candidate_post_model,envelope='candidate')
    def post(self):
        ''' Create a candidate '''
        data=request.get_json()
        name=data.get('name')
        qualification=data.get('qualification')
        contact_number=data.get('contact_number')
        email=data.get('email')
        new_candidate=Candidate(name=name,qualification=qualification,
                                contact_number=contact_number,email=email)
        db.session.add(new_candidate)
        db.session.commit()
        return {'result' : 'candidate added'}, 201      #201(Created)
  

@api.route('/skills')
class Skills(Resource):   

    @api.marshal_with(skill_model2,envelope='skills')
    def get(self):
        '''List all the Skills'''
        skill=Skill.query.all()
        return skill


    @api.expect(skill_post_model,envelope='skill')
    def post(self):
        ''' Add a skills '''
        data=request.get_json()
        skill_name=data.get('skill_name')
        candidate_id=data.get('candidate_id')

        new_skill=Skill(skill_name =skill_name ,candidate_id=candidate_id)
        db.session.add(new_skill)
        db.session.commit()
        return {'result' : 'skill added'}, 201     #201(Created)



@api.route('/candidates/<int:id>')
@api.response(404, 'id is not found.')
class CandidateResource(Resource):

    @api.marshal_with(candidate_model,envelope="candidate")
    def get(self,id):

        ''' Get a candidate by id '''
        candidate=Candidate.query.get(id)
        
            
      
        if not candidate:
            response_object = {
                                'status': 'fail',
                                'message': 'id is not exists.'}
            return response_object, 404
    
        else:   
            return candidate

    @api.expect(candidate_post_model,envelope='candidate')
    def put(self,id):
        ''' Update a candidate'''
        candidate_to_update=Candidate.query.get(id)
        data = request.get_json()

        candidate_to_update.name=data.get('name')
        candidate_to_update.qualification=data.get('qualification')
        candidate_to_update.contact_number=data.get('contact_number')
        candidate_to_update.email=data.get('email')
        #candidate_to_update.skills=data.get('skills')
        
        db.session.commit()
        return {'result' : 'candidate is updated'} 

    @api.marshal_with(candidate_model,envelope="candidate_deleted")
    def delete(self,id):
        '''Delete a candidate'''
        candidate_to_delete=Candidate.query.get(id)

        db.session.delete(candidate_to_delete)

        db.session.commit()

        return {'result' : 'candidate is deleted'}   


# @app.route('/candidate',methods=['GET'])
# #@api.marshal_with(candidate_model,envelope='candidate')
# def get():
#     cqualification=request.args.get("qualification")
#     cskills=request.args.get("cskills")
#     data = db.session.query(Candidate).filter((Candidate.qualification==cqualification) and (Candidate.skills==cskills))   #wk

#     #print('data ',data)
#     result = candidateSchema.dump(data)
#     return jsonify(result)




@app.route("/candidates/skills")
@api.marshal_with(candidate_model,envelope='candidate')
def getcandidate():
    skill = request.args.get("skill")
    query = db.session.query(Candidate).join(Skill).filter(Candidate.id==Skill.candidate_id).filter(Skill.skill_name==skill).all()
    return  query


class CandidateSchema(ma.Schema):
    class Meta:
        fields = ('id', "name", 'qualification', 'contact_number', 'email', 'skills', 'created_at', "updated_at")
candidateSchema = CandidateSchema()
candidateSchema = CandidateSchema(many=True)




if __name__ == '__main__':
    app.run(debug= True)




