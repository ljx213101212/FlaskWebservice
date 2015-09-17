from sqlalchemy import create_engine
from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import config
import sqlite3


Base = declarative_base()
#Base.metadata.create_all(bine=engine)

engine = create_engine(config.DATABASEURI)
metadata = MetaData(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()


'''
location
zone
estate
fax_no
objectid
sunday
longitude
telephone
sn
clinic
monday_friday
public_holiday
address_1
address_2
updatedat
latitude
postal
saturday
createdat
aviva_code
'''


# User class was only used for testing
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(120))

    def __init__(self, id,name=None, email=None):
        self.id = id
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)



class Clinic(Base):
    __tablename__ = 'clinic'
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(128))
    aviva_code =  Column(String(32))
    estate =  Column(String(64))
    address_1 =  Column(String(256))
    address_2 =  Column(String(256))
    postal =  Column(String(32))
    telephone =  Column(String(64))
    fax =  Column(String(64))
    latitude = Column(String(256))
    longtitude = Column(String(256))
    # for operating hours I just stored them as strings
    # you guys figure it out
    # weekday =  Column(String(256))
    # saturday =  Column(String(256))
    # sunday =  Column(String(256))
    # public_holiday = Column(String(256))
    # remarks =  Column(String(256))
    # foreign keys
    # this one here is for querying patients of a hospital
    
    patient_detail = relationship('PatientDetail', backref='clinic')
    doctors = relationship('Doctor', backref='doctors')


    def __init__(self,name="None", aviva_code="None",\
                 estate="None",address_1="None",address_2="None",\
                 postal="None",telephone="None",fax="None",\
                 latitude = "None", longitude="None"):

        self.name = name
        self.aviva_code = aviva_code
        # self.zone = zone
        self.estate = estate
        self.address1 = address_1
        self.address2 = address_2
        self.postal = postal
        self.telephone = telephone
        self.fax = fax
        # self.weekday = weekday
        # self.saturday = saturday
        # self.sunday = sunday
        # self.public_holiday = public_holiday
        # self.remarks = remarks
        self.latitude = latitude
        self.longtitude = longitude
        
    def __repr__(self):
        return '<Clinic %r>' % (self.name)
    


class Doctor(Base):
    __tablename__ = 'doctors'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    # current queue num is used to record the current queue status of
    # the doctor
    current_queue_num = Column(Integer)
    clinic_id = Column(Integer, ForeignKey('clinic.id'))   ## add some foreign key factor inside
    flag = Column(Integer)
    queue_id = relationship('Queue', backref='queue')

    def __init__(self, id, name=None,clinic_id=None,flag=0):
        self.id = id
        self.name = name
        self.clinic_id = clinic_id
        self.flag = flag

    def __repr__(self):
        return '<Doctor %r>' % (self.name)


class Queue(Base):
    __tablename__ = 'queue'
    id = Column(Integer, primary_key=True) # maximum 10,
    key = Column(String(50))
    uuid = Column(String(256))  ## only useful for mobile phones
    queue_number = Column(String(10))
    doctor_id = Column(Integer, ForeignKey('doctors.id'))
    patient_id = Column(Integer, ForeignKey('patient.patient_id'))
    clinic_id = Column(Integer,ForeignKey('clinic.id'))


    def __init__(self,key=None,uuid=None,clinic_id=None):
        self.key = key
        self.uuid = uuid
        self.clinic_id = clinic_id

    def __repr__(self):
        return '<Queue Number %r>' % (self.id)


class Patient(Base):
    __tablename__ = 'patient'
    patient_id = Column(Integer, primary_key=True)
    name = Column(String(64))
    detail = relationship('PatientDetail', backref='patient')
    insurance = relationship('Insurance', backref='insurance')
    queue = relationship('Queue', backref='patient')

    def __init__(self,name=None):
        self.name = name

    def __repr__(self):
        return '<Patient ID %r>' % (self.patient_id)


class PatientDetail(Base):
    __tablename__ = 'patient_detail'
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer,ForeignKey('patient.patient_id'))
    clinic_id = Column(Integer,ForeignKey('clinic.id'))     ### here you need a foreign key linking to the clinic
    ic_num = Column(String(32),unique=True)
    phone_num = Column(String(64))
    address_1 = Column(String(255))
    address_2 = Column(String(255))
    postal_code = Column(String(20))
    blood_group = Column(String(20))
    uuid = Column(String(64))




    def __init__(self, patient_id, clinic_id=None,ic_num=None, phone_num=None,address_1=None,address_2=None,\
        blood_group=None):
        self.patient_id = patient_id
        self.ic_num = ic_num
        self.phone_num = phone_num
        self.clinic_id = clinic_id
        self.address_1 = address_1
        self.address_2 = address_2
        self.blood_group = blood_group

    def __repr__(self):
        return '<Patient Detail of %r>' % (self.patient_id)



class Insurance(Base):
    __tablename__ = 'insurance'
    insurance_id = Column(Integer, primary_key=True)
    insurance_type = Column(String(64))
    patien_name =Column(String(10))
    patien_id = Column(Integer, ForeignKey('patient.patient_id'))

    def __init__(self, insurance_id, insurance_type=None, patient_name=None):
        self.insurance_id = insurance_id
        self.insurance_type = insurance_type
        self.patien_name = patient_name

    def __repr__(self):
        return '<Insurance of Patient %r>' % (self.patien_name)