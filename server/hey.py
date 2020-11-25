# मनोरंजन,कोरोना,कोरोना,लाइफस्टाइल,चुनाव,भारत,होम

import requests
from bs4 import BeautifulSoup

URL = "https://www.aajtak.in/"
page = requests.get(URL)


topic = "मनोरंजन"

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

# ola is main
