# मनोरंजन,कोरोना,कोरोना,लाइफस्टाइल,चुनाव,भारत,होम

# import requests
# from bs4 import BeautifulSoup

# URL = "https://www.aajtak.in/"
# page = requests.get(URL)


# topic = "मनोरंजन"

# if topic == "मनोरंजन":
#     start = 37
# if topic == "कोरोना":
#     start = 43
# if topic == "कोरोना":
#     start = 42
# if topic == "लाइफस्टाइल":
#     start = 42
# if topic == "चुनाव":
#     start = 13
# if topic == "भारत":
#     start = 42
# if topic == "होम":
#     start = 42


# soup = BeautifulSoup(page.content, "html.parser")
# j = soup.find_all("ul", class_="at-menu")
# for i in j:
#     link = i.find("a", title=topic)["href"]
# # print(link)
# page1 = requests.get(link)
# soup1 = BeautifulSoup(page1.content, "html.parser")
# ola = {}
# for i in soup1.find_all("li")[start:]:  # 37 manoranjan 42 corona
#     try:  # print(i)
#         ola[i.find("a")["title"]] = i.find("a")["href"]
#     except:
#         break

# ola is main


# मनोरंजन,कोरोना,कोरोना,लाइफस्टाइल,चुनाव,भारत,होम
from flask import Flask, request, Response, redirect, render_template
from flask import jsonify
import json
import pickle
import jsonpickle
import requests
from bs4 import BeautifulSoup

import numpy as np
import pandas as pd
import itertools
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

df = pd.read_csv("news.csv")
labels = df.label
x_train, x_test, y_train, y_test = train_test_split(
    df["text"], labels, test_size=0.2, random_state=7
)
tfidf_vectorizer = TfidfVectorizer(stop_words="english", max_df=0.7)
tfidf_train = tfidf_vectorizer.fit_transform(x_train)
tfidf_test = tfidf_vectorizer.transform(x_test)
pac = PassiveAggressiveClassifier(max_iter=50)
pac.fit(tfidf_train, y_train)
y_pred = pac.predict(tfidf_test)
score = accuracy_score(y_test, y_pred)
# print(f'Accuracy: {round(score*100,2)}%')
# a=tfidf_vectorizer.transform(['hehe'])
# pac.predict(a)[0]

app = Flask(__name__)


@app.route("/", methods=["POST"])
def home():

    topic = request.form["topic"]
    URL = "https://www.aajtak.in/"
    page = requests.get(URL)

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
    ola = []
    uu = 0
    for i in soup1.find_all("li")[start:]:  # 37 manoranjan 42 corona
        try:
            gg = i.find("a")["title"]
            a = tfidf_vectorizer.transform([gg])
            # pac.predict(a)[0]

            ola[uu] = [
                gg,
                i.find("a")["href"],
                pac.predict(a)[0],
                i.find("img")["data-src"],
            ]
        except:
            break
    response_pickled = jsonpickle.encode(ola)

    return Response(response=response_pickled, status=200, mimetype="application/json")
    # [[headline,url,fakeness,image url]]


# ola is main
@app.route("/details", methods=["POST"])
def details():
    url = request.form["url"]
    page = requests.get(url)
    soups = BeautifulSoup(page.content, "html.parser")
    j = " "
    for i in soups.find_all("p"):
        j = j + i.getText()
    details = j.replace("Feedback", "")
    response_pickled = jsonpickle.encode(details)

    return Response(response=response_pickled, status=200, mimetype="application/json")
