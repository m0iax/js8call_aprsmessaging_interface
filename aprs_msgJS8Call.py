#! /usr/bin/python3
'''
Created on 23 September 2019
APRS Messageing Using JS8Call Copyright 2019 M0IAX

With thanks to Jordan, KN4CRD for JS8Call - http://js8call.com

@author: Mark Bumstead M0IAX
http://m0iax.com

this is the lite version and uses a unix command to send the message to JS8Call,
this was adapted from a script by Jason, KM4ACK.

I may consider writing a more complicated version to use more of the JS8Call API
'''

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
        
        if messageString==None:
            return
        
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
        print(mode)
        if self.tocall.get()=="":
            return "Error, no email address is set"
        
        text=self.st.get('1.0', 'end-1c')  # Get all text in widget.
    
        if text=="":
            return "Error, message is empty, please enter a message to send"
        
        number = self.seq
        number = format(number, '02d')
#        t.rjust(10, '0')
        if self.combo.get()=="Email":
            message = "@ALLCALL APRS::"+mode+":"+self.tocall.get()+" "+text+"{"+number+"}"
        elif self.combo.get()=="APRS":
            tocallsign=self.tocall.get()
            tocallsign=tocallsign.ljust(9)
            message = "@ALLCALL APRS::"+tocallsign+":"+text+"{"+number+"}"
        else:
            message = None
        
        self.seq=self.seq+1
        #APRS sequence number is 2 char, so reset if >99
        if self.seq>99:
            self.seq=1
        
        
        messageString = message #mode+" "+self.tocall.get()+" "+text
        return messageString
    
    def setMessage(self):
        messageType=TYPE_TX_SETMESSAGE
        
        messageString=self.createMessageString()
        
        if messageString.startswith("Error"):
            print(messageString)
            return
    
        self.sendMessageToJS8Call(messageType, messageString)
        
    def txMessage(self):
        
        messageType=TYPE_TX_SEND
        messageString=self.createMessageString()
        
        if messageString.startswith("Error"):
            print(messageString)
            return

        self.sendMessageToJS8Call(messageType, messageString)
    
    def comboChange(self, event):
        print(self.combo.get())
        mode = self.combo.get()
        if mode=="APRS":
            self.callLbl.config(text='Enter Callsign (including SSID)')
        elif mode=="Email":
            self.callLbl.config(text='Enter Email Address to send to')
        elif mode=="SMS":
            self.callLbl.config(text='Enter cell phone number')
            
    def __init__(self):
        
        self.window = Tk()
 
        self.window.title("APRS Messaging for JS8Call")
 
        self.window.geometry('350x200+300+300')
 
        self.combo = Combobox(self.window, state='readonly')
        
        self.combo.bind('<<ComboboxSelected>>', self.comboChange)    
    
        self.combo['values']= ("Email", "SMS", "APRS")
 
        self.combo.current(0) #set the selected item
 
        self.combo.grid(column=0, row=0,columnspan=2)
 
        self.lbl1 = Label(self.window, text="JS8Call Mode", justify="left")
 
        self.lbl1.grid(column=0, row=1,columnspan=2)
 
        self.combo2 = Combobox(self.window)
 
        self.combo2['values']= ("Normal", "xxx", "yyy")
 
        self.combo2.current(0) #set the selected item
 
        self.combo2.grid(column=0, row=2,columnspan=2)
 
 
        self.callLbl = Label(self.window, text="Enter Email Address", justify="left")
 
        self.callLbl.grid(column=0, row=3,columnspan=2)
 
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

        self.note1label = Label(self.window, text="Click Set JS8Call text to set the message text in JS8Call", justify="center", wraplength=300)
 
        self.note1label.grid(column=0, row=10,columnspan=2)
 
        self.note1label = Label(self.window, text="Click TX with JS8Call to set the message text in JS8Call and start transmitting", justify="center", wraplength=300)
 
        self.note1label.grid(column=0, row=11,columnspan=2)
 
        self.window.geometry("350x350+300+300")
        self.window.mainloop()
    
ui = UserInterface()

