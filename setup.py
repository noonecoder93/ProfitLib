#!/usr/bin/env python
from setuptools import setup, find_packages
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='ProfitLib',
    version='0.1',
    description='altcoin mining profitability calculator',
    long_description=read('README.md'),
    url='https://github.com/salfter/ProfitLib',
    py_modules=['ProfitLib'],
    zip_safe=False,
    install_requires=["jsonrpc","PyCryptsy","python-bittrex","PyCCEX","PyCryptopia","poloniex","bleuBot"],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ],
)
