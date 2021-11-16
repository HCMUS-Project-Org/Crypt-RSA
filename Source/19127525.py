from random import randint
from os import system
from os import path

def input_directory(use = 'take info'):
    while True:
        directory = input('Input DIRECTORY: ')

        # create directory
        if not path.isdir(directory):
            if use == 'gen key':
                command = 'mkdir '+ directory 
                system(command)
                break
            else:
                print('error: file not found\n')
        else:
            break
            
    return directory


def take_message(type):
    while True:
        while True: 
            try:
                file_name = input('Input {} file (.txt): '. format(type))
                
                if file_name.split('.')[1] == 'txt':
                    break 
                else:
                    print('error: file not found')            
            except:
                print("error: invalid input (must contain '.txt')")

        if path.isfile(file_name):
            with open(file_name, 'r', encoding='utf-8') as file:
                message = file.readlines()
                for i in range(len(message)):
                    message[i] = message[i].rstrip('\n')
                return message
        else: 
            print('error: file not found')    


def take_key(directory, type):   
    while True:
        if type == "PUBLIC KEY":
            file_name = 'rsa_pub.txt' 
        else:
            file_name = 'rsa.txt' 

        if path.isfile(directory + '/' + file_name):
            with open(directory + '/' + file_name, 'r', encoding='utf-8') as file:
                tupple_key = file.readline().split()
                n = int(tupple_key[0])
                ed_key = int(tupple_key[1])
                return n, ed_key
        else:
            print('error: file not found\n')


def extEuclidean(x,y):
    mn = min(x,y)
    mx = max(x,y)

    if mn == 0: 
        return mx,1,0

    a1, a2 = 1, 0
    b1, b2 = 0, 1
    
    while (mn > 0):
        quotient = mx // mn
        remainder = mx % mn

        a = a2 - quotient*a1
        b = b2 - quotient*b1

        mx = mn
        mn = remainder
        a2, a1 = a1, a
        b2, b1 = b1, b

    return mx, a2, b2


def is_prime(n):
    if n == 2:
        return True

    if n < 2 or n % 2 == 0:
        return False

    for i in range(3, int(n**(1/2)) + 1, 2):
        if n % i == 0:
            return False

    return True


def generate_prime(exp_min, exp_max): #little Fermat
    n = randint(exp_min, exp_max)

    prime = 2**n + 1 

    while not is_prime(prime):
        prime += 2

    return prime


def MulMod(x, y, mod): 
    return ((x % mod) * (y % mod)) % mod


def PowerMod(x, y, mod):
    # Input: x, y, MOD
    # Output: x^y mod MOD
    
    p = 1
    yb = bin(y).replace("0b", "") # convert decimal to binary       

    for i in range(len(yb)):
        p = p**2 % mod
        if int(yb[i]) == 1:
            p = (x * p) % mod

    return p


def co_prime(a):
    b = 3
    
    while True:
        gcd,x,y = extEuclidean(a, b)
    
        if gcd == 1:
            return b

        b += 1


def generate_key(directory): # generate public/ secrect key
    # pk: n, e
    # n = p*q (p, q is large prime)
    # 1 < e < pi(n) [pi(n) is co-prime with e] - pi(n) = (p-1)(q-1)
    # --------------------------
    # sk: n, d 
    # 0 < d < n [(d*e) mod pi(n) = 1]

    # generate p, q 
    exp_min = 20
    exp_max = 25

    q = generate_prime(exp_min, exp_max)
    
    while True:
        p = generate_prime(exp_min, exp_max)
        if p != q:
            break

	# calulate n, piN, e
    n = p*q
    piN = (p-1)*(q-1)
    e = co_prime(piN)
    
    k = 1
    while True:
        d = (k * piN + 1) // e

        if MulMod(d, e, piN) == 1:
            break
        k += 1

    # save public key in "rsa_pub.txt"
    with open(directory + '/rsa_pub.txt', 'w', encoding='utf-8') as file:
        file.write('{} {}'. format(n, e))

    # save secrect key in "rsa.txt"  
    with open(directory + '/rsa.txt', 'w', encoding='utf-8') as file:
        file.write('{} {}'. format(n, d))


def encryption(plaintext, n, e):
    # convert plaintext into ascii
    ascii_text = []    
    for message_text in plaintext:
        for i in message_text:
            ascii_num = str(ord(i))
            ascii_num = '0' * (3 - len(ascii_num)) + ascii_num
            ascii_text.append(ascii_num)

        ascii_text.append('010') # enter / newline

    # split message into smaller msg
    ciphertext = []
    message = []
    i = 0
    while i < len(ascii_text): 
        msg = ascii_text[i]
        while int(msg) < n:
            i += 1
            try:
                msg += ascii_text[i]
            except:
                break

        if int(msg) > n:
            msg = msg[:-3]

        message.append(int(msg))

    # --------- encrypt ---------
    # c = m^e mod n
    for msg in message:
        c = PowerMod(msg,e,n)
        ciphertext.append(str(c) + '\n')

    # write encrypt message into file 
    with open('encrypted.txt', 'w', encoding='utf-8') as encrypt_file:
        encrypt_file.writelines(ciphertext)


def decryption(ciphertext, n, d):
    #----- decrypt -----
    message = []
    for cipher_part in ciphertext:
        c = int(cipher_part)
        # m = c^d mod n
        m = str(PowerMod(c,d,n))
        message.append(m)

    plaintext = ''

    for msg in message:
        # standardized msg with len % 3 == 0
        add_zero = (3 - len(msg) % 3) % 3
        msg = '0'*add_zero + msg
        start = 0
        end = 2
        
        # decode ascii to utf-8 char
        while end < len(msg):
            c = chr(int(msg[start:end + 1]))
            plaintext += c
            
            start += 3
            end += 3
    
    # write decrypt message into file 
    with open('decrypted.txt', 'w', encoding='utf-8') as decrypt_file:
        decrypt_file.write(plaintext)


def menu(os):
    if os == 'window':
        system('cls')
    else:
        system('clear')

    print('===================================')
    print('==   INTRODUCE TO CRYPTOGRAPHY   ==')
    print('==         Class: 19MMT          ==')
    print('==                               ==')
    print('== Name: Nguyen Thanh Quan       ==')
    print('== Student ID: 19127525          ==')
    print('===================================')
    print('\nWeek 04 exercise -- Main Menu\n')
    print('[1] Generate RSA key')
    print('[2] Encrypt plaintext')
    print('[3] Dencrypt ciphertext')
    print('[4] Exit\n')

    while True:
        try: 
            choice = int(input('Choice: '))
        except:
            choice = 5
            print('error: invalid input\n')
        if choice >= 1 and choice <= 4:
            return choice
    

if __name__ == '__main__':
    # get os windown or linux
    error = system('clear')
    if error == 1: 
        os = 'window'
    else:
        os = 'linux'

    while True:
        choice = menu(os)
        print('-----------------------------------')
        # 1: Generate key
        if choice == 1: 
            directory = input_directory('gen key')
            generate_key(directory)
            print('\n > Generate key done!! <')
            a = input("Press any key to continue")

        # 2: Encrypt plaintext
        elif choice == 2:
            plaintext = take_message('PLAIN TEXT')
            key_directory = input_directory()
            n, e = take_key(key_directory, 'PUBLIC KEY')
            encryption(plaintext, n, e)
            print('\n   > Encrypt done!! <')
            a = input("Press any key to continue")

        # 3: Decrypt ciphertext
        elif choice == 3:
            ciphertext = take_message('CIPHER TEXT')
            key_directory = input_directory()
            n, d = take_key(key_directory, 'SECRECT KEY')
            decryption(ciphertext, n, d)

            print('\n    > Decrypt done!! <')
            a = input("Press any key to continue")
        
        # 4: Exit
        else:
            break