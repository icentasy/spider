from distutils.core import setup
from setuptools import find_packages


setup(name='pylon',
      version='0.1',
      description='web framework pylon',
      author="xiaoyu ren",
      author_email="xyren@bainainfo.com",
      packages=find_packages('src'),
      package_dir={'': 'src'},
      include_package_data=True,
      install_requires=[
          'flask >= 0.9'
      ])
