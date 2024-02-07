#!/bin/env python3

import threading
import time
"""

class MyThread(threading.Thread):
    def __init__(self, n, m, s):
        threading.Thread.__init__(self)
        self.s=s
        self.n=n
        self.m=m

    def run(self):
        start_time=time.time()
        for i in range(self.n):
            time.sleep(self.s)
            current_time = time.time()
            elapsed_time = current_time - start_time
            print(f"[{elapsed_time:.2f} s]:{self.m}")
            

if __name__ == '__main__':
    mytask = MyThread(n=5,m="Hello",s=2)
    mytask.start()
    mytask2 = MyThread(n=6,m="Yo !",s=1)
    mytask2.start()
    mytask3 = MyThread(n=4,m="Coucou :)", s=3)
    mytask3.start()
"""
"""
class Add(threading.Thread):
    s=0
    mon_verrou = threading.Lock()
    def __init__(self, a):
        threading.Thread.__init__(self)
        self.a=a

    def run(self):
        
        Add.mon_verrou.acquire()
        x=Add.s
        time.sleep(0.001) # temporisation
        x += self.a
        time.sleep(0.001)
        Add.s = x
        Add.mon_verrou.release()
        #print(Add.s,flush=True)
    
n=100

if __name__ == '__main__':
    tasks=[]
    for b in range(1,n+1) :
        tasks.append(Add(b))
    for task in tasks:
        task.start()
    for task in tasks:
        task.join()
    print(Add.s)
"""

"""
import threading,sys

class Serie(threading.Thread):

    def __init__(self,i,k):
        threading.Thread.__init__(self)
        self.k = k
        self.i = i

    def run(self):
        self.s = 0
        s2 = -1
        i = self.i
        while self.s!=s2:
            s2 = self.s
            self.s += 1./(i*i)
            # if i%10000==0: print(f"{self.i:2d} : {s} ", end="\n", flush=True)
            i += self.k

if __name__=="__main__":
    nbtache = int(sys.argv[1])

    taches = []
    for i in range(1,nbtache+1):
        taches.append(Serie(i,nbtache))

    for t in taches:
        t.start()

    for t in taches:
        t.join()

    s = 0
    for t in taches:
        s += t.s    

    print(s)

"""

import threading,subprocess

class C(threading.Thread):
    def __init__(self,ip):
        threading.Thread.__init__(self)
        self.ip = ip

    def ping(self, host, count=1, wait_sec=1):
        cmd = f"ping -c {count} -W {wait_sec} {host}".split(' ')
        try:
            output = subprocess.check_output(cmd).decode().strip()
            lines = output.split("\n")
            total = lines[-2].split(',')[3].split()[1]
            loss = lines[-2].split(',')[2].split()[0]
            timing = lines[-1].split()[3].split('/')
            return {
                'type': 'rtt',
                'min': timing[0],
                'avg': timing[1],
                'max': timing[2],
                'mdev': timing[3],
                'total': total,
                'loss': loss,
            }
        except subprocess.CalledProcessError :
            return None
        except Exception as e:
            print(type(e),e)
        return None

    def run(self):
        if self.ping(self.ip):
            print(f"{self.ip} is reachable")

if __name__=="__main__":
    net = "172.20.45."
    tasks = []

    for i in range(1, 255):
        tasks.append(C(f"{net}{i}"))

    for t in tasks:
        t.start()

    for t in tasks:
        t.join()