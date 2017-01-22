#! /usr/bin/env python3
"""
license: PD
"""

from setuptools import setup

version = "0.1"


entry_points = {"gui_scripts": []}

install_requirements = []
# for certificate generation
install_requirements += ["cryptography>=1.1"]
# for pidlock
install_requirements += ["psutil>=3.0"]
# require speed by default
install_requirements += speed_requirements

install_extras = {}
# for markdown help
install_extras["leds"] = ["gpiozero"]

entry_points["gui_scripts"].append('wakemeupextreme = wakemeupextreme.__main__:main')

# plugins imported by MANIFEST.in
setup(name='wakemeupextreme',
      version=version,
      #version_format='{tag}',
      description='Wake me up with math',
      license='Public Domain',
      url='https://github.com/devkral/wakemeupextreme',
      download_url='https://github.com/devkral/wakemeupextreme/tarball/'+version,
      entry_points=entry_points,
      #zip_safe=True,
      platforms='Platform Independent',
      include_package_data=True,
      install_requires=install_requirements,
      extras_require=install_extras,
      packages=['wakemeupextreme'],
      classifiers=[
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3 :: Only',
          'Topic :: Communications',
          'Topic :: Internet',
          'Topic :: Security'],
      keywords=['alarm', 'clock'])
