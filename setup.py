from setuptools import setup

# read the contents of README file as long description
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'centrify.PySDK',
  packages = ['PySDK'],
  version = '0.1', 
  description = 'Set up to do REST API calls and authentication via Oauth Token',
  author = 'Andrew Schilling',
  author_email = 'andrew.schilling@centrify.com',
  url = 'https://github.com/ajskrilla/PySDK',
  download_url = 'https://github.com/ajskrilla/PySDK/archive/v0.1-alpha.tar.gz',
  keywords = ['PySDK', 'Windows', 'Linux', 'PAS'],
  install_requires=[pandas, requests, configparser],
  classifiers=[
    'Operating System :: POSIX :: Linux'
  ],
)
