from collections import deque
from time import time as t
class SDES:
    r=deque([])
    l=deque([])
    rp=deque([])
    lp=deque([])
    s0=[['01','00','11','10'],['11','10','01','00'],['00','10','01','11'],['11','01','11','10']]
    s1=[['00','01','10','11'],['10','00','01','11'],['11','00','01','00'],['10','01','00','11']]
    k1=""
    k2=""


##########################################

    def __to_bin(self, n):
        self.n=n
        bi=["0","0","0","0","0","0","0","0","0","0"]
        for i in range(9,-1,-1):
            if self.n>=(2**i):
                self.n= self.n % (2**i)
                bi[i]="1"
            else:
                bi[i]="0"
        result=""
        bi=reversed(bi)
        for k in bi:
            result+=k
        return result

##################################

    def __p10(self, k):
        self.k=k
        lk=list(k)
        results=""
        result=[]
        result.append(lk[2])
        result.append(lk[4])
        result.append(lk[1])
        result.append(lk[6])
        result.append(lk[3])
        result.append(lk[9])
        result.append(lk[0])
        result.append(lk[8])
        result.append(lk[7])
        result.append(lk[5])
        for i in result:
            results+=i
        return results

######################################

    def __p8(self, k):
        self.k=k
        lk=list(k)
        results=""
        result=[]
        result.append(lk[5])
        result.append(lk[2])
        result.append(lk[6])
        result.append(lk[3])
        result.append(lk[7])
        result.append(lk[4])
        result.append(lk[9])
        result.append(lk[8])
        for i in result:
            results+=i
        return results
########################################

    def __p4(self, k):
        self.k=k
        lk=list(k)
        results=""
        result=[]
        result.append(lk[1])
        result.append(lk[3])
        result.append(lk[2])
        result.append(lk[0])
        for i in result:
            results+=i
        return results

########################################
    def __split_keys(self, k):
        self.k=k
        #global l
        l=deque([])
        #global r
        r=deque([])
        for i in range(len(self.k)):
            if i<len(self.k)/2:
                l.append(self.k[i])
            else:
                r.append(self.k[i])
        self.l=l
        self.r=r
########################################
    def __split_ptext(self, k):
        self.k=k
        #global lp
        self.lp=deque([])
        #global rp
        self.rp=deque([])
        for i in range(len(k)):
            if i<len(k)/2:
                self.lp.append(k[i])
            else:
                self.rp.append(k[i])
########################################
#########################################
    def __sw(self, l,r):
        result=""
        for i in l:
            result+=i
        for j in r:
            result+=j
        return result
########################################
    def __lshift(self, k, j):
        k.rotate(-j)
        return k
########################################
    def __keys(self, key):
        k1=""
        k2=""
        key=self.__p10(key)
        self.__split_keys(key)
        left=self.__lshift(self.l,1)
        right=self.__lshift(self.r,1)
        k1=left+right
        self.k1=self.__p8(k1)
        left=self.__lshift(left,2)
        right=self.__lshift(right,2)
        k2=left+right
        self.k2=self.__p8(k2)
#######################################
    def __ip(self, k):
        lk=list(k)
        results=""
        result=[]
        result.append(lk[1])
        result.append(lk[5])
        result.append(lk[2])
        result.append(lk[0])
        result.append(lk[3])
        result.append(lk[7])
        result.append(lk[4])
        result.append(lk[6])
        for i in result:
            results+=i
        return results
#######################################
    def __IP_minus_one(self, k):
        lk=list(k)
        results=""
        result=[]
        result.append(lk[3])
        result.append(lk[0])
        result.append(lk[2])
        result.append(lk[4])
        result.append(lk[6])
        result.append(lk[1])
        result.append(lk[7])
        result.append(lk[5])
        for i in result:
            results+=i
        return results
#######################################
    def __ep(self, k):
        lk=list(k)
        results=""
        result=[]
        result.append(lk[3])
        result.append(lk[0])
        result.append(lk[1])
        result.append(lk[2])
        result.append(lk[1])
        result.append(lk[2])
        result.append(lk[3])
        result.append(lk[0])
        for i in result:
            results+=i
        return results
#######################################
    def __str_xor(self, a,b):
        result=""
        for i in range(len(a)):
            if a[i]=="0":
                if b[i]=="0":
                    result+="0"
                else:
                    result+="1"
            elif a[i]=="1":
                if b[i]=="0":
                    result+="1"
                else:
                    result+="0"
        return result
#######################################
    def __s0_cal(self, a):
        global s0
        result=""
        t=self.__bin_to_int(a[0]+a[3])
        g= self.__bin_to_int(a[1]+a[2])
        #print(t,g)
        result=self.s0[t][g]
        return result
########################################
    def __s1_cal(self, a):
        global s0
        result=""
        t=self.__bin_to_int(a[0]+a[3])
        g= self.__bin_to_int(a[1]+a[2])
        #print(t,g)
        result=self.s1[t][g]
        return result
#######################################
    def __bin_to_int(sef, k):
        result=0
        g=0
        for i in range(len(k)-1,-1,-1):
            a=((len(k)-1)-i)
            g=2**(int(i))*int(k[a])
            result+=g
        return result
#######################################
    def sdes_decoder(self, p_text, key):
        self.__keys(key)
        p_text=self.__ip(p_text)
        self.__split_ptext(p_text)
        r1=self.__ep(self.rp)
        r2= self.__str_xor(r1,self.k2)
        r2_1=self.__s0_cal(r2[:int(len(r2)/2)])
        r2_2=self.__s1_cal(r2[int(len(r2)/2):])
        r3=self.__p4(r2_1+r2_2)
        r4=self.__str_xor(r3,self.lp)
        r5=self.__sw(r4,self.rp)  ##### The output of SW in a whole string
        r6=self.__ep(r5[:int(len(r5)/2)])
        r7=self.__str_xor(r6,self.k1)
        r8_1=self.__s0_cal(r7[:int(len(r7)/2)])
        r8_2=self.__s1_cal(r7[int(len(r7)/2):])
        r9=self.__p4(r8_1+r8_2)
        r10=self.__str_xor(r9,r5[int(len(r5)/2):])
        result=self.__IP_minus_one(r10+r4)
        return result
#######################################
    def sdes_encoder(self, p_text, key):
        self.__keys(key)
        p_text=self.__ip(p_text)
        self.__split_ptext(p_text)
        r1=self.__ep(self.rp)
        r2= self.__str_xor(r1,self.k1)
        r2_1=self.__s0_cal(r2[:int(len(r2)/2)])
        r2_2=self.__s1_cal(r2[int(len(r2)/2):])
        r3=self.__p4(r2_1+r2_2)
        r4=self.__str_xor(r3,self.lp)
        r5=self.__sw(r4,self.rp)  ##### The output of SW in a whole string
        r6=self.__ep(r5[:int(len(r5)/2)])
        r7=self.__str_xor(r6,self.k2)
        r8_1=self.__s0_cal(r7[:int(len(r7)/2)])
        r8_2=self.__s1_cal(r7[int(len(r7)/2):])
        r9=self.__p4(r8_1+r8_2)
        r10=self.__str_xor(r9,r5[int(len(r5)/2):])
        result=self.__IP_minus_one(r10+r4)
        return result
###################################################
    """ def three_sdes_decoder(self, data, key1, key2):
        r1=self.__sdes_decoder(data, key1)
        r2=self.__sdes_encoder(r1, key2)
        r3=self.__sdes_decoder(r2, key1)
        r4=self.__bin_to_int(r3)
        return r3#chr(r4)
##################################################
    def three_sdes_encoder(self, data, key1, key2):
        r1=self.__sdes_encoder(data, key1)
        r2=self.__sdes_decoder(r1, key2)
        r3=self.__sdes_encoder(r2, key1)
        return r3 """

#######################################################
################# END OF CLASS ########################
#######################################################

