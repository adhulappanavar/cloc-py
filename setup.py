#!/usr/bin/env python3
"""
Setup script for cloc-py
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

setup(
    name="cloc-py",
    version="1.0.0",
    author="Anil Dhulappanavar",
    author_email="adhula@gmail.com",
    description="Python implementation of cloc (Count Lines of Code)",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/adhulappanavar/cloc-py",
    py_modules=["cloc_py"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "cloc-py=cloc_py:main",
        ],
    },
    keywords="cloc, lines of code, code metrics, programming languages",
    project_urls={
        "Bug Reports": "https://github.com/adhulappanavar/cloc-py/issues",
        "Source": "https://github.com/adhulappanavar/cloc-py",
        "Documentation": "https://github.com/adhulappanavar/cloc-py#readme",
        "Original cloc": "https://github.com/AlDanial/cloc",
    },
    # Additional metadata for attribution
    maintainer="Anil Dhulappanavar",
    maintainer_email="adhula@gmail.com",
    # Note: This is based on the original cloc by Al Danial
    # Original cloc: Copyright (C) 2006-2025, Al Danial <al.danial@gmail.com>
) 