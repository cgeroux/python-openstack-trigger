from __future__ import print_function

__version__ = "1.0.0"

import optparse as op
from lxml import etree

import telnetlib

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
def parseOptions():
  """Parses command line options
  
  """
  
  parser=op.OptionParser(usage="Usage: %prog [options] SETTINGS.xml"
    ,version="%prog "+__version__,description="")
  
  #add options
  addParserOptions(parser)
  
  #parse command line options
  return parser.parse_args()
def parseMetric(response):
  """
  """
  root=etree.fromstring(response)
  #print(etree.tostring(root))
  
  #get grid node
  xmlGrid=root.findall("GRID")[0]
  
  #get cluster node
  xmlCluster=xmlGrid.findall("CLUSTER")[0]
  
  
  for xmlHost in xmlCluster:
    
    print("hostname:",xmlHost.get("NAME"))
    print("ip:",xmlHost.get("IP"))
    
    xmlMetrics=xmlHost.findall("METRIC")
    
    for xmlMetric in xmlMetrics:
      
      print("  "+xmlMetric.get("NAME")+":"+xmlMetric.get("VAL")+" "+xmlMetric.get("UNITS"))
      xmlExtraData=xmlMetric.findall("EXTRA_DATA")[0]
      xmlExtras=xmlExtraData.findall("EXTRA_ELEMENT")
      for xmlExtra in xmlExtras:
        print("    "+xmlExtra.get("NAME")+":"+xmlExtra.get("VAL"))
        
    #print(item.tag)
  
  return []
def main():
  
  #parse command line options
  (options,args)=parseOptions()
  
  #check we got the expected number of arguments
  #if (len(args)!=1):
  #  raise Exception("Expected an xml settings file.")
    
  #load schema to validate against
  #schemaFileName=os.path.join(os.path.dirname(__file__),"xmlSchema/actions.xsd")
  #schema=etree.XMLSchema(file=schemaFileName)
  
  #parse xml file
  #tree=etree.parse(args[0])
  
  #strip out any comments in xml
  #comments=tree.xpath('//comment()')
  #for c in comments:
  #  p=c.getparent()
  #  p.remove(c)
  
  #validate against schema
  #schema.assertValid(tree)
  
  #get ganglia stats
  tn=telnetlib.Telnet(options.gangliaHost,options.gangliaPort)
  result=tn.read_all()
  parseMetric(result)
  
  print("end of execution!")