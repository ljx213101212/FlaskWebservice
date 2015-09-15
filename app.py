from flask import Flask
from flask import render_template
from flask import request
from flask import url_for, redirect
from database import *
import flask
import time
import models.queue_api as qapi
import models.registration as registration
import models.gcm_li as gcm_li
import models.route_api as rapi
from models.registration import *
import json
from sqlalchemy import update

import sys
sys.path.insert(0, '/Users/jixiang/Documents/ISS/SEProject/www/DocHeroku2/controller')




current_milli_time = lambda: int(round(time.time() * 1000))
def make_app():
    app = Flask(__name__)
    app.config.from_object('config')
    return app

app = make_app()


@app.route('/')
def hello_world():
    return render_template('index.html')
    #return qapi.testmodel()
    # tested how to write functions in models lol
    # but I'm not sure whether it is the right way
    #return a

@app.route('/queryall')
def queryall():
    clinics = session.query(Clinic).order_by(Clinic.id.desc())
    res = []
    for clinic in clinics:
        result = {}
        #print clinic.__dict__
        for i in clinic.__dict__:
            print clinic.__dict__[i]
            if i[0] == '_':
                continue
            else:
                result[i] = clinic.__dict__[i]
        res.append(result)
                
    r = {}
    r['result'] = res

    return flask.jsonify(**r)


#
@app.route('/querybykilo',methods=['GET'])
def querybykilo():
    print request.args.get('src_lat')
    print request.args.get('src_lng')
    print request.args.get('kilo')
    src_lat = request.args.get('src_lat')
    src_lng = request.args.get('src_lng')
    kilo = request.args.get('kilo')

    if 'src_lat' not in request.args:
        result["error"] = "give me src_lat"
        return flask.jsonify(**result)
    if 'src_lng' not in request.args:
        result["error"] = "give me src_lng"
        return flask.jsonify(**result)
    if 'kilo' not in request.args:
        result["error"] = "give me kilo"
        return flask.jsonify(**result)

    clinics = session.query(Clinic).order_by(Clinic.id.desc())
    res = []
    counter = 0
    for clinic in clinics:
        result = {}
        if clinic.latitude and clinic.longtitude:
            if not rapi.isWithNKilometers(src_lat,src_lng,kilo,clinic.latitude,clinic.longtitude):
                continue
            else:
                counter+=1
                print clinic.name
                for i in clinic.__dict__:
                    #print clinic.__dict__[i]
                    if i[0] == '_':
                        continue
                    else:
                        result[i] = clinic.__dict__[i]
                res.append(result)
    
    print counter        
    r = {}
    r['result'] = res

    return flask.jsonify(**r)
    


@app.route('/testpost',methods=["POST"])
def testPost():
    data = request.get_json()
    print data
    #print data["id"]
    return "SUCCESS"


@app.route('/createClinic',methods=["POST"])
def createClinic():
    ## this one is dangerous, cause there should at least be some management part for the id management
    ## this one assume that you already have an exclusive ID
    ## in the new version you don't have to care about the ID number anymore cause it
    ## can auto increment
    data = request.form
    if not data:
        return "No data!"
 
    # params = ['name', 'aviva_code',\
    #              'zone', 'estate','address1','address2',\
    #              'postal','telephone','fax','weekday',\
    #              'saturday','sunday','public_holiday','remarks','latitude','longitude']
    clinic = Clinic()
    if 'name' in data:
        clinic.name = data['name']
    if 'address_1' in data:
        clinic.address_1 = data['address_1']
    if 'address_2' in data:
        clinic.address_2 = data['address_2']
    print data
    print clinic
    session.add(clinic)
    session.commit()

    return "SUCCESS"




@app.route('/update',methods=["POST"])
def updateById():
    # this one should be post
    # first this function is gonna support address 1 and address 2 and name update
    if not request.form:
        return "No Data!"
    data = request.form
    if 'id' not in data:
        return "Specify ID!"

    a = session.query(Clinic).filter_by(id=data['id']).first()

    if 'name' in data:
        a.name = data['name']
    if 'address_1' in data:
        a.address_1 = data['address_1']
    if 'address_2' in data:
        a.address_2 = data['address_2']
    # ## if you want to add more simply add here
    # session.add(a)

    session.commit()
    return "SUCCESS"


@app.route('/deleteById/<iden>')
def deleteById(iden):
    c = session.query(Clinic).filter_by(id=iden).first()
    if c == None:
        return "No Clinic with Id Found!"
    session.delete(c)
    session.commit()
    return "success"
    
    

@app.route('/queryById/<iden>')
def queryById(iden):
    print iden
    #r = Clinic.
    r = session.query(Clinic).filter_by(id=iden).first()
    result = {}
    print r.__dict__
    for i in r.__dict__:
        print i
        if i[0] == '_':
            continue
        else:
            result[i] = r.__dict__[i]
            
    return flask.jsonify(**result)

@app.route('/testquery')
def testQuery():

    a = session.query(User).all()
    if len(a)==0:
        return "nothing"
    print a[0].__dict__
    print a[0].name
    res = {}
    for i in a[0].__dict__:
        if i[0]=="_":
            continue
        res[i] = a[0].__dict__[i]
    
    """
    print a.id
    print a.name
    print a.email
    """
    return flask.jsonify(**res)


@app.route('/queue',methods=["POST"])
def queue():

    data = request.get_json()
    print data
    result = {}
    if 'reg_id' in data:
        result["reg_id"] = data['reg_id']

    if 'uuid' not in data:
        result["error"] = "give me uuid!"
        return flask.jsonify(**result)
    if 'clinic_name' not in data:
        result["error"] = "give me clinic name!"
        return flask.jsonify(**result)
    if 'fin_no' not in data:
        result["error"] = "give me fin number!"
        return flask.jsonify(**result)

    #print data

    # q = session.query(Queue).filter_by(uuid=data['uuid']).first()
    # if q is not None:

    #     result["key"] = q.key
    #     result["queue_num"] = q.queue_number
    #     d = session.query(Doctor).filter_by(id=q.doctor_id).first()
    #     result["doctor"] = d.name

    #     #json = flask.jsonify(**result)
    #     # if "reg_id" not in data:
    #     #     result['error'] = "at least tell me the reg_id"
        
    #     print "**********"
    #     if 'reg_id' in data:
    #        gcm_li.gcm_li(data['reg_id'],result)
    #     print "990090902930912093012"
    #     return flask.jsonify(**result)
        #return flask.jsonify(**result)

        #return "uuid already exist!"
    c = session.query(Clinic).filter_by(name=data['clinic_name']).first()
    if not c:
        result["error"] =  "clinic name does not exsit!"
        return flask.jsonify(**result)

    result = qapi.generate_queue_li(data['clinic_name'],data['uuid'],data['fin_no'])
    #result = qapi.generate_queue(data['clinic_name'],data['uuid'])  
    # json = flask.jsonify(**result)
    # if "reg_id" not in data:
    #     result['error'] = "at least tell me the reg_id"
        
    print "------------"
    if 'reg_id' in data:
        print "######reg_id###$$$--->"+data['reg_id']
        gcm_li.gcm_li(data['reg_id'],result)
    return flask.jsonify(**result)
    #return "tetett"

    #curl --data "uuid=test&clinic_name=test&fin_no=test" http://10.10.2.223:5000/queue


@app.route('/registration',methods=['POST'])
def registration():
    # this version of registration does not contain
    # shit the fucking meeting made me forget about what
    # I want to write
    data = request.get_json()
    result = ""
    if "name" not in data:
        result['error'] = "at least tell me your name!"
        return flask.jsonify(**result)
    if "ic_num" not in data:
        result['error'] = "at least tell me your IC number!"
        return flask.jsonify(**result)
    if "clinic_name" not in data:
        result['error'] = "at least tell me the clinic_name"
        return flask.jsonify(**result)
    if "patient_phone" not in data:
        result['error'] = "at least tell me the patient_phone"
        return flask.jsonify(**result)

    #result = register_li(data['name'],data['clinic_name'],data['ic_num'],data['patient_phone'])
    result = register_li_2(data)

    return result


@app.route('/queue_reg',methods=['POST'])
def queue_reg():
    
    data = request.args['messages']
    result = data

    if "reg_id" not in data:
        result['error'] = "at least tell me the reg_id"

    print "**********"
    gcm_li.gcm_li(data['reg_id'],result)
    return flask.jsonify(**result)
    





# @app.route('/registerdata',methods = ['POST'])
# def registData():
#     # modification for registration


#     return "SUCCESS"



# @app.route('/QNAuth',methods=["POST"])
# def qnauth():
#     data = request.form
#     a = session.query(Queue).filter_by(id=data['id']).first()
#     if not a:
#         return "ID Does Not Exist!"
#     elif a.key == data['key']:
#         return "success"

#     return "Auth Failed"
    
if __name__ == '__main__':
    app.run(host='0.0.0.0')
