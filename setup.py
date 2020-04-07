from setuptools import setup, find_packages
from os import path

with open(
    path.join(path.abspath(path.dirname(__file__)), "README.md"), encoding="utf-8"
) as f:
    long_description = f.read()

setup(
    name="graphcache",
    version="0.1.4",
    description="Python library to store connected nodes and their properties on cache storage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="graphcache graph cache python node redis",
    url="http://github.com/wilspi/graphcache",
    author="wilspi",
    author_email="the.wilspi@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=["redis==3.4.1"],
    include_package_data=True,
    zip_safe=False,
)
