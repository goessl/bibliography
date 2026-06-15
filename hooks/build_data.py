from pathlib import Path
import yaml
import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "bibliography.yml"
TARGET = ROOT / "docs" / "bibliography.md"


def on_pre_build(config, **kwargs):
    with open(SOURCE, "r", encoding="utf-8") as ifile, open(TARGET, "w", encoding="utf-8") as ofile:
        data = yaml.safe_load(ifile)
        
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
        df = pd.DataFrame.from_dict(data)
        df = df.convert_dtypes() #edition from float to Int64 (allows NA)
        df = df.astype('object').where(df.notna(), '') #prepare NA cells as empty string
        df.to_markdown(ofile, index=False)
