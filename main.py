import httplib2
import sys
from bs4 import BeautifulSoup, SoupStrainer


def check_slashes(hrefs):
    slash_counter = 0
    for element in hrefs:
        if element == '/':
            slash_counter += 1
    if slash_counter <= 6:
        return False
    return True

link_set = set()
base_html = "https://akispetretzikis.com/"
http = httplib2.Http()
status, response = http.request('https://akispetretzikis.com/el/categories/keik/keik-sokolatas')


for i in range(3):
    soup = BeautifulSoup(response, features="html.parser")
    div = soup.find('div', id='cmeProductSlatePaginiationTop')
    section = soup.find('section')

    for a in section.find_all('a', href=True):
        link = base_html+a['href']
        if check_slashes(link):
            link_set.add(link)
    response = http.request(next(iter(link_set)))
    print(next(iter(link_set)))

print(link_set)

"""
for link in BeautifulSoup(response, parse_only=SoupStrainer('a'), features="html.parser"):
    if link.has_attr('href'):
        print(link['href'])
"""
