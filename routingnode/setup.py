# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

# with open('LICENSE') as f:
#     license = f.read()

setup(
    name='covacomputenode',
    version='0.1.0',
    description='COVA Compute Node',
    long_description=readme,
    author='Covalent Foundation',
    author_email='contact@covalent.ai',
    url='https://covalent.ai',
    # license=license,
    packages=find_packages(exclude=('tests'))
)

