from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="nl-philter",
    version="0.0.2",
    author="nonlogicaldev",

    description="cLUT/Cube toolkit for recording color transformations.",
    long_description=long_description,
    long_description_content_type='text/markdown',

    install_requires=[
        "numpy>=1.16.2",
        "Pillow>=6.2.0",
    ],

    packages=find_packages(),
    scripts=[
        "bin/philter"
    ]
)

