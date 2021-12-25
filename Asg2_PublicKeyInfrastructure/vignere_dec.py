

def vignere_decryption(keyinput,decmsginput):
	klen=len(keyinput)
	decmsglen=len(decmsginput)

	dcmsgchunk=[]
	for i in range(0,decmsglen,klen):
		chk=decmsginput[i:i+klen]
		dcmsgchunk.append(chk)
	print('dcmsgchunk - ',dcmsgchunk)

	msgchk=''

	for chk in dcmsgchunk:
		dechk=''
		for i in range(len(chk)):
			k=ord(chk[i])
			if k>=97 and k<=122:
				m=ord(keyinput[i])
				if m>=97 and m<=122:
					off=m-97
				else:
				    off=m-65
				k=(k-97-off)%26
				k=k+97
			elif k>=65 and k<=91:
			    m=keyinput[i]
			    if m>=97 and m<=122:
			        off=m-97
			    else:
			        off=m-65
			    k=(k-65-off)%26
			    k=k+97
			else:
			    m=k
			    k=m
			t=chr(k)
			dechk=dechk+t
		msgchk=msgchk+dechk

	
	print('decrypted message - ',msgchk)

	outputfile=open("vig_out_decryt_msg.txt","w")
	outputfile.write(str(msgchk))
	outputfile.close()	
		





keyinputfile = open('vignerekey.txt','r')
keyinput = keyinputfile.read()
keyinputfile.close()

decmsginputfile = open('vig_inp_dec_msg.txt','r')
decmsginput = decmsginputfile.read()
decmsginputfile.close()

vignere_decryption(keyinput,decmsginput)