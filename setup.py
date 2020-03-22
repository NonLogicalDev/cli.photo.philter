from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="philter",
    version="0.0.1",
    description="LUT creation toolkit.",
    author="nonlogicaldev",

    install_requires=requirements,
    packages=find_packages(),
    scripts=[
        "bin/philter"
    ]
)

