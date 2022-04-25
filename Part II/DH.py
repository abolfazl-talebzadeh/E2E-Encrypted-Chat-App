import random
import SDES as Encryptor
class DH:
    primes=[]
    z=[]
    f_k_dec=0
    f_k_bin=''
    p=ya=yb=k=a=b=q_times_p=p_q=0
    def __init__(self, n):
        self.n=n
        self.primes_gen()
        self.q_assigner()
        self.g_calculator()
        p=self.bss_random_selector()
        q=self.bss_random_selector()
        self.q_times_p=p*q
        return
    ##############################
    def primes_gen(self):
        is_prime=True
        for i in range (2,self.n):
            for j in range(2,i):
                if i % j ==0:
                    is_prime=False
                    break
                else:
                    is_prime=True
            if is_prime==True:
                self.primes.append(i)
                is_prime=False
    ####################################
    def q_assigner(self):
        pos=random.randint(0,len(self.primes)-1)
        self.p=self.primes[pos]
    #####################################
    def g_calculator(self):
        generators=[]
        for x in range(1, self.p):
            self.z.append(x)
        for g in self.primes:
            if g<self.p:
                temp=[]
                for y in range(1, self.p):
                    temp.append((g**y)%self.p)
                temp.sort()
                temp_set=set(temp)
                if temp_set==set(self.z):
                    generators.append(g)
        self.g=generators[random.randint(0,len(generators)-1)]
        return generators
    #####################################
    def secret_number_generattor(self):
        self.a=random.randint(1,self.p-1)
        self.ya=(self.g**self.a)%(self.p)
        return
    ########################################
    def k_generator(self):
        self.k=(self.yb ** self.a) % (self.p)
        return 
    ######################################
    def bss(self):
        seed=self.k
        key=[None]*10
        f_k=0
        for i in range (0,10):
            seed=(seed**2) % self.q_times_p
            key[i]=seed % 2
            f_k+=(2**(9-i))*(seed % 2)
        self.f_k_dec=f_k
        for h in key:
            self.f_k_bin+=str(h)
        return 
    ######################################
    ######################################
    def bss_random_selector(self):
        n=random.randint(1,1024)
        is_prime=False
        while not is_prime:
            for i in range(2,n):
                if n % i==0:
                    n+=1
                    is_prime=False
                    break
                elif  n % 4 !=3:
                    n+=1
                    is_prime=False
                else:
                    is_prime=True
        return n
    ######################################

""" d=DH(90)
print("P = ", d.p,"\n")
print("Cyclic group = ",d.z,"\n")
print("Generators: ",d.g_calculator(),"\n")
print("g = ",d.g, "<<g is selected randomly among other numbers>>\n")
d.secret_number_generattor()
print("Alice's private Key= ", d.a)
print("Alice's Pub Key= ", d.ya,"\n")
d.k_generator()
d.bss()
print(f"n={d.n}\np={d.p}\ng={d.g}\np_q={d.p_q}\nprimes={d.primes}\nq_times_p={d.q_times_p}\nya={d.ya}\nyb={d.yb}\nz={d.z}")
print(f"bin={d.f_k_bin}\ndec={d.f_k_dec}\ng={d.g}\np_q={d.p_q}\nprimes={d.primes}\nq_times_p={d.q_times_p}\nya={d.ya}\nyb={d.yb}\nz={d.z}") """
""" def select_file(i):
    file_path={
        1:"1.txt",
        2:"2.txt",
    }
    with open(file_path.get(i)) as file:
        data = file.read()
    return data
if __name__=="__main__":
    sdes=Encryptor.SDES()
    cipher=""
    cipher_list=[]
    plain=""
    plain_list=[]
    d=DH(90)
    print("P = ", d.p,"\n")
    print("Cyclic group = ",d.z,"\n")
    print("Generators: ",d.g_calculator(),"\n")
    print("g = ",d.g, "<<g is selected randomly among other numbers>>\n")
    d.secret_number_generattor()
    print("Alice's private Key= ", d.a)
    print("Alice's Pub Key= ", d.ya,"\n")
    print("Bob's private Key= ", d.b)
    print("Bob's Pub Key= ", d.yb,"\n")
    print(f"k(a,b)=(Alice's Pub key:{d.ya} ^ Bob's Priv key:{d.b}) mod (p:{d.p}) which equals:{d.k}\n")
    d.bss()
    print(f"Alice and Bob agreed on the values 'q' and 'p' which (n = q * p)={d.q_times_p}\n")
    print(f"final key in binary: {d.f_k_bin}")
    print(f"final key in decimal:{d.f_k_dec}")
    
    plain=select_file(1)
    print(f"This is the original plain text:")
    print(plain,"\n")
    [plain_list.append(plain[i:i+8]) for i in range (0, len(plain)-1,8)]
    for plain_word in plain_list: 
        cipher+=sdes.sdes_encoder(plain_word,d.f_k_bin)
    print(f"This is the encrypted cipher text:")
    print(cipher,"\n")
    with open("2.txt","w") as file:
        file.write(cipher)
    ##########################################################################
    cipher_list=[]
    cipher=""
    plain_list=[]
    plain=""
    cipher=select_file(2)
    [cipher_list.append(cipher[i:i+8]) for i in range (0, len(cipher)-1,8)]
    for cipher_word in cipher_list: 
        plain+=sdes.sdes_decoder(cipher_word,d.f_k_bin)
    print(f"This is the what have decoded from the cipher text using the same key:")
    print(f"plain: {plain}\n") """