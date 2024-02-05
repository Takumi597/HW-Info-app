
import psutil,platform,winapps,shutil,os,socket,re,pickle,sys
s=socket.socket()
port=40444
################################################################################################
def pobranie():
   allFiles = []
   core=str(psutil.cpu_count())
   thread=str(psutil.cpu_count(logical=False))
   takt=str(psutil.cpu_freq()[0]) + ' MHz'
   usage=str(psutil.cpu_percent()) + ' %'
   uname=platform.uname()
   OS=str(uname.system)
   node=str(uname.node)
   rel=str(uname.release)
   ver=str(uname.version)
   mach=str(uname.machine)
   totalRam=1.0
   totalRam=psutil.virtual_memory()[0] *totalRam
   totalRam=str(totalRam/(1024*1024*1024))
   availRam=1.0
   availRam=psutil.virtual_memory()[1] *availRam
   availRam=str(availRam/(1024*1024*1024))
   usedRam=1.0
   usedRam=psutil.virtual_memory()[3] *usedRam
   usedRam=str(usedRam/(1024*1024*1024))
   freeRam=1.0
   freeRam=psutil.virtual_memory()[4] *freeRam
   freeRam=str(freeRam/(1024*1024*1024))
   nameregex=re.compile(r"name=\'[\"\']?([A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ0-9 _.-:()+-/*®]+)[\"\']?\'")
   tab=[]
   Programs=[]
   for app in winapps.list_installed():
      tab.append(str(app))
    
   for i in tab:
      bagno=nameregex.search(i)
      Programs.append(bagno.group(1))
   Urzadzenie=[]
   Zaczep=[]
   SystemPlikow=[]
   Wielkosc=[]
   Zajete=[]
   Wolne=[]
   storage_device=psutil.disk_partitions(all=False)
   for x in storage_device:
      if os.name=='nt' and x.fstype=='':
         continue
      disk_usage=shutil.disk_usage(x.mountpoint)
      Urzadzenie.append(x.device)
      Zaczep.append(x.mountpoint)
      SystemPlikow.append(x.fstype)
      Wielkosc.append(str((disk_usage.total/(1024*1024*1024)))+' GB')
      Zajete.append(str((disk_usage.used/(1024*1024*1024)))+' GB')
      Wolne.append(str((disk_usage.free/(1024*1024*1024)))+' GB')
   
   allFiles.append([[Urzadzenie,Zaczep,SystemPlikow,Wielkosc,Zajete,Wolne ], ["func", Programs ] ,[core,thread,takt,usage,OS,node,rel,ver,mach,totalRam,availRam,usedRam,freeRam ] ]) 
   return allFiles
################################################################################################
while True:
    try:
        s.connect(('127.0.0.1', port))
        confirm = s.recv(1024)
        if confirm:
            data = pickle.dumps(pobranie())
            s.send(data)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        s.close()
        s = socket.socket()
################################################################################################

   