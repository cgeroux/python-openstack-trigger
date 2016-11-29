import re
from setuptools import setup

version = re.search(
  '^__version__\s*=\s*"(.*)"',
  open('openstack_trigger/openstack_trigger.py').read(),
  re.M
  ).group(1)

with open("README.md", "rb") as f:
  long_descr = f.read().decode("utf-8")
    
setup(
  name="openstack_trigger",
  packages=["openstack_trigger"],
  entry_points={"console_scripts":['openstack-trigger=openstack_trigger.openstack_trigger:main']},
  version=version,
  description="Uses ganglia XML to trigger python-openstack-executor actions.",
  long_description=long_descr,
  author="Chris Geroux",
  author_email="chris.geroux@ace-net.ca",
  url="",
  test_suite='nose.collector',
  test_require=['nose'],
  include_package_data=True
  )