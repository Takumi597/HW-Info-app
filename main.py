
import sys,os,sqlite3,psutil
from PySide6 import *
from PySide6.QtCore import QTimer
from ui_untitled import *
con = sqlite3.connect("dane.db")
cur = con.cursor()
table_for_queries=[
    "SELECT totalRam,availRam,usedRam,freeRam FROM his;",
    "SELECT OS,machine,version,node,release FROM his;",
    "SELECT rdzenie,watki,takt,usagecpu FROM his;",
    "SELECT programs FROM programy;",
    "SELECT device,zaczep,SysP,Wielkosc,zajete,wolne FROM storage;"
]

class MainWindow(QMainWindow):
    def __init__(self):
        
        QMainWindow.__init__(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("HiS INFO")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(3000)  
        self.update_data()
        def moveWindow(e):
            if self.isMaximized()==False:
                if e.buttons()==Qt.LeftButton:
                    self.move(self.pos()+e.globalPos() - self.clickPosition)
                    self.clickPosition=e.globalPos()
                    e.accept()

        self.ui.minimalizuj.clicked.connect(lambda:self.showMinimized())
        self.ui.zamknij.clicked.connect(lambda:self.close())
        self.ui.pelnyekran.clicked.connect(lambda:self.restore_or_maximize_window())
        self.ui.gora.mouseMoveEvent=moveWindow
        self.ui.dol.mouseMoveEvent=moveWindow
        self.ui.srodek.mouseMoveEvent=moveWindow
        self.ui.procesor.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.strona_proca_2))
        self.ui.ram.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.strona_ramu))
        self.ui.programy.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.strona_programow))
        self.ui.system_bt.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.strona_systemu))
        self.ui.dyski.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.strona_dyskow))
    
        self.show()
    def restore_or_maximize_window(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
    def update_data(self):
        self.ram()
        self.cpu()
        self.system()
        self.programy()
        self.storage()
    def ram(self):
        c1 = cur.execute(table_for_queries[0])
        ram = list(c1.fetchall())
        if ram:
            self.ui.total.setText(str(ram[0][0])[:-6])
            self.ui.available.setText(str(ram[0][1])[:-6])
            self.ui.used.setText(str(ram[0][2]))
            self.ui.free.setText(str(ram[0][3])[:-6])
    def cpu(self):
        c2 = cur.execute(table_for_queries[2])
        cpu = list(c2.fetchall())
        if cpu:
            self.ui.rdzenie.setText(str(cpu[0][0]))
            self.ui.watki.setText(str(cpu[0][1]))
            self.ui.taktowanie.setText(str(cpu[0][2]))
            self.ui.usage.setText(str(cpu[0][3]))
    def system(self):
        c3 = cur.execute(table_for_queries[1])
        sus = list(c3.fetchall())
        if sus:
            self.ui.system.setText(str(sus[0][0]))
            self.ui.node.setText(str(sus[0][1]))
            self.ui.release.setText(str(sus[0][2]))
            self.ui.wersja.setText(str(sus[0][3]))
            self.ui.maszyna.setText(str(sus[0][4]))
    def programy(self):
        c4 = cur.execute(table_for_queries[3])
        pro = c4.fetchall()
        temp=pro[0]
        temp2=temp[0]
        temp3=temp2[1:-1].split(',')
        proglist=[item.strip() for item in temp3]
       
        for i in range(0,len(proglist)):
            rowPosition=self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(rowPosition)
            try:
                self.create_table_widget(rowPosition, 0, proglist[i], "tableWidget")
                if rowPosition  >= len(proglist):
                        self.ui.tableWidget.removeRow(rowPosition)
            except Exception as e:
                print(e)
        if rowPosition  >= len(proglist):
                        self.ui.tableWidget.removeRow(rowPosition)
    def create_table_widget(self,rowPosition, columnPosition,text,tableName):
        qtablewidgetitem=QTableWidgetItem()
        getattr(self.ui, tableName).setItem(rowPosition, columnPosition, qtablewidgetitem)
        qtablewidgetitem=getattr(self.ui, tableName).item(rowPosition,columnPosition)
        qtablewidgetitem.setText(text);
    
    def storage(self):
        def checkChar(dyski):
            char = dyski.split(",")
            return char
        c5 = cur.execute(table_for_queries[4])
        boze = list(c5.fetchall())
        dyski=boze[0][0]
        znaki=":\\,"
        dyski2=[i for i in dyski if i not in znaki and i !=" "]
        sysplik=checkChar(boze[0][2])
        
        maxspace=checkChar(boze[0][3])
        usedspace=checkChar(boze[0][4])
        freee=checkChar(boze[0][5])

        storage_device=psutil.disk_partitions(all=False)
        itemfromtable=[]
        rowPosition=self.ui.tableWidget_2.rowCount()
        self.ui.tableWidget_2.setRowCount(0)
        rowPosition = self.ui.tableWidget_2.rowCount()
        for x in storage_device:
                if os.name=='nt' and x.fstype=='':
                    continue 
        for k in range(len(dyski2)):
                    self.ui.tableWidget_2.insertRow(rowPosition)
                    self.create_table_widget(rowPosition, 0,dyski2[k] , "tableWidget_2")
                    self.create_table_widget(rowPosition, 1,dyski2[k] , "tableWidget_2")
                    self.create_table_widget(rowPosition, 2,sysplik[k] , "tableWidget_2")
                    self.create_table_widget(rowPosition, 3,maxspace[k] , "tableWidget_2")
                    self.create_table_widget(rowPosition, 4,usedspace[k] , "tableWidget_2")
                    self.create_table_widget(rowPosition, 5,freee[k], "tableWidget_2")
                    
    def mousePressEvent(self, event):
        self.clickPosition=event.globalPos()
   
if __name__=="__main__":
    app=QApplication(sys.argv)
    window=MainWindow()
    sys.exit(app.exec_())