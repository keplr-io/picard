from setuptools import setup, find_packages

setup(
    name='picard',
    version="2.0",
    author="Jake Bian",
    author_email="jake@keplr.io",
    description=('Distributed model architecture optimization for neural nets'),
    license='fuckyou',
    keywords='picard',
    packages=find_packages(),
    install_requires=[
        'keras',
        'tensorflow',
        'flask',
        'flask_cors',
        'gevent',
        'numpy',
        'networkx',
        'hyperopt'
    ]
)
