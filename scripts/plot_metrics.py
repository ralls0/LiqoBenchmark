import os, sys
import re
from datetime import *
from tokenize import String
from typing import List
import matplotlib.pyplot as plt
import numpy as np

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

def getResponseTimeP95(fileName: String, path: String):
  p95 = 0
  with open(f"{path}{fileName}") as f:
    for line in f:
      if re.search(f"^locust_requests_current_response_time_percentile_95.*", line):
        p95 = float((line.split(" "))[1])
  
  return p95

def getResponseTimeP50(fileName: String, path: String):
  p50 = 0
  with open(f"{path}{fileName}") as f:
    for line in f:
      if re.search(f"^locust_requests_current_response_time_percentile_50.*", line):
        p50 = float((line.split(" "))[1])
  
  return p50

def getTime(values):
  _date = []
  for v in values:
    _dt = datetime.fromtimestamp(int(v.get("timestamp")))
    _hour = _dt.hour
    _minute = _dt.minute
    _date.append(f"{_hour}:{_minute}")
  
  return _date

def getP95(values):
  p95 = [v.get("response_time_percentile_95") for v in values]
  
  return p95

def getP50(values):
  p50 = [v.get("response_time_percentile_50") for v in values]
  
  return p50

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
    value["response_time_percentile_95"] = getResponseTimeP95(f"{n}_locust_exporter_{timestampFile}.logs", path)
    value["response_time_percentile_50"] = getResponseTimeP50(f"{n}_locust_exporter_{timestampFile}.logs", path)
    #value["loadAvg"] = getLoadAverage(f"{n}_uptime_{timestampFile}.logs", path)
    values.append(value)
  
  print(f"values: {values}")

  metricsTime = getTime(values)
  p95 = getP95(values)
  p50 = getP50(values)

  xpoints = np.array(metricsTime)
  yP95 = np.array(p95)
  yP50 = np.array(p50)

  plt.title("Response Time Percentile 95")
  plt.xlabel("Time")
  plt.ylabel("ms")
  plt.plot(xpoints, yP95)
  plt.plot(xpoints, yP50)
  plt.show()
