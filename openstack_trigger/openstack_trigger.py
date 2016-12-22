from __future__ import print_function

__version__ = "1.0.0"

import optparse as op
from lxml import etree
import os
from .TriggerManager import TriggerManager
from .Ganglia import Ganglia
import openstack_executor

def addParserOptions(parser):
  """Adds command line options
  """
  
  parser.add_option("--ganglia-host"
    ,dest="gangliaHost"
    ,help="Sets the host the ganglia master daemon is running on "\
    +"[default: %default]."
    ,default="localhost")
  
  parser.add_option("--ganglia-port"
    ,dest="gangliaPort"
    ,help="Sets the port the ganglia master daemon is listening on "\
    +"[default: %default]."
    ,default="8651")
  
  parser.add_option("--list-metrics",dest="listMetrics"
    ,action="store_true",default=False
    ,help="Only list available ganglia metrics and stop. Useful to see what "
    +"metrics are available to trigger on [not default].")
  
  openstack_executor.addParserOptions(parser)
def parseOptions():
  """Parses command line options
  
  """
  
  parser=op.OptionParser(usage="Usage: %prog [options] SETTINGS.xml"
    ,version="%prog "+__version__,description="")
  
  #add options
  addParserOptions(parser)
  
  #parse command line options
  return parser.parse_args()
#def processTriggers(xmlTriggers,options,path):
#  """
#  """
#  
#
#  
#  ###
#  #Redo below code
#  
#  #get metric node
#  xmlMetric=xmlTrigger.find("metric")
#  metricName=xmlMetric.find("name").text
#  metricCombine=xmlMetric.find("combine").text
#  
#  metricHostNames=[]
#  xmlHosts=xmlMetric.find("hosts")
#  for xmlHostName in xmlHosts:
#    metricHostNames.append(xmlHostName.text)
#  
#  
#  print("metricName:"+metricName)
#  print("metricCombine:"+metricCombine)
#  print("reference:"+str(reference))
#  print("comparison:"+str(comparison))
#  print("action-file:"+actionFile)
#  
#  print("metricHostNames:"+str(metricHostNames))
#  
#  #get all hosts which contributed to the metric
#  hostNames=ganglia.getHostNames()
#  filteredHostNames=set()
#  for metricHostName in metricHostNames:
#    filteredHostNames=filteredHostNames.union(
#      set(fnmatch.filter(hostNames,metricHostName)))
#  
#  #TODO: think about how to add string support for this
#  #  not entirely sure it makes sense to add string support
#  #  as many of the string fields are fixed data about a host
#  #  that doesn't change, thus not something you would likely
#  #  want to trigger on.
#  
#  #combine values form the contributing hosts
#  if metricCombine=="max":
#    combinedMetric=-1.0*sys.float_info.max
#  elif metricCombine=="min":
#    combinedMetric=sys.float_info.max
#  elif metricCombine=="sum" or metricCombine=="ave":
#    combinedMetric=0.0
#  if metricCombine=="ave":
#    count=0
#  for hostName in filteredHostNames:
#    value=ganglia.getMetricValueForHost(metricName,hostName)
#    
#    if metricCombine=="max":
#      if float(value)>combinedMetric:
#        combinedMetric=float(value)
#    elif metricCombine=="min":
#      if float(value)<combinedMetric:
#        combinedMetric=float(value)
#    elif metricCombine=="sum" or metricCombine=="ave":
#      combinedMetric=combinedMetric+float(value)
#    if metricCombine=="ave":
#      count+=1
#  if metricCombine=="ave":
#    combinedMetric=combinedMetric/float(count)
#  
#  #test for triggering an action
#  trigger=False
#  if comparison=="lt":
#    if combinedMetric < reference:
#      trigger=True
#  elif comparison=="gt":
#    if combinedMetric > reference:
#      trigger=True
#  elif comparison=="eq":
#    if combinedMetric == reference:
#      trigger=True
#  elif comparison=="ne":
#    if combinedMetric != reference:
#      trigger=True
#  elif comparison=="le":
#    if combinedMetric <= reference:
#      trigger=True
#  elif comparison=="ge":
#    if combinedMetric >= reference:
#      trigger=True
#  
#  print("metric from hostnames:"+str(filteredHostNames))
#  print("combined metric value:"+str(combinedMetric))
#  print("trigger:"+str(trigger))
#  if trigger:
#    
#    #if relative path, correct
#    if actionFile[0:2]=="./":
#      actionFile=os.path.join(path,actionFile)
#    f=open(actionFile,'r')
#    openstack_executor.run(f.read(),options)
def main():
  
  #parse command line options
  (options,args)=parseOptions()
  
  if options.listMetrics:
    #print out ganglia metrics
    ganglia=Ganglia(host=options.gangliaHost,port=options.gangliaPort)
    ganglia.printMetrics()
  else:
    
    #check we got the expected number of arguments
    if (len(args)!=1):
      raise Exception("Expected an xml settings file.")
    
    #load schema to validate against
    schemaFileName=os.path.join(os.path.dirname(__file__)
      ,"xmlSchema/triggers.xsd")
    schema=etree.XMLSchema(file=schemaFileName)
    
    #parse xml file
    tree=etree.parse(args[0])
    
    #strip out any comments in xml
    comments=tree.xpath('//comment()')
    for c in comments:
      p=c.getparent()
      p.remove(c)
    
    #validate against schema
    schema.assertValid(tree)
    
    #get path to settings file
    settingsPath=os.path.dirname(args[0])
    options.path=settingsPath
    
    #Initialize all triggers
    triggerManager=TriggerManager(tree.getroot(),options)
    
    #check triggers and perform any triggered actions
    triggerManager.run()
    
    #process triggers 
    #TODO: at some point will likely want to loop on processTriggers
    #  though I will need a cool down time for the various triggers, and keep
    #  track of the last time a trigger was triggered. Seems like I will need
    #  a trigger class
    #processTriggers(tree.getroot(),options,settingsPath)
  

