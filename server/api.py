# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 17:56:30 2020

@author: user
"""

import pymysql
import jwt
import datetime
import requests
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request, session, make_response, render_template, Response
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_cors import CORS

from werkzeug.utils import secure_filename
import os
import jsonpickle
import numpy as np
import cv2
# importing files named ocr extractpdf
import ocr as ocr  # not a python package.
import extractpdf as extractpdf  # not a python package.
import jobs as job  # not a python package.

import resumes as resume  # not a python package.
import resume_edu as r_edu  # not a python package.
import resume_work as r_work  # not a python package.
import resume_skills as r_skills  # not a python package.
import resume_projects as r_projects  # not a python package.
import resume_trainings as r_trainings  # not a python package.
import resume_wexp as r_wexp  # not a python package.
import resume_fetch as getresume  # not a python package.

import user_apis as user_side
import admin_api as ad_api
import no_auth_apis as no_auth
import courses as courses
import recommendation as recommend
import resumeocr as rocr
CORS(app)


# Fetch input fields Locations title


@app.route('/locationsfield')
def locations():
    response = no_auth.locations()
    return response


@app.route('/titlesfield')
def titles():
    response = no_auth.titles()
    return response

# Fetch All Courses


@app.route('/allcourses', methods=['POST'])
def all_courses():
    response = no_auth.all_courses()
    return response


# Fetch All Skills
@app.route('/allskills', methods=['POST'])
def all_skills():
    response = no_auth.all_skills()
    return response

# Fetch jobs


@app.route('/fetch-jobs', methods=['POST'])
def fetch_jobs():
    response = no_auth.fetch_jobs()
    return response


@app.route('/latestjobs')
def latestjobs():
    response = no_auth.latest_jobs()
    return response
# USER SIDE REQUESTS.


def check_for_token(param):
    @wraps(param)
    def wrapped(*args, **kwargs):
        token = ''
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        # token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Missing Token'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            # can use this data to fetch current user with contact number encoded in token
        except:
            return jsonify({'message': 'Invalid Token'}), 403
        return param(*args, **kwargs)
    return wrapped


# Get current active user
@app.route('/user')
@check_for_token
def user():
    token = request.headers['Authorization']
    username = jwt.decode(token, app.config['SECRET_KEY'])
    response = user_side.user(username)
    return response


@app.route('/login', methods=['POST'])
def login():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if(request.json['type'] == 0):
        cur.execute("Select * from users Where phone_no = " +
                    str(request.json['contact'])+";")
        rows = cur.rowcount
        records = cur.fetchall()
        if rows != 0:
            for data in records:
                token = jwt.encode({'number': request.json['contact'], 'user_id': data["user_id"],  'exp': datetime.datetime.utcnow(
                ) + datetime.timedelta(minutes=120)}, app.config['SECRET_KEY'])
                print(token.decode('utf-8'))
                resp = jsonify({'token': token.decode('utf-8')})
                resp.status_code = 200
                return resp
        else:
            resp = jsonify({'message': 'ERROR Occured.'})
            resp.status_code = 401
            return resp
        cur.close()
        conn.close()
    elif (request.json['type'] == 1):
        cur.execute("Select user_id,passw from users Where phone_no = " +
                    str(request.json['contact'])+";")
        records = cur.fetchall()
        for row in records:
            if check_password_hash(row["passw"], request.json['password']):
                token = jwt.encode({'number': request.json['contact'],  'user_id': row["user_id"], 'exp': datetime.datetime.utcnow(
                ) + datetime.timedelta(minutes=120)}, app.config['SECRET_KEY'])
                print(token.decode('utf-8'))
                resp = jsonify({'token': token.decode('utf-8')})
                resp.status_code = 200
                return resp
            else:
                resp = jsonify({'message': 'ERROR Occured.'})
                resp.status_code = 401
                return resp
            cur.close()
            conn.close()
    else:
        resp = jsonify({'message': 'ERROR.'})
        return resp


@app.route('/register', methods=['POST'])
def register():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    try:
        check = cur.execute("SELECT  phone_no FROM users WHERE ( email = '"+str(
            request.json['email'])+"' AND phone_no = '"+str(request.json['contact'])+"');")
        if check:
            resp = jsonify({'message': 'User already Exists!!'})
            resp.status_code = 300  # invalid
            return resp
        else:
            cur.execute("Insert into users(email,lname,fname,passw,is_verified,phone_no) VALUES ('"+str(request.json['email'])+"','"+str(
                request.json['lname'])+"','"+str(request.json['fname'])+"','"+generate_password_hash(str(request.json['passw']))
                + "',1,'"+str(request.json['contact'])+"');")
            conn.commit()
            if cur:
                resp = jsonify({'message': 'success'})
                resp.status_code = 200
                return resp
            resp = jsonify({'message': 'Error.'})
            resp.status_code = 401
            return resp
    finally:
        cur.close()
        conn.close()


@app.route('/resume-details', methods=['POST'])
# @check_for_token
def get_resume():
    token = request.headers['Authorization']
    username = jwt.decode(token, app.config['SECRET_KEY'])
    if(request.json['want'] == "personaldetails"):
        results = getresume.fetch_pd(username)
        return results
    elif(request.json['want'] == "edu_details"):
        results = getresume.fetch_edu(username)
        if len(results) != 0:
            resp = jsonify({'output': results})
            return resp
    elif(request.json['want'] == "job_details"):
        results = getresume.fetch_jobs(username)
        if len(results) != 0:
            resp = jsonify({'output': results})
            return resp
    elif(request.json['want'] == "projects_lists"):
        results = getresume.fetch_projects(username)
        if len(results) != 0:
            resp = jsonify({'output': results})
            return resp
    elif(request.json['want'] == "skills_list"):
        results = getresume.fetch_skills(username)
        if len(results) != 0:
            resp = jsonify({'output': results})
            return resp
    elif(request.json['want'] == "trainings_list"):
        results = getresume.fetch_trainings(username)
        if len(results) != 0:
            resp = jsonify({'output': results})
            return resp
    elif(request.json['want'] == "work_examples"):
        results = getresume.fetch_wexamples(username)
        return results
    elif(request.json['want'] == "everything"):
        resp = getresume.fetch_all(username)
        return resp
    else:
        resp = jsonify({'message': 'Invalid Request.'})
        return resp


@app.route('/resume', methods=['POST'])
@check_for_token
def cud_resume():
    token = request.headers['Authorization']
    username = jwt.decode(token, app.config['SECRET_KEY'])
    if(request.json['mode'] == "add"):
        resp = resume.create_resume(username)
        return resp
    elif(request.json['mode'] == "delete"):
        resp = resume.delete_resume(username)
        return resp
    elif(request.json['mode'] == "update"):
        resp = resume.update_resume(username)
        return resp
    else:
        resp = jsonify({'message': 'Invalid Request.'})
        return resp


@app.route('/resume-edu', methods=['POST'])
@check_for_token
def cud_resume_edu():
    token = request.headers['Authorization']
    username = jwt.decode(token, app.config['SECRET_KEY'])
    if(request.json['mode'] == "add"):
        resp = r_edu.create_resume_edu(username)
        return resp
    elif(request.json['mode'] == "delete"):
        resp = r_edu.delete_resume_edu(username)
        return resp
    elif(request.json['mode'] == "update"):
        resp = r_edu.update_resume_edu(username)
        return resp
    else:
        resp = jsonify({'message': 'Invalid Request.'})
        return resp


@app.route('/resume-work', methods=['POST'])
@check_for_token
def cud_resume_work():
    token = request.headers['Authorization']
    username = jwt.decode(token, app.config['SECRET_KEY'])
    if(request.json['mode'] == "add"):
        resp = r_work.create_resume_w(username)
        return resp
    elif(request.json['mode'] == "delete"):
        resp = r_work.delete_resume_w(username)
        return resp
    elif(request.json['mode'] == "update"):
        resp = r_work.update_resume_w(username)
        return resp
    else:
        resp = jsonify({'message': 'Invalid Request.'})
        return resp


@app.route('/resume-trainings', methods=['POST'])
@check_for_token
def cud_resume_trainings():
    token = request.headers['Authorization']
    username = jwt.decode(token, app.config['SECRET_KEY'])
    if(request.json['mode'] == "add"):
        resp = r_trainings.create_resume_trainings(username)
        return resp
    elif(request.json['mode'] == "delete"):
        resp = r_trainings.delete_resume_trainings(username)
        return resp
    elif(request.json['mode'] == "update"):
        resp = r_trainings.update_resume_trainings(username)
        return resp
    else:
        resp = jsonify({'message': 'Invalid Request.'})
        return resp


@app.route('/resume-workexp', methods=['POST'])
@check_for_token
def cud_resume_workexp():
    token = request.headers['Authorization']
    username = jwt.decode(token, app.config['SECRET_KEY'])
    if(request.json['mode'] == "add"):
        resp = r_wexp.create_resume_job_details(username)
        return resp
    elif(request.json['mode'] == "delete"):
        resp = r_wexp.delete_resume_job_details(username)
        return resp
    elif(request.json['mode'] == "update"):
        resp = r_wexp.update_resume_job_details(username)
        return resp
    else:
        resp = jsonify({'message': 'Invalid Request.'})
        return resp


@app.route('/resume-skills', methods=['POST'])
@check_for_token
def cud_resume_skills():
    token = request.headers['Authorization']
    username = jwt.decode(token, app.config['SECRET_KEY'])
    if(request.json['mode'] == "add"):
        resp = r_skills.create_resume_skills(username)
        return resp
    elif(request.json['mode'] == "delete"):
        resp = r_skills.delete_resume_skills(username)
        return resp
    elif(request.json['mode'] == "update"):
        resp = r_skills.update_resume_skills(username)
        return resp
    else:
        resp = jsonify({'message': 'Invalid Request.'})
        return resp


@app.route('/resume-projects', methods=['POST'])
@check_for_token
def cud_resume_projects():
    token = request.headers['Authorization']
    username = jwt.decode(token, app.config['SECRET_KEY'])
    if(request.json['mode'] == "add"):
        resp = r_projects.create_resume_projects(username)
        return resp
    elif(request.json['mode'] == "delete"):
        resp = r_projects.delete_resume_projects(username)
        return resp
    elif(request.json['mode'] == "update"):
        resp = r_projects.update_resume_projects(username)
        return resp
    else:
        resp = jsonify({'message': 'Invalid Request.'})
        return resp

# enroll courses & jobs


@app.route('/enroll-course', methods=['POST'])
@check_for_token
def enroll_courses():
    token = request.headers['Authorization']
    username = jwt.decode(token, app.config['SECRET_KEY'])
    response = user_side.enroll_courses(username)
    return response


@app.route('/enroll-job', methods=['POST'])
@check_for_token
def enroll_jobs():
    token = request.headers['Authorization']
    username = jwt.decode(token, app.config['SECRET_KEY'])
    response = user_side.enroll_jobs(username)
    return response


# Get active user's applied jobs
@app.route('/user-applied-jobs')
@check_for_token
def user_applied_jobs():
    token = request.headers['Authorization']
    username = jwt.decode(token, app.config['SECRET_KEY'])
    response = user_side.applied_jobs(username)
    return response


# Get active user's enrolled courses
@app.route('/user-enrolled-courses')
@check_for_token
def user_enrolled_courses():
    token = request.headers['Authorization']
    username = jwt.decode(token, app.config['SECRET_KEY'])
    response = user_side.my_courses(username)
    return response

# Courses Recommendtaions


@app.route('/recommendations', methods=['POST'])
@check_for_token
def recommendations():
    token = request.headers['Authorization']
    username = jwt.decode(token, app.config['SECRET_KEY'])

    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur2 = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT skill_id,level FROM resume_skills WHERE user_id = " +
                str(username['user_id'])+" ;")

    skill_list = []
    category_list = []
    level_list = []
    for r in cur:
        level_list.append(r['level'])
        cur2.execute("SELECT title,category FROM skills WHERE skill_id ='" +
                     str(r['skill_id'])+"';")
        records2 = cur2.fetchone()
        skill_list.append(records2['title'])
        category_list.append(records2['category'])

    if(request.json['which'] == "pred_cat"):
        response = recommend.apna_cat_predictor(
            skill_list, level_list, category_list)
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        if(response == 'fincount'):
            cur.execute('SELECT * FROM courses WHERE category in ("Finance & Accounting Courses", "Business", "Marketing", "Office Productivity", "Personal Development"'+') '+'  ORDER BY price DESC LIMIT 10')
            records = cur.fetchall()
            courses = records
        elif(response == 'itbizcount'):
            cur.execute('SELECT * FROM courses WHERE category in ("Finance & Accounting Courses", "Development", "Business", "IT & Software", "Design","Marketing", "Office Productivity"'+') ' + 'ORDER BY price DESC LIMIT 10')

            records = cur.fetchall()
            courses = records
        elif(response == 'itcount'):
            cur.execute('SELECT * FROM courses WHERE category in ("Development", "IT & Software", "Design","Marketing", "Teaching & Academics"' +
                        ') ' + ' ORDER BY price DESC LIMIT 10')

            records = cur.fetchall()
            courses = records
        else:
            cur.execute('SELECT * FROM courses WHERE category in ("Personal Development", "Lifestyle", "Photography","Music", "Teaching & Academics", "Health & Fitness"'+') ' + 'ORDER BY price DESC LIMIT 10')

            records = cur.fetchall()
            courses = records

        return jsonify({"recommended_courses": courses})
    elif (request.json['which'] == "upgradeskill"):
        response = recommend.mainMain(skill_list, level_list)
        return response

@app.route('/job-recommendations')
@check_for_token
def job_recom():
    token = request.headers['Authorization']
    username = jwt.decode(token, app.config['SECRET_KEY'])
    getdetails=getresume.fetch_jobs(username)
    recommendations=recommend.job_recommendations(getdetails)
    return recommendations
    
@app.route('/resume-ocr', methods=['POST'])
@check_for_token
def resume_ocr():
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        response = rocr.de_bhai_pdf(filename)
        return jsonify({"op": response})


def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['pdf'])
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/quizy' ,methods=['POST'])
def ques():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("Select * from quiz Where jobid = '" +
                str(request.json['job_id'])+"';")
    records = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'qna':records})



    # ADMIN SIDE REQUESTS.


def check_for_token_admin(param):
    @ wraps(param)
    def wrapped(*args, **kwargs):
        token = request.headers['Authorization'] or ''
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if not token:
            print('missing')
            return jsonify({'message': 'Missing Token'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY_ADMIN'])
            rew = data["username"]
        except Exception as e:
            print(e)
            return jsonify({'message': 'Invalid Token'}), 403
        return param(*args, **kwargs)
    return wrapped


@ app.route('/admin/login', methods=['POST'])
def admin_login():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute("Select password from admin Where username = '" +
                str(request.json['username'])+"';")
    records = cur.fetchall()
    for row in records:
        if check_password_hash(row["password"], request.json['password']):
            token = jwt.encode({'username': request.json['username'], 'exp': datetime.datetime.utcnow(
            ) + datetime.timedelta(minutes=1440)}, app.config['SECRET_KEY_ADMIN'])
            print(token.decode('utf-8'))
            resp = jsonify({'token': token.decode('utf-8')})
            resp.status_code = 200
            return resp
        else:
            resp = jsonify({'message': 'ERROR Occured.'})
            resp.status_code = 401
            return resp
        cur.close()
        conn.close()


@app.route('/admin/register', methods=['POST'])
def admin_register():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cur.execute("Insert into admin(username,password) VALUES ('"+str(
            request.json['username'])+"','"+generate_password_hash(str(request.json['password'])) + "');")
        conn.commit()
        if cur:
            resp = jsonify({'message': 'success'})
            resp.status_code = 200
            return resp
        resp = jsonify({'message': 'Error.'})
        resp.status_code = 401
        return resp
    finally:
        cur.close()
        conn.close()


@app.route('/admin/post-job', methods=['POST'])
@check_for_token_admin
def upload_file():
    s = []
    # check if the post request has the file part

    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowedd_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        s = extractpdf.yoohoo(filename)

        main = []
        name = []
        pos = []
        sti = []
        desc = []
        lonk = []
        alt = []
        alt = ''

        for i in range(len(s)):
            print(i)
            for j in s[i]['NameOfPosition']:
                name.append(j)
            for j in s[i]['NumberOfPosition']:
                pos.append(j)
            for j in s[i]['Stipend']:
                sti.append(j)
            for j in s[i]['Description']:
                desc.append(j)
            for j in s[i]['Links']:
                lonk.append(j)
            alt = alt+''+s[i]['AllText']


# print(len(name), len(pos), len(sti), len(desc))

        for i in range(len(name)):
            try:
                a = name[i]
            except:
                a = ''
            try:
                b = pos[i]
            except:
                b = ''
            try:
                c = sti[i]
            except:
                c = ''
            try:
                d = desc[i]
            except:
                d = ''
            try:
                e = lonk[i]
            except:
                e = ''
            ssh = {'NameOfPosition': a, 'NumberOfPosition': b,
                   'Stipend': c, 'Description': d, 'Links': e}
            main.append(ssh)

        resp = jsonify({"jobs": main, "all-text-bubbles": alt.split("\n\n")})
        resp.status_code = 200
        return resp
    # else:
    #     resp = jsonify(
    #         {'message': 'Allowed file type is .pdf only.'})
    #     resp.status_code = 400
    #     return resp


def allowedd_file(filename):
    ALLOWED_EXTENSIONS = set(['pdf'])
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/extraction', methods=['POST'])
def test():
    r = request
# convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # do some fancy processing here....
    a, b, c, d, e, f = ocr.ocr(img)
    # build a response dict to send back to client
    response = {'NameOfPosition': a, 'NumberOfPosition': b, 'Stipend': c, 'Description': d, 'AllText': e, 'Links': f
                }
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")


@app.route('/admin/cud_job', methods=['POST'])
@check_for_token_admin
def crud_job():
    token = request.headers['Authorization']
    username = jwt.decode(token, app.config['SECRET_KEY_ADMIN'])

    if(request.json['mode'] == "add"):
        resp = job.create_job(username)
        if resp == 200 or resp == 2000:
            resp = jsonify({'message': 'success'})
            resp.status_code = 200
        elif resp == 401:
            resp = jsonify({'message': 'Error posting job.'})
            resp.status_code = 401
        else:
            resp = jsonify(
                {'message': 'Error while adding quiz but job added. '})
            resp.status_code = 403
        return resp

    elif(request.json['mode'] == "delete"):
        resp = job.delete_job(username)
        return resp
    elif(request.json['mode'] == "update"):
        resp = job.update_job(username)
        return resp
    else:
        resp = jsonify({'message': 'Invalid Request.'})
        return resp


@app.route('/admin/joblist', methods=['GET'])
@check_for_token_admin
def all_jobs():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    token = request.headers['Authorization']
    username = jwt.decode(token, app.config['SECRET_KEY_ADMIN'])
    cur.execute("Select * from job WHERE posted_by ='" +
                str(username['username'])+"';")
    records = cur.fetchall()
    if records:
        resp = jsonify({'alljobs': records})
        resp.status_code = 200
        return resp
    else:
        resp = jsonify({'message': 'ERROR.'})
        resp.status_code = 401
        return resp
    cur.close()
    conn.close()


@app.route('/admin/cud_courses', methods=['POST'])
@check_for_token_admin
def cud_courses():
    token = request.headers['Authorization']
    username = jwt.decode(token, app.config['SECRET_KEY_ADMIN'])
    if(request.json['mode'] == "add"):
        resp = courses.create_course(username)
        return resp
    elif(request.json['mode'] == "delete"):
        resp = courses.delete_course(username)
        return resp
    elif(request.json['mode'] == "update"):
        resp = courses.update_course(username)
        return resp
    else:
        resp = jsonify({'message': 'Invalid Request.'})
        return resp

# get all aplicants details


@app.route('/admin/applicants-jobs', methods=['POST'])
@check_for_token_admin
def postedjobs():
    resp = ad_api.postedjobs()
    return resp


@app.route('/admin/enrollments-courses-count', methods=['GET'])
@check_for_token_admin
def enrollments_courses_count():
    token = request.headers['Authorization']
    username = jwt.decode(token, app.config['SECRET_KEY_ADMIN'])
    resp = ad_api.enrollments_courses_count(username)
    return resp


@app.route('/admin/applicants-jobs-count', methods=['GET'])
@check_for_token_admin
def applicantjobs_count():
    token = request.headers['Authorization']
    username = jwt.decode(token, app.config['SECRET_KEY_ADMIN'])
    resp = ad_api.applicantjobs_count(username)
    return resp


@app.route('/admin/applicants-details', methods=['POST'])
@check_for_token_admin
def applicantdetails():
    resp = ad_api.applicantdetails()
    return resp


@app.route('/admin/update-status', methods=['POST'])
@check_for_token_admin
def ustatus():
    if(request.json['mode'] == 'fetch'):
        resp = ad_api.dispstatus()
        return resp
    if(request.json['mode'] == 'update'):
        resp = ad_api.ustatus()
        return resp
    if(request.json['mode'] == 'meetid'):
        resp = ad_api.umeetid()
        return resp


@app.route('/users-count',  methods=['GET'])
def ucounts():
    resp = no_auth.ucounts()
    return resp


@ app.route('/skills-count',  methods=['GET'])
def skillcounts():
    resp = no_auth.skillcounts()
    return resp


@ app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found ' + request.url,
    }

    resp = jsonify(message)
    resp.status_code = 404

    return resp


if __name__ == "__main__":
    app.run(debug=False)
