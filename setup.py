from setuptools import setup, find_packages

setup(name='bdrcmodels',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'eulfedora>=1.7.2',
        'bdrxml==0.8a1',
    ],
    dependency_links=[
        'https://github.com/Brown-University-Library/bdrxml/archive/v0.8a1.zip#egg=bdrxml-0.8a1',
    ],
)
