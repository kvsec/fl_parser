from bs4 import BeautifulSoup
import urllib
import requests
import re
import sys
from random import choice
import multiprocessing
from multiprocessing import Pool
from io import StringIO
import csv
import logging


logger = logging.getLogger(__name__)


def random_headers():
    useragents = open('useragents.txt').read().split('\n')
    return choice(useragents)


search_string = input("Enter search value: ")


def main(search_string):
    logger.info('Start retrive')
    target_url = 'http://fayloobmennik.cloud/files/search.html'
    find_pattern = r'<a href=\"/files/search.html\?p=\d*\">'
    page_count = 0
    csv_file = StringIO()
    csv_writer = csv.writer(csv_file)
    payload = 'search={}'.format(search_string)
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Content-Length': len(payload),
    'User-Agent': random_headers()
    }
    request_object = urllib.request.Request(target_url, payload.encode('utf-8'), headers)
    response = urllib.request.urlopen(request_object)
    response_text = response.read().decode('cp1251')
    cookies = response.getheader("Set-Cookie")
    find_pages = re.findall(find_pattern, response_text)
    for page in find_pages:
        _ = int(page.replace('<a href="/files/search.html?p=','').replace('">', ''))
        if _ > page_count:
            page_count = _
    print(page_count)
    for i in range(1, page_count + 1):
        target_url = "http://fayloobmennik.cloud/files/search.html?p={}"
        headers = {
        'Content-Length': len(payload),
        'User-Agent': random_headers(),
        'Cookie' : cookies
        }
        request_object = urllib.request.Request(target_url.format(i), payload.encode('utf-8'), headers)
        response = urllib.request.urlopen(request_object)
        response_text = response.read().decode('cp1251')
        soup = BeautifulSoup(response_text, 'lxml')
        table = soup.find('tbody')
        rows = table.find_all('tr')
        for row in rows:
            _buff = []
            for col in row.find_all('td'):
                try:
                    url = 'http://fayloobmennik.cloud{}'.format(col.find('a').get('href'))
                    _buff.append(url)
                except AttributeError:
                    pass
                _buff.append(col.get_text())
            csv_writer.writerow(_buff)


        with open('result-' + search_string + '.csv', 'w', errors='replace', encoding='UTF-8') as open_file:
            open_file.write(csv_file.getvalue())


if __name__ == "__main__":
    main(search_string)
