import os, sys
import re
import json
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
  nlst = lst
  lst = []
  print(nlst)
  for n, e in enumerate(nlst):
    if re.search(f".+NAME$", e):
      lst.append(e[0:len(e)-4])
      lst.append("NAME")
    else:
      lst.append(e)

  print(lst)
  for n, e in enumerate(lst):
    if n%5 == 0:
      if el != []:
        newLst.append(el)
        el = []
      if re.search(f"[^NAME|READY|UP\-TO\-DATE|AVAILABLE|AGE]", e):
        el.append(e)
    else:
      if re.search(f"[^NAME|READY|UP\-TO\-DATE|AVAILABLE|AGE]", e):
        el.append(e)

  print(newLst)
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
    _sec = _dt.second
    _date.append(f"{_hour}:{_minute}:{_sec}")
  
  return _date

def getP95(values):
  p95 = [v.get("response_time_percentile_95") for v in values]
  
  return p95

def getP50(values):
  p50 = [v.get("response_time_percentile_50") for v in values]
  
  return p50

def getDeploy(values):
  sum = 0
  deployment = {}
  deploy = values[0].get("deploy").keys()

  deployment["running_pods"] = []
  for d in deploy:
    deployment[d] = []
    for v in values:
      deployment[d].append(int(v["deploy"].get(d)))

  for v in values:
    for d in deploy:
      sum += int(v["deploy"].get(d))
    deployment["running_pods"].append(sum)
    sum = 0
  
  return deployment

if __name__ == "__main__":
  path = "/Users/rallso/Desktop/test5/" # os.getcwd()+"/"
  # print(f"path: {path}")

  values = []

  print("[i] Retrieve the list of the file")
  listDir = os.listdir(path)
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
  
  fileName = input("Insert the name of the file in which you want to store data: ")
  with open(f"{path}{fileName}.json","w+") as f:
    f.write(json.dumps(values))

  metricsTime = getTime(values)
  p95 = getP95(values)
  p50 = getP50(values)

  xpoints = np.array(metricsTime)
  yP95 = np.array(p95)
  yP50 = np.array(p50)
  deploy = getDeploy(values)

  plot1 = plt.subplot2grid((2, 1), (0, 0)) #
  plot2 = plt.subplot2grid((2, 1), (1, 0)) #

  plot1.set_title("Response Time")
  plot1.set_xlabel("Time")
  plot1.set_ylabel("ms")
  plot1.plot(xpoints, yP95, label = "P95")
  plot1.plot(xpoints, yP50, label = "P50")

  plot1.set_xticklabels(xpoints, rotation=45, fontsize="small")
  plot1.set_xticks(np.arange(0, len(xpoints)+1, 12))
  plot1.legend()

  plot2.set_title("Deployments")
  plot2.set_xlabel("Time")
  for d in deploy:
    plot2.plot(xpoints,  np.array(deploy[d]), label = d)
  
  plot2.set_xticklabels(xpoints, rotation=45, fontsize="small")
  plot2.set_xticks(np.arange(0, len(xpoints)+1, 12))
  plot2.set_yticks(np.arange(0, max(deploy["running_pods"]), 3))
  plot2.legend()

  plt.show()
