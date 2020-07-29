#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
import time
import datetime
import psutil #pip install psutil ，或离线whl安装
import random
import gc
from numpy import *  #pip install numpy ，或离线whl安装
import numpy as np
import signal

cpuPercent = 100
memPercent = 0
changedFlag = True

class cpuThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        global cpuPercent
        global changedFlag
        threshold = 25  #CPU阀值
        mychangeFlag = False
        matns = [10000,100000,500000,1000000,5000000,10000000,20000000,50000000]
        matn = 0
        print ("Strat Thread: " + self.name)
        while True:
            thrh = random.randint(threshold-5,threshold+5)
            if mychangeFlag != changedFlag:
                mychangeFlag = changedFlag
                if cpuPercent < thrh:
                    if matn < 7:
                        matn += 1
                else:
                    if matn > 0:
                        matn -= 1
                nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(nowTime,self.name,"matn:",matns[matn])
            else:
                for i in range(1,matns[matn]):  #循环次数可能每台机都要相应调整才有最佳效果
                    9999.999 * 9999.999
                time.sleep(0.1)
        #print ("Stop Thread: " + self.name)

class memThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        global memPercent
        global changedFlag
        mthreshold = 3221225472 #内存阀值，单位字节
        minthreshold = mthreshold - 104857600 #减少100MB
        arrSize = 1
        arrMaxSize = 1000000000  #增长最大值
        x = np.zeros(arrSize,dtype = np.int)
        print ("Strat Thread: " + self.name)
        while True:
            time.sleep(5)
            if memPercent < minthreshold:
                if arrSize < arrMaxSize:
                    arrSize+=20000000
                    x.resize(arrSize)
            elif memPercent > mthreshold:
                if arrSize > 20000000:
                    arrSize-=20000000
                    x.resize(arrSize)
            #否则arrSize已降至1，或在minthreshold和mthreshold之间，不做任何处理
            nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(nowTime,self.name,"arrSize:",arrSize)
            #gc.collect()
        #print ("Stop Thread: " + self.name)

class colUsage (threading.Thread):
    def __init__(self,threadID,name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        global cpuPercent
        global changedFlag
        global memPercent
        while True:
            cpuPercent = psutil.cpu_percent(1)
            memPercent = psutil.virtual_memory().used
            changedFlag = bool(1-changedFlag)
            nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print (nowTime,self.name,"cpu usage: ",cpuPercent)
            print (nowTime,self.name,"mem usage: ",memPercent)
            time.sleep(2)  #必要时可调整周期          

if __name__ == "__main__":
    signal.signal(signal.SIGINT, colUsage)
    signal.signal(signal.SIGTERM, colUsage)
    signal.signal(signal.SIGINT, cpuThread)
    signal.signal(signal.SIGTERM, cpuThread)
    signal.signal(signal.SIGINT, memThread)
    signal.signal(signal.SIGTERM, memThread)
    # 创建线程
    colthread = colUsage(1, "col_Thread")
    cputh2 = cpuThread(2, "cpu_Thread-2")  ###必要时可启动多几个线程，或者跑多几个进程
    time.sleep(0.5)
    #cputh3 = cpuThread(3, "cpu_Thread-3")
    memth = memThread(10, "mem_Thread")
    
    colthread.setDaemon(True)
    cputh2.setDaemon(True)
    memth.setDaemon(True)
    # 启动线程
    colthread.start()
    cputh2.start()
    #cputh3.start()
    memth.start()

    #colthread.join()
    #cputh2.join()
    #cputh3.join()
    #memth.join()
    input("Waiting For Ctrl+C\n")
    #print ("Quit Main Thread.")


