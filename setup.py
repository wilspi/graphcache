from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='grapheap',
      version='0.1',
      description='Read optimised graph, inspired by heap',
      long_description=readme(),
      keywords='grapheap graph heap python node memcache',
      url='http://github.com/practo/grapheap',
      author='Sourabh Deokar (wilspi)',
      author_email='thewilspi@gmail.com',
      license='MIT',
      packages=['grapheap'],
      install_requires=[
          'pylibmc',
      ],
      include_package_data=True,
      zip_safe=False)
