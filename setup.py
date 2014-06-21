from setuptools import setup, find_packages

setup(
    name='candv',
    version='1.1.1',
    description="Constants and Values: create grouped non-standard named "
                "constants, add values, verbose names, help hexts or anything "
                "you like to them",
    license='LGPLv3',
    url='https://github.com/oblalex/candv',
    author='Alexander Oblovatniy',
    author_email='oblovatniy@gmail.com',
    packages=find_packages(),
    install_requires=[i.strip() for i in open("requirements.pip").readlines()],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries',
    ],
)
