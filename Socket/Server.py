from tokenize import Token
from flask import Flask, request
import hashlib
import threading
import time

class clientTokenState:
    def __init__(self, token):
        self.Token = token
        self.Make = 0
        self.LastLoginTime =time.time()

class CommunicationManager:
    def __init__(self):
        self.content = []
        self.ClientToken = []
        
        self.serverContentLenLimit = 0
        self.serverPurview = "使用非法令牌，請依正規程序獲取"
        self.serverFull = "閒置過久，令牌以過期。"
        
        self.serverToken= 0
        self.serverGiveToken= 0

        self.clientConnectLimit = 0
        self.clientContentLimit = 0

    def SetServerLimitCommunication(self, serverContentLenLimit):
        self.serverContentLenLimit = serverContentLenLimit

    def SetClientLimitCommunication(self, clientContentLimit):
        self.clientContentLimit = clientContentLimit

    def SetClientConnectLimit(self, clientConnectLimit):
        self.clientConnectLimit = clientConnectLimit

    def timeLimit(self):
        while True:
            time.sleep(1)
            _current= time.time()
            for _i in range(len(self.ClientToken)):
                _passTime= _current - self.ClientToken[_i].LastLoginTime
                if _passTime > 10:
                    self.ClientToken.pop(_i)
                    print('88')
    
    def AddCommunication(self, addContent, clientToken):
        _correct = self.tokenParse(clientToken) == True
        if _correct:
            self.content.append(addContent)
            return True
        return False
    
    def tokenParse(self,clientToken):
        try:
            for i in range(len(self.ClientToken)):
                if clientToken[0] == self.ClientToken[i].Token:
                    self.Generate(clientToken[0])
                    return True
                
            self.serverGiveToken= None
            return False
        except:
            self.SetToken()
            self.giveToken()
            return True

    def giveToken(self):
        for _i in range(len(self.ClientToken)):
            _revers= len(self.ClientToken)- 1- _i
            self.serverGiveToken= self.ClientToken[_revers].Token
            break    

    def SetToken(self):
            _model= hashlib.sha256()
            _key= str(self.serverToken)
            _model.update(_key.encode())
            self.serverToken+= 1
            _token=_model.hexdigest()

            self.ClientToken.append(clientTokenState(_token))

    def ParseServerCommunication(self): # 限制 server 儲存數量的方法。
        _len = len(self.content) - self.serverContentLenLimit
        if len(self.content) > self.serverContentLenLimit:
            for i in range(_len):
                self.content.pop(0) 

    def ParseClientCommunication(self): # 限制 clientGET 數量的方法。
        if len(self.ClientToken) < self.clientContentLimit:
            _start = len(self.content)-len(self.content)
            _stop = len(self.content)
            return _start,_stop

        if len(self.ClientToken) > self.clientContentLimit:
            _start = len(self.content)-self.clientContentLimit
            _stop = len(self.content)
            return _start,_stop

        if len(self.ClientToken) == self.clientContentLimit:
            _start = None
            _stop = len(self.content)
            return _start,_stop

    def GetCommunication(self):
        _Ss= self.ParseClientCommunication()
        return {'GiveToken': self.serverGiveToken,
                'Content': self.content[_Ss[0] : _Ss[1]], 
                'clientLimit': self.clientConnectLimit,
                'Full':self.serverFull,
                'Purview': self.serverPurview }
        
server = Flask(__name__)
manager = CommunicationManager()
manager.SetServerLimitCommunication(5)
manager.SetClientLimitCommunication(3)
manager.SetClientConnectLimit(3)

tkt = threading.Thread(target=manager.timeLimit, daemon=True)
tkt.start()

@server.route('/selfAddProtocol',methods=['POST'])
def selfAdd():
    selfAddContent= request.json
    if manager.AddCommunication(selfAddContent['selfAdd'],
                            selfAddContent['Token']) == True:
        manager.ParseServerCommunication()
    

    return manager.GetCommunication()



server.run(host='127.0.0.1')