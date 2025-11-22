from setuptools import setup, find_packages

setup(
    name="topcap",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=2.0",
        "matplotlib>=3.9",
        "networkx>=3.2",
    ],
    python_requires=">=3.7",
    author="Léo Brucker",
    description="A package for topcap game with heuristics and plotting",
)
