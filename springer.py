import sys
import re
import argparse
import requests
from datetime import datetime
from collections import defaultdict
from bs4 import BeautifulSoup
import yaml


def find_exactly_one(element, *args, **kwargs):
    results = element.find_all(*args, **kwargs)
    assert len(results) == 1
    return results[0]



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse a Springer book page and output bibliography YAML.')
    parser.add_argument('urls', nargs='+', help='Springer book URL(s)')
    args = parser.parse_args()
    
    entries = []
    for url in args.urls:
        #request webpage
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        #find information list
        bibliography_list = find_exactly_one(soup, 'ul', class_='c-bibliographic-information__list')
        
        #extract all key-value pairs
        d = defaultdict(list)
        dates = []
        for li in bibliography_list.find_all('li', class_='c-bibliographic-information__list-item'):
            key   = find_exactly_one(li, 'span', class_='u-text-bold')
            value = find_exactly_one(li, 'span', class_='c-bibliographic-information__value')
            key, value = key.text, value.text
            d[key].append(value)
            if key == 'eBook ISBN':
                date = find_exactly_one(li, 'span', {'data-test':'electronic_isbn_publication_date'}).text
                date = date.removeprefix('Published: ')
                dates.append(date)
        for k, v in d.items():
            assert len(v) == 1
            d[k] = v[0]
        assert len(dates) == 1
        date = dates[0]
        
        #format
        isbn = d['eBook ISBN']
        doi  = d['DOI'].removeprefix('https://doi.org/')
        
        #verify url, doi, isbn are consistent
        assert re.fullmatch(r'https://link\.springer\.com/book/10\.\d{4,}/[\w\-]+', url), \
            f'Unexpected URL format: {url!r}'
        assert re.fullmatch(r'10\.\d{4,}/.+', doi), \
            f'Unexpected DOI format: {doi!r}'
        assert re.fullmatch(r'978-[\d\-]+', isbn), \
            f'Unexpected ISBN format: {isbn!r}'
        assert url.endswith(isbn), \
            f'URL {url!r} does not end with ISBN {isbn!r}'
        assert doi.endswith(isbn), \
            f'DOI {doi!r} does not end with ISBN {isbn!r}'
        
        entry = {'type': 'Book', 'id': 'TODO'}
        if 'Authors' in d:
            entry['author'] = [d['Authors']]
        elif 'Editors' in d:
            entry['editor'] = [d['Editors']]
        else:
            raise ValueError('No Authors or Editors found')
        entry['title'] = d['Book Title']
        if 'Book Subtitle' in d:
            entry['subtitle'] = d['Book Subtitle']
        entry['date']      = datetime.strptime(date, '%d %B %Y').date()
        entry['edition']   = int(d['Edition Number'])
        entry['publisher'] = d['Publisher']
        entry['isbn']      = isbn
        entry['doi']       = doi
        entry['url']       = url
        entries.append(entry)
    
    print(yaml.dump(entries, allow_unicode=True, sort_keys=False))