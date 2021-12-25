



def vignere_encryption(keyinput,messageinput):
	klen=len(keyinput)
	msglen=len(messageinput)

	msgchunk=[]
	for i in range(0,msglen,klen):
		chk=messageinput[i:i+klen]
		msgchunk.append(chk)
	print('msgchunk - ',msgchunk)

	demsgchk=''

	for chk in msgchunk:
		enchk=''
		for i in range(len(chk)):
			k=ord(chk[i])
			if k>=97 and k<=122:
				m=ord(keyinput[i])
				if m>=97 and m<=122:
					off=m-97
				else:
				    off=m-65
				k=(k-97+off)%26
				k=k+97
			elif k>=65 and k<=91:
			    m=keyinput[i]
			    if m>=97 and m<=122:
			        off=m-97
			    else:
			        off=m-65
			    k=(k-65+off)%26
			    k=k+97
			else:
			    m=k
			    k=m
			t=chr(k)
			enchk=enchk+t
		demsgchk=demsgchk+enchk

	
	print('encrypted message - ',demsgchk)

	outputfile=open("vig_out_enc_msg.txt","w")
	outputfile.write(str(demsgchk))
	outputfile.close()	
		

keyinputfile = open('vignerekey.txt','r')
keyinput = keyinputfile.read()
keyinputfile.close()

messageinputfile = open('message.txt','r')
messageinput = messageinputfile.read()
messageinputfile.close()

vignere_encryption(keyinput,messageinput)
