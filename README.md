Uses [ganglia](http://ganglia.info/) XML to trigger [python-openstack-executor](https://github.com/cgeroux/python-openstack-executor) actions. This could be used for automatically creating/remove VMs based on various ganglia metrics, attaching new volumes etc.


Requirements
============

+ Python2.6+

+ pip or pip3

  for installing lxml
  
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
  
+ [python-openstack-executor](https://github.com/cgeroux/python-openstack-executor)


If running in an OpenStack VM
=============================

There is a cloud init file which will provision a VM with the correct installation of Ganglia, python, openstack client, apache2, etc. required by python-openstack-trigger as well as python-openstack-trigger its self. This is likely the simplest way to get started. This script is in `python-openstack-trigger/openstack_trigger/cloud_init_setup/ganglia_master.yaml`. This script has been used with the CC cloud images `ubuntu-server-16.04-amd64` and `ubuntu-server-14.04-amd64` on west-cloud and will likely work with most Ubuntu based images. For images of other Linux OSs the package names will likely be different, and the location of some configuration files may change. 

To use this script see the CC documetation on using [CloudInit](https://docs.computecanada.ca/wiki/OpenStack_VM_Setups#Using_CloudInit).

Once you have provisiond a new VM using the `ganglia_master.yaml` script you will need to copy over your CC cloud credentials file, see [Connecting CLI to OpenStack](https://docs.computecanada.ca/wiki/OpenStack_Command_Line_Clients#Connecting_CLI_to_OpenStack) as the [python-openstack-executor](https://github.com/cgeroux/python-openstack-executor) uses the same method to connect to your OpenStack project to perform actions.

Installing openstack-trigger Manually
=====================================

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

For an example of a `SETTINGS.XML` file look at `python-openstack-trigger/openstack_trigger/example_xml/example.xml`. In addition there is some help on various options avabile by running `openstack-trigger -h`.
