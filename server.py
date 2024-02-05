import socket
import pickle
import sqlite3

def handle_client(conn, cur, con):
    data = b""
    while True:
        odczyt1 = conn.recv(4096)
        if not odczyt1:
            break
        data += odczyt1

    data_arr = pickle.loads(data)
    #print(data_arr)

    pobranie = data_arr[0][0]
    pobranie1 = data_arr[0][1][1]
    pobranie2 = data_arr[0][2]

    query = "INSERT INTO programy(programs) VALUES(\""
    query += f"["
    for i in range(0, len(pobranie1)):
        query += "" + f"{data_arr[0][1][1][i]},"
    query = query[:-1]
    query += "]\");"

    query1 = "INSERT INTO his(rdzenie,watki,takt,usagecpu,OS,machine,version,node,release,totalRam,availRam,usedRam,freeRam) VALUES("
    for j in range(0, len(pobranie2)):
        query1 += "" + f"\"{data_arr[0][2][j]}\","
    query1 = query1[:-1]
    query1 += ");"
    
    query2 = "INSERT INTO storage(device,zaczep,SysP,Wielkosc,zajete,wolne) VALUES("
    query2 += f"["
    for g in range(0, len(pobranie)):
        query2 += "" + f"\"{data_arr[0][0][g]}\","
    query2 = query2[:-1]
    query2 += "]);"

    chars = "'[]"
    testcase = [s for s in query2]
    for slash in testcase:
        if slash in chars:
            index = testcase.index(slash)
            testcase[index] = ""
    query2 = ""
    for k in testcase:
        query2 += k

    cur.execute("DELETE FROM his")
    con.commit()

    cur.execute("DELETE FROM programy")
    con.commit()

    cur.execute("DELETE FROM storage")
    con.commit()

    cur.execute(query)
    con.commit()
    cur.execute(query1)
    con.commit()
    cur.execute(query2)
    con.commit()

    cos1 = cur.execute("SELECT * FROM storage")
    dwa = cos1.fetchall()
    print(dwa)

    query = ""
    query2 = ""
    query1 = ""
    conn.sendall("Take".encode())
    conn.close()

def start_server():
    con = sqlite3.connect("dane.db")
    s = socket.socket()
    port = 40444
    s.bind(('127.0.0.1', port))
    s.listen(5)

    cur = con.cursor()
    cur.execute("CREATE TABLE if not exists his(rdzenie,watki,takt,usagecpu,OS,machine,version,node,release,totalRam,availRam,usedRam,freeRam)")
    con.commit()
    cur.execute("CREATE TABLE if not exists programy(id INTEGER PRIMARY KEY AUTOINCREMENT,programs)")
    con.commit()
    cur.execute("CREATE TABLE if not exists storage(id INTEGER PRIMARY KEY AUTOINCREMENT,device,zaczep,SysP,Wielkosc,zajete,wolne)")
    con.commit()
    

    while True:
        print("Waiting for connection...")
        conn, addr = s.accept()
        print("Connection from", addr)
        conn.sendall("Connected".encode())

        handle_client(conn, cur, con)

if __name__ == "__main__":
    start_server()