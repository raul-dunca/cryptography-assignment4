import math
import random


def euclidian(a,b):         #returns gcd(a,b)
    while b:                # loop until b is 0
        rest= a%b
        a=b
        b=rest
    return a


def is_prime(n):        #return True if n is prime, False otherwise
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n))+1):
        if n % i == 0:
            return False
    return True

def generate_e(euler):         #generetes a random e where 1<e<euler(n) with gcd(e,euler(n))=1
    e = random.randint(1, euler)
    while euclidian(e,euler)!=1:
        e = random.randint(1, euler)

    return e

def generate_prime(start, end):     #generates 2 prime different number between an interval
    prime1 = random.randint(start, end)
    prime2= random.randint(start, end)
    while not is_prime(prime1):
        prime1 = random.randint(start, end)
    while not is_prime(prime2) or prime1==prime2:
        prime2 = random.randint(start, end)

    return prime1, prime2

def euler_fun(p,q):             #calcualte euler(n)
    return (p-1)*(q-1)


def binary(x):
    # turns a number in a kind of binary representation as a list: 21 -> [1,-1,4,-1,16]

    power=[]
    cnt=0
    while x>0:
        if x%2==1:
            power.append(2**cnt)
        else:
            power.append(-1)
        x=x//2
        cnt+=1
    return power

def extended_euclidian_algorithm(a,b):
    if euclidian(a,b)==1:
        u2=1
        u1=0
        v2=0
        v1=1
        while b>0:
            q=a//b
            r=a-q*b
            u=u2-q*u1
            v=v2-q*v1
            a=b
            b=r
            u2=u1
            u1=u
            v2=v1
            v1=v
        d=a
        u=u2
        v=v2

        return d, u, v


def repeated_squaring(b,n,k):               #calculates (b^k)%n using repeated squaring
    a=1
    if k == 0:
        return a
    c=b
    power=binary(k)
    if power[0]==1:                             # if k odd
        a=b                                     #special case: add b^1 to rezult
    for i in range(1, len(power)):
        c =(c**2)%n                             #we calculate b^(2^x)%n
        if power[i]!=-1:                        #if the power of 2 is in k's binary repr save it
            a = (c*a)% n
    return a

def text_to_nr(text):                       #transform text to nr
    val=0
    p=1
    for i in range(len(text)-1,-1,-1):
        val+=alphabet.index(text[i])*p
        p=p*len(alphabet)
    return val

def nr_to_text(nr,l):                       #transform nr to text
    text=""
    for power in range(l - 1, -1, -1):
        coeff = nr // (len(alphabet) ** power)
        text+=alphabet[coeff]
        nr =nr % len(alphabet) ** power
    return text


def find_power_range(n):                          #find k and l where: 27^k<n<27^l
    lower_bound = math.floor(math.log(n, len(alphabet)))
    upper_bound = math.ceil(math.log(n, len(alphabet)))
    return lower_bound,upper_bound

def encrypt(message, public_key):
    n=public_key[0]
    e=public_key[1]
    k,l=find_power_range(n)

    extra_spaces= (k - (len(message) % k)) % k
    if extra_spaces!=0:
        while extra_spaces:
            message+= "_"
            extra_spaces-=1
    ciphertext=""
    for i in range(0, len(message), k):
        val_message=text_to_nr(message[i:i + k])
        rez=repeated_squaring(val_message,n,e)
        encrypted_text=nr_to_text(rez,l)
        ciphertext+=encrypted_text

    return ciphertext, message

def decrypt(ciphertext, public_key, private_key):
    n = public_key[0]
    d = private_key
    k, l = find_power_range(n)
    plaintext = ""

    for i in range(0,len(ciphertext),l):
        val_ciphertext=text_to_nr(ciphertext[i:i+l])
        rez=repeated_squaring(val_ciphertext, n, d)
        decrypted_text = nr_to_text(rez, k)
        plaintext+=decrypted_text

    return plaintext

def generate_keys():
    p, q = generate_prime(start, end)
    n = p * q
    euler = euler_fun(p, q)
    e = generate_e(euler)
    d = extended_euclidian_algorithm(euler, e)[2]

    # so its positive
    while d < 0:
        d += euler

    public_key = [n, e]
    private_key = d
    return public_key, private_key

def validate_plaintext(plaintext):
    if not all(char in alphabet for char in plaintext):
        raise ValueError("Invalid characters in plaintext. Only characters in the alphabet are allowed.")

alphabet = ['_','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

try:
    text=input("What do you want to encrypt: ")
    validate_plaintext(text)

    start=int(input("Enter the start of interval: "))

    end=int(input("Enter the end of interval: "))

    public_key, private_key = generate_keys()
    print("Public key is: "+str(public_key))
    print("Private key is: "+str(private_key))

    encrypted_message,message_with_spaces = encrypt(text, public_key)
    print("Encrypted message is: "+encrypted_message)
    decrypted_message = decrypt(encrypted_message, public_key, private_key)
    print("Decrypted message is: "+decrypted_message)

    assert message_with_spaces==decrypted_message
except Exception as e:
    print(e)


