from distutils.core import setup
from setuptools import find_packages


setup(name='overseer',
      version='1.1',
      description='report framework multalisk',
      author="Xiang Shu",
      author_email="xshu@bainainfo.com",
      packages=find_packages('src'),
      package_dir={'': 'src'},
      include_package_data=True,
      scripts=[
      ],
      install_requires=[
          # 'celery >= 3.1.13',
          # 'pytz >= 2014.10',
      ])
