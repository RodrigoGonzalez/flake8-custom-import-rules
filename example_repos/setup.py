""" The setup.py file for example base module. """
from setuptools import find_packages
from setuptools import setup

setup(
    name="my_base_module",
    description="An example base module",
    version="0.0.1",
    packages=find_packages(),
    install_requires=["attrs", "pendulum"],
    extras_require={"dev": ["pytest"]},
)
