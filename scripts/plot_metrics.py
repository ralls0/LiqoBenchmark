import os, sys
import re
from tokenize import String
from typing import List

def getFileName(check: String, itemList: List):
  """
  get:
    - check: Number the file name starts with
    - itemList: list of file name
  """
  res = [idx for idx in itemList if re.search(f"^{check}_.*", idx)]
  return res

def extractDigits(lst):
  newLst = []
  el = []
  for n, e in enumerate(lst):
    if n%5 == 0 and n != 0:
      if el != []:
        newLst.append(el)
        el = []
      el.append(e)
    else:
      if n > 5:
        el.append(e)

  return newLst

def getDeployInfo(fileName: String, path: String):
  deploy = {}
  with open(f"{path}{fileName}") as f:
    for line in f:
      line = line.split(" ")
      line =  extractDigits(line)
      for e in line:
        deploy[e[0]] = deploy.get(e[0], 0) + int(e[3])

  return deploy

def getLoadAverage(fileName: String, path: String):
  with open(f"{path}{fileName}") as f:
    for line in f:
      line = line.split("load average")[1]
      line = line[2:len(line)-2]
      line = [float(idx) for idx in line.split(", ")]
  
  return line

def getResponseTime(fileName: String, path: String):
  p95 = 0
  with open(f"{path}{fileName}") as f:
    for line in f:
      if re.search(f"^locust_requests_current_response_time_percentile_95.*", line):
        p95 = float((line.split(" "))[1])
  
  return p95



if __name__ == "__main__":
  path = "/Users/rallso/Desktop/metrics/" # os.getcwd()+"/"
  # print(f"path: {path}")

  values = []

  print("[i] Retrieve the list of the file")
  listDir = os.listdir("/Users/rallso/Desktop/metrics")
  # print(f"list type: {type(listDir)}, listDir: {listDir}")
  lastIndex = int(input("Insert the last file name index: "))+1

  for n in range(1, lastIndex):
    value = {}
    processingFiles = getFileName(str(n), listDir)

    timestampFile = (processingFiles[0])[-15:-5]
    value["timestamp"] = timestampFile

    print(f"[i] Processing files number {n}: {processingFiles}")

    value["deploy"] = getDeployInfo(f"{n}_deploy_{timestampFile}.logs", path)
    value["loadAvg"] = getLoadAverage(f"{n}_uptime_{timestampFile}.logs", path)
    value["response_time_percentile_95"] = getResponseTime(f"{n}_locust_exporter_{timestampFile}.logs", path)
    #value["loadAvg"] = getLoadAverage(f"{n}_uptime_{timestampFile}.logs", path)
    values.append(value)
  
  print(f"values: {values}")
