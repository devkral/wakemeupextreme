#! /usr/bin/env python3
__license__ = "Public Domain"

from setuptools import setup

version = "0.1"


entry_points = {"gui_scripts": []}

install_requirements = []

install_extras = {}
# for markdown help
install_extras["leds"] = ["gpiozero"]

entry_points["gui_scripts"].append('wakemeupextreme = wakemeupextreme.__main__:main')

# plugins imported by MANIFEST.in
setup(name='wakemeupextreme',
      version=version,
      #version_format='{tag}',
      description='Wake me up with math',
      license='MIT',
      author='Alexander K.',
      author_email='devkral@web.de',
      url='https://github.com/devkral/wakemeupextreme',
      download_url='https://github.com/devkral/wakemeupextreme/tarball/'+version,
      entry_points=entry_points,
      #zip_safe=True,
      platforms='Platform Independent',
      install_requires=install_requirements,
      extras_require=install_extras,
      packages=['wakemeupextreme'],
      classifiers=[
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3 :: Only'],
      keywords=['alarm', 'clock'])
