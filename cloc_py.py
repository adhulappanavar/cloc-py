#!/usr/bin/env python3
"""
cloc-py -- Count Lines of Code (Python version)
Based on the original cloc by Al Danial <al.danial@gmail.com>
"""

import os
import re
import sys
import argparse
import mimetypes
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from collections import defaultdict
import json


@dataclass
class CountResult:
    """Results of counting lines in a file"""
    language: str
    blank: int
    comment: int
    code: int
    total: int


class ClocCounter:
    """Main class for counting lines of code"""
    
    def __init__(self):
        self.language_by_extension = self._init_language_mappings()
        self.filters_by_language = self._init_filters()
        self.script_languages = {
            'Python', 'Perl', 'Ruby', 'Bash', 'Shell', 'JavaScript', 
            'PHP', 'Tcl', 'Lua', 'R', 'Raku', 'Julia', 'Elixir'
        } 
    
    def _init_language_mappings(self) -> Dict[str, str]:
        """Initialize file extension to language mappings"""
        return {
            # Python
            'py': 'Python', 'pyw': 'Python', 'pyi': 'Python', 'pyx': 'Cython',
            'pxd': 'Cython', 'pxi': 'Cython', 'ipynb': 'Jupyter Notebook',
            
            # C/C++
            'c': 'C', 'h': 'C/C++ Header', 'cpp': 'C++', 'cc': 'C++', 
            'cxx': 'C++', 'hpp': 'C/C++ Header', 'hxx': 'C/C++ Header',
            'c++': 'C++', 'h++': 'C++',
            
            # Java
            'java': 'Java', 'jsp': 'JSP', 'jspf': 'JSP',
            
            # JavaScript/TypeScript
            'js': 'JavaScript', 'jsx': 'JSX', 'ts': 'TypeScript', 
            'tsx': 'TypeScript', 'mjs': 'JavaScript', 'cjs': 'JavaScript',
            
            # Web
            'html': 'HTML', 'htm': 'HTML', 'css': 'CSS', 'xml': 'XML',
            'xhtml': 'XHTML', 'svg': 'SVG',
            
            # Shell
            'sh': 'Bourne Again Shell', 'bash': 'Bourne Again Shell',
            'zsh': 'Zsh', 'fish': 'Fish Shell', 'csh': 'C Shell',
            'ksh': 'Korn Shell',
            
            # Other languages
            'rb': 'Ruby', 'pl': 'Perl', 'pm': 'Perl', 'php': 'PHP',
            'rs': 'Rust', 'go': 'Go', 'swift': 'Swift', 'kt': 'Kotlin',
            'scala': 'Scala', 'clj': 'Clojure', 'hs': 'Haskell',
            'ml': 'OCaml', 'fs': 'F#', 'cs': 'C#', 'vb': 'Visual Basic',
            'f': 'Fortran 77', 'f90': 'Fortran 90', 'f95': 'Fortran 95',
            'pas': 'Pascal', 'ada': 'Ada', 'asm': 'Assembly',
            's': 'Assembly', 'S': 'Assembly',
            
            # Configuration/Markup
            'json': 'JSON', 'yaml': 'YAML', 'yml': 'YAML', 'toml': 'TOML',
            'ini': 'INI', 'cfg': 'INI', 'conf': 'INI', 'md': 'Markdown',
            'rst': 'reStructuredText', 'txt': 'Text',
            
            # Build/Config
            'makefile': 'make', 'Makefile': 'make', 'cmake': 'CMake',
            'dockerfile': 'Dockerfile', 'Dockerfile': 'Dockerfile',
            'gradle': 'Gradle', 'pom.xml': 'Maven',
            
            # Data
            'csv': 'CSV', 'tsv': 'TSV', 'sql': 'SQL',
            
            # Documentation
            'tex': 'TeX', 'bib': 'BibTeX', 'sty': 'TeX',
            
            # Other
            'r': 'R', 'dart': 'Dart', 'elm': 'Elm', 'cl': 'Lisp',
            'lisp': 'Lisp', 'scm': 'Scheme', 'ss': 'Scheme',
            'lua': 'Lua', 'tcl': 'Tcl', 'v': 'Verilog', 'vhdl': 'VHDL',
            'coffee': 'CoffeeScript', 'litcoffee': 'CoffeeScript',
            'ls': 'LiveScript', 'iced': 'IcedCoffeeScript',
        } 
    
    def _init_filters(self) -> Dict[str, List]:
        """Initialize comment removal filters by language"""
        return {
            'Python': [
                ('remove_python_comments',),
                ('remove_python_docstrings',),
            ],
            'C': [
                ('remove_cpp_comments',),
            ],
            'C++': [
                ('remove_cpp_comments',),
            ],
            'C/C++ Header': [
                ('remove_cpp_comments',),
            ],
            'Java': [
                ('remove_cpp_comments',),
            ],
            'JavaScript': [
                ('remove_cpp_comments',),
                ('remove_js_comments',),
            ],
            'TypeScript': [
                ('remove_cpp_comments',),
                ('remove_js_comments',),
            ],
            'JSX': [
                ('remove_cpp_comments',),
                ('remove_js_comments',),
            ],
            'PHP': [
                ('remove_cpp_comments',),
                ('remove_php_comments',),
            ],
            'HTML': [
                ('remove_html_comments',),
            ],
            'XML': [
                ('remove_html_comments',),
            ],
            'CSS': [
                ('remove_css_comments',),
            ],
            'SQL': [
                ('remove_sql_comments',),
            ],
            'Bourne Again Shell': [
                ('remove_shell_comments',),
            ],
            'Bash': [
                ('remove_shell_comments',),
            ],
            'Ruby': [
                ('remove_ruby_comments',),
            ],
            'Perl': [
                ('remove_perl_comments',),
            ],
            'Rust': [
                ('remove_cpp_comments',),
            ],
            'Go': [
                ('remove_cpp_comments',),
            ],
            'Swift': [
                ('remove_cpp_comments',),
            ],
            'Kotlin': [
                ('remove_cpp_comments',),
            ],
            'Scala': [
                ('remove_cpp_comments',),
            ],
            'C#': [
                ('remove_cpp_comments',),
            ],
            'Visual Basic': [
                ('remove_vb_comments',),
            ],
            'Fortran 77': [
                ('remove_fortran_comments',),
            ],
            'Fortran 90': [
                ('remove_fortran90_comments',),
            ],
            'Pascal': [
                ('remove_pascal_comments',),
            ],
            'Assembly': [
                ('remove_asm_comments',),
            ],
            'JSON': [
                ('remove_json_comments',),
            ],
            'YAML': [
                ('remove_yaml_comments',),
            ],
            'Markdown': [
                ('remove_markdown_comments',),
            ],
            'reStructuredText': [
                ('remove_rst_comments',),
            ],
            'TeX': [
                ('remove_tex_comments',),
            ],
            'Dockerfile': [
                ('remove_dockerfile_comments',),
            ],
            'make': [
                ('remove_make_comments',),
            ],
            'CMake': [
                ('remove_cmake_comments',),
            ],
        } 
    
    def detect_language(self, filepath: str) -> str:
        """Detect programming language from file extension or content"""
        path = Path(filepath)
        ext = path.suffix.lower().lstrip('.')
        
        # Check extension mapping
        if ext in self.language_by_extension:
            return self.language_by_extension[ext]
        
        # Check for shebang
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                first_line = f.readline().strip()
                if first_line.startswith('#!'):
                    return self._detect_from_shebang(first_line)
        except:
            pass
        
        return '(unknown)'
    
    def _detect_from_shebang(self, shebang: str) -> str:
        """Detect language from shebang line"""
        shebang = shebang.lower()
        if 'python' in shebang:
            return 'Python'
        elif 'perl' in shebang:
            return 'Perl'
        elif 'ruby' in shebang:
            return 'Ruby'
        elif 'bash' in shebang or 'sh' in shebang:
            return 'Bourne Again Shell'
        elif 'node' in shebang or 'nodejs' in shebang:
            return 'JavaScript'
        elif 'php' in shebang:
            return 'PHP'
        elif 'lua' in shebang:
            return 'Lua'
        elif 'r' in shebang:
            return 'R'
        elif 'julia' in shebang:
            return 'Julia'
        elif 'elixir' in shebang:
            return 'Elixir'
        return '(unknown)'
    
    def is_binary(self, filepath: str) -> bool:
        """Check if file is binary"""
        try:
            with open(filepath, 'rb') as f:
                chunk = f.read(1024)
                return b'\x00' in chunk
        except:
            return True
    
    def read_file(self, filepath: str) -> List[str]:
        """Read file and return lines"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return f.readlines()
        except UnicodeDecodeError:
            # Try with different encoding
            try:
                with open(filepath, 'r', encoding='latin-1') as f:
                    return f.readlines()
            except:
                return []
    
    def remove_blank_lines(self, lines: List[str]) -> Tuple[List[str], int]:
        """Remove blank lines and return remaining lines and blank count"""
        original_count = len(lines)
        non_blank = [line for line in lines if line.strip()]
        blank_count = original_count - len(non_blank)
        return non_blank, blank_count
    
    def remove_python_comments(self, lines: List[str]) -> List[str]:
        """Remove Python comments"""
        result = []
        in_multiline_string = False
        string_char = None
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                result.append(line)
                continue
            
            # Handle multiline strings
            if '"""' in line or "'''" in line:
                if not in_multiline_string:
                    # Start of multiline string
                    in_multiline_string = True
                    string_char = '"""' if '"""' in line else "'''"
                else:
                    # End of multiline string
                    if string_char in line:
                        in_multiline_string = False
                        string_char = None
            
            if in_multiline_string:
                result.append(line)
                continue
            
            # Remove single-line comments
            if '#' in line:
                # Find the # that's not inside a string
                in_string = False
                string_delimiter = None
                comment_pos = -1
                
                for i, char in enumerate(line):
                    if char in '"\'' and (i == 0 or line[i-1] != '\\'):
                        if not in_string:
                            in_string = True
                            string_delimiter = char
                        elif char == string_delimiter:
                            in_string = False
                            string_delimiter = None
                    elif char == '#' and not in_string:
                        comment_pos = i
                        break
                
                if comment_pos != -1:
                    line = line[:comment_pos]
                    if line.strip():
                        result.append(line + '\n')
                else:
                    result.append(line)
            else:
                result.append(line)
        
        return result
    
    def remove_python_docstrings(self, lines: List[str]) -> List[str]:
        """Remove Python docstrings"""
        result = []
        in_docstring = False
        docstring_delimiter = None
        
        for line in lines:
            stripped = line.strip()
            
            if not stripped:
                result.append(line)
                continue
            
            # Check for docstring start
            if stripped.startswith('"""') or stripped.startswith("'''"):
                if not in_docstring:
                    in_docstring = True
                    docstring_delimiter = stripped[:3]
                    # If docstring ends on same line, don't start
                    if stripped.endswith(docstring_delimiter) and len(stripped) > 3:
                        in_docstring = False
                        docstring_delimiter = None
                else:
                    # End of docstring
                    in_docstring = False
                    docstring_delimiter = None
                continue
            
            if in_docstring:
                # Skip docstring lines
                continue
            
            result.append(line)
        
        return result 
    
    def remove_cpp_comments(self, lines: List[str]) -> List[str]:
        """Remove C/C++ style comments"""
        result = []
        in_multiline_comment = False
        
        for line in lines:
            if not line.strip():
                result.append(line)
                continue
            
            # Handle multiline comments
            if '/*' in line and '*/' in line:
                # Single line multiline comment
                line = re.sub(r'/\*.*?\*/', '', line)
                if line.strip():
                    result.append(line)
                continue
            
            if '/*' in line:
                in_multiline_comment = True
                line = re.sub(r'/\*.*$', '', line)
                if line.strip():
                    result.append(line)
                continue
            
            if '*/' in line:
                in_multiline_comment = False
                line = re.sub(r'^.*?\*/', '', line)
                if line.strip():
                    result.append(line)
                continue
            
            if in_multiline_comment:
                continue
            
            # Remove single-line comments
            if '//' in line:
                line = line.split('//')[0]
                if line.strip():
                    result.append(line)
            else:
                result.append(line)
        
        return result 
    
    def remove_shell_comments(self, lines: List[str]) -> List[str]:
        """Remove shell comments"""
        result = []
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                result.append(line)
                continue
            
            # Remove comments (everything after #)
            if '#' in line:
                # Find # that's not inside quotes
                in_quotes = False
                quote_char = None
                comment_pos = -1
                
                for i, char in enumerate(line):
                    if char in '"\'' and (i == 0 or line[i-1] != '\\'):
                        if not in_quotes:
                            in_quotes = True
                            quote_char = char
                        elif char == quote_char:
                            in_quotes = False
                            quote_char = None
                    elif char == '#' and not in_quotes:
                        comment_pos = i
                        break
                
                if comment_pos != -1:
                    line = line[:comment_pos]
                    if line.strip():
                        result.append(line + '\n')
                else:
                    result.append(line)
            else:
                result.append(line)
        
        return result
    
    def remove_html_comments(self, lines: List[str]) -> List[str]:
        """Remove HTML comments"""
        result = []
        
        for line in lines:
            if not line.strip():
                result.append(line)
                continue
            
            # Remove HTML comments
            line = re.sub(r'<!--.*?-->', '', line)
            if line.strip():
                result.append(line)
        
        return result
    
    def remove_css_comments(self, lines: List[str]) -> List[str]:
        """Remove CSS comments"""
        result = []
        
        for line in lines:
            if not line.strip():
                result.append(line)
                continue
            
            # Remove CSS comments
            line = re.sub(r'/\*.*?\*/', '', line)
            if line.strip():
                result.append(line)
        
        return result
    
    def remove_sql_comments(self, lines: List[str]) -> List[str]:
        """Remove SQL comments"""
        result = []
        
        for line in lines:
            if not line.strip():
                result.append(line)
                continue
            
            # Remove SQL comments
            line = re.sub(r'--.*$', '', line)  # Single line comments
            line = re.sub(r'/\*.*?\*/', '', line)  # Multiline comments
            if line.strip():
                result.append(line)
        
        return result 
    
    def apply_filters(self, lines: List[str], language: str) -> List[str]:
        """Apply language-specific filters to remove comments"""
        if language not in self.filters_by_language:
            return lines
        
        filtered_lines = lines.copy()
        for filter_name in self.filters_by_language[language]:
            method_name = filter_name[0]
            if hasattr(self, method_name):
                method = getattr(self, method_name)
                filtered_lines = method(filtered_lines)
        
        return filtered_lines
    
    def count_file(self, filepath: str) -> Optional[CountResult]:
        """Count lines in a single file"""
        if not os.path.exists(filepath):
            return None
        
        if self.is_binary(filepath):
            return None
        
        language = self.detect_language(filepath)
        if language == '(unknown)':
            return None
        
        lines = self.read_file(filepath)
        if not lines:
            return CountResult(language, 0, 0, 0, 0)
        
        total_lines = len(lines)
        
        # Remove blank lines
        non_blank_lines, blank_count = self.remove_blank_lines(lines)
        
        # Apply comment filters
        code_lines = self.apply_filters(non_blank_lines, language)
        
        # Count remaining lines as code
        code_count = len(code_lines)
        
        # Calculate comment count
        comment_count = total_lines - blank_count - code_count
        
        return CountResult(
            language=language,
            blank=blank_count,
            comment=comment_count,
            code=code_count,
            total=total_lines
        )
    
    def count_directory(self, directory: str, exclude_dirs: Set[str] = None) -> Dict[str, CountResult]:
        """Count lines in all files in a directory"""
        if exclude_dirs is None:
            exclude_dirs = {'.git', '.svn', '.hg', '__pycache__', 'node_modules', 'vendor'}
        
        results = {}
        
        for root, dirs, files in os.walk(directory):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                filepath = os.path.join(root, file)
                result = self.count_file(filepath)
                if result:
                    results[filepath] = result
        
        return results
    
    def generate_report(self, results: Dict[str, CountResult], output_format: str = 'text') -> str:
        """Generate a report from counting results"""
        if not results:
            return "No files found to count.\n"
        
        # Aggregate by language
        language_stats = defaultdict(lambda: {'files': 0, 'blank': 0, 'comment': 0, 'code': 0})
        
        for result in results.values():
            lang = result.language
            language_stats[lang]['files'] += 1
            language_stats[lang]['blank'] += result.blank
            language_stats[lang]['comment'] += result.comment
            language_stats[lang]['code'] += result.code
        
        if output_format == 'json':
            return self._generate_json_report(language_stats)
        elif output_format == 'csv':
            return self._generate_csv_report(language_stats)
        else:
            return self._generate_text_report(language_stats)
    
    def _generate_text_report(self, language_stats: Dict) -> str:
        """Generate text report"""
        lines = []
        lines.append("Language                     files          blank        comment           code")
        lines.append("-" * 70)
        
        total_files = 0
        total_blank = 0
        total_comment = 0
        total_code = 0
        
        for lang, stats in sorted(language_stats.items()):
            lines.append(f"{lang:<30} {stats['files']:>8} {stats['blank']:>12} {stats['comment']:>12} {stats['code']:>12}")
            total_files += stats['files']
            total_blank += stats['blank']
            total_comment += stats['comment']
            total_code += stats['code']
        
        lines.append("-" * 70)
        lines.append(f"{'SUM':<30} {total_files:>8} {total_blank:>12} {total_comment:>12} {total_code:>12}")
        
        return '\n'.join(lines)
    
    def _generate_json_report(self, language_stats: Dict) -> str:
        """Generate JSON report"""
        report = {
            'languages': {},
            'total': {'files': 0, 'blank': 0, 'comment': 0, 'code': 0}
        }
        
        for lang, stats in language_stats.items():
            report['languages'][lang] = stats
            report['total']['files'] += stats['files']
            report['total']['blank'] += stats['blank']
            report['total']['comment'] += stats['comment']
            report['total']['code'] += stats['code']
        
        return json.dumps(report, indent=2)
    
    def _generate_csv_report(self, language_stats: Dict) -> str:
        """Generate CSV report"""
        lines = ['Language,files,blank,comment,code']
        
        for lang, stats in sorted(language_stats.items()):
            lines.append(f"{lang},{stats['files']},{stats['blank']},{stats['comment']},{stats['code']}")
        
        return '\n'.join(lines) 

    def remove_ruby_comments(self, lines: List[str]) -> List[str]:
        """Remove Ruby comments"""
        result = []
        
        for line in lines:
            if not line.strip():
                result.append(line)
                continue
            
            # Remove Ruby comments
            if '#' in line:
                line = line.split('#')[0]
                if line.strip():
                    result.append(line)
            else:
                result.append(line)
        
        return result
    
    def remove_perl_comments(self, lines: List[str]) -> List[str]:
        """Remove Perl comments"""
        result = []
        
        for line in lines:
            if not line.strip():
                result.append(line)
                continue
            
            # Remove Perl comments
            if '#' in line:
                line = line.split('#')[0]
                if line.strip():
                    result.append(line)
            else:
                result.append(line)
        
        return result
    
    def remove_vb_comments(self, lines: List[str]) -> List[str]:
        """Remove Visual Basic comments"""
        result = []
        
        for line in lines:
            if not line.strip():
                result.append(line)
                continue
            
            # Remove VB comments
            if "'" in line:
                line = line.split("'")[0]
                if line.strip():
                    result.append(line)
            else:
                result.append(line)
        
        return result
    
    def remove_fortran_comments(self, lines: List[str]) -> List[str]:
        """Remove Fortran comments"""
        result = []
        
        for line in lines:
            if not line.strip():
                result.append(line)
                continue
            
            # Remove Fortran comments (lines starting with C, c, *, or !)
            stripped = line.strip()
            if stripped and stripped[0] in 'Cc*!':
                continue
            
            result.append(line)
        
        return result
    
    def remove_fortran90_comments(self, lines: List[str]) -> List[str]:
        """Remove Fortran 90 comments"""
        result = []
        
        for line in lines:
            if not line.strip():
                result.append(line)
                continue
            
            # Remove Fortran 90 comments (lines starting with !)
            stripped = line.strip()
            if stripped and stripped[0] == '!':
                continue
            
            result.append(line)
        
        return result
    
    def remove_pascal_comments(self, lines: List[str]) -> List[str]:
        """Remove Pascal comments"""
        result = []
        in_multiline_comment = False
        
        for line in lines:
            if not line.strip():
                result.append(line)
                continue
            
            # Handle multiline comments
            if '{' in line and '}' in line:
                # Single line multiline comment
                line = re.sub(r'\{.*?\}', '', line)
                if line.strip():
                    result.append(line)
                continue
            
            if '{' in line:
                in_multiline_comment = True
                line = re.sub(r'\{.*$', '', line)
                if line.strip():
                    result.append(line)
                continue
            
            if '}' in line:
                in_multiline_comment = False
                line = re.sub(r'^.*?\}', '', line)
                if line.strip():
                    result.append(line)
                continue
            
            if in_multiline_comment:
                continue
            
            # Remove single-line comments
            if '//' in line:
                line = line.split('//')[0]
                if line.strip():
                    result.append(line)
            else:
                result.append(line)
        
        return result
    
    def remove_asm_comments(self, lines: List[str]) -> List[str]:
        """Remove assembly comments"""
        result = []
        
        for line in lines:
            if not line.strip():
                result.append(line)
                continue
            
            # Remove assembly comments (everything after ;)
            if ';' in line:
                line = line.split(';')[0]
                if line.strip():
                    result.append(line)
            else:
                result.append(line)
        
        return result
    
    def remove_json_comments(self, lines: List[str]) -> List[str]:
        """Remove JSON comments (JSON doesn't have comments, but some tools add them)"""
        result = []
        
        for line in lines:
            if not line.strip():
                result.append(line)
                continue
            
            # Remove JSON comments (// or /* */)
            line = re.sub(r'//.*$', '', line)
            line = re.sub(r'/\*.*?\*/', '', line)
            if line.strip():
                result.append(line)
        
        return result
    
    def remove_yaml_comments(self, lines: List[str]) -> List[str]:
        """Remove YAML comments"""
        result = []
        
        for line in lines:
            if not line.strip():
                result.append(line)
                continue
            
            # Remove YAML comments
            if '#' in line:
                line = line.split('#')[0]
                if line.strip():
                    result.append(line)
            else:
                result.append(line)
        
        return result
    
    def remove_markdown_comments(self, lines: List[str]) -> List[str]:
        """Remove Markdown comments (HTML comments)"""
        return self.remove_html_comments(lines)
    
    def remove_rst_comments(self, lines: List[str]) -> List[str]:
        """Remove reStructuredText comments"""
        result = []
        
        for line in lines:
            if not line.strip():
                result.append(line)
                continue
            
            # Remove RST comments
            if line.strip().startswith('.. '):
                continue
            
            result.append(line)
        
        return result
    
    def remove_tex_comments(self, lines: List[str]) -> List[str]:
        """Remove TeX comments"""
        result = []
        
        for line in lines:
            if not line.strip():
                result.append(line)
                continue
            
            # Remove TeX comments
            if '%' in line:
                line = line.split('%')[0]
                if line.strip():
                    result.append(line)
            else:
                result.append(line)
        
        return result
    
    def remove_dockerfile_comments(self, lines: List[str]) -> List[str]:
        """Remove Dockerfile comments"""
        result = []
        
        for line in lines:
            if not line.strip():
                result.append(line)
                continue
            
            # Remove Dockerfile comments
            if '#' in line:
                line = line.split('#')[0]
                if line.strip():
                    result.append(line)
            else:
                result.append(line)
        
        return result
    
    def remove_make_comments(self, lines: List[str]) -> List[str]:
        """Remove Makefile comments"""
        result = []
        
        for line in lines:
            if not line.strip():
                result.append(line)
                continue
            
            # Remove Makefile comments
            if '#' in line:
                line = line.split('#')[0]
                if line.strip():
                    result.append(line)
            else:
                result.append(line)
        
        return result
    
    def remove_cmake_comments(self, lines: List[str]) -> List[str]:
        """Remove CMake comments"""
        result = []
        
        for line in lines:
            if not line.strip():
                result.append(line)
                continue
            
            # Remove CMake comments
            if '#' in line:
                line = line.split('#')[0]
                if line.strip():
                    result.append(line)
            else:
                result.append(line)
        
        return result
    
    def remove_js_comments(self, lines: List[str]) -> List[str]:
        """Remove JavaScript-specific comments (same as C++ for now)"""
        return self.remove_cpp_comments(lines)
    
    def remove_php_comments(self, lines: List[str]) -> List[str]:
        """Remove PHP comments"""
        result = []
        
        for line in lines:
            if not line.strip():
                result.append(line)
                continue
            
            # Remove PHP comments
            line = re.sub(r'//.*$', '', line)  # Single line comments
            line = re.sub(r'#.*$', '', line)   # Shell-style comments
            line = re.sub(r'/\*.*?\*/', '', line)  # Multiline comments
            if line.strip():
                result.append(line)
        
        return result 


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Count Lines of Code (Python version)')
    parser.add_argument('paths', nargs='+', help='Files or directories to count')
    parser.add_argument('--exclude-dir', action='append', help='Directories to exclude')
    parser.add_argument('--format', choices=['text', 'json', 'csv'], default='text', 
                       help='Output format')
    parser.add_argument('--by-file', action='store_true', help='Show results by file')
    parser.add_argument('--version', action='version', version='cloc-py 1.0.0')
    
    args = parser.parse_args()
    
    counter = ClocCounter()
    all_results = {}
    
    exclude_dirs = set(args.exclude_dir or [])
    exclude_dirs.update({'.git', '.svn', '.hg', '__pycache__', 'node_modules', 'vendor'})
    
    for path in args.paths:
        if os.path.isfile(path):
            result = counter.count_file(path)
            if result:
                all_results[path] = result
        elif os.path.isdir(path):
            dir_results = counter.count_directory(path, exclude_dirs)
            all_results.update(dir_results)
        else:
            print(f"Warning: {path} does not exist", file=sys.stderr)
    
    if args.by_file:
        # Show results by file
        print("File,Language,Blank,Comment,Code,Total")
        for filepath, result in sorted(all_results.items()):
            print(f"{filepath},{result.language},{result.blank},{result.comment},{result.code},{result.total}")
    else:
        # Show aggregated results
        report = counter.generate_report(all_results, args.format)
        print(report)


if __name__ == '__main__':
    main() 