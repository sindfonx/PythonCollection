from flask import Flask, request
import hashlib
import time
import threading

class User:
    def __init__(self, token):
        self.Token = token
        self.LastTime = time.time()

class Manager:
    def __init__(self):
        self.CurrentClientNumber = 0
        self.WaitUser = [] # 等待使用者
        self.OnlineUser = [] # 現在線上的使用者
        
        self.CurrentOnlineUser = 0
        self.MaximumUser = 3
        self.IdleSeconds = 20
        
    def GenerateTokenInManager(self):
        _model= hashlib.sha256()
        _key= str(self.CurrentClientNumber) + str(time.time())
        _model.update(_key.encode())
        self.CurrentClientNumber += 1
        _token=_model.hexdigest()

        self.WaitUser.append(User(_token))
        self.refreshOnlineUser()
        
        return _token
    
    def refreshOnlineUser(self):
        for i in range(len(self.WaitUser)):
            if len(self.OnlineUser) >= self.MaximumUser:
                break
            
            reverseIndex = len(self.WaitUser) - i - 1
            self.WaitUser[reverseIndex].LastTime = time.time()
            self.OnlineUser.append(self.WaitUser[reverseIndex])
            self.WaitUser.pop(reverseIndex)
    
    def CheckPlayerOnline(self):
        while True:
            time.sleep(1)
            
            currentTime = time.time()
            for i in range(len(self.OnlineUser)):
                reverseIndex = len(self.OnlineUser) - i - 1
                # 踢掉站線的人，從 self.OnlineUser 
                if currentTime - self.OnlineUser[reverseIndex].LastTime > self.IdleSeconds:
                    #踢掉 OnlineUser 
                    self.OnlineUser.pop(reverseIndex)
                        
            self.refreshOnlineUser()
            self.debug_print_user()
            
    def debug_print_user(self):
        waitUser = ''
        for i in range(len(self.WaitUser)):
            waitUser += self.WaitUser[i].Token + ', '
        
        print(f'等待使用者 : {waitUser}')
        
        onlineUser = ''
        currentTime = time.time()
        for i in range(len(self.OnlineUser)):
            seconds = self.IdleSeconds - (currentTime - self.OnlineUser[i].LastTime)
            onlineUser += f'使用者 : {self.OnlineUser[i].Token} 剩餘秒數 : {round(seconds, 2)} '
        
        print(f'上線使用者 : {onlineUser}')
        
        

server = Flask(__name__)
manager = Manager()
td = threading.Thread(target=manager.CheckPlayerOnline)
td.start()

@server.route('/GenerateToken', methods=['POST'])
def GenerateToken():
    return {'Token': manager.GenerateTokenInManager()}

@server.route('/WaitUserToken', methods=['POST'])
def GenerateToken():
    return {'Token': manager.GenerateTokenInManager()}

@server.route('/AddConversation', methods=['POST'])
def AddConversation():
    content= request.json
    token = content['Token']
    conversation = content['Content']
    manager.AddConversation(token, conversation)
    return {'Content': manager.GetConversation(), 'Result': 2}

server.run(host='127.0.0.1')