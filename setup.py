from setuptools import setup, find_packages
from os.path import expanduser

setup(
    name="graphcache",
    version="0.1.2",
    description="Python library to store connected nodes and their properties on cache storage",
    long_description="Read http://github.com/wilspi/graphcache",
    keywords="graphcache graph cache python node memcache",
    url="http://github.com/wilspi/graphcache",
    author="wilspi",
    author_email="the.wilspi@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
    ],
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    data_files=[(expanduser("~") + "/", ["config/graphcache_config.conf"])],
    install_requires=["pylibmc"],
    include_package_data=True,
    zip_safe=False,
)
