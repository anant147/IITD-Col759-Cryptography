import string
import gmpy2
from gmpy2 import mpz
import random
import math

chrmap={
	0:'a',1:'b',2:'c',3:'d',
	4:'e',5:'f',6:'g',7:'h',
	8:'i',9:'j',10:'k',11:'l',12:'m',
	13:'n',14:'o',15:'p',16:'q',
	17:'r',18:'s',19:'t',20:'u',21:'v',22:'w',
	23:'x',24:'y',25:'z',26:'0',
	27:'1',28:'2',29:'3',30:'4',31:'5',32:'6',33:'7',34:'8',35:'9'
}

numap = {v: k for k, v in chrmap.items()}

print('chrmap - ',chrmap)
print('\n')
print('numap - ',numap)
print('\n')


def cleantext(messageinput):
	msglower=messageinput.lower()
	reqmsg=''

	for ch in msglower:
		m=ord(ch)
		if (m >=97 and m<=122) or (m>=48 and m <= 57):
			reqmsg=reqmsg+ch		

	return reqmsg

def vignere_encryption(keyinput,messageinput):
	clmsg=cleantext(messageinput)
	print('clean msg - ',clmsg)
	klen=len(keyinput)
	clmsglen=len(clmsg)
	msgchk=[]

	for i in range(0,clmsglen,klen):
		chk=clmsg[i:i+klen]
		msgchk.append(chk)
	print('msgchk - ',msgchk)
	print('\n')

	vig_enc_msg=''

	for chk in msgchk:
		enchk=''
		for i in range(len(chk)):
			val1=numap[chk[i]]
			val2=numap[keyinput[i]]
			val=(val1+val2)%36
			
			chval=chrmap[val]
			enchk=enchk+chval
		vig_enc_msg=vig_enc_msg+enchk

	print('\n before append - ',vig_enc_msg)	
	vig_enc_msg = str(klen)+keyinput+vig_enc_msg
	print('\n after append - ',vig_enc_msg)
	return vig_enc_msg

###################################################################################################################	

def encrypt_val(chk,d,n):
    chunk=chk[::-1]
    sumval=0

    for i in range(len(chunk)):
        k=chunk[i]
        val=numap[k]
        val=val*(36**i)
        sumval=sumval+val
#     print(sumval)
    sumval=gmpy2.powmod(sumval,d,n)
    return sumval   

def get_encrypt_chk(val,bsize):
    chk=''

    for i in range(bsize,-1,-1):
        k=val//(36**i)
        chrval=chrmap[k]
        val=val%(36**i)
        chk=chk+chrval

    return chk  


def encrypt_by_user(msg,bsize,d,n):
    mlen=len(msg)
    msgchk=[]
    for i in range(0,mlen,bsize):
        chk=msg[i:i+bsize]
        msgchk.append(chk)
#     print(msgchk)

    if len(msgchk[len(msgchk)-1]) != bsize:
        val=bsize-len(msgchk[len(msgchk)-1])
        appstr='x'*val
        msgchk[len(msgchk)-1]=msgchk[len(msgchk)-1]+appstr

    enmsgchk=[]
    enmsg=''    
#     print(msgchk)
    for chk in msgchk:
       enval=encrypt_val(chk,d,n)
       print(enval)
       enchk=get_encrypt_chk(enval,bsize)
       enmsgchk.append(enchk)
       enmsg=enmsg+enchk

    return enmsg 


  

#############################################################################################3



messageinputfile = open('message.txt','r')
messageinput = messageinputfile.read()
messageinputfile.close()

vigklen = random.randrange(20,30,1)
print('vigklen - ',vigklen)
print('\n')

keyinput = ''.join(random.choices(string.ascii_lowercase, k = vigklen))
print('keyinput - ',keyinput)
print('\n')

enc_msg_by_vig=vignere_encryption(keyinput,messageinput)
print('enc_msg_by_vig - ',enc_msg_by_vig)
print('\n')


vigencrfile=open('vigencr_msg.txt','w')
vigencrfile.write('vig encrypted text - '+str(enc_msg_by_vig))
vigencrfile.close()

sender_privkeyfile=open('u1_privkey_dir.txt','r')
sender_privkey=sender_privkeyfile.read()
sender_privkeyfile.close()

sender_datakey=sender_privkey.split()

print('sender_datakey - ',sender_datakey)

sender_d=int(sender_datakey[0])
sender_n=int(sender_datakey[1])

print('sender_d - ',sender_d)
print('sender_n - ',sender_n)


# bsize=10

# while((36**bsize)<sender_n):
# 	bsize=bsize+1

# bsize=bsize-1
bsize = math.floor(math.log(sender_n, 36))


# enc_msg_by_vig=messageinput # testing  

######## encrypytion of vignere encrypted text by private key of sender
msg_encrypt_by_sender=encrypt_by_user(enc_msg_by_vig,bsize,sender_d,sender_n)



print('msg_encrypt_by_sender - ',msg_encrypt_by_sender)


msg_encrypt_by_sender_file=open('msg_encrypt_by_sender.txt',"w")
msg_encrypt_by_sender_file.write(str(msg_encrypt_by_sender))
msg_encrypt_by_sender_file.close()


all_pubkeyfile=open("user_pubkey_dir.txt","r")
all_pubkey=all_pubkeyfile.readlines()

for lin in all_pubkey:
	linval = lin.split(':')
	if linval[0].find('User2') != -1:
		rec_pubkeydata=linval[1]
		print('\n rec_pubkeydata - ',rec_pubkeydata)
		break

all_pubkeyfile.close()

rec_pubkey=rec_pubkeydata.split()

receiver_enc_e=int(rec_pubkey[0])
print(' \n receiver_enc_e - ',receiver_enc_e)

receiver_enc_n=int(rec_pubkey[1])
print(' \n receiver_enc_n - ',receiver_enc_n)


ca_pubkeyfile=open("ca_pubkey_dir.txt","r")
ca_pubkeydata=ca_pubkeyfile.read()


ca_pub=ca_pubkeydata

ca_pubkeyfile.close()


ca_pubkey=ca_pub.split()

ca_e = int(ca_pubkey[0])
ca_n = int(ca_pubkey[1])


print('\n ca_e - ',ca_e)
print(' \n ca_n - ',ca_n)


receiver_e=gmpy2.powmod(receiver_enc_e,ca_e,ca_n)

receiver_n=gmpy2.powmod(receiver_enc_n,ca_e,ca_n)


print('\n receiver_e - ',receiver_e)

print('\n receiver_n - ',receiver_n)


# bsize=10

# while((36**bsize)<receiver_n):
# 	bsize=bsize+1

# bsize=bsize-1
bsize = math.floor(math.log(receiver_n,36))

######## encrypytion of sender (by private key) encrypted text by public key of receiver

msg_encrypt_by_rec_publ=encrypt_by_user(msg_encrypt_by_sender,bsize,receiver_e,receiver_n)


print('msg_encrypt_by_rec_publ - ',msg_encrypt_by_rec_publ)


sender_encryp_msgfile=open('sender_encryp_msg_dir.txt',"w")
sender_encryp_msgfile.write(str(msg_encrypt_by_rec_publ))
sender_encryp_msgfile.close()




