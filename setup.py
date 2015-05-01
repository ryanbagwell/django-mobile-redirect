#/usr/bin/env python
import codecs
import os
from setuptools import setup, find_packages


read = lambda filepath: codecs.open(filepath, 'r', 'utf-8').read()

setup(
    name='django-mobile-redirect',
    version='1.0.0',
    description='Redirects devices with mobile user agent strings to a specified url.',
    long_description=read(os.path.join(os.path.dirname(__file__), 'README.rst')),
    author='Ryan Bagwell',
    author_email='ryan@ryanbagwell.com',
    license='MIT',
    url='https://github.com/ryanbagwell/django-mobile-redirect',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'Django>=1.5',
    ],
)
