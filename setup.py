try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='PokeFlex',
    version='0.0.1',
    author='Michael Carolin, Ben Churchill',
    packages=[],
    install_requires=['Flask-API'],
    license='Apache License 2.0',
    long_description=open('README.md').read()
)
