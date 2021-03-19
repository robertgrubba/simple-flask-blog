from bs4 import BeautifulSoup
import re, sys

url = sys.argv[1]  

date = re.findall(r"\d{2,4}",url)
slug = re.sub(r'/index.html','',re.sub(r'./\d+/\d+/','',url,1),1)
if (slug == "./index.html" or slug=="" or (re.match(r"feed",url)!=None)):
    exit

print(date)
print(slug)

soup = BeautifulSoup(open(url),"html.parser")

for title in soup.find_all('h1', {'class':'entry-title'}):
    print(title.text)

for content in soup.find_all('div', {'class':'entry-content'}):
    print(content)

categories = []
for category in soup.find_all('a', {'rel':'category tag'}):
    categories.append(category.text)

print(categories)

tags = []
for tag in soup.find_all('a', {'rel':'tag'}):
    if tag.text not in categories:
        tags.append(tag.text)

print(tags)

dates=[]
for timestamp in soup.find_all('time',{'class':'entry-date'}):
        dates.append(timestamp['datetime'])
print(dates)
