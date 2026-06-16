from pathlib import Path
from datetime import date
import yaml
import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "bibliography.yml"
TARGET = ROOT / "docs" / "bibliography.md"

BOOKLET_FIELDS = {'author', 'title'}
BOOK_FIELDS = {'author', 'title', 'date', 'edition', 'publisher', 'isbn', 'doi', 'url'}


def on_pre_build(config, **kwargs):
    with open(SOURCE, "r", encoding="utf-8") as ifile, open(TARGET, "w", encoding="utf-8") as ofile:
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
        
        
        #tabulate
        df = pd.DataFrame.from_dict(data)
        
        
        #format
        #column sorting
        PRIO_COLUMNS = ('type', 'id', 'author', 'title', 'subtitle', 'url')
        columns = [c for c in df.columns if c in PRIO_COLUMNS]
        columns += [c for c in df.columns if not c in PRIO_COLUMNS]
        df = df[columns]
        #edition from float to Int64 (allows NA)
        df = df.convert_dtypes()
        #html
        if "author" in df.columns:
            df["author"] = df["author"].apply(
                lambda x: '<ul>'+''.join(f'<li>{e}</li>' for e in x)+'</ul>'# if pd.notna(x) else x
            )
        if "doi" in df.columns:
            df["doi"] = df["doi"].apply(
                lambda x: f'<a href="https://doi.org/{x}" target="_blank">{x}</a>' if pd.notna(x) else x
            )
        if "url" in df.columns:
            df["url"] = df["url"].apply(
                lambda x: f'<a href="{x}" target="_blank">{x}</a>' if pd.notna(x) else x
            )
        #prepare NA cells as empty string
        df = df.astype('object').where(df.notna(), '')
        
        
        #write
        ofile.write('---\n'
                    'hide:\n'
                    '  - toc\n'
                    'extra:\n'
                    '  layout: full\n'
                    '---\n'
                    '\n'
                    '# Bibliography\n'
                    '\n'
        )
        df.to_markdown(ofile, index=False)
