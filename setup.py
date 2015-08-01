# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages


__here__ = os.path.abspath(os.path.dirname(__file__))

README = open(os.path.join(__here__, 'README.rst')).read()
REQUIREMENTS = [
    i.strip() for i in
    open(os.path.join(__here__, 'requirements', 'dist.txt')).readlines()
]

setup(
    name='candv',
    version='1.3.1',
    description="Constants and Values: create grouped non-standard named "
                "constants, add values, verbose names, help texts or anything "
                "you like to them",
    long_description=README,
    keywords=[
        'constants', 'values', 'structures', 'choices',
    ],
    license='LGPLv3',
    url='https://github.com/oblalex/candv',
    author='Alexander Oblovatniy',
    author_email='oblovatniy@gmail.com',
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries',
    ],
    platforms=[
        'any',
    ],
)
