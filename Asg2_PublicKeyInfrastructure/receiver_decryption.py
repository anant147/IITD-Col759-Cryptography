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

def vignere_decryption(messageinput):
    klen=''
    messageinput=messageinput.strip()
    
    i=0
    cond=1
    while cond==1:
        m=ord(messageinput[i])
        if m>=48 and m <=57:
            klen=klen+messageinput[i]
            i=i+1
        else:
            cond=0
            break
    
    if len(klen)==0:
        return 'Wrong input'
            
    klen=int(klen)
    
    messageinput=messageinput[i:]
    keyinput=messageinput[0:klen]
    messageinput=messageinput[klen:]
    print('klen - ',klen)
    print('keyinput - ',keyinput)
    print('messageinput - ',messageinput)
    
    mlen=len(messageinput)
    msgchk=[]
    
    for i in range(0,mlen,klen):
        chk=messageinput[i:i+klen]
        msgchk.append(chk)
    
    print('\n msgchk - ',msgchk)
    print('\n')
    
    vig_dec_msg=''

    for chk in msgchk:
        dechk=''
        for i in range(len(chk)):
            val1=numap[chk[i]]
            val2=numap[keyinput[i]]
            val=(val1-val2)%36
			
            chval=chrmap[val]
            dechk=dechk+chval
        vig_dec_msg=vig_dec_msg+dechk
    print('vig_dec_msg - ',vig_dec_msg)
    
    return vig_dec_msg

############################################################################################################################################

def decrypt_val(enchk,d,n):
    sumval=0

    for i in range(0, len(enchk)):
        k=enchk[len(enchk)-i-1]
        val=numap[k]
        val=val*(36**i)
        sumval=sumval+val
    # print(sumval)
    sumval=gmpy2.powmod(sumval,d,n)
    return sumval


def get_decrypt_chk(decval,bsize):
    chk=''

    for i in range(bsize-2, -1, -1):
        k=decval//(36**i)
        # print(k)
        chrval=chrmap[k%36]
        decval=decval%(36**i)
        chk=chk+chrval

    return chk  


def decrypt_by_user(enmsg,bsize,d,n):
    emlen=len(enmsg)
    emsgchk=[]

    for i in range(0,emlen,(bsize)):
        chk=enmsg[i:i+bsize]
        emsgchk.append(chk)
    # print(emsgchk)
    # if len(emsgchk[len(emsgchk)-1]) !=(bsize+1):
    #   val=(bsize+1)-len(emsgchk[len(emsgchk)-1])
    #   appstr='x'*val
    #   emsgchk[len(emsgchk)-1]=emsgchk[len(emsgchk)-1]+appstr

    decmsgchk=[]
    decmsg=''   

    for enchk in emsgchk:
        # print(enchk)
        decval=decrypt_val(enchk,d,n)
        # print(decval)
        dechk=get_decrypt_chk(decval,bsize)
        decmsgchk.append(dechk)
        decmsg=decmsg+dechk

    return decmsg.split("xxxxxxxxxx")[0]




############################################################################################################################################


# reading encrypted msg by the sender (user1)
encryptmsgfile = open('sender_encryp_msg_dir.txt','r')
encmsginput = encryptmsgfile.read().replace('\n','')
encryptmsgfile.close()

# reading private key of the receiver (user2)
receiver_privkeyfile = open('u2_privkey_dir.txt','r')
receiver_privkeydata = receiver_privkeyfile.read()
receiver_privkeyfile.close()

receiver_data = receiver_privkeydata.split()

receiver_d = int(receiver_data[0])
receiver_n = int(receiver_data[1])


# getting block size for the receiver value of  n
# bsize=10

# while((36**bsize)<receiver_n):
# 	bsize=bsize+1

# bsize=bsize

bsize = math.floor(math.log(receiver_n, 36))

print('\n receiver_d - ',receiver_d)
print('\n receiver_n - ',receiver_n)
print('\n bsize - ',bsize)


decrypted_msg_receiver_priv = decrypt_by_user(encmsginput,bsize+1,receiver_d,receiver_n)

print('\n decrypted_msg_receiver_priv - ',decrypted_msg_receiver_priv)


decrypted_msg_receiver_priv_file=open('decrypted_msg_receiver_priv.txt',"w")
decrypted_msg_receiver_priv_file.write(str(decrypted_msg_receiver_priv))
decrypted_msg_receiver_priv_file.close()


#################################################################################################################################


# reading public key of sender(user1)
all_pubkeyfile=open("user_pubkey_dir.txt","r")
all_pubkey=all_pubkeyfile.readlines()

for lin in all_pubkey:
	linval = lin.split(':')
	if linval[0].find('User1') != -1:
		send_pubkeydata=linval[1]
		print('\n send_pubkeydata - ',send_pubkeydata)
		break


all_pubkeyfile.close()

send_pubkey=send_pubkeydata.split()

send_pubkey_enc_e=int(send_pubkey[0])
send_pubkey_enc_n=int(send_pubkey[1])


# reading public key of ca
ca_pubkeyfile=open("ca_pubkey_dir.txt","r")
ca_pubkeydata=ca_pubkeyfile.read()


ca_pub=ca_pubkeydata
ca_pubkeyfile.close()
ca_pubkey=ca_pub.split()

ca_e = int(ca_pubkey[0])
ca_n = int(ca_pubkey[1])

print('\n ca_e - ',ca_e)
print(' \n ca_n - ',ca_n)


send_pubkey_e=gmpy2.powmod(send_pubkey_enc_e,ca_e,ca_n)
send_pubkey_n=gmpy2.powmod(send_pubkey_enc_n,ca_e,ca_n)

# bsize=10

# while((36**bsize)<receiver_n):
# 	bsize=bsize+1

# bsize=bsize

bsize= math.floor(math.log(send_pubkey_n,36))

# decryption by the sender public key for the decrypted_msg_receiver_priv

decrypt_msg_sender_publ=decrypt_by_user(decrypted_msg_receiver_priv,bsize+1,send_pubkey_e,send_pubkey_n)

print(' decrypt_msg_sender_publ -  ',decrypt_msg_sender_publ)


decrypt_msg_sender_publ_file=open('decrypt_msg_sender_publ.txt',"w")
decrypt_msg_sender_publ_file.write(str(decrypt_msg_sender_publ))
decrypt_msg_sender_publ_file.close()


msg_by_vig_dec = vignere_decryption(decrypt_msg_sender_publ)
print('obtained message -  ',msg_by_vig_dec)


msg_by_vig_dec_file=open('original_msg_by_vig_dec_dir.txt',"w")
msg_by_vig_dec_file.write(str(msg_by_vig_dec))
msg_by_vig_dec_file.close()