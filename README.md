# cloc-py

A Python implementation of [cloc](https://github.com/AlDanial/cloc) (Count Lines of Code).

## Overview

cloc-py is a Python port of the original Perl-based cloc tool by Al Danial. It counts blank lines, comment lines, and physical lines of source code in many programming languages.

## Acknowledgments

This project is based on the original [cloc](https://github.com/AlDanial/cloc) tool by **Al Danial** <al.danial@gmail.com>.

- **Original cloc**: Copyright (C) 2006-2025, Al Danial
- **cloc-py**: Copyright (C) 2024, Anidhula

The original cloc tool has been hosted on GitHub since September 2015 and was previously hosted at http://cloc.sourceforge.net/ since August 2006. It has over 21.5k stars and 1.1k forks, making it one of the most popular code counting tools.

## Features

- **Language Detection**: Automatically detects programming languages from file extensions and shebang lines
- **Comment Removal**: Language-specific comment detection and removal
- **Multiple Output Formats**: Text, JSON, and CSV output formats
- **Directory Scanning**: Recursively scan directories with configurable exclusions
- **Binary File Detection**: Automatically skips binary files

## Supported Languages

The tool supports many programming languages including:

- **Python** (py, pyw, pyi, pyx, pxd, ipynb)
- **C/C++** (c, cpp, cc, cxx, h, hpp, hxx)
- **Java** (java, jsp)
- **JavaScript/TypeScript** (js, jsx, ts, tsx, mjs, cjs)
- **Web** (html, htm, css, xml, xhtml, svg)
- **Shell Scripts** (sh, bash, zsh, fish, csh, ksh)
- **Other Languages**: Ruby, Perl, PHP, Rust, Go, Swift, Kotlin, Scala, C#, Visual Basic, Fortran, Pascal, Assembly, and many more

## Installation

No installation required! Just download the `cloc_py.py` file and run it with Python 3.6+.

## Usage

### Basic Usage

```bash
# Count lines in a single file
python cloc_py.py file.py

# Count lines in a directory
python cloc_py.py /path/to/project

# Count lines in multiple files/directories
python cloc_py.py file1.py file2.py /path/to/project
```

### Command Line Options

```bash
python cloc_py.py [OPTIONS] paths...

Options:
  paths                   Files or directories to count
  --exclude-dir DIR       Directories to exclude (can be used multiple times)
  --format {text,json,csv}  Output format (default: text)
  --by-file               Show results by file instead of by language
  --version               Show program version
  -h, --help             Show help message
```

### Examples

```bash
# Default text output
python cloc_py.py my_project/

# JSON output
python cloc_py.py my_project/ --format json

# CSV output
python cloc_py.py my_project/ --format csv

# Show results by file
python cloc_py.py my_project/ --by-file

# Exclude certain directories
python cloc_py.py my_project/ --exclude-dir node_modules --exclude-dir .git
```

## Output Formats

### Text Format (Default)
```
Language                     files          blank        comment           code
----------------------------------------------------------------------
Python                               15          165          227          594
JavaScript                            5            3            0           15
C++                                   4          132          173          570
...
SUM                                 681         4972         8572        56293
```

### JSON Format
```json
{
  "languages": {
    "Python": {
      "files": 15,
      "blank": 165,
      "comment": 227,
      "code": 594
    }
  },
  "total": {
    "files": 681,
    "blank": 4972,
    "comment": 8572,
    "code": 56293
  }
}
```

### CSV Format
```csv
Language,files,blank,comment,code
Python,15,165,227,594
JavaScript,5,3,0,15
C++,4,132,173,570
```

## How It Works

1. **File Discovery**: Recursively scans directories for files
2. **Language Detection**: Maps file extensions to languages, with fallback to shebang detection
3. **Binary Detection**: Skips files that contain null bytes
4. **Comment Removal**: Applies language-specific filters to remove comments
5. **Line Counting**: Counts blank, comment, and code lines
6. **Reporting**: Aggregates results by language and generates reports

## Comment Detection

The tool uses language-specific filters to detect and remove comments:

- **Python**: `#` comments and docstrings (`"""` and `'''`)
- **C/C++**: `//` and `/* */` comments
- **Shell**: `#` comments (respecting quoted strings)
- **HTML**: `<!-- -->` comments
- **CSS**: `/* */` comments
- **SQL**: `--` and `/* */` comments
- And many more...

## Comparison with Original cloc

This Python implementation provides similar functionality to the original Perl-based cloc:

| Feature | Original cloc | cloc-py |
|---------|---------------|---------|
| Language Support | 400+ languages | 50+ languages |
| Performance | Very fast | Good |
| Dependencies | Perl + modules | Python 3.6+ only |
| Extensibility | High | High |
| Output Formats | Many | Text, JSON, CSV |

## Limitations

- Supports fewer languages than the original cloc
- Some complex comment patterns may not be perfectly detected
- Performance may be slower than the original for very large codebases

## Contributing

Feel free to contribute by:
- Adding support for more languages
- Improving comment detection accuracy
- Adding new output formats
- Optimizing performance

## License

This project is based on the original cloc by Al Danial, which is licensed under the GPL-2.0 license.

## Acknowledgments

- Original cloc by Al Danial: https://github.com/AlDanial/cloc
- Inspired by the need for a pure Python implementation 