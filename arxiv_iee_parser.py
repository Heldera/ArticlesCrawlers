from urllib.request import urlopen

from bs4 import BeautifulSoup
import urllib.request
import re
import json

url = 'http://export.arxiv.org/api/query?search_query=system+dynamics&max_results=3'
with urlopen(url) as request:
     data = request.read()

number = 1

from xml.etree import ElementTree
root = ElementTree.fromstring(data)

for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
             title = entry.findall('{http://www.w3.org/2005/Atom}title')[0].text
             summary = entry.findall('{http://www.w3.org/2005/Atom}summary')[0].text
             published_date = entry.findall('{http://www.w3.org/2005/Atom}published')[0].text
             authors = [x[0].text for x in entry.findall('{http://www.w3.org/2005/Atom}author')]
             print(str(number), '[Title]: '+ title.replace('\n',' ') + '\n', ' [Published_date]: ' + published_date + '\n', ' [Authors]: ' + str(authors).replace('[','').replace(']','') + '\n', ' [Abstract]' + summary.replace('\n',' '), '\n')
             number += 1   

url_1 = 'http://ieeexplore.ieee.org/xpl/mostRecentIssue.jsp?punumber=4410506'
response = urllib.request.urlopen(url_1)
soup = BeautifulSoup(response.read().decode('utf-8'), "html.parser")

for element in soup.find_all('a', href=re.compile("stamp\\.jsp")):
    page_url = 'http://ieeexplore.ieee.org' + element.get('href')
    page_response = urllib.request.urlopen(page_url)
    page_soup = BeautifulSoup(page_response.read().decode('utf-8'), "html.parser")
    json_re = re.compile("global\\.document\\.metadata\\s*=\\s*(.+);")
    if number < 8:
                  #print('\n' + str(number) + ' doc')
                  for page_element in page_soup.find_all('script', string=re.compile("global\\.document\\.metadata")):
                      match = json_re.search(page_element.string)
                      data_1 = json.loads(match.group(1))
                      doi = data_1['doi']
                      authors = data_1['authors']
                      print('999 ', str(authors))
                      abstract = data_1['abstract']
                      #print(str(number), str(abstract))
    number += 1                            
