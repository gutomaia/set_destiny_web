# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os


here = os.path.abspath(os.path.dirname(__file__))


with open(os.path.join(here, 'requirements.txt')) as f:
    REQUIREMENTS = [line for line in iter(f)]


setup(
    name='set-destiny-web',
    version='0.0.0',
    author="Guto Maia",
    license="Mit",
    packages=find_packages(exclude=["*.tests", "*.tests.*"]),
    classifiers=[
        'Development Status :: 3 - Alpha',
    ],
    include_package_data=True,
    install_requires=REQUIREMENTS,
)
