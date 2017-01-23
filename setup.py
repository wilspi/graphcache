from setuptools import setup, find_packages
from os.path import expanduser


setup(name='grapheap',
      version='0.1',
      description='Read optimised graph, inspired by heap',
      long_description='Read http://github.com/practo/grapheap',
      keywords='grapheap graph heap python node memcache',
      url='http://github.com/practo/grapheap',
      author='Sourabh Deokar (wilspi)',
      author_email='thewilspi@gmail.com',
      license='MIT',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
      ],
      packages=find_packages(
          exclude=[
              "*.tests",
              "*.tests.*",
              "tests.*",
              "tests"]),
      data_files=[
          (expanduser("~") +
           '/grapheap_configs',
           ['config/cache.conf'])],
      install_requires=[
          'pylibmc',
      ],
      include_package_data=True,
      zip_safe=False)
