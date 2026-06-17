# bibliography

Physics bibliography.

## Usage

**Enjoy the [webpage](https://goessl.github.io/bibliography).**

## Bibliography conventions

- `.bib` reference: [Overleaf/BibLaTeX](https://www.overleaf.com/learn/latex/Bibliography_management_with_biblatex)
- Bibliography file as YAML: [`bibliography.yml`](https://github.com/goessl/bibliography)
    - Every entry has a `type` and `id` item.
    - Remaining as for usual `bib` file.

### Necessary items

- Book
    - `author`
    - `title`
    - `date`
    - `edition`
    - `publisher`
    - `isbn`
    - `doi`
    - `url`
- Booklet
    - `author`
    - `title`

### Values and formats

- `author`s as list
- e-book vs. hardcover
    Use e-book values. Often fields `date` and `isbn`.
- `date` in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601).

## Design

- **mkdocs-material**
    Setup from [goessl/templates](https://github.com/goessl/templates).
- **bibliography as YAML: [`bibliography.yml`](https://github.com/goessl/bibliography/bibliography.yml)**
    - Single source of truth.
    - Common format that is easy to maintain and machine readable and convertible.
- **Hook: [`hooks/build_data.py`](https://github.com/goessl/bibliography/hooks/build_data.py)**
    - Validates the YAML on every build.
    - Exports to JSON for Tabulator to read.
- **[Tabulator.js](https://www.tabulator.info/)**
    Needed for advanced formatting and filtering (especially because of authors column, which contains an array).

## Roadmap

- [x] Load from single source of truth
- [x] Filtering
- [x] Deploy
- [ ] Complete bibliography
- [ ] Perfectly use material for tabulator styling
- [ ] Improved filtering (checkbox list for authors, date and edition number ranges)
- [ ] Subject tags
- [ ] Author list with additional information like homepage
- [ ] Production
- [x] Ballin

## License (MIT)

Copyright (c) 2026 Sebastian Gössl

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
