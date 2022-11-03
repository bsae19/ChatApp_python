import socket
import threading
import sys
from Crypto.Util.number import getPrime,inverse

mycles=[]
message=""
def gen_rsa_keypair(bits):
    p=getPrime(bits//2)
    q=getPrime(bits//2)
    assert(p != q)
    n=p*q
    phi_n=(p-1)*(q-1)
    e=65537
    assert(e < phi_n and phi_n%e != 0)
    d=inverse(e,phi_n)
    return((e,n),(d,n))

def rsa_enc(m,key):
    msg=int.from_bytes(m.encode('utf-8'),'big')
    assert(msg < key[1])
    res=pow(msg,key[0],key[1])
    return res

def rsa_dec(msg,key):
    msg=pow(msg,key[0],key[1])
    assert(msg < key[1])
    res=msg.to_bytes((msg.bit_length()+7)//8,'big').decode('utf-8')
    return res



def recu(c,nom):
	while True:
		data = c.recv(1024)
		if not data:
			print('Serveur deconnecter')
			break
		dat=data.decode()
		if dat=="-1":
			print("aucune personne avec ce nom")
		elif dat[0]=='@':
			dat = dat.replace('@','')
			ncles=dat.split()
			nc=[int(ncles[0]),int(ncles[1])]
			me=message.split()
			name=me.pop(0)
			mess="mp de "+nom
			for i in me:
				mess=mess+" "+i
			aff_mess="mp pour "
			for i in me:
				aff_mess=aff_mess+" "+i
			print(aff_mess)
			msg_chiffre=rsa_enc(mess,nc)
			c.send((str(msg_chiffre)).encode())
		elif dat[0]=='|':
			dat = dat.replace('|','')
			ncles=dat.split()
			nc=[int(ncles[0]),int(ncles[1])]
			mes=nom+" -> "+message
			msg_chiffre=rsa_enc(mes,nc)
			c.send((str(msg_chiffre)).encode())
		else:
			msg_dechiffre=rsa_dec(int(dat),mycles)
			print(msg_dechiffre)
	thread_reicv.stop()
	c.close()


def Main():
	Host = 'localhost'
	Port = 5001
	c = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
	c.connect((Host, Port))
	nom = input('entrez votre nom: ')
	sys.stdout.write('\x1b[1A') 
	sys.stdout.write('\x1b[2K')
	c.send(nom.encode())
	cpub,cpriv=gen_rsa_keypair(2048)
	global mycles
	mycles=cpriv
	c.send((str(cpub[0])+" "+str(cpub[1])).encode())
	global thread_reicv
	thread_reicv = threading.Thread(target = recu,args=[c,nom])
	thread_reicv.start()
	while True:
		global message
		message = input('')
		sys.stdout.write('\x1b[1A') 
		sys.stdout.write('\x1b[2K')
		if message[0]=='@':
			mot=message.split()
			c.send(mot[0].encode())
		else:
			c.send("all".encode())
	thread_reicv.stop()
	s.close()

if __name__ == '__main__':
	Main()
