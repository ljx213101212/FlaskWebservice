__author__ = 'andypan'
# this script is only used for the initiation of the database.
# after the database is initiated there will have to some cases in the database to be tested.
from database import *

print "Start Initiation of Database Schema"
print "Adding cases into the database"


Base.metadata.create_all(bind=engine)

# from database import *
# c = session.query(Clinic).filter_by(id=1).first()

'''
# already done
doc1 = Doctor(id=1)
doc1.name= "Andy"
c.doctors.append(doc1)
session.add(doc1)
'''
#session.commit()

