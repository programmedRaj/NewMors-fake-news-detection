import pymysql
import jwt
import datetime
import requests
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request, session, make_response, render_template, Response
from functools import wraps
from flask_cors import CORS
import random
import string


def user(naam):
    try:
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("Select * from users WHERE user_id=" +
                    str(naam['user_id'])+";")
        rows = cur.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()


def applied_jobs(naam):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cur.execute("Select * FROM enrolled_jobs WHERE user_id ='" +
                    str(naam['user_id'])+"';")
        joblists = cur.fetchall()
        if cur:
            resp = jsonify({'appliedjobs': joblists})
            resp.status_code = 200
            conn.commit()
            return resp
        resp = jsonify({'message': 'No Jobs Applied.'})
        resp.status_code = 401
        return resp
    finally:
        cur.close()
        conn.close()


def my_courses(naam):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cur.execute(
            "Select * FROM enrolled_courses WHERE user_id ='" + str(naam['user_id'])+"';")
        mycourses = cur.fetchall()
        if cur:
            resp = jsonify({'enrolledcourses': mycourses})
            resp.status_code = 200
            conn.commit()
            return resp
        resp = jsonify({'message': 'No Courses Applied.'})
        resp.status_code = 401
        return resp
    finally:
        cur.close()
        conn.close()


def enroll_jobs(naam):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("Select * from job Where job_id = '" +
                str(request.json['job_id'])+"';")
    records = cur.fetchall()
    cur.execute("Select * from enrolled_jobs Where job_id = '" +
                str(request.json['job_id'])+"' and user_id ='"+str(naam['user_id'])+"';")
    already = cur.fetchall()
    try:
        if len(records) > 0:
            if len(already) == 0:
                cur.execute(
                    "INSERT INTO enrolled_jobs (job_id,user_id,question,status) VALUES ('"+str(request.json['job_id'])+"',"+str(naam['user_id'])+",'"+str(request.json['answer'])+"','submitted');")
                conn.commit()
                if cur:
                    resp = jsonify({'message': 'success'})
                    resp.status_code = 200
                    return resp
                resp = jsonify({'message': 'Error.'})
                resp.status_code = 401
                return resp
            resp = jsonify({'message': 'Already Applied for job.'})
            resp.status_code = 403
            return resp
        resp = jsonify({'message': 'no job found with this id.'})
        resp.status_code = 401
        return resp
    finally:
        cur.close()
        conn.close()


def enroll_courses(naam):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("Select * from courses Where course_id = '" +
                str(request.json['course_id'])+"';")
    records = cur.fetchall()
    cur.execute("Select * from enrolled_courses Where course_id = '" +
                str(request.json['course_id'])+"' and user_id ='"+str(naam['user_id'])+"';")
    already = cur.fetchall()
    try:
        if len(records) > 0:
            if len(already) == 0:
                cur.execute(
                    "INSERT INTO enrolled_courses (user_id,course_id) VALUES ("+str(naam['user_id'])+","+str(request.json['course_id'])+");")
                conn.commit()
                if cur:
                    resp = jsonify({'message': 'success'})
                    resp.status_code = 200
                    return resp
                resp = jsonify({'message': 'Error.'})
                resp.status_code = 401
                return resp
            resp = jsonify({'message': 'Already enrolled for course.'})
            resp.status_code = 403
            return resp
        resp = jsonify({'message': 'no course found with this id.'})
        resp.status_code = 401
        return resp
    finally:
        cur.close()
        conn.close()
