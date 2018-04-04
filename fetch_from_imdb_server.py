import requests
from bs4 import BeautifulSoup
page = requests.get("http://www.imdb.com/title/tt1327195/?ref_=fn_al_tt_2")
print page.content
soup = BeautifulSoup(page.content, 'html.parser')
print soup.prettify()
print list(soup.children)