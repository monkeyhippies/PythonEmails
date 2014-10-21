# -*- coding: utf-8 -*-
"""
Created on Sat Oct 18 22:59:44 2014

@author: Michael
"""
from selenium import webdriver
from bs4 import BeautifulSoup
import re
from emails import *


def main():
    """
    """
    driver=setupdriver()
    
    #go to www.google.com    
    driver.get('http://www.google.com')
    
    #go to gmail page
    soup=parsehtml(driver)
    driver.get(htmllinks(soup,'mail')[0]['href'])
    
    #go to sign in page
    soup=parsehtml(driver)
    driver.get(htmllinks(soup,'Sign in')[0]['href'])
    
    #login to gmail
    driver=gmaillogin(driver)
    
    #Extract emails
    emaillist=[]
    n_pages=2
    
    for page_n in range(n_pages):   
        emailspage=driver.current_url
        
        flag=False
        for counter in range(100):        
            try:
                [emailsonpage,n_emails]=allemails(driver)
                flag=True
            except:
                print counter, 'emailsonpage: StaleWebElement'
            
            if flag:
                break
        
        n_emails=10
        for email_n in range(n_emails):
            
            #Go to and expand threads
            
            try:
                emailsonpage[email_n].click()
            except:
                flag=False
                for counter in range(100):
                    try:
                       emailsonpage=allemails(driver)[0] 
                       emailsonpage[email_n].click()
                       flag=True
                    except:
                        print counter, 'email_n: StaleWebElement'
                    
                    if flag:
                        break
                        
            [driver,flag]=expandthread(driver)
            
            #Extract threads
            flag=False
            for counter in range(100):
                try:
                    subject=getthreadsubject(driver)
                    timestamps=getthreadtimestamps(driver)
                    [sendernames,senderemails,receivernames,receiveremails]=getthreadcontactinfo(driver)
                    content=getthreadcontent(driver)
                    flag=True
                except:
                    print counter, 'extract threads: StaleWebElement'
                
                if flag:
                    break
                
            #Add new email
            email=Email()
            email.addthreads(subject,timestamps,sendernames,senderemails,receivernames,receiveremails,content)
            emaillist.append(email)
            
            #Go back to emails page
            driver.get(emailspage) 
        
        #Go to next emails page
        driver=nextemailspage(driver)   
    
    printemails(emaillist)
    return emaillist
            
    
    
def setupdriver():
    """
    Description:    
        Sets up Firefox browser
    
    Usage:
        driver=setupdriver()
    
    Inputs:
        none
        
    Outputs:
        Selenium driver

    """

    driver = webdriver.Firefox()
    driver.implicitly_wait(10)
    
    return driver
    
def parsehtml(driver):
    """
    Description:    
        Parses current url's html
    
    Usage:
        driver=setupdriver()
        driver.get("http://www.google.com")
        soup=parsehtml(driver)
        
    Inputs:
        Selenium driver

    Output:
        BeautifulSoup parsed html
        
    """
    
    html_source=driver.page_source
    soup=BeautifulSoup(html_source)
    
    return soup

def htmlobjects(soup,tag,string=''):
    """
    Description:
        Makes list of html tags on webpage that contains (optional) string text
        Prints text values of links
        
    Usage:
        
    Inputs:
        BeautifulSoup parsed html
    
    Output:
        list of html links w/ given string
    
    """
    if string=='':
        linkslist=soup.find_all(tag)
    else:
        linkslist=soup.find_all(tag,text=re.compile(string))
    
    printtext(linkslist)

    return linkslist
    
def htmllinks(soup,string=''):
    """
    Description:
        Makes list of html links on webpage that contains (optional) string text
        Prints text values of links
        
    Usage:
        
    Inputs:
        BeautifulSoup parsed html
    
    Output:
        list of html links w/ given string
    
    """
    
    linkslist=htmlobjects(soup,'a',string)
    
    return linkslist
    
def htmlinput(soup, string=''):
    """
    Description:
        Makes list of html inputs on webpage that contains (optional) string text
        Prints text values of inputs
        
    Usage:
        
    Inputs:
        BeautifulSoup parsed html
    
    Output:
        list of html links w/ given string
    
    """   
    inputslist=htmlobjects(soup,'input',string)
    
    return inputslist
    
def printtext(webelements):
   """
    Description:
        Prints list of html/javscript elements' text
        
    Usage:
    
    Inputs: 
        webelements list
    
    Output:
        NA
    
    """    
   for index, text in enumerate(webelements):
        print index+1,text.text

def gmaillogin(driver):
    """
    Description:
        Selenium driver (at gmail login page)
        
    Usage:
    
    Inputs:
        Selenium driver
    Output:
        Selenium drier
    
    """
    currenturl=driver.current_url
    
    while True:
        email=driver.find_element_by_name('Email')
        password=driver.find_element_by_name('Passwd')
        email.send_keys(raw_input('EMAIL :'))
        password.send_keys(raw_input('PASSWORD :'))
        submit=driver.find_element_by_name('signIn')
        submit.click()
    
        #check login success
        if currenturl!=driver.current_url:
            break
        else:
            print 'LOGIN FAILED. TRY AGAIN'
    
    return driver
    
def allemails(driver):
    """
    Description:
        Gets webelements of all emails on page
        
    Usage:
    
    Inputs:
        Selenium driver
        
    Output:
        list of all email webelements
    
    """    
    emailsonpage=driver.find_elements_by_xpath(("//table[@cellpadding='0']/tbody/tr[@tabindex='-1']"))
    n_emails=len(emailsonpage)
    return (emailsonpage,n_emails)

def expandthread(driver):
    """
    Description:
        expands all threads if necessary
        returns true/false
        
    Usage:
    
    Inputs:
        Selenium driver
    
    Output:
        Selenium driver, expand-option flag
    
    """
    try:
        expandelement=driver.find_element_by_xpath("//div[@aria-label='Expand all']")
        flag=expandelement.is_displayed()
    except Exception:
        flag=False
        
    if flag:
        expandelement.click()
        
    return (driver,flag)
    
def getthreadsubject(driver):
    """
    Description:
        With driver at expanded threads url, gets thread subject
        
    Usage:
    
    Inputs:
        Selenium driver
    
    Output: string: subject of thread
        
    
    """
    soup=parsehtml(driver)
    subject=soup.title.text
    
    return subject
    
def getthreadtimestamps(driver):
    """
    Description:
        With driver at expanded threads url, gets thread timestamps
        
    Usage:
    
    Inputs:
        Selenium driver
    
    Output: string: subject of thread
        
    """    
    timestampelements=driver.find_elements_by_xpath("//div/span[@alt and @title]")
    filteredtimestampelements=filterdisplayed(timestampelements)
    timestamps=map(lambda x: x.get_attribute('title'),filteredtimestampelements)
    
    return timestamps
    
def getthreadcontactinfo(driver):
    """
    Description:
        With driver at expanded threads url, gets email addresses and names of exchange
        
    Usage:
    
    Inputs:
        Selenium driver
    
    Output: 
        string: subject of thread
        
    """ 
    contactinfo=driver.find_elements_by_xpath("//table//span[@name and @email and text()]")
    filteredcontactinfo=filterdisplayed(contactinfo)
    
    ##Get contact email addresses
    emails=map(lambda x: x.get_attribute('email'),filteredcontactinfo)
    [senderemails,receiveremails]=splitsendersreceivers(emails)
    
    ##Get contact names
    names=map(lambda x: x.text, filteredcontactinfo)
    [sendernames,receivernames]=splitsendersreceivers(names)
    
    return(sendernames,senderemails,receivernames,receiveremails)
    
def getthreadcontent(driver):
    """
    Description:
        With driver at expanded threads url, gets email addresses and names of exchange
        
    Usage:
    
    Inputs:
        Selenium driver
    
    Output: 
        list of strings: content
        
    """
    contentelements=driver.find_elements_by_xpath("//div[@style=not('display:none')]/div[@style='overflow: hidden;']")
    content=map(lambda x: x.text, contentelements)
    
    return content

def filterdisplayed(webelementlist):
    """
    Description:
        Takes displayed webelements from webelementlist
        
    Usage:
    
    Inputs:
        List of webelements
    
    Output:
        List of webelements        
    
    """ 
    webelementlist=filter(lambda x: x.is_displayed(),webelementlist)
    
    return webelementlist
    
def splitsendersreceivers(contactslist):
    """
    Description:
        Takes takes contact info lists and splits into sender and receiver
        
    Usage:
    
    Inputs:
        list of webelements
    
    Output:
        (senderlist,receiverlist)
        list of webelements: senderlist
        list of webelements: receiverlist       
    
    """ 
    senderlist=contactslist[0:len(contactslist):2]
    receiverlist=contactslist[1:len(contactslist):2]
    
    return (senderlist,receiverlist)
    
def nextemailspage(driver):
    """
    Description:
        Goes to next page of emails
        
    Usage:
    
    Inputs:
        Selenium driver
    
    Output:
        Selenium driver       
    
    """
    for counter in range(100):
        try:        
            driver.find_element_by_xpath("//div[@aria-label='Older' and @role='button']").click()
            return driver
        except:
            print counter+1, 'nextemailspage: StaleWebElement'

def stalelementretry(function,argument):
    """
    Description:
        Retries function if StaleWebElementError occurs
        
    Usage:
    
    Inputs:
        function and 1 argument
    
    Output:
        1 function output       
    
    """    
    flag=False
    for counter in range(100):        
        try:
            output=function(argument)
            flag=True
        except:
            print counter, 'StaleWebElement'
        
        if flag:
            break
    return output

def printemails(emaillist):
    """
    Description:
        prints emails in emaillist
        
    Usage:
    
    Inputs:
        list of emails: emailslist
    
    Output:
        NA    
    
    """  
    for email in emaillist:
        print 'SUBJECT:',email.subject,'\n\n'
        for thread in email.threads:
            printthread(thread)
        print '\n\n\n'
            
def printthread(thread):
    """
    Description:
        prints email thread
        
    Usage:
    
    Inputs:
        thread
    
    Output:
        NA  
    
    """
    print 'TIMESTAMP:',thread.timestamp,'\n'
    print 'SENDER:',thread.sender,'\n'
    print 'SENDER EMAIL:',thread.senderemail,'\n'
    print 'RECIPIENT:',thread.receiver,'\n'
    print 'RECIPIENT EMAIL:',thread.receiveremail,'\n'
    print 'CONTENT:',thread.content,'\n'
        
    
