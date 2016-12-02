import telnetlib
from lxml import etree

class Ganglia(object):
  """
  """
  
  def __init__(self,host=None,port=None,xml=None):
    """
    """
    
    self.host=host
    self.port=port
    self.xml=xml
    self.hostsData=None
  def getData(self):
    """Get data from the Ganglia host
    
    Will overwrite any previous data with more up-to-date data
    it is stored in self.hosts
    """
    
    if self.host==None or self.port==None:
      raise Exception("Both host and port not set. Have host=\""
        +str(self.host)+"\", port="+str(self.port))
    
    tn=telnetlib.Telnet(self.host,self.port)
    
    xmlStr=tn.read_all()
    root=etree.fromstring(xmlStr)
    
    #get grid node
    xmlGrid=root.find("GRID")
    
    #get cluster node
    xmlCluster=xmlGrid.find("CLUSTER")
    
    self.xml=xmlCluster
    
    self.hostsData={}
    for xmlHost in self.xml:
      
      name=xmlHost.get("NAME")
      self.hostsData[name]={}
      self.hostsData[name]["IP"]=xmlHost.get("IP")
      
      xmlMetrics=xmlHost.findall("METRIC")
      
      for xmlMetric in xmlMetrics:
        metricName=xmlMetric.get("NAME")
        units=xmlMetric.get("UNITS")
        value=xmlMetric.get("VAL")
        self.hostsData[name][metricName]={}
        self.hostsData[name][metricName]["unit"]=units
        self.hostsData[name][metricName]["val"]=value

        xmlExtraData=xmlMetric.findall("EXTRA_DATA")[0]
        xmlExtras=xmlExtraData.findall("EXTRA_ELEMENT")
        for xmlExtra in xmlExtras:
          self.hostsData[name][metricName][xmlExtra.get("NAME")]=xmlExtra.get("VAL")
  def printMetrics(self):
    """Prints available metrics
    
    This function prints and describes the available metrics complete with the 
    current value of that metric.
    """
    
    #if we don't have xml data, try to get some
    if self.xml==None:
      self.getData()
      
    for xmlHost in self.xml:
      
      print("hostname:",xmlHost.get("NAME"))
      print("ip:",xmlHost.get("IP"))
      
      xmlMetrics=xmlHost.findall("METRIC")
      
      for xmlMetric in xmlMetrics:
        
        print("  metric-name:"+xmlMetric.get("NAME"))
        print("    val:"+xmlMetric.get("VAL")+" "+xmlMetric.get("UNITS"))
        xmlExtraData=xmlMetric.findall("EXTRA_DATA")[0]
        xmlExtras=xmlExtraData.findall("EXTRA_ELEMENT")
        for xmlExtra in xmlExtras:
          print("    "+xmlExtra.get("NAME")+":"+xmlExtra.get("VAL"))
  def getMetricValueForHost(self,metricName,hostName):
    """Returns the value for the given metric on the given host
    
    if the host doesn't have that metric None is returned
    """
    
    if self.hostsData==None:
      self.getData()
    
    if hostName in self.hostsData.keys():
      if metricName in self.hostsData[hostName].keys():
        return self.hostsData[hostName][metricName]["val"]
    return None
  def getHostNames(self):
    """Returns a list of host names
    """
    
    if self.hostsData==None:
      self.getData()
    
    return self.hostsData.keys()
