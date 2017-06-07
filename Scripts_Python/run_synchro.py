#!/usr/bin/env python
# -*- coding: utf-8 -*-
import naoqi
from naoqi import ALProxy
import time
from threading import Thread, Event

NB_BOTS = 4
PORT = 9559
allTabletReady = True
allConnected = True
names = ["Superman","GrineLanterne","FlashGordone","Batman"]
ips = ["192.168.8.105","192.168.8.101", "192.168.8.112", "192.168.8.115"]
#/!\ IP PLUS BAS

class c_debug(Thread):
#BEGIN CLASS
    def __init__(self, thrds):
    #BEGIN INIT
        Thread.__init__(self)
        self.thrs = thrds
    #END INIT
    def run(self):
    #BEGIN RUN
        time.sleep(33)
        get_on_all(thrds, "debug")
        get_on_all(thrds, "reset")
        get_on_all(thrds, "join")
        print("END")
    #END RUN
#END CLASS

class c_thr(Thread):
#BEGIN Class
    def __init__(self):
    #BEGIN INIT
        Thread.__init__(self)
        self.name = "Default"
        self.port = PORT
        self.ip = 0
        self.connected = False
        self.allConnected = False
        self.tabletReady = False
        self.allTabletReady = False
    #END INIT

    def dancing(self):
        # self.Behavior.runBehavior("techweek/behavior_1")
        if (self.Behavior.isBehaviorRunning("techweek/behavior_1") == False):
            self.Behavior.startBehavior("techweek/behavior_1")

    def startChrono(self):
        if (self.Memory.getData('TabletChronoLoaded') == 1):
            ev.wait()
            if (self.allTabletReady == True):
                self.Memory.raiseEvent("startScriptJS","1")

    def reset(self):
    #BEGIN RESET
        if (self.Behavior.isBehaviorRunning("techweek/behavior_1")):
            self.Behavior.stopBehavior("techweek/behavior_1")
        # if self.AutonomousLife.getState() != "disabled":
        #     self.AutonomousLife.setState("disabled")
        if self.Motion.robotIsWakeUp():
            self.Motion.rest()
    #END RESET

    def debug(self):
    #BEGIN DEBUG
        if (self.Behavior.isBehaviorRunning("techweek/behavior_1")):
            self.Behavior.stopBehavior("techweek/behavior_1")
            print self.name + " IS DEAD INSIDE, KILL HIM NOW !"
            self.reset()
    #END DEBUG

    def run(self):
    #BEGIN RUN
        try:
        #BEGIN TRY CONNECT
            self.AutonomousLife = ALProxy("ALAutonomousLife", self.ip, self.port)
            self.Behavior = ALProxy("ALBehaviorManager", self.ip, self.port)
            self.RobotPosture = ALProxy("ALRobotPosture", self.ip, self.port)
            self.Speech = ALProxy("ALTextToSpeech", self.ip, self.port)
            self.Motion = ALProxy("ALMotion", self.ip, self.port)
            self.Memory = ALProxy("ALMemory", self.ip, self.port)
            self.connected = True
            print "Connection to " + self.ip + " Completed on " + self.name + ".\n"
        #END TRY
        except:
        #BEGIN EXCEPT
            self.connected = False
            print "Connection to " + self.ip + " Failed on " + self.name + ".\n"
        #END EXCEPT
        ev.wait()
        if (self.allConnected == True):
            self.Memory.subscribeToEvent('TabletChronoLoaded', self.getName(), 'startChrono')
            self.Memory.subscribeToEvent('BehaviorEnded', self.getName(), 'reset')
        #BEGIN CHOREGRAPHIE
            '''INSERT CHOREGRAPHIE (uncomment for play)'''
            #self.RobotPosture.goToPosture("StandInit", 0.5)
            #tosay = "Bonjour, je suis" + self.name
            #self.Speech.say(tosay)
            self.dancing()
            # self.reset()
        #END CHOREGRAPHIE
    #END RUN
#END Class


def get_on_all(seq, method, *args, **kwargs):
#BEGIN START NETHOD IN >= 1 OBJ
    if isinstance(seq, list):
        for obj in seq:
             getattr(obj, method)(*args, **kwargs)
    else:
        getattr(seq, method)(*args, **kwargs)
#END GET_ON_ALL

def set_on_all(seq, attribute, values):
#BEGIN CHANGE VAR IN >= 1 OBJ
    if isinstance(seq, list):
        for index, obj in enumerate(seq):
            setattr(obj, attribute, values[index])
    else:
        setattr(seq, attribute, values[0])
#END set_on_all

def testTabletReady():
    allTabletReady = True
    for x in thrds:
        if x.tabletReady == False :
            allTabletReady = False
    for x in thrds:
         x.allTabletReady = allTabletReady
    return allTabletReady

def testConnected():
    allConnected = True
    for x in thrds:
        if x.connected == False:
            allConnected = False
    for x in thrds:
        x.allConnected = allConnected
    return allConnected


#DEL IN FINAL VERSION
ips = ["169.254.158.71", "192.168.8.105","192.168.8.101", "192.168.8.112", "192.168.8.115"]
NB_BOTS = 1

ev = Event()
thrd_1 = c_thr()
thrd_2 = c_thr()
thrd_3 = c_thr()
thrd_4 = c_thr()
allThreads = [thrd_1, thrd_2, thrd_3, thrd_4]
thrds = allThreads[1:NB_BOTS + 1] #Beware: Last element not included
t_debug = c_debug(thrds)
set_on_all(thrds, "name", names)
set_on_all(thrds, "ip", ips)
get_on_all(thrds,"start")
time.sleep(1)


if (testConnected() == True):
#BEGIN EVENT
    print "All connected."
    ev.set()
    ev.clear()
    t_debug.start()
    print "Event connected sent.\nChoreography in progress..."
    allTabletReady = testTabletReady()
    timer = 0
    while (allTabletReady != True):
    #BEGIN TABLETS
        if (timer > 30):
            break
        if (testTabletReady() == True):
            print "All Tablet Ready"
            ev.set()
            print "Event TabletReady Sent"
        else:
            timer += 1
            print "All Tablet not ready yet"
        time.sleep(1)
    #END TABLETS
#END EVENT
else:
#BEGIN KILL THREADS
    ev.set()
    print "Not all connected.\nEND"
#END
