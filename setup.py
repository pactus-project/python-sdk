from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = "0.0.1"
DESCRIPTION = "Pactus development kit"
LONG_DESCRIPTION = "This SDK is used to provide python utilities to interact with the Pactus blockchain, create transactions, sign messages or generate keys."

# Setting up
setup(
    name="pactus-sdk",
    version=VERSION,
    author="Pactus foundation",
    author_email="<info@pactus.org>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=["ripemd", "bech32m"],
    keywords=["pactus", "blockchain", "web3", "dapp", "bls", "bech32"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
