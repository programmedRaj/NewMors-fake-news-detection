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

CORS(app)


@app.route("/recommendations", methods=["POST"])
def recommendations():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cur.execute(
            "Insert into admin(username,password) VALUES ('"
            + str(request.json["username"])
            + "','"
            + generate_password_hash(str(request.json["password"]))
            + "');"
        )
        conn.commit()
        if cur:
            resp = jsonify({"message": "success"})
            resp.status_code = 200
            return resp
        resp = jsonify({"message": "Error."})
        resp.status_code = 401
        return resp
    finally:
        cur.close()
        conn.close()


@app.route("/edit", methods=["GET"])
def ucounts():
    resp = "h1"
    return resp


@app.errorhandler(404)
def not_found(error=None):
    message = {
        "status": 404,
        "message": "Not Found " + request.url,
    }

    resp = jsonify(message)
    resp.status_code = 404

    return resp


if __name__ == "__main__":
    app.run(debug=False)
