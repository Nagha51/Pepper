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
allConnected = True
# allTabletReady = False
# allChoreBeginEnded = False
OneChoreEnded = False
CHOREGID = "fastchoregdemo/behavior_1"
# CHOREGID = "techweektest/behavior_1"
names = ["Superman","GrineLanterne","FlashGordone","Batman"]
ips = ["192.168.8.102","192.168.8.104", "192.168.8.112", "192.168.8.115"]
#/!\ IP PLUS BAS

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
        # self.tabletReady = False
        # self.allTabletReady = False
        # self.choreBeginEnded = False
    #END INIT

    def dancing(self):
        self.Behavior.runBehavior(CHOREGID)
        # self.Behavior.startBehavior("techweek/behavior_1")
        

    def startChrono(self):
        if (self.Memory.getData('TabletChronoLoaded') == 1):
            ev.wait()
            # if (self.allTabletReady == True):
            self.Memory.raiseEvent("startScriptJS","1")

    def startJS(self):
        script = "toggleImage()"
        self.TabletService.executeJS(script)


    def choreBeginEnded(self):
        self.choreBeginEnded = True

    def stop(self):
    #BEGIN STOP
        if (self.Behavior.isBehaviorRunning(CHOREGID)):
            self.Behavior.stopBehavior(CHOREGID)
    #END STOP

    def reset(self, *value):
    #BEGIN RESET
        global OneChoreEnded
        print "OneChoreEnded Before %s " % OneChoreEnded
        OneChoreEnded = True
        print "OneChoreEnded %s " % OneChoreEnded
        print "Reset called on {0} at {1}".format(self.ip, str(datetime.now().time()))
        self.stop()
        # if self.AutonomousLife.getState() != "disabled":
        #     self.AutonomousLife.setState("disabled")
        if self.Motion.robotIsWakeUp():
            print "RobotIsWakeup"
            self.Motion.rest()
        else:
            print "RobotIsNOTWakeup"
    #END RESET

    def reset2(self, value):
        print "RESET CALLED"
        # self.Memory.unsubscribeToEvent('BehaviorEnded',"c_thr")

    def debug(self):
    #BEGIN DEBUG
        if (self.Behavior.isBehaviorRunning(CHOREGID)):
            self.Behavior.stopBehavior(CHOREGID)
            print self.name + " IS DEAD INSIDE, KILL HIM NOW !"
            self.reset()
    #END DEBUG

    def run(self):
    #BEGIN RUN
        try:
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
            #s = qi.Session()
            #s.connect("tcp://127.0.0.1:9559")
            #self.session = qi.Session("tcp://127.0.0.1:9559")
            #self.session = qi.Session(self.ip + ":" + self.port)
            # self.TabletService = self.session().service("ALTabletService")
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
            # self.Memory.subscribeToEvent('ChoregraphieBeginningENDED', self.getName(), 'choreBeginEnded')
            # self.Memory.subscribeToEvent('TabletChronoLoaded', self.getName(), 'startChrono')
        #BEGIN CHOREGRAPHIE
            '''INSERT CHOREGRAPHIE (uncomment for play)'''
            #self.RobotPosture.goToPosture("StandInit", 0.5)
            #tosay = "Bonjour, je suis" + self.name
            #self.Speech.say(tosay)
            self.dancing()
            # self.reset()
            # self.rese()
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

def testChoreBeginEnded():
    readys = 0
    for x in thrds:
        if x.choreBeginEnded == True:
            readys += 1
    if readys == NB_BOTS :
        allChoreBeginEnded == True
    # for x in thrds:
        # if x.choreBeginEnded == False :
            # allChoreBeginEnded = False
    # for x in thrds:
    #      x.allChoreBeginEnded = allChoreBeginEnded
    return allChoreBeginEnded

def testTabletReady():
    readys = 0
    for x in thrds:
        if x.tabletReady == True :
            readys += 1
    if readys == NB_BOTS : 
        for x in thrds:
            x.allTabletReady = allTabletReady
    return allTabletReady
    # for x in thrds:
    #     if x.tabletReady == False :
    #         allTabletReady = False
    # for x in thrds:
    #      x.allTabletReady = allTabletReady
    # return allTabletReady

def testConnected():
    allConnected = True
    for x in thrds:
    #BEGIN EACH THREADS
        if x.connected == False:
            allConnected = False
    #END EACH THREADS
    for x in thrds:
        x.allConnected = allConnected
    return allConnected


#DEL IN FINAL VERSION
ips = ["192.168.8.104","192.168.8.102", "192.168.8.105", "192.168.8.115"]
NB_BOTS = 2

ev = Event()
thrd_1 = c_thr()
thrd_2 = c_thr()
thrd_3 = c_thr()
thrd_4 = c_thr()
allThreads = [thrd_1, thrd_2, thrd_3, thrd_4]
thrds = allThreads[1:NB_BOTS + 1] #Beware: Last element not included
set_on_all(thrds, "name", names)
set_on_all(thrds, "ip", ips)
get_on_all(thrds,"start")

timer = 0
while (testConnected() != True and timer < 5):
    print "Waiting ..." + str(timer)
    timer += 1
    time.sleep(1)

if (testConnected() == True):
#BEGIN EVENT
    timer = 0
    print "All connected."
    ev.set()
    print "Event connected sent.\nChoregraphy in progress..."
    # while(allTabletReady != True && allChoreBeginEnded != True):
    #     if timer == 35:
    #         break
    #     if (testTabletReady() == True):
    #         print "All Tablet Ready"
    #     if (testChoreBeginEnded() == True):
    #         print "All ChoreBegin Ended"
    #     if (testTabletReady() == True && testChoreBeginEnded() == True):
    #         print "Event TabletReady Sent"
    #         ev.set()
    #     else:
    #         timer += 1
    #         print "Not Ready/BeginEnded yet"
    #     time.sleep(1)
    # time.sleep(60)              #SAFETY ON BUG
    # get_on_all(thrds, "debug")  #SAFETY ON BUG
    #_ get_on_all(thrds, "reset")  #SAFETY ON BUG
    #
    while (OneChoreEnded != True and timer < 90):
        print "Waiting End..." + str(timer)
        timer += 1
        time.sleep(1)

    get_on_all(thrds, "debug")
    # get_on_all(thrds, "join") // Creating Python Error
    print("END")
#END EVENT
else:
#BEGIN KILL THREADS
    ev.set()
    print "Not all connected.\nEND"
#END