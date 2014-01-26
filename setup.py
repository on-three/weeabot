# vim: set ts=2 expandtab:
from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='weeabot',
  version='0.1',
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
    'weeabot.jisho',
    'weeabot.webserver',
  ],
  install_requires=[
    'twisted',
    'argparse',
    'romkan',
    'beautifulsoup4',
    'pytz',
    'django',
  ],
	data_files=[
    ('/etc/init',
      [
      'daemon/weeabot.conf',
      'daemon/weeabot.override',
      ])
  ],
	package_data = {
    '': ['*.html', '*.rst', '*.css'],
	},
  entry_points = {
    'console_scripts': [
      'weeabot-daemon=weeabot:main',
			'weeabot-django-manage=weeabot.manage:main',
    ],
  },
  zip_safe=True)
