from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="Blackwing Client",
    version="0.0.1",
    author="Sergio Branco | The Architech",
    author_email="asergio.branco@gmail.com",
    description="Blackwing is a decentralized network package, to build strong, powerfull and secure applications.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://blackwing.readthedocs.io",
    packages=['bwclient'],
    package_dir={'': 'src'},
    package_data={
        '': ['*.md'],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Network"
    ],
)
