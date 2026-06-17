from pathlib import Path
from datetime import date
import yaml
import json


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'bibliography.yml'
JSON_TARGET = ROOT / 'docs' / 'bibliography.json'
BIB_TARGET  = ROOT / 'bibliography.bib'

BOOKLET_FIELDS = {'author', 'title'}
BOOK_FIELDS0 = {'author', 'title', 'date', 'edition', 'publisher', 'isbn', 'doi', 'url'}
BOOK_FIELDS1 = {'editor', 'title', 'date', 'edition', 'publisher', 'isbn', 'doi', 'url'}


def to_bibtex(entry):
    field_lines = []
    for key in ('author', 'editor'):
        if key in entry:
            field_lines.append(f'{key} = {{{" and ".join(entry[key])}}}')
    for key, value in entry.items():
        if key not in {'type', 'id', 'author', 'editor'}:
            field_lines.append(f'{key} = {{{value}}}')
    return f'@{entry["type"]}{{{entry["id"]},\n  ' \
        + ',\n  '.join(field_lines) \
        + '\n}'


def on_post_build(config, **kwargs):
    (Path(config['site_dir']) / '.nojekyll').touch()


def on_pre_build(config, **kwargs):
    with open(SOURCE, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    #validate
    if not isinstance(data, list):
        raise TypeError('Bibliography not a list')
    for entry in data:
        if not isinstance(entry, dict):
            raise TypeError(f'Bibliography entry not a dict: {entry}')
        if not ('type' in entry and 'id' in entry):
            raise ValueError(f'Entry without type or id: {entry}')
        match entry['type']:
            case 'Booklet':
                if not entry.keys() >= BOOKLET_FIELDS:
                    raise ValueError(f'Booklet with missing fields: {entry}')
            case 'Book':
                if not (entry.keys() >= BOOK_FIELDS0 or entry.keys() >= BOOK_FIELDS1):
                    raise ValueError(f'Book with missing fields: {entry}')
            case _:
                raise ValueError(f'Unrecognised entry type: {entry}')
        for k, v in entry.items():
            match k:
                case 'author' | 'editor':
                    if not (isinstance(v, list) and all(isinstance(a, str) for a in v)):
                        raise TypeError(f'Wrong author/editor format: {entry}')
                case _:
                    if not isinstance(v, (str, int, date)):
                        raise TypeError(f'Wrong format: {entry}')
    
    #write JSON
    with open(JSON_TARGET, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, default=str)
    
    #write BibTeX
    with open(BIB_TARGET, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(to_bibtex(e) for e in data))
        f.write('\n')
