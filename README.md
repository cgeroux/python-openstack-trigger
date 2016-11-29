Uses ganglia XML to trigger python-openstack-executor actions.

Requirements
============

+ Python2.6+
  
  Already available on ACENET machines and most current Linux 
  distributions. Tested specifically with Python3.4.1 and Python2.7.10

+ pip or pip3
  
  Already available on ACENET machines, if not on an ACENET machine 
  search within your Linux distribution package manager for pip (e.g. 
  "apt-cache search pip" and install with "apt-get install 
  <pip-package-name>" in Ubuntu)
  
+ lxml
  
  If you have admin access on your server do:
  ```
  sudo pip install lxml
  ```
  otherwise do:
  ```
  pip install --user lxml
  ```
  Or if using python3 with pip3 then replace ```pip``` with ```pip3```
+ Ganglia
  
  Should be setup and configured on your cluster nodes. Here is a good [page describing](https://www.digitalocean.com/community/tutorials/introduction-to-ganglia-on-ubuntu-14-04) how to do that.
  
  
Installation openstack-trigger
===============================

From inside the python-openstack-trigger directory run:

```
$ python setup.py install --user
```

to install to your home directory. The --record <filename> option will output 
a list of files created during install.


Usage
=====

To run the program use the command:

```
$ openstack-trigger SETTINGS.XML
```