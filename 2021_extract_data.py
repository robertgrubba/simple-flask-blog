import app
from models import *

from bs4 import BeautifulSoup
import re, sys

url = sys.argv[1]  

date = re.findall(r"\d{2,4}",url)
slug = re.sub(r'/index.html','',re.sub(r'/data/wordpress/\d+/\d+/','',url,1),1)
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

for tag in tags:
    exists = Tag.query.filter_by(name=tag).first()
    if not exists:
        new_tag = Tag(name=tag)
        db.session.add(new_tag)

for category in categories:
    exists = Category.query.filter_by(name=category).first()
    if not exists:
        new_category = Category(name=category)
        db.session.add(new_category)

#page_date = datetime.datetime.strptime(re.sub(r'+00:00','',dates[0],1),'%Y-%m-%dT%H:%M:%S')
page_date = datetime.datetime.strptime(dates[0][0:19],'%Y-%m-%dT%H:%M:%S')

exists = Page.query.filter_by(title=title.text,created=page_date).first()
if not exists:
    new_page = Page(slug=str(slug), title=str(title.text), content=str(content), created=page_date)
    db.session.add(new_page)
else:
        for category in categories:
            exists.categories.append(Category.query.filter_by(name=category).first())

        for tag in tags:
            exists.tags.append(Tag.query.filter_by(name=tag).first())

db.session.commit()


