import numpy as np
import math
import sys

########### encrypt function ###############

def encrypt(plaintext,keymatrix):
	plainlist = plaintext.split()
	#print("plainlist = ",plainlist)
	s = ''
	plaininp = s.join(plainlist)
	#print("plaininp = ",plaininp)
	n = len(keymatrix)
	plsize = len(plaininp)
	plainchunk = []

	for i in range(0,plsize,n):
		plainchunk.append(plaininp[i:i+n])
	#print("case 1 - chunks = ",plainchunk)	
	totchunks = len(plainchunk)
	lastchunksize = len(plainchunk[totchunks-1])
	charadd = 0
	if (lastchunksize!=n):
		charadd = n-lastchunksize
		temp = 'z'*charadd
		plainchunk[totchunks-1]+=temp
	#print("case 2 - chunks = ",plainchunk)
	cipmatnum = []
	plainmatnum = []
	for i in plainchunk:
		a=[]
		for j in range(len(i)):
			k = ord(i[j])-97
			a.append(k)
		plainmatnum.append(a)
		b = keymatrix.dot(a)
		# print("b = ",b)
		b = list(np.remainder(b,26))
		# print("b = ",b)
		cipmatnum.append(b)
	#print("plainmatnum = ",plainmatnum)
	#print("cipmatnum = ",cipmatnum)

	ciphertext = ""

	for i in range(len(cipmatnum)):
		chunks=""
		for j in range(len(cipmatnum[i])):
			k=chr(cipmatnum[i][j]+97)
			chunks=chunks+k
		#print('chunks - ',chunks)
		ciphertext=ciphertext+chunks
	#print('from loop,ciphertext obtained - ',ciphertext)	
	#prodciplen = len(ciphertext)
	#ciphertext = ciphertext[0:prodciplen-charadd]
	#print('edited ciphertext = ',ciphertext)		

	#print('\n in the function \n')
	return ciphertext

	############ encrypt function ends ##############

########## taking input of the key here #################


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

 # cond1 is for checking whether matrix is square matrix or not
 # cond2 is for checking whether inverse of the matrix exist or not. 
 # given character space of plaintext and cipbhertext is a-z i,e 26 alphabets 

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
	#print('condition 1 fails')
	sys.exit(0)


if(cond1==True and cond2==True):
	#print("yes")
	#print(keymatrix) 
	plainfile = open("plaintext.txt","r")
	plaintext = plainfile.read()
	plainfile.close()
	ciphertext = encrypt(plaintext,keymatrix)
	print("ciphertext - ",ciphertext)
	cipherfile = open("cipherout.txt","w")
	cipherfile.write(ciphertext)
	cipherfile.close()
else:
    print("no")	
    print("cond1 and cond2 fail")
    sys.exit(0)

