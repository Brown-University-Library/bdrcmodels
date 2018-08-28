from setuptools import setup, find_packages

setup(name='bdrcmodels',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'ply==3.8',
        'eulfedora>=1.7.2',
        'bdrxml==0.8.1',
    ],
    dependency_links=[
        'https://github.com/Brown-University-Library/bdrxml/archive/v0.8.1.zip#egg=bdrxml-0.8.1',
    ],
)
