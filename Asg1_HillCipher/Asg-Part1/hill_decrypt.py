import numpy as np
import math
import sys

############# decryption function starts #############

def decrypt(ciphertext,keymatrix):
	detval = int(round(np.linalg.det(keymatrix)))
	invmat1 = np.linalg.inv(keymatrix) 
	#print("invmat1 = ",invmat1)
	adjmat = invmat1*detval
	#print("adjmat = ",adjmat)

	for i in range(1,26):
		val = (i*detval)%26
		if val == 1:
			detinv =i
			break
	invmatm = adjmat * detinv	
	#print("invmatm :- ",invmatm)	
	invmatm = (np.remainder(invmatm,26)).round()
	#print("invmatm :- ",invmatm)
	n = len(keymatrix)
	cipsize = len(ciphertext)
	cipherchunk = []
	for i in range(0,cipsize,n):
		cipherchunk.append(ciphertext[i:i+n])
	#print("case 1 - cipherchunk = ",cipherchunk)
	totchunks = len(cipherchunk)
	lastchunksize = len(cipherchunk[totchunks-1])
	charadd = 0
	if (lastchunksize!=n):
		charadd = n-lastchunksize
		temp = 'z'*charadd
		cipherchunk[totchunks-1]+=temp
	#print("case 2 - cipherchunk = ",cipherchunk)
	cipmatnum = []
	plainmatnum = []
	for i in cipherchunk:
		a = []
		for j in range(len(i)):
			k = ord(i[j])-97
			a.append(k)
		cipmatnum.append(a)
		b = invmatm.dot(a)
		#print("without mod b = ",b)
		b = list(np.remainder(b,26))
		#print("after mod26 b = ",b)
		plainmatnum.append(b)
	#print("cipmatnum = ",cipmatnum)
	# plainmatnum = plainmatnum.astype(int)
	#print("plainmatnum = ",plainmatnum)

	plaintext = ""

	for i in range(len(plainmatnum)):
		chunks=""
		for j in range(len(plainmatnum[i])):
			k=chr(int(plainmatnum[i][j])+97)
			chunks=chunks+k
		#print('chunks - ',chunks)
		plaintext=plaintext+chunks
	#print('from loop, plaintext obtained - ',plaintext)
	prodplnlen = len(plaintext)
	plaintext = plaintext[0:prodplnlen-charadd]
	plnlen = len(plaintext)
	cnt = 0
	while cnt!=(n-1):
		if plaintext[-1] == 'z':
			plaintext = plaintext[0:-1]
			cnt=cnt+1
		else:
			break

	#print('edited plaintext = ',plaintext)
	return plaintext


############## decryption function ends ###########

keyfile = open("key.txt",'r')
keyinput = keyfile.read()

keyfile.close()



#print('taking input for key :- ')

keyinp = list(map(int, keyinput.split()))

#print('length of value entered :')

sz = len(keyinp)

#print(sz)

b = math.sqrt(sz)

#print('sqrt of sz - ',b)

cond1 = (b==math.floor(b))

###################################################

######### checking condition for key ###########

if cond1==True:
	n = int(b)
	keymatrix = np.array(keyinp).reshape(n,n)
	detval = int(round(np.linalg.det(keymatrix)))
	#print("determinant value - ",detval)
	if detval<0:
		deta = detval%26
	else:
	    deta = detval
	res = math.gcd(deta,26)
	cond2 = res==1
else:
	print('condition 1 fails')
	sys.exit(0)

##################################################

if(cond1==True and cond2==True):
	#print("yes")
	#print(keymatrix) 
	cipherfile = open("ciphertext.txt","r")
	ciphertext = cipherfile.read()
	cipherfile.close()
	ptextout = decrypt(ciphertext,keymatrix)
	plainoutfile = open("plainout.txt","w")
	plainoutfile.write(ptextout)
	plainoutfile.close()
	print("--ptext output = ",ptextout)
else:
    print("no")	
    print("cond1 and cond2 fail")
    sys.exit(0)

########################################