#!/usr/bin/env python
# -*- coding: utf-8 -*-
import naoqi
import qi
from naoqi import ALProxy
import time
from datetime import datetime
from threading import Thread, Event

NB_BOTS = 4
PORT = 9559
TIME_MAX = 70 #70 Default Techweek
allConnected = True
OneChoreEnded = False
CHOREO_ID = "fastchoregdemo/behavior_1"
#CHOREO_TEST_ID = "techweektest/behavior_1"
names = ["Superman","GrineLanterne","FlashGordone","Batman"]
ips = ["192.168.8.102","192.168.8.104", "192.168.8.112", "192.168.8.115"]

###############################################################################

class c_thr(Thread) :
#BEGIN Class

    def __init__(self, event) :
    #BEGIN INIT
        Thread.__init__(self)
        self.name = "Default"
        self.port = PORT
        self.ip = 0
        self.connected = False
        self.allConnected = False
        self.event = event
    #END INIT

    def reset(self, *value) :
    #BEGIN RESET
        global OneChoreEnded
        OneChoreEnded = True
        if (self.Behavior.isBehaviorRunning(CHOREO_ID)):
            self.Behavior.stopBehavior(CHOREO_ID)
        if (self.Motion.robotIsWakeUp()) :
            self.Motion.rest()
    #END RESET

    def debug(self) :
    #BEGIN DEBUG
        if (self.Behavior.isBehaviorRunning(CHOREO_ID)):
        #BEGIN IF STILL RUNNING
            self.Behavior.stopBehavior(CHOREO_ID)
            print(self.name + " IS DEAD INSIDE, KILL HIM NOW !")
            self.reset()
        #END IF STILL RUNNING
    #END DEBUG

    def run(self) :
    #BEGIN RUN
        try :
        #BEGIN TRY CONNECT
            session = qi.Session()
            session.connect(self.ip, self.port)
            self.AutonomousLife = ALProxy("ALAutonomousLife", self.ip, self.port)
            self.Behavior = ALProxy("ALBehaviorManager", self.ip, self.port)
            self.RobotPosture = ALProxy("ALRobotPosture", self.ip, self.port)
            self.Speech = ALProxy("ALTextToSpeech", self.ip, self.port)
            self.Motion = ALProxy("ALMotion", self.ip, self.port)
            self.Memory = session.service("ALMemory")
            self.MemorySubscriber = self.Memory.subscriber("BehaviorEnded")
            self.MemorySubscriber.signal.connect(self.reset)
            self.connected = True
            print("Connection to " + self.ip + " Completed on " + self.name + ".\n")
        #END TRY CONNECT
        except :
        #BEGIN EXCEPT
            self.connected = False
            print("Connection to " + self.ip + " Failed on " + self.name + ".\n")
        #END EXCEPT
        self.event.wait()
        if (self.allConnected == True):
            self.Behavior.runBehavior(CHOREO_ID)
    #END RUN
#END Class

###############################################################################

def get_on_all(seq, method, *args, **kwargs) :
#BEGIN START NETHOD IN >= 1 OBJ
    if isinstance(seq, list) :
        for obj in seq :
             getattr(obj, method)(*args, **kwargs)
    else :
        getattr(seq, method)(*args, **kwargs)
#END GET_ON_ALL

###############################################################################

def set_on_all(seq, attribute, values) :
#BEGIN CHANGE VAR IN >= 1 OBJ
    if isinstance(seq, list) :
        for index, obj in enumerate(seq) :
            setattr(obj, attribute, values[index])
    else :
        setattr(seq, attribute, values[0])
#END set_on_all

###############################################################################

def testConnected(thrds) :
#BEGIN TEST ALL CONNECTED
    allConnected = True
    for x in thrds :
        if x.connected == False :
            allConnected = False
    for x in thrds :
        x.allConnected = allConnected
    return allConnected
#END TEST ALL CONNECTED

###############################################################################

def main ():
#BEGIN MAIN
    ev = Event()
    thrd_1 = c_thr(ev)
    thrd_2 = c_thr(ev)
    thrd_3 = c_thr(ev)
    thrd_4 = c_thr(ev)
    allThreads = [thrd_1, thrd_2, thrd_3, thrd_4]
    thrds = allThreads[1 : NB_BOTS + 1] #Beware: Last element not included
    set_on_all(thrds, "name", names)
    set_on_all(thrds, "ip", ips)
    get_on_all(thrds,"start")
    timer = 0
    while (testConnected(thrds) != True and timer < 5) :
    #BEGIN WAIT CONNECTING
        print("Waiting ..." + str(timer))
        timer += 1
        time.sleep(1)
    #END WAIT CONNECTING
    if (testConnected(thrds) == True) :
    #BEGIN EVENT
        timer = 0
        print "All connected."
        ev.set()
        print("Event connected sent.\nChoregraphy in progress...")
        while (OneChoreEnded != True and timer < TIME_MAX) :
        #BEGIN WHILE RUNNING BEHAVIOR
            print("Waiting End..." + str(timer))
            timer += 1
            time.sleep(1)
        #END WHILE RUNNING BEHAVIOR
        get_on_all(thrds, "debug")
        get_on_all(thrds, "join")
        print("END")
    #END EVENT
    else :
    #BEGIN KILL THREADS
        ev.set()
        print "Not all connected.\nEND"
    #END
#END MAIN

###############################################################################
if __name__ == "__main__" :
    main()
