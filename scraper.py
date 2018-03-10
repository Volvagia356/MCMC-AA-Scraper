import time

from bs4 import BeautifulSoup

import ajax

def get_soup(html):
   return BeautifulSoup(html, 'html.parser')

def get_entries(soup, columns):
    rows = soup.table.tbody.find_all("tr", recursive=False)
    
    for row in rows:
        entry = {}
        for column in columns:
            entry[column] = row.find(class_=column).get_text().strip()
        yield entry

def get_page_entries(aa_type, columns, page):
    response = ajax.fetch(aa_type, page)
    commands = ajax.parse(response.text)
    content = ajax.get_content(commands)

    soup = get_soup(content)
    entries = get_entries(soup, columns)
    return entries

def get_all_entries(aa_type, columns, page_count):
    for page in range(1, page_count + 1):
        print("Scraping page {}...".format(page))
        entries = get_page_entries(aa_type, columns, page)
        for entry in entries:
            yield entry
        time.sleep(1)
