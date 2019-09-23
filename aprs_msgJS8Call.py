from tkinter import * 
 
from tkinter.ttk import *

from tkinter.scrolledtext import ScrolledText
from subprocess import call
import os
    
TYPE_TX_SEND='TX.SEND_MESSAGE'
TYPE_TX_SETMESSAGE='TX.SET_TEXT'


     
class UserInterface:
    mycall="M0IAX"
    first=True
    addr = ('127.0.0.1',65500)
    getResponse=False
    laststatusString=""
    seq=1
    def sendMessageToJS8Call(self, messageType, messageString):
        
        print(messageType+" "+messageString)
        
        cmdstring = "echo '{\"params\": {}, \"type\": \""+messageType+"\", \"value\":\""+messageString+"\"'} | nc -l -u -w 10 2237"
        print(cmdstring)
        os.system(cmdstring)
        
    def createMessageString(self):
        messageString=""
        mode=""
        if self.combo.get()=="Email":
            mode="EMAIL-2"
        elif self.combo.get()=="SMS":
            mode = "SMSGTE"
        elif self.combo.get()=="APRS":
            mode=self.combo.get()
           
        mode = mode.ljust(9)
        if self.tocall.get()=="":
            return "Error, no email address is set"
        
        text=self.st.get('1.0', 'end-1c')  # Get all text in widget.
    
        if text=="":
            return "message is empty, please enter a message to send"
        
        message = "@ALLCALL APRS::"+mode+":"+self.tocall.get()+" "+text+" {"+str(self.seq)+"}"
        
        self.seq=self.seq+1
        
        messageString = message #mode+" "+self.tocall.get()+" "+text
        return messageString
    
    def setMessage(self):
        messageType=TYPE_TX_SETMESSAGE
        
        messageString=self.createMessageString()
        
        self.sendMessageToJS8Call(messageType, messageString)
        
    def txMessage(self):
        
        messageType=TYPE_TX_SEND
        messageString=self.createMessageString()
        
        self.sendMessageToJS8Call(messageType, messageString)
        
    def __init__(self):
        
        self.window = Tk()
 
        self.window.title("APRS Messaging for JS8Call")
 
        self.window.geometry('350x200+300+300')
 
        self.combo = Combobox(self.window)
 
        self.combo['values']= ("Email", "SMS")
 
        self.combo.current(0) #set the selected item
 
        self.combo.grid(column=0, row=0,columnspan=2)
 
        self.lbl1 = Label(self.window, text="JS8Call Mode", justify="left")
 
        self.lbl1.grid(column=0, row=1,columnspan=2)
 
        self.combo2 = Combobox(self.window)
 
        self.combo2['values']= ("Normal", "xxx", "yyy")
 
        self.combo2.current(0) #set the selected item
 
        self.combo2.grid(column=0, row=2,columnspan=2)
 
 
        self.lbl = Label(self.window, text="Enter Email Address", justify="left")
 
        self.lbl.grid(column=0, row=3,columnspan=2)
 
        self.tocall = Entry(self.window,width=30)
 
        self.tocall.grid(column=0, row=4, columnspan=2)

        self.msgLabel = Label(self.window, text="Message Text", justify="left")
 
        self.msgLabel.grid(column=0, row=5,columnspan=2)
 
        self.st = ScrolledText(self.window, height=5, width=40)
        self.st.grid(row=6, column=0,columnspan=2)

        self.btn = Button(self.window, text="Set JS8Call Text", command=self.setMessage)
 
        self.btn.grid(column=0, row=9)

        self.btn2 = Button(self.window, text="TX With JS8Call", command=self.txMessage)

        self.btn2.grid(column=1, row=9)

        self.window.geometry("350x300+300+300")
        self.window.mainloop()
    
ui = UserInterface()

