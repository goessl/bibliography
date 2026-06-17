from pathlib import Path
from datetime import date
import yaml
import json


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'bibliography.yml'
TARGET = ROOT / 'docs' / 'bibliography.json'

BOOKLET_FIELDS = {'author', 'title'}
BOOK_FIELDS = {'author', 'title', 'date', 'edition', 'publisher', 'isbn', 'doi', 'url'}


def on_post_build(config, **kwargs):
    (Path(config['site_dir']) / '.nojekyll').touch()


def on_pre_build(config, **kwargs):
    with open(SOURCE, 'r', encoding='utf-8') as ifile, open(TARGET, 'w', encoding='utf-8') as ofile:
        #read
        data = yaml.safe_load(ifile)
        
        
        #validate
        #check structure
        if not isinstance(data, list):
            raise TypeError('Bibliography not a list')
        for entry in data:
            if not isinstance(entry, dict):
                raise TypeError(f'Bibliography entry not a dict: {entry}')
            #check keys
            if not ('type' in entry and 'id' in entry):
                raise ValueError(f'Entry without type or id: {entry}')
            match entry['type']:
                case 'Booklet':
                    if not entry.keys() >= BOOKLET_FIELDS:
                        raise ValueError(f'Booklet with missing fields: {entry}')
                case 'Book':
                    if not entry.keys() >= BOOK_FIELDS:
                        raise ValueError(f'Book with missing fields: {entry}')
                case _:
                    raise ValueError(f'Unrecognised entry type: {entry}')
            #check values
            for k, v in entry.items():
                match k:
                    case 'author':
                        if not (isinstance(v, list) and all(isinstance(a, str) for a in v)):
                            raise TypeError(f'Wrong author format: {entry}')
                    case _:
                        if not isinstance(v, (str, int, date)):
                            raise TypeError(f'Wrong format: {entry}')
        
        
        #write
        json.dump(data, ofile, ensure_ascii=False, default=str)
