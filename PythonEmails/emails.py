# -*- coding: utf-8 -*-
"""
Created on Sun Oct 19 17:55:14 2014

@author: Michael
"""
from emailthread import *

class Email(object):
    
    def __init__(self):
       self.subject=''
       self.threads=[]
       self.n_threads=0
       
    def addthreads(self,subject,timestamps,sendernames,senderemails,receivernames,receiveremails,content):
        self.subject=subject
        n_threads=len(timestamps)
        for index in range(n_threads):
            self.threads.append(EmailThread(timestamps[index],sendernames[index],senderemails[index],receivernames[index],receiveremails[index],content[index]))
        
        self.n_threads=n_threads