
import winapps, re
def pobranie_programy():
   nameregex=re.compile(r"name=\'[\"\']?([A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ0-9 _.-:()+-/*®]+)[\"\']?\'\,")
   tab=[]
   Programs=[]
   for app in winapps.list_installed():
      tab.append(str(app))
    
   for i in tab:
      bagno=nameregex.search(i)
      Programs.append(bagno.group(1))
   return Programs
print(pobranie_programy())

