import threading
from time import sleep,ctime
 
loops=[4,2]
 
def loop1(nloop,nsec):
       print 'start loop',nloop,'at:',ctime()
       sleep(nsec)
       print 'loop',nloop,'done at:',ctime()
       
def loop2(nloop,nsec):
       print 'start loop',nloop,'at:',ctime()
       sleep(nsec)
       print 'loop',nloop,'done at:',ctime()     
       
       
def main():
       print 'starting at:',ctime()
       threads=[]
       nloops=range(len(loops))
       for i in nloops:
              t=threading.Thread(target=loop,args=(i,loops[i]))
              threads.append(t)
       for i in nloops:
              threads[i].start()
       for i in nloops:
              threads[i].join()
             
       print 'all done at:',ctime()
      
if __name__=='__main__':
       main()
