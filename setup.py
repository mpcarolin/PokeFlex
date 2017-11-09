try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='PokedexFlexApi',
    version='0.0.1',
    author='Michael Carolin',
    packages=[],
    install_requires=['Flask-API'],
    license='Apache License 2.0',
    long_description=open('README.md').read()
)
