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
  
  Noticed gmond was using nearly 100% of CPU on slave nodes, this [link ](https://adamo.wordpress.com/2015/05/27/gmond-occupying-100-of-the-cpu/) describes how to fix it.
  
  Also, this contains a bunch of extra metrics which are nice for linux, io,fs, multiple_cpu
  
  ```sudo apt-get install ganglia-modules-linux```
  
  then edit config. files for this module in /etc/ganglia/conf.d (e.g. mod_fs.conf-sample, mod_multicpu.conf-sample)
  
  
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