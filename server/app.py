# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 17:44:47 2020

@author: user
"""

import os
from flask import Flask
app = Flask(__name__)

UPLOAD_FOLDER = os.getcwd()+'/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config["SECRET_KEY"] = "SIh2020jobocr"
app.config["SECRET_KEY_ADMIN"] = "SIH2020ADMIN"
