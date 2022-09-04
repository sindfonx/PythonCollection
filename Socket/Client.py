from tokenize import Token
import requests
import tkinter as tk                       # 視窗圖形化標準模組
from tkinter import scrolledtext as tkSt   # 視窗圖形化標準模組 (帶有滾動條的視窗)
from tkinter import messagebox as tkMs     # 視窗圖形化標準模組 (提示對話視窗)
import threading                           # 線程
import time
from enum import Enum

class ServerState(Enum):
    ServerFull = 1
    NotHasToken = 2
    Success = 3

class selfManger:
    def __init__(self):
        self.PrevInfoIndex = 0
        self.inToken= ""
        self.Conversation = ""

def APISend(_selfStr,selfID):
    recv1 = requests.post('http://127.0.0.1:5000/selfAddProtocol',json={'selfAdd':f'{_selfStr}',
                                                                        'Token':SelfManger.inToken
                                                                        })
    decodeJsonData = recv1.json()
    getInfoMy(decodeJsonData,selfID)
    # getInfoOther()

def selfTextSend():
    _selfStr = inputText.get('1.0','end-1c')    # 獲取 input 的內容。
    inputText.delete(1.0,'end')                 # 刪除 input 的內容。
    selfID = 'A'

    if _selfStr != "" :                         # str 不是 空字串 的狀況下...建立編輯個人視窗。
        APISend(_selfStr,selfID)                           # 傳送發送訊息 至 另一端口
    else:
        tkMs.showerror('警告',"不能發送空白訊息！")

def getInfoMy(decodeJsonData,selfID):
    _ServerGiveToken = decodeJsonData['GiveToken']
    _ServerContent = decodeJsonData['Content']
    _ServerClientLimit = decodeJsonData['clientLimit']
    _serverPurview= decodeJsonData['Purview']
    _ServerFull = decodeJsonData['Full']

    _correct= tokenParse(_ServerGiveToken)

    if _correct==ServerState.Success:
        '''
        if SelfManger.PrevInfoIndex <= len(_ServerContent):
            addContent = []
            for i in range(len(_ServerContent)):
                reverseIndex = len(_ServerContent) - i - 1
                addContent.append(_ServerContent[reverseIndex])
                
                if len(_ServerContent) - i - 1 == SelfManger.PrevInfoIndex:
                    break

            SelfManger.PrevInfoIndex = len(_ServerContent)
            # addContent.reverse()
            selfContent=addContent[0]
        '''
    else:
        if _correct==ServerState.ServerFull:
            selfContent= _ServerFull
        if _correct==ServerState.NotHasToken:
            selfContent= _serverPurview

        
    
    textEdit.config(state='normal')             # 開啟聊天室編輯的功能
    
    title = f'{selfID}客戶端:'                   # 建立用戶title
    next = '\n'    
    textEdit.insert(tk.END, title,'server', next)   # 顯示title，並賦予紅色。
    textEdit.insert(tk.END, selfContent, next, next)   # 顯示輸入值，並換行。
    textEdit.see('end')                        # 設定 滾動條拉 移至最新消息。

    textEdit.config(state='disabled')           # 停止聊天室編輯的功能
    
def tokenParse(GiveToken):
    try:
        if GiveToken == None:
            return ServerState.ServerFull
        if len(SelfManger.inToken) == 0:
            SelfManger.inToken.append(GiveToken)
            return ServerState.Success
            
        if SelfManger.inToken == GiveToken:
            return ServerState.Success
        else:
            return ServerState.NotHasToken
    except:
        # if SelfManger.state == 0:
            # SelfManger.inToken.pop()
            # return False
            ...
            
        


def getInfoOther():
    recv1 = requests.get('http://127.0.0.1:5000/ContentClient2List', json={"Index": 0})
    Client1 = recv1.json()

    ii = len(Client1['Client2'])-1

    if len(Client1['Client2']) != 0 :
        textEdit.config(state='normal')             # 開啟聊天室編輯的功能

        title = '客戶端2:'                   # 建立用戶title
        next = '\n'    
        textEdit.insert(tk.END, title,'guest', next)   # 顯示title，並賦予紅色。
        textEdit.insert(tk.END, Client1['Client2'][ii], next, next)   # 顯示輸入值，並換行。
        textEdit.see('end')                        # 設定 滾動條拉 移至最新消息。

        textEdit.config(state='disabled')           # 停止聊天室編輯的功能
        

# 建立 tkinter 物件
root = tk.Tk()          
uesName = '客戶端1'
root.title(uesName)     # 建立 視窗title Name

#顯示聊天窗口
textEdit = tkSt.ScrolledText(root,width = 40 , height = 20 )  # 建立 聊天室顯示窗口
textEdit.grid (pady = 5 , padx = 5 )                          # 設定 聊天室顯示窗口內縮 (好看而已)
textEdit.tag_config('guest',foreground='blue')                # 設定 客戶端輸入顯示的顏色為藍
textEdit.tag_config('server',foreground='red')                # 設定 客戶端輸入顯示的顏色為藍
textEdit.config (state='disabled')                            # 執行 停止聊天室編輯的功能

#編輯窗口
inputText = tkSt.ScrolledText(root,width = 40 , height = 3 ) # 建立 聊天室輸入窗口
inputText.grid (pady = 5 , padx = 5 )                        # 設定 聊天室輸入窗口 (好看而已)

#發送按鈕
btnSend = tk.Button(text='發送', width = 5, height = 2, command = selfTextSend) # 建立 發送按鈕
btnSend.grid(row=2,column=0)                                                    # 設定 按鈕位置

#其他使用者
other = 0
SelfManger = selfManger()
root.mainloop()