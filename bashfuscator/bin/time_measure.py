#!/usr/bin/env python

#Imported Libraries
import time
import timeit
import plotly
import plotly.graph_objs as go
from subprocess import STDOUT, PIPE, Popen
from bashfuscator.core.obfuscation_handler import ObfuscationHandler


#Variables
longObfName="token/special_char_only"
repeat_cmd=":;\n"

#list of times to run the command.  These values were chosen to work well on a logrithmic scale:
#iterations=["1", "2", "3", "4", "5", "10", "20", "30", "40", "50", "100", "200", "300", "400", "500", "1000", "2000", "3000", "4000", "5000", "10000", "20000", "30000", "40000", "50000"]
iterations=["1", "2", "3", "4", "5", "10", "20", "30", "40", "50", "100", "200", "300", "400", "500"]

unobfTimeData=[]
obfTimeData=[]
timeDelta=[]

#Functions
def timeRun(payload): #Returns double: time it took to run payload in bash
	mysetup='''from subprocess import STDOUT, PIPE, Popen
from __main__ import payload, runProcess'''

	snippet="runProcess(payload)"
	t=timeit.timeit(setup=mysetup, stmt=snippet, number=1)
	print(t)
	return t

def runProcess(payload):
	proc = Popen(payload, executable="/bin/bash", stdout=PIPE, stderr=STDOUT, shell=True, universal_newlines=True)
	__, __ = proc.communicate()
	return

def  processData(runTimeList):	#Returns list: "timeDelta" values for plotting
	#Fill timeDelta list
	#timeDelta is one element shorter than the runTime list, it's the time increase between runs, first value of timeDelta is always 0.
	timeDeltaList=[]
	for i in range(len(runTimeList)):
		if i==0:
			timeDeltaList.append(0)
		else:
			timeDeltaList.append(runTimeList[i]-runTimeList[i-1])
	return timeDeltaList

def plotAllTheThings(xList, yList, Title):
	#Still a work in progress: I don't have the right numbers or processed lists yet.
	plotly.offline.plot({
    "data": [go.Scatter(x=xList, y=yList)],
    "layout": go.Layout(title=Title,
		xaxis=dict(
        	type='log',
        	autorange=True
    	)
	)
	}, auto_open=True)


#Try catch
for i in iterations:        #Yo Dawg, I heard you liked iterations.  So I iterated over your iterations.
	j=0 #Index counter for list maniputlation
	i=int(i)
	payload = repeat_cmd * i

	#Generate a baseline time (how long it takes to run unobfuscated)
	unobfTimeData.append(timeRun(payload))
	print("Baseline time for {0} Iterations: {1}".format(i, unobfTimeData[-1]))


	#Obfuscate the command
	obHandler = ObfuscationHandler()
	obfCommand=obHandler.genObfuscationLayer(payload, longObfName)

	#Time run of obfuscated code
	print("Running Obfuscated code...")
	##$n/$len_cmd"*1000"
	obfTime=timeRun(obfCommand)
	print(obfTime)
	obfTimeData.append((obfTime-unobfTimeData[-1])/(i*len(repeat_cmd)*1000))	#Append to list

plotAllTheThings(iterations, obfTimeData, longObfName)