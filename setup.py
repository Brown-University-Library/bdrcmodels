from setuptools import setup, find_packages

setup(name='bdrcmodels',
    version='0.3a1',
    packages=find_packages(),
    install_requires=[
        'eulfedora>=1.7.2',
        'bdrxml @ https://github.com/Brown-University-Library/bdrxml/archive/v1.0a1.zip#sha1=5802ed82ee80a9627657cbb222fe9c056f73ad2c',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
