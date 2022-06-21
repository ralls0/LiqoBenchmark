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
  for n, e in enumerate(nlst):
    if re.search(f".+NAME$", e):
      lst.append(e[0:len(e)-4])
      lst.append("NAME")
    else:
      lst.append(e)

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

  return newLst

def getDeployInfo(fileName: String, path: String, linkerd = False):
  deploy = {}
  with open(f"{path}{fileName}") as f:
    for line in f:
      line = line.split(" ")
      line =  extractDigits(line)
      for e in line:
        if e[0] != "loadgenerator" and e[0] != "locust-exporter":
          deploy[e[0]] = deploy.get(e[0], 0) + int(e[3])
  
  if linkerd:
    for d in deploy:
      deploy[d] = deploy.get(d, 0) - 1

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

def getCurrentRPSAggregated(fileName: String, path: String):
  rpsA = 0
  with open(f"{path}{fileName}") as f:
    for line in f:
      if re.search(f"^locust_requests_current_rps.*Aggregated.*", line):
        rpsA = float((line.split(" "))[1])
  
  return rpsA

def getTime(values):
  _date = []
  init = -1
  for v in values:
    if init == -1:
      init = int(v.get("timestamp"))

    _dt = datetime.fromtimestamp(int(v.get("timestamp"))-init)
    _minute = '{:02d}'.format(int(_dt.minute))
    _sec = '{:02d}'.format(int(_dt.second))
    _date.append(f"{_minute}:{_sec}")
  
  return _date

def getP95(values):
  p95 = [v.get("response_time_percentile_95") for v in values]
  
  return p95

def getP50(values):
  p50 = [v.get("response_time_percentile_50") for v in values]
  
  return p50

def getRSPA(values):
  rpsA = [v.get("current_rps_aggregated") for v in values]
  
  return rpsA

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

def plotAll(xpoints, yP95, yP50, yrpsA, deploy, startHPA):
  plot1 = plt.subplot2grid((3, 1), (0, 0))
  plot2 = plt.subplot2grid((3, 1), (1, 0))
  plot3 = plt.subplot2grid((3, 1), (2, 0))

  plot1.set_title("Response Time")
  plot1.set_xlabel("Time")
  plot1.set_ylabel("ms")
  plot1.plot(xpoints, yP95, label = "P95")
  plot1.plot(xpoints, yP50, label = "P50")
  

  plot1.set_xticklabels(xpoints, rotation=45, fontsize="small")
  plot1.set_xticks(np.arange(0, len(xpoints)+1, 12))
  plot1.axvline(x = startHPA, color = 'r', label = 'axvline - full height')
  plot1.grid()
  plot1.legend()

  plot2.set_title("Current RPS Aggregated")
  plot2.set_xlabel("Time")
  plot2.set_ylabel("rps")

  plot2.plot(xpoints, yrpsA, label = "rps")

  plot2.set_xticklabels(xpoints, rotation=45, fontsize="small")
  plot2.set_xticks(np.arange(0, len(xpoints)+1, 12))
  plot2.axvline(x = startHPA, color = 'r', label = 'axvline - full height')
  plot2.grid()
  plot2.legend()

  plot3.set_title("Deployments")
  plot3.set_xlabel("Time")
  for d in deploy:
    plot3.plot(xpoints,  np.array(deploy[d]), label = d)
  
  plot3.set_xticklabels(xpoints, rotation=45, fontsize="small")
  plot3.set_xticks(np.arange(0, len(xpoints)+1, 12))
  plot3.set_yticks(np.arange(0, max(deploy["running_pods"]), 3))
  plot3.axvline(x = startHPA, color = 'r', label = 'axvline - full height')
  plot3.grid()
  plot3.legend()

  plt.show()

def plotResponceTime(xpoints, yP95, yP50, startHPA):
  plot1 = plt.subplot2grid((1, 1), (0, 0)) #

  plot1.set_title("Response Time")
  plot1.set_xlabel("Time")
  plot1.set_ylabel("ms")
  plot1.plot(xpoints, yP95, label = "P95")
  plot1.plot(xpoints, yP50, label = "P50")
  
  plot1.set_xticklabels(xpoints, rotation=45, fontsize="small")
  plot1.set_xticks(np.arange(0, len(xpoints)+1, 12))
  plot1.legend()

  plt.axvline(x = startHPA, color = 'r', label = 'axvline - full height')
  plt.grid()
  plt.show()

def plotRPS(xpoints, yrpsA, startHPA):
  plot1 = plt.subplot2grid((1, 1), (0, 0)) #

  plot1.set_title("Current RPS Aggregated")
  plot1.set_xlabel("Time")
  plot1.set_ylabel("rps")

  plot1.plot(xpoints, yrpsA, label = "rps")

  plot1.set_xticklabels(xpoints, rotation=45, fontsize="small")
  plot1.set_xticks(np.arange(0, len(xpoints)+1, 12))
  plot1.legend()

  plt.axvline(x = startHPA, color = 'r', label = 'axvline - full height')
  plt.grid()
  plt.show()

def plotDeploy(xpoints, deploy, startHPA):
  plot1 = plt.subplot2grid((1, 1), (0, 0)) #

  plot1.set_title("Deployments")
  plot1.set_xlabel("Time")
  for d in deploy:
    plot1.plot(xpoints,  np.array(deploy[d]), label = d)
  
  plot1.set_xticklabels(xpoints, rotation=45, fontsize="small")
  plot1.set_xticks(np.arange(0, len(xpoints)+1, 12))
  plot1.set_yticks(np.arange(0, max(deploy["running_pods"]), 3))
  plot1.legend()

  plt.axvline(x = startHPA, color = 'r', label = 'axvline - full height')
  plt.grid()
  plt.show()

def getStartHPA(listDir, lastIndex: int, path: String, linkerd = False):
  startHPA = 0

  for n in range(1, lastIndex+1):
    processingFiles = getFileName(str(n), listDir)
    timestampFile = (processingFiles[0])[-15:-5]

    try:
      with open(f"{path}{n}_hpa_{timestampFile}.logs") as f:
          if linkerd:
            for line in f:
              if len(line) > 1:
                startHPA = n
                break
            if startHPA > 0:
              break
          else:
            startHPA = n
            break
    except IOError:
      pass

  return startHPA

if __name__ == "__main__":
  path = os.getcwd()+"/tests/test5/"

  values = []

  print("[i] Retrieve the list of the file")
  listDir = os.listdir(path)

  lastIndex = 264 #int(input("Insert the last file name index: "))+1

  for n in range(1, lastIndex+1):
    value = {}
    processingFiles = getFileName(str(n), listDir)

    timestampFile = (processingFiles[0])[-15:-5]
    value["timestamp"] = timestampFile

    print(f"[i] Processing files number {n}: {processingFiles}")

    value["deploy"] = getDeployInfo(f"{n}_deploy_{timestampFile}.logs", path, False) # True solo per test 4
    value["loadAvg"] = getLoadAverage(f"{n}_uptime_{timestampFile}.logs", path)
    value["response_time_percentile_95"] = getResponseTimeP95(f"{n}_locust_exporter_{timestampFile}.logs", path)
    value["response_time_percentile_50"] = getResponseTimeP50(f"{n}_locust_exporter_{timestampFile}.logs", path)
    value["current_rps_aggregated"] = getCurrentRPSAggregated(f"{n}_locust_exporter_{timestampFile}.logs", path)
    values.append(value)

  startHPA = getStartHPA(listDir, lastIndex, path, False) # True solo per test 4
  
  fileName = input("Insert the name of the file in which you want to store data: ")
  with open(f"{path}{fileName}.json","w+") as f:
    f.write(json.dumps(values))

  metricsTime = getTime(values)
  p95 = getP95(values)
  p50 = getP50(values)
  rpsA = getRSPA(values)

  xpoints = np.array(metricsTime)
  yP95 = np.array(p95)
  yP50 = np.array(p50)
  yrpsA = np.array(rpsA)
  deploy = getDeploy(values)

  plotResponceTime(xpoints, yP95, yP50, startHPA)
  plotRPS(xpoints, yrpsA, startHPA)
  plotDeploy(xpoints, deploy, startHPA)
  plotAll(xpoints, yP95, yP50, yrpsA, deploy, startHPA)
