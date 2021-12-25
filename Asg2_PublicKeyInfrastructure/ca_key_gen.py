import gmpy2
from gmpy2 import mpz
import random

def generate_strprime(bitcount):
	startval=random.getrandbits(bitcount)
	startval=(1<<511)|startval
	prevprime=gmpy2.next_prime(startval)

	while not gmpy2.is_prime(prevprime):
		prevprime=gmpy2.next_prime(prevprime)

	curprime=gmpy2.next_prime(prevprime)

	while not gmpy2.is_prime(curprime):
		curprime=gmpy2.next_prime(curprime)

	cond=1
	cnt=0
	while(cond==1):
		aftprime=gmpy2.next_prime(curprime)
		while not gmpy2.is_prime(aftprime):
			aftprime=gmpy2.next_prime(aftprime)
		# print('\n prevprime - ',prevprime)
		# print('curprime - ',curprime)
		# print('aftprime - ',aftprime)
		cnt=cnt+1

		if curprime > ((prevprime+aftprime)/2):
			break
		else:
			prevprime=curprime
			curprime=aftprime

		if cnt == 20:
			cnt=0
			startval=random.getrandbits(bitcount)
			startval=(1<<511)|startval
			prevprime=gmpy2.next_prime(startval)

			while not gmpy2.is_prime(prevprime):
				prevprime=gmpy2.next_prime(prevprime)

			curprime=gmpy2.next_prime(prevprime)

			while not gmpy2.is_prime(curprime):
				curprime=gmpy2.next_prime(curprime)

	return curprime

def generate_e(phi):
	e=random.randrange(2,phi,1)

	if e%2==0:
		e=e+1

	while(gmpy2.gcd(e,phi)!=1 and e < phi):
		e=e+2

		if e >= phi:
			e=random.randrange(2,phi,1)
			if e%2==0:
				e=e+1

	return e				



def encrypt_by_ca(val,e,n):
	result=gmpy2.powmod(val,e,n)
	return result

def generate_prime(bitcount):
	startval=random.getrandbits(bitcount)
	reqprime=gmpy2.next_prime(startval)
	return reqprime



# code for ca key generation
p_ca = generate_strprime(512)
print('p_ca - ',p_ca)
print('\n')

q_ca = generate_strprime(512)
print('q_ca - ',q_ca)
print('\n')


n_ca = (p_ca*q_ca)
phi_ca = (p_ca-1)*(q_ca-1)

print('n_ca - ',n_ca)
print('\n')


print('phi_ca - ',phi_ca)
print('\n')

e_ca = generate_e(phi_ca)
print('e_ca - ',e_ca)
print('\n')

d_ca = gmpy2.invert(e_ca,phi_ca)
print('d_ca - ',d_ca)
print('\n')

# writing public key of ca in ca  public key directory
ca_pubkey_dir=open("ca_pubkey_dir.txt","w")
ca_pubkey_dir.write(str(e_ca)+" "+str(n_ca))
ca_pubkey_dir.close()

print('\n \n')


# code for user1 key generation
p_u1 = generate_strprime(512)
print('p_u1- ',p_u1)
print('\n')

q_u1 = generate_strprime(512)
print('q_u1 - ',q_u1)
print('\n')

n_u1 = (p_u1*q_u1)
phi_u1 = (p_u1-1)*(q_u1-1)

print('n_u1 - ',n_u1)
print('\n')

print('phi_u1 - ',phi_u1)
print('\n')

e_u1 = generate_e(phi_u1)
print('e_u1 - ',e_u1)
print('\n')

d_u1 = gmpy2.invert(e_u1,phi_u1)
print('d_u1 - ',d_u1)
print('\n')


enc_e_u1 = encrypt_by_ca(e_u1,d_ca,n_ca)
print('enc_e_u1 - ',enc_e_u1)
print('\n')


enc_n_u1 = encrypt_by_ca(n_u1,d_ca,n_ca)
print('enc_n_u1 - ',enc_n_u1)
print('\n')


# writing private key of user1 in user1 private key directory
u1_privkey_dir=open("u1_privkey_dir.txt","w")
u1_privkey_dir.write(str(d_u1)+" "+str(n_u1))
u1_privkey_dir.close()

print('\n \n')

# code for user2 key generation
p_u2 = generate_strprime(512)
print('p_u2- ',p_u2)
print('\n')

q_u2 = generate_strprime(512)
print('q_u2 - ',q_u2)
print('\n')


n_u2 = (p_u2*q_u2)
phi_u2 = (p_u2-1)*(q_u2-1)

print('n_u2 - ',n_u2)
print('\n')

print('phi_u2 - ',phi_u2)
print('\n')

e_u2 = generate_e(phi_u2)
print('e_u2 - ',e_u2)
print('\n')


d_u2 = gmpy2.invert(e_u2,phi_u2)
print('d_u2 - ',d_u2)
print('\n')



enc_e_u2 = encrypt_by_ca(e_u2,d_ca,n_ca)
print('enc_e_u2 - ',enc_e_u2)
print('\n')

enc_n_u2 = encrypt_by_ca(n_u2,d_ca,n_ca)
print('enc_n_u2 - ',enc_n_u2)
print('\n')


# writing private key of user2 in user2 private key directory
u2_privkey_dir=open("u2_privkey_dir.txt","w")
u2_privkey_dir.write(str(d_u2)+" "+str(n_u2))
u2_privkey_dir.close()


# writing public key( encrypted by private key of ca) of user1 and user2 in user public key directory
user_pubkey_dir=open("user_pubkey_dir.txt","w")
user_pubkey_dir.write("User1 : "+str(enc_e_u1)+" "+str(enc_n_u1)+"\n")
user_pubkey_dir.write("User2 : "+str(enc_e_u2)+" "+str(enc_n_u2))
user_pubkey_dir.close()










