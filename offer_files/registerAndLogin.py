import pickle
import os
import datetime
import time
import hashlib  # this should be done in client

import result as result

PASSWORD=0
RECOVERY_EMAIL=1
IS_LOGGED=2
LAST_LOGIN=3
USER_ALREADY_EXISTS= 11
USER_ADDED =10
LOGIN_SUCCESS=12

INCORRECT_PASSWORD=13
USER_NOT_EXIST=14
LOGOUT_SUCCESS=15
USER_ALREADY_LOGGED_OUT=16
MAX_LOGIN_COUNT=5

def calcMd5(psf):
    # encoding GeeksforGeeks using encode()
    # then sending to md5()
    res = hashlib.md5(psf.encode())
    # printing the equivalent hexadecimal value.
    # this should be in client
    print("The hexadecimal equivalent of hash is : ", end="")
    hexPass = res.hexdigest()
    return hexPass
def registrer(useriid,psf,email,registerLogin):
    encripted=calcMd5()


class registerLogin():
    def __init__(self):
        self.userFile="usersDB.pkl"
        self.users={}
        self.atemptLogin=0
        self.firstAttemptTime=0

        if os.path.exists(self.userFile):
            with open(self.userFile, 'rb') as handle:
                self.users = pickle.load(handle)

    def __delitem__(self, key):
        if key in self.users.keys():
            del self.users[key]
            return True
        return False

    def register(self,username,psf,recoveryEmail):
        if username in self.users.keys():
            return USER_ALREADY_EXISTS

        else:
           self.users[username]=[psf,recoveryEmail,False, time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())]
           with open(self.userFile, 'wb') as handle:
               pickle.dump(self.users, handle, protocol=pickle.HIGHEST_PROTOCOL)
               return USER_ADDED
    def login(self,username,psf):
        if username in self.users.keys():
            data=self.users[username]
            password=data[PASSWORD]
            if password==psf:
                new_data = [data[PASSWORD], data[RECOVERY_EMAIL], True,
                            time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())]
                self.users[username]=new_data
                with open(self.userFile, 'wb') as handle:
                    pickle.dump(self.users, handle, protocol=pickle.HIGHEST_PROTOCOL)
                return LOGIN_SUCCESS
            else:
                if self.atemptLogin==0:
                    self.firstAttemptTime= tempPsf= time.time_ns() // 1000000
                self.atemptLogin+=1
                return INCORRECT_PASSWORD
        else:
            return USER_NOT_EXIST
    def logout(self,username):
        if username in self.users.keys():
            data = self.users[username]
            if data[IS_LOGGED]==True:
                new_data= new_data=[data[PASSWORD],data[RECOVERY_EMAIL],False,time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())]
                self.users[username] = new_data
                with open(self.userFile, 'wb') as handle:
                    pickle.dump(self.users, handle, protocol=pickle.HIGHEST_PROTOCOL)
                return LOGOUT_SUCCESS
            else:
                return USER_ALREADY_LOGGED_OUT
        else:
            return USER_NOT_EXIST



    def sendRecoveryEmail(self,username):
        data = self.users[username]
        email=data[RECOVERY_EMAIL]
        tempPsf = str(time.time_ns() // 1000000)
        #to be implemented
    def printUsers(self):
        for key in self.users.keys():
            print(key,self.users[key])

if __name__=="__main__":

    u=registerLogin()
    psf = "1234"


    stat= u.register('ofer','i234','ofer12@gmail.com')
    stat= u.register('eden', '5679', 'o@gmail.com')
    u.printUsers()
    stat=u.login('ofer','i234')
    if stat==LOGIN_SUCCESS:
        print ('login sucess')
    elif stat== INCORRECT_PASSWORD:
        print ('incorrect password')
    else:
        print('user not exist')

    u.printUsers()

    u.logout('ofer')
    u.printUsers()
