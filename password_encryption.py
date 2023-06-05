# -*- coding: utf-8 -*-
"""
******** Email ID and Password Encryption  *******************************************************
                                                                                                 *
Authors: Team C8 - Aastha Shah, Shradhdha Gupte, Pratyaksh Verma, Aashish Pitchai                *
Input: Email ID  and Password from pwd.txt                                                       *                                    *   
Output: encryptedPWD.txt (Encrypted Email and Password) and refKey.txt (Reference Key)           *   
                                                                                                 *
**************************************************************************************************

"""

# Description: This program will be executed only when we have a new password file.

from cryptography.fernet import Fernet
import os


### 1. read your password file
with open('pwd.txt') as f:
    mypwd = ''.join(f.readlines())

### 2. generate key and write it in a file
key = Fernet.generate_key()
f = open("refKey.txt", "wb")
f.write(key)
f.close()

### 3. encrypt the password and write it in a file
refKey = Fernet(key)
mypwdbyt = bytes(mypwd, 'utf-8') # convert into byte
encryptedPWD = refKey.encrypt(mypwdbyt)
f = open("encryptedPWD.txt", "wb")
f.write(encryptedPWD)
f.close()

### 4. delete the password file
if os.path.exists("pwd.txt"):
  os.remove("pwd.txt")
else:
  print("File is not available")