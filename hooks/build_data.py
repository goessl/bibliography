from pathlib import Path
import yaml
import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "bibliography.yml"
TARGET = ROOT / "docs" / "bibliography.md"


def on_pre_build(config, **kwargs):
    with open(SOURCE, "r", encoding="utf-8") as ifile, open(TARGET, "w", encoding="utf-8") as ofile:
        #read
        data = yaml.safe_load(ifile)
        
        #tabulate
        df = pd.DataFrame.from_dict(data)
        
        #format
        df = df.convert_dtypes() #edition from float to Int64 (allows NA)
        if "author" in df.columns: #make authors a list
            df["author"] = df["author"].apply(
                lambda x: '<ul>'+''.join(f'<li>{e}</li>' for e in x)+'</ul>'# if pd.notna(x) else x
            )
        if "doi" in df.columns: #make dois clickable
            df["doi"] = df["doi"].apply(
                lambda x: f'<a href="https://doi.org/{x}" target="_blank">{x}</a>' if pd.notna(x) else x
            )
        if "url" in df.columns: #make urls clickable
            df["url"] = df["url"].apply(
                lambda x: f'<a href="{x}" target="_blank">{x}</a>' if pd.notna(x) else x
            )
        df = df.astype('object').where(df.notna(), '') #prepare NA cells as empty string
        
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
