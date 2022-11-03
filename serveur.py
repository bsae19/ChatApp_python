import socket
import threading
 
List=[]
cles_pub=[]
List_nom=[]
def threaded(c,nom,addr,cles):
    while True:
        data = c.recv(1024)
        if not data:
            print('Deconnection de ',addr)
            break
        dat=data.decode()
        if dat[0]=='@':
            dat = dat.replace('@','')
            ind=-1
            compt=0
            for i in List_nom:
                if i==dat:
                    ind=compt
                compt+=1
            if ind==-1:
                c.send(str(ind).encode())
            else:
                c.send(('@'+str(cles_pub[ind])).encode())
                d=c.recv(2048)
                List[ind].send(d)
        elif dat=="all":
            compt=0
            for i in List:
                c.send(('|'+str(cles_pub[compt])).encode())
                mes=c.recv(2048)
                i.send(mes)
                compt+=1
    List.remove(c)
    cles_pub.remove(cles)
    List_nom.remove(nom)
    c.close()

 
 
def main():
    Host = 'localhost'
    Port = 5001
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    s.bind((Host, Port)) 
    s.listen(5)
    print("serveur demarrer")
    while True:
        c,addr = s.accept()
        nom = c.recv(1024)
        List.append(c)
        List_nom.append(nom.decode())
        cles = c.recv(1024)
        cles_pub.append(cles.decode())
        print('Connection de ',addr[1])
        thread_all = threading.Thread(target = threaded,args=[c,nom.decode(),addr[1],cles.decode()])
        thread_all.start()
    thread_all.stop()
    s.close()
 
if __name__ == '__main__':
    main()