import numpy as np
import math
import operator
import sys
from itertools import permutations 
from itertools import combinations 
from collections import defaultdict

punigram = ['e', 'a', 'r', 'i', 'o', 't', 'n', 's', 'l', 'c', 'u', 'd', 'p', 'm', 'h', 'g', 'b', 'f', 'y', 'w', 'k', 'v', 'x', 'z', 'j', 'q']

pqdgram = ['that','ther','tion','with','tion','here','atio','ould', 'ight','have','hich','whic','with']

pbgram = ['th','he','in','er','an','re','nd','at','on','nt','ha','ta','es','st']

# ptrgram = ['the','and','tha','ent','ing','ion','tio','for','nde','has','nce','edt','tis','oft','sth','men']

ptrgram = ['the', 'and','ing','her','hat','his','tha','ere','for','ent','ion','nde']

pqdgram = ['that','ther','tion','with','tion','here','atio','ould', 'ight','have','hich','whic','with']


ic_engl = 0.0686

zeromat = [[0,0],[0,0]]


######################## prodplmat function  starts ############################

def prodplmat(l):
	#print(l)
	plmat=[]
	for i in l:
		k=[]
		for j in range(len(i)):
			u=ord(i[j])-97
			k.append(u)
		plmat.append(k)
	#print(plmat)	
	plmat = np.array(plmat).transpose()
	#print(plmat)
	return plmat

######################## prodplmat function  ends ############################


######################## prodcipmat function  starts ############################

def prodcipmat(k):
	#print(l)
	cipmat=[]
	for i in k:
		m=[]
		for j in range(len(i)):
			u=ord(i[j])-97
			m.append(u)
		cipmat.append(m)
	#print('cipmat wo tp - ',cipmat)	
	cipmat = np.array(cipmat).transpose()
	#print('cipmat with tp- ',cipmat)
	return cipmat

######################## prodcipmat function  ends ############################


######################## prodkeyinv function  starts ############################


def prodkeyinv(plmat,cipmat):
	#print('in the prodkey function')
	pdetval = int(round(np.linalg.det(plmat)))
	if math.gcd(pdetval,26)!=1:
		return zeromat,zeromat
	pinvmat1 = np.linalg.inv(plmat)
	padjmat = pinvmat1*pdetval
	pdetinv=1
	for i in range(1,26):
		val = (i*pdetval)%26
		if val == 1:
			pdetinv=i
			break
	pinvmat = padjmat * pdetinv
	pinvmat = (np.remainder(pinvmat,26)).round()
	keymat = cipmat.dot(pinvmat)
	keymat = (np.remainder(keymat,26)).round()
	kdetval = int(round(np.linalg.det(keymat)))
	if math.gcd(kdetval,26)!=1:
		return zeromat,zeromat
	kinvmat1 = np.linalg.inv(keymat)
	kadjmat = kinvmat1*kdetval
	kinvdet=1
	for i in range(1,26) :
		val = (i*kdetval)%26
		if val == 1:
			kinvdet=i
			break
	kinvmat=kadjmat*kinvdet
	kinvmat = (np.remainder(kinvmat,26)).round().tolist()
	keymat = keymat.tolist()
	#print(type(kinvmat))
	return keymat,kinvmat		

######################## prodkeyinv function  end ############################


######################## prodciplist function  starts ############################


def prodciplist(cipchunk):
	ciplist=[]
	#print('cipchunk - ',cipchunk)
	for i in cipchunk:
		k=[]
		for j in range(len(i)):
			u=ord(i[j])-97
			k.append(u)
		ciplist.append(k)	
	#print('ciplist - ',ciplist)
	return ciplist		

######################## prodciplist function  ends ############################


######################## producetext function  starts ############################


def producetext(cipchunk,keyinvobt):
	ciplist = prodciplist(cipchunk)  # used to convert cipchunks into numerical chunks
	plist = []
	keyinvobt=np.array(keyinvobt)
	for a in ciplist:
		b = keyinvobt.dot(a)
		b = list(np.remainder(b,26))
		plist.append(b)	
	#print('plist - ',plist)
	pltext=""
	for i in plist:
		chunk=''
		for j in range(len(i)):
			k=chr(int(i[j]+97))
			chunk=chunk+k
		pltext=pltext+chunk
	#print('pltext - ',pltext)		
	return pltext

######################## producetext function  ends ############################

######################## isValidIoc function  starts ############################


def isValidIoc(ioc_prod):
	upplim = 0.072
	lowlim = 0.060
	if lowlim <= ioc_prod and ioc_prod <= upplim :
		#print("ioc prod is in range")
		return True
	else :
		#print('ioc prod is not in range')
		return False
		
######################## isValidIoc function  ends ############################


######################## calculate_ioc function  starts ############################

def calculate_ioc(text):
	textlen = len(text)
	deno = textlen*(textlen-1)
	alphcnt = [0]*26
	#print('alphcnt - ',alphcnt)
	summ = 0
	for k in text:
		m=ord(k)-97
		alphcnt[m]=alphcnt[m]+1
	for k in range(len(alphcnt)):
		u = alphcnt[k]
		summ = summ + (u*(u-1))
	#print('sum -',summ)
	#print('deno - ',deno)
	ioc = summ/deno
	#print('ioc - ',ioc)
	#print('alphcnt - ',alphcnt)
	#print('text length - ',textlen)		
	return ioc

######################## calculate_ioc function  ends ############################


######################## prodpltext function  starts ############################


def prodpltext(cipchunk,cipinput):
	#print('cipchunk - ',cipchunk)
	n = len(cipchunk[0])
	print("n - ",n)
	#print('cipchunk -',cipchunk)
	#print('cipinput - ',cipinput)

	if n==1:
		plist = punigram
	elif n==2:
		plist = pbgram
	elif n==3:
		plist = ptrgram
	elif n==4:
	    plist = pqdgram
	else :
		print("key length should be 1,2,3 or 4")
		return

	# print('plist - ',plist)
	#ptextprod = []
	#ioclist = []
	kinvlist = []
	keylist = []
	permplnlist = permutations(plist,n)
	pchklist = list(permplnlist)

	combciplist = combinations(cipinput,n)
	cchklist = list(combciplist)

	outputfile = open("out_crypt.txt","w")

	condition = 0
	for l in cchklist:
		cipmat = prodcipmat(l)
		#print('cipmat - ',cipmat)
		for k in pchklist:
			plmat = prodplmat(k)
			keyobt,keyinvobt = prodkeyinv(plmat,cipmat)
			#print('key obta- ',keyinvobt)
			if keyinvobt != zeromat and keyobt not in keylist:
				kinvlist.append(keyinvobt)
				keylist.append(keyobt)
				text = producetext(cipchunk,keyinvobt)
				#print('text - ',text)
				iocval = calculate_ioc(text)
				#print('iocval -',iocval)
				if isValidIoc(iocval) == True:
					condition = 1
					outputfile.write('key -'+str(keyobt)+"\n")
					outputfile.write('keyinverse -'+str(keyinvobt)+"\n")
					outputfile.write('ioc value -'+str(iocval)+"\n")
					outputfile.write(text+"\n \n")

	if condition == 0:
		outputfile.write("no output is written, may be assumed plaintext chunks are not properly mapped to file")

	outputfile.close()				

			

######################## prodpltext function  ends ############################


######################## cryptanlysis function  starts ############################

def cryptanalysis(cipherinput,klength):
	ciplen = len(cipherinput)
	print('cipher length - ',ciplen)

	cipchunk = []
	cipcnt = {}

	for i in range(0,ciplen,klength):
		k = cipherinput[i:i+klength]
		cipchunk.append(k)
		if k in cipcnt:
			cipcnt[k]=cipcnt[k]+1
		else:
			cipcnt[k]=1

	if len(cipchunk[-1])!=klength :
		cipcnt.pop(cipchunk[-1])
		cipchunk=cipchunk[:-1]			
	#print(cipchunk)
	sortcipcnt = list(reversed(sorted(cipcnt.items(), key=operator.itemgetter(1))))
	#print('sortcipcnt - ',sortcipcnt)
	#print('\n')
	lcnt=0
	cipinput=[]
	for k in sortcipcnt:
		cipinput.append(k[0])
		lcnt=lcnt+1
		if lcnt==10:
			break
	print('cipinput - ',cipinput)			

	prodpltext(cipchunk,cipinput)		 # calling prodpltext function
	print('in the cryptanalysis function')

######################## cryptanlysis function ends ############################


######################## input taken ############################



# keylengthfile = open("keylen.txt",'r')  # taking keylength
# keylengthinput = keylengthfile.read()
# keylengthfile.close()

# klength = int(keylengthinput)

# cipherinputfile = open("cipher_crypt.txt",'r') # taking cipher input
# cipherinput = cipherinputfile.read()
# cipherinputfile.close()

# print(klength)
# print(cipherinput)

klength = int(sys.argv[1])
cipherinputtext = sys.argv[2]

cipherinputfile = open(cipherinputtext,'r') # taking cipher input
cipherinput = cipherinputfile.read()
cipherinputfile.close()

cryptanalysis(cipherinput,klength) # calling cryptanalysis function



######################## input taken ############################
