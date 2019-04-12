from setuptools import setup, find_packages

setup(
    name="philter",
    version="0.0.1",
    description="LUT creation toolkit.",
    author="nonlogicaldev",

    packages=find_packages(),
    scripts=[
        "bin/philter"
    ]
)

