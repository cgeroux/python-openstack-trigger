from __future__ import print_function

__version__ = "1.0.0"

import optparse as op
from lxml import etree

def addParserOptions(parser):
  """Adds command line options
  """
  
  group=op.OptionGroup(parser,title="Already Exists Behaviour",description="These options force a "
    +"global behaviour when ever an existing resource with the same name of "
    +"the one being created is encountered. For finner grained control use "
    +"the <already-exists> element in an specific action's parameters "
    +"element, (e.g. <create-instance>, <download-image> etc.).")
  
  group.add_option("--overwrite-all",action="store_const"
    ,dest="alreadyExistsGlobal",const="overwrite"
    ,help="Forces global overwrite behaviour, will overwrite existing "
    +"resource when encountered [not default].",default=None)
  group.add_option("--skip-all",action="store_const"
    ,dest="alreadyExistsGlobal",const="skip"
    ,help="Forces global skip behaviour, will skip creating a resource "
    +"when it already exists [not default].",default=None)
  group.add_option("--fail-all",action="store_const"
    ,dest="alreadyExistsGlobal",const="fail"
    ,help="Forces global fail behaviour, will throw an exception when "
    +"creating a resource when it already exists [not default]."
    ,default=None)
  parser.add_option_group(group)
def parseOptions():
  """Parses command line options
  
  """
  
  parser=op.OptionParser(usage="Usage: %prog [options] SETTINGS.xml"
    ,version="%prog "+__version__,description="")
  
  #add options
  addParserOptions(parser)
  
  #parse command line options
  return parser.parse_args()
def main():
  
  #parse command line options
  (options,args)=parseOptions()
  
  #check we got the expected number of arguments
  if (len(args)!=1):
    raise Exception("Expected an xml settings file.")
    
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
  
  print("end of execution!")