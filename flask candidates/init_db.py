from app import db, Candidate, Skill  ,Candidate_skill_map
# db.drop_all()
# db.create_all()

#candidate1 = Candidate(name='rahul',qualification='be',contact_number=9663125721,email='rahul@gmail.com')
#candidate2 = Candidate(name='pavan',qualification='bca',contact_number=9663125722,email='pavan@gmail.com')
# candidate2 = Candidate(name='nikil',qualification='be',contact_number=9663125723,email='nikil@gmail.com')

skill1 = Skill(skill_name='reactjs', candidate_id=3)
# skill2 = Skill(skill_name='css')
# skill3 = Skill(skill_name='javascript')

# # # # skill3 = Skill(skill_name='javascript')
# # # #skill1 = Skill(skills='python',candidate_id=1)
# # # #skill2 = Skill(skills='flask',candidate_id=4)

candidate_skill_map1 = Candidate_skill_map(candidate_id =3 , skill_id = 8)
# # # # candidate_skill_map2 = Candidate_skill_map(candidate_id = 2, skill_id = 4)

# # # #skill1.candidate.append(candidate1)
# # # # skill2.candidates.append(candidate2)
# # # # skill3.candidates.append(candidate2)

# # # # db.session.add(skill1)
# # # # db.session.add_all([skill1,skill2,skill3])
# # # # db.session.commit()


# db.session.add(candidate2)
db.session.add(skill1)

db.session.add(candidate_skill_map1)

db.session.commit()



