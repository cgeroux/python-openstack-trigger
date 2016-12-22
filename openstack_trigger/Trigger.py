import openstack_executor
import os
import sys
import fnmatch

class Trigger(object):
  """
  """
  
  def __init__(self,xml,options):
    """
    """
    
    self.options=options
    xmlMetric=xml.find("metric")
    self.metricName=xmlMetric.find("name").text
    self.metricCombine=xmlMetric.find("combine").text
    self.reference=float(xml.find("reference").text)
    self.comparison=xml.find("comparison").text
    self.actionFile=xml.find("action-file").text
    if self.actionFile[0:2]=="./":
      self.actionFile=os.path.join(self.options.path,self.actionFile)
    xmlHosts=xmlMetric.find("hosts")
    self.metricHostNames=[]
    for xmlHostName in xmlHosts:
      self.metricHostNames.append(xmlHostName.text)
    
    #TODO: remove below once initial debugging complete
    #print out settings for debugging
    print("metricName:"+self.metricName)
    print("metricCombine:"+self.metricCombine)
    print("reference:"+str(self.reference))
    print("comparison:"+str(self.comparison))
    print("action-file:"+self.actionFile)
    print("metricHostNames:"+str(self.metricHostNames))
  def check(self,hostNames,getMetricValueForHost):
    """Check if trigger conditions met
    """
    
    #get all hosts which contributed to the metric
    filteredHostNames=set()
    for metricHostName in self.metricHostNames:
      filteredHostNames=filteredHostNames.union(
        set(fnmatch.filter(hostNames,metricHostName)))
    
    #combine values form the contributing hosts
    if self.metricCombine=="max":
      combinedMetric=-1.0*sys.float_info.max
    elif self.metricCombine=="min":
      combinedMetric=sys.float_info.max
    elif self.metricCombine=="sum" or metricCombine=="ave":
      combinedMetric=0.0
    if self.metricCombine=="ave":
      count=0
    for hostName in filteredHostNames:
      value=getMetricValueForHost(self.metricName,hostName)
      
      if self.metricCombine=="max":
        if float(value)>combinedMetric:
          combinedMetric=float(value)
      elif self.metricCombine=="min":
        if float(value)<combinedMetric:
          combinedMetric=float(value)
      elif self.metricCombine=="sum" or metricCombine=="ave":
        combinedMetric=combinedMetric+float(value)
      if self.metricCombine=="ave":
        count+=1
    if self.metricCombine=="ave":
      combinedMetric=combinedMetric/float(count)
    
    #test for triggering an action
    if self.comparison=="lt":
      if combinedMetric < self.reference:
        return True
    elif self.comparison=="gt":
      if combinedMetric > self.reference:
        return True
    elif self.comparison=="eq":
      if combinedMetric == self.reference:
        return True
    elif self.comparison=="ne":
      if combinedMetric != self.reference:
        return True
    elif self.comparison=="le":
      if combinedMetric <= self.reference:
        return True
    elif self.comparison=="ge":
      if combinedMetric >= self.reference:
        return True
    return False
  def performAction(self):
    """
    """
    
    f=open(self.actionFile,'r')
    
    
    
    
    openstack_executor.run(f.read(),self.options)
    
    #TODO: Resource names should have some way to indicate they are incremented