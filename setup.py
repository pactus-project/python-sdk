import codecs
from pathlib import Path

from setuptools import find_packages, setup

here = Path.abspath(Path.dirname(__file__))

with codecs.open(here / "README.md", encoding="utf-8") as fh:
    long_description = fh.read()

NAME = "pactus-sdk"
VERSION = "1.0.0"
AUTHOR = "Pactus Foundation"
AUTHOR_EMAIL = "info@pactus.org"
DESCRIPTION = "Pactus development kit"
LONG_DESCRIPTION_CONTENT_TYPE = "text/markdown"
URL = "https://github.com/pactus-project/python-sdk"

# Package dependencies
REQUIRED = [
    "ripemd",
    "bech32m",
]

CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Operating System :: OS Independent",
]

setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    url=URL,
    packages=find_packages(),
    install_requires=REQUIRED,
    keywords=["pactus", "blockchain", "web3", "dapp", "bls", "bech32"],
    classifiers=CLASSIFIERS,
    python_requires=">=3.6",
)
