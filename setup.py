from pathlib import Path

from setuptools import find_packages, setup

setup(
    name="pactus-sdk",
    version="1.2.3",
    author="Pactus Development Team",
    author_email="info@pactus.org",
    description="Pactus Development Kit",
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/pactus-project/python-sdk",
    packages=find_packages(),
    license="MIT",
    install_requires=[
        "pactus_grpc",
        "ripemd-hash",
        "grpcio",
        "grpcio-tools",
        "cryptography>=43.0",
        "zmq",
    ],
    keywords=["pactus", "blockchain", "sdk", "web3", "dapp", "bls", "bech32"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
