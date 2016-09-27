# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 19:14:50 2016

@author: fergal

$Id$
$URL$
"""

__version__ = "$Id$"
__URL__ = "$URL$"



import matplotlib.pyplot as mp
import numpy as np
import apj

def plotScore(fn):
    mp.clf()
#    apj.pre()

    data = np.loadtxt(fn, delimiter=",", dtype=str)
    eventTimes = data[:,0].astype(float)/60.
    data[:,0] = eventTimes.astype(str)


    mins = np.linspace(0, eventTimes[-1], 1000)
    us = np.zeros_like(mins)
    them = np.zeros_like(mins)
#
#    wh = np.where(data[:,3] == "PointScored")[0]
#    eventMins = eventTimes[wh]
#
#    for t in eventMins:
#        idx = mins >= float(t)
#        us[idx] += 1

    us = updateScore(data, mins, us, 'PointScored', 1)
    us = updateScore(data, mins, us, 'GoalScored', 3)

    them = updateScore(data, mins, them, 'PointConceded', 1)
    them = updateScore(data, mins, them, 'GoalConceded', 3)

    addEventType(data, mins, us, 'GoalScored', 'bo', ms=14)
    addEventType(data, mins, us, 'PointScored', 'bo', ms=10)
    addEventType(data, mins, us, 'Wide', 'bs', ms=8)

    addEventType(data, mins, them, 'GoalConceded', 'go', ms=14)
    addEventType(data, mins, them, 'PointConceded', 'go', ms=10)
    addEventType(data, mins, them, 'WideConceded', 'gs', ms=8)







    mp.xlabel("Time Elapsed (mins)")
    mp.ylabel("Score")
    mp.step(mins, us, 'b-', lw=2)
    mp.step(mins, them, 'g-', lw=2)
    apj.post()


def updateScore(data, time, score, eventName, eventValue):
    wh = np.where(data[:,3] == eventName)[0]
    eventMins = data[wh,0].astype(float)

    for t in eventMins:
        idx = time >= t
        score[idx] += eventValue
    return score

def addEventType(data, time, score, eventName, *args, **kwargs):
    wh = np.where(data[:,3] == eventName)[0]
    eventMins = data[wh,0].astype(float)

    for t in eventMins:
        i = np.argmin( np.fabs(time-t)) + 1
        mp.plot(time[i], score[i], *args, **kwargs)
