import json


class RiosConfig:

 def getConfigData(self):

  url = "device.config"
  
  #print url
  with open(url) as f:
    content = f.readline()
  
# assume that content is a json reply
# parse content with the json module
  #print content
  data = json.loads(content)
  #print data
  #djson = json.loads(data)
  return data #['coord']
