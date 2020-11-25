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

import requests
from bs4 import BeautifulSoup

CORS(app)


@app.route("/categories", methods=["GET"])
def get_cats():
    URL = "https://www.aajtak.in/"
    page = requests.get(URL)
    topic = str(request.json["c_name"])
    if topic == "मनोरंजन":
        start = 37
    if topic == "कोरोना":
        start = 43
    if topic == "कोरोना":
        start = 42
    if topic == "लाइफस्टाइल":
        start = 42
    if topic == "चुनाव":
        start = 13
    if topic == "भारत":
        start = 42
    if topic == "होम":
        start = 42

    soup = BeautifulSoup(page.content, "html.parser")
    j = soup.find_all("ul", class_="at-menu")
    for i in j:
        link = i.find("a", title=topic)["href"]
    # print(link)
    page1 = requests.get(link)
    soup1 = BeautifulSoup(page1.content, "html.parser")
    ola = {}
    for i in soup1.find_all("li")[start:]:  # 37 manoranjan 42 corona
        try:  # print(i)
            ola[i.find("a")["title"]] = i.find("a")["href"]
        except:
            break
    resp = jsonify(ola)
    resp.status_code = 200
    return resp


@app.route("/get-details", methods=["GET"])
def details():
    url = str(request.json["url"])
    page = requests.get(url)
    soups = BeautifulSoup(page.content, "html.parser")
    j = " "
    for i in soups.find_all("p"):
        j = j + i.getText()
    details = j.replace("Feedback", "")
    resp = details
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


# @app.route("/recommendations", methods=["POST"])
# def recommendations():
#     conn = mysql.connect()
#     cur = conn.cursor(pymysql.cursors.DictCursor)
#     try:
#         cur.execute(
#             "Insert into admin(username,password) VALUES ('"
#             + str(request.json["username"])
#             + "','"
#             + generate_password_hash(str(request.json["password"]))
#             + "');"
#         )
#         conn.commit()
#         if cur:
#             resp = jsonify({"message": "success"})
#             resp.status_code = 200
#             return resp
#         resp = jsonify({"message": "Error."})
#         resp.status_code = 401
#         return resp
#     finally:
#         cur.close()
#         conn.close()


if __name__ == "__main__":
    app.run(debug=False)
