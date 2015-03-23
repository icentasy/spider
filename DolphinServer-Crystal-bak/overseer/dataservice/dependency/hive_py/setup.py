from distutils.core import setup
from setuptools.extension import Extension
from setuptools import find_packages


setup(name='hive',
      version='0.1',
      description='web framework armory',
      author="yeqing liao",
      author_email="yqliao@bainainfo.com",
      packages=find_packages('hive'),
      package_dir={'': 'hive'},
      include_package_data=True,
      install_requires=[])
