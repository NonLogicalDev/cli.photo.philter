from setuptools import setup, find_packages

setup(
    name="philter",
    version="0.0.1",
    description="LUT creation toolkit.",
    author="nonlogicaldev",

    install_requires=[
        "numpy>=1.16.2",
        "Pillow>=6.0.0",
    ],

    packages=find_packages(),
    scripts=[
        "bin/philter"
    ]
)

