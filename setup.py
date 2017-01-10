from setuptools import setup, find_packages

setup(name='grapheap',
      version='0.1',
      description='Read optimised graph, inspired by heap',
      long_description='Read http://github.com/practo/grapheap',
      keywords='grapheap graph heap python node memcache',
      url='http://github.com/practo/grapheap',
      author='Sourabh Deokar (wilspi)',
      author_email='thewilspi@gmail.com',
      license='MIT',
      packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      install_requires=[
          'pylibmc',
      ],
      include_package_data=True,
      zip_safe=False)
