#!/usr/bin/env python
# coding: utf-8

# In[1]:


consoledomain=''#@param {type:"string"}
numberdays=3#@param {type:"number"}
gmail_user = ''
gmail_password = ''
send_to_mails=''


# In[49]:


#!pip install git+https://github.com/joshcarty/google-searchconsole
import searchconsole
import urllib3
import pandas as pd
from pandas import DataFrame
import warnings


# In[48]:


http = urllib3.PoolManager()
account = searchconsole.authenticate(client_config='client_secrets.json',credentials='/Users/Michael.vandenreym/Desktop/python/credentials.json')
webproperty = account[consoledomain]
report = webproperty.query.range('today', days=-numberdays).dimension('page').get()


# In[4]:


warnings.filterwarnings("ignore")
error4 = []
badcodes=['400','401','402','403','404','500','501','502','503','504']
for i in range(0,len(report.rows)-1):
    try:
        resp = http.request('GET', report.rows[i][0])
        #zoek de statuscode
        if(str(resp.status) in badcodes):
            print(resp.status,report.rows[i][0])
            error4.append([resp.status,report.rows[i][0],report.rows[i][1],report.rows[i][2]])
    except:
        print("")


# In[44]:


body="Overview 404 errors \n\n"
for error in error4:
    body = body + "\n" +str(error[0])+"-"+str(error[1])+"" 
    body = body + "\nLast "+str(numberdays)+" days : "+str(error[2])+" clicks and "+str(error[3])+" impressions\n"


# In[45]:


body


# In[46]:


import smtplib
if(len(error4)>0):


    sent_from = gmail_user
    to = [send_to_mails]
    subject = '404 errors in Google'

    email_text = """From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

    #try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()

    print('Email sent!')
#except:
#print('Something went wrong...')


# In[ ]:




