# vim: set ts=2 expandtab:
from setuptools import setup

#version 0.2: include basic webserver and jisho database display
#version 0.3: added katakanize function
#version 0.4: Removed web backend for easier running
#             Web backend still available in weeabot_site repository.

def readme():
    with open('README.md') as f:
        return f.read()

def requirements():
  with open('requirements.txt') as f:
    return f.read().splitlines()

setup(name='weeabot',
  version='0.4',
  description='Japanese support IRC bot.',
  long_description = readme(),
	classifiers=[
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.7',
    'Topic :: Communications :: Chat :: Internet Relay Chat',
  ],
  keywords = 'irc bot japan japanese definitions lookup',
  url='https://github.com/on-three/weeabot',
  author='on_three',
  author_email='on.three.email@gmail.com',
  license='MIT',
  packages=[
    'weeabot',
  ],
  install_requires = requirements(),
  entry_points = {
    'console_scripts': [
      'weeabot-daemon=weeabot:main',
    ],
  },
  zip_safe=True)
