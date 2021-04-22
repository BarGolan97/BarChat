import hashlib

def calcMd5(psf):
    # encoding GeeksforGeeks using encode()
    # then sending to md5()
    res = hashlib.md5(psf.encode())
    # printing the equivalent hexadecimal value.
    # this should be in client
    print("The hexadecimal equivalent of hash is : ", end="")
    hexPass = res.hexdigest()
    return hexPass
def registrer(userid,psf,email):
    encripted=calcMd5()
    # send to server RGISTER message with userid,encripted,email
def login(userid, psf):
    encripted = calcMd5()
    # send to server LOGIN with userid and encripted