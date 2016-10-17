from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='linkcom',
    version='0.1',
    description='Runs link community detection with networkx graphs.',
    author='Nathaniel Rodriguez',
    packages=['linkcom'],
    url='https://github.com/Nathaniel-Rodriguez/linkcom.git',
    install_requires=[
          'networkx'
      ],
    include_package_data=True,
    zip_safe=False)