from .Ganglia import Ganglia
from .Trigger import Trigger
import time

class TriggerManager(object):
  """
  """
  
  def __init__(self,xml,options):
    """
    """
    
    self.triggers=[]
    self.checkFrequency=int(xml.find("check-frequency").text)
    self.lastCheck=None
    
    
    self.ganglia=Ganglia(host=options.gangliaHost
      ,port=options.gangliaPort)
    xmlTriggers=xml.findall("trigger")
    for xmlTrigger in xmlTriggers:
      self.triggers.append(Trigger(xmlTrigger,options))
  def run(self):
    """
    """
    
    while True:
      
      self.lastCheck=time.time()
      timeString=time.strftime("%a %b %d %H:%M:%S UTC %Y",time.gmtime())
      print("-----------------------------------------------------------"
        +"--------------------")
      print(timeString+": checking triggers ...")
      
      #check triggers and perform actions as needed
      for trigger in self.triggers:
        if trigger.check(self.ganglia.getHostNames()
          ,self.ganglia.getMetricValueForHost):
          trigger.performAction()
      
      #Wait as needed
      timeElapsed=time.time()-self.lastCheck
      waitTime=self.checkFrequency-timeElapsed
      if waitTime>0:
        print("waiting "+str(waitTime)+" s before checking again ...")
        time.sleep(waitTime)
