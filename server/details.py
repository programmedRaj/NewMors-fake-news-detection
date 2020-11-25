url=''
page = requests.get(url)
soups = BeautifulSoup(page.content, 'html.parser')
j=' '
for i in soups.find_all('p'):
    j=j+i.getText()
details=j.replace('Feedback','') 