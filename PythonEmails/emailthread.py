# -*- coding: utf-8 -*-
"""
Created on Sun Oct 19 18:00:10 2014

@author: Michael
"""

class EmailThread(object):
    
    def __init__(self,timestamp,sender,senderemail,receiver,receiveremail,content):
       self.timestamp=timestamp
       self.sender=sender
       self.senderemail=senderemail
       self.receiver=receiver
       self.receiveremail=receiveremail
       self.content=content