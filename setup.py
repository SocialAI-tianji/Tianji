from setuptools import setup, find_packages

setup(
    name="tianji",
    version="1.0",
    packages=find_packages(exclude=["build", "dist"]),
)
