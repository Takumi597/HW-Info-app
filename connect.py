import sqlite3,time,winapps,re,psutil,platform,os,shutil,socket
################################################################################################
con=sqlite3.connect("dane.db")
cur=con.cursor()
################################################################################################
def pobranie():
   core=psutil.cpu_count()
   thread=psutil.cpu_count(logical=False)
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
   totalRam=totalRam/(1024*1024*1024)
   availRam=1.0
   availRam=psutil.virtual_memory()[1] *availRam
   availRam=availRam/(1024*1024*1024)
   usedRam=1.0
   usedRam=psutil.virtual_memory()[3] *usedRam
   usedRam=usedRam/(1024*1024*1024)
   freeRam=1.0
   freeRam=psutil.virtual_memory()[4] *freeRam
   freeRam=freeRam/(1024*1024*1024)
   return core,thread,takt,usage,OS,node,rel,ver,mach,totalRam,availRam,usedRam,freeRam
################################################################################################
def pobranie_dyski():
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
   return Urzadzenie,Zaczep,SystemPlikow,Wielkosc,Zajete,Wolne
################################################################################################
def pobranie_programy():
   nameregex=re.compile(r"name=\'[\"\']?([A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ0-9 _.-:;()+-/*®]+)[\"\']?\'")
   tab=[]
   Programs=[]
   for app in winapps.list_installed():
      tab.append(str(app))
    
   for i in tab:
      bagno=nameregex.search(i)
      Programs.append(bagno.group(1))
   return Programs
################################################################################################
def insert(Programs,Urzadzenie,Zaczep,SystemPlikow,Wielkosc,Zajete,Wolne,core,thread,takt,usage,totalRam,availRam,usedRam,freeRam,rel,ver,mach,node,OS):
   counter=0
   for i in Programs:
      cur.execute(f"INSERT INTO programy(id,programs) VALUES('{counter}','{i}')")
      con.commit()
      counter+=1

   for i in range(len(Urzadzenie)):
      cur.execute(f"INSERT INTO storage(id,device,zaczep,SysP,Wielkosc,zajete,wolne) VALUES('{i}','{Urzadzenie[i]}','{Zaczep[i]}','{SystemPlikow[i]}','{Wielkosc[i]}','{Zajete[i]}','{Wolne[i]}')")
      con.commit()
   
   cur.execute(f"INSERT INTO his(rdzenie,watki,takt,usagecpu,totalRam,availRam,usedRam,freeRam,release,version,machine,node,OS) VALUES('{core}','{thread}','{takt}','{usage}','{totalRam}','{availRam}','{usedRam}','{freeRam}','{rel}','{ver}','{mach}','{node}','{OS}')")
   con.commit()
################################################################################################ 
cur.execute("CREATE TABLE if not exists his(rdzenie,watki,takt,usagecpu,totalRam,availRam,usedRam,freeRam,release,version,machine,node,OS)")
con.commit()
cur.execute("CREATE TABLE if not exists programy(id,programs)")
con.commit()
cur.execute("CREATE TABLE if not exists storage(id,device,zaczep,SysP,Wielkosc,zajete,wolne)")
con.commit()
################################################################################################
core,thread,takt,usage,OS,node,rel,ver,mach,totalRam,availRam,usedRam,freeRam=pobranie()
Urzadzenie,Zaczep,SystemPlikow,Wielkosc,Zajete,Wolne=pobranie_dyski()
Programs=pobranie_programy()
insert(Programs,Urzadzenie,Zaczep,SystemPlikow,Wielkosc,Zajete,Wolne,core,thread,takt,usage,totalRam,availRam,usedRam,freeRam,rel,ver,mach,node,OS)
################################################################################################
def update():
   cur.execute("DELETE FROM his")
   con.commit()
   cur.execute("DELETE FROM programy")
   con.commit()
   cur.execute("DELETE FROM storage")
   con.commit()
   core,thread,takt,usage,OS,node,rel,ver,mach,totalRam,availRam,usedRam,freeRam=pobranie()
   Urzadzenie,Zaczep,SystemPlikow,Wielkosc,Zajete,Wolne=pobranie_dyski()
   Programs=pobranie_programy()
   insert(Programs,Urzadzenie,Zaczep,SystemPlikow,Wielkosc,Zajete,Wolne,core,thread,takt,usage,totalRam,availRam,usedRam,freeRam,rel,ver,mach,node,OS)
   cos=cur.execute("SELECT rdzenie,watki,takt,usagecpu,totalRam,availRam,usedRam,freeRam,release,version,machine,node,OS FROM his")
   jeden=cos.fetchall()
   cos1=cur.execute("SELECT id,programs FROM programy")
   dwa=cos1.fetchall()
   cos2=cur.execute("SELECT id,device,SysP,Wielkosc,zajete,wolne FROM storage")
   trzy=cos2.fetchall()
   print(dwa)
   print(jeden)
   print(trzy)

while True:
    update()
    time.sleep(10)
    
    

