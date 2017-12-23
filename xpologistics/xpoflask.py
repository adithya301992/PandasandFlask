# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 14:35:37 2017

@author: user
"""

#!/usr/bin/python
from flask import Flask ,render_template,request,url_for
import os

import pandas as pd
pickedpoint=""

loadboard = pd.read_excel("C:\\Users\\user\\Desktop\\loadBoard.xlsx")
Weatherandroadcondition =pd.read_excel("C:\\Users\\user\\Desktop\\dr.xlsx")
helpdesk=pd.read_excel("C:\\Users\\user\\Desktop\\helpdesk.xlsx")
users=pd.read_excel("C:\\Users\\user\\Desktop\\users.xlsx")

pickup_points_list=loadboard.PICKUP.unique()
deliver_points=loadboard.DELIVERY.unique()
MATERIALTYPE=loadboard.MATERIAL.unique()

pickup_points_quote=helpdesk.PICKUP.unique()
deliver_points_quote=helpdesk.DELIVERY.unique()


CITY_fetched=Weatherandroadcondition.PLACE.unique()

print (helpdesk)

app= Flask(__name__)
 
@app.route('/')
def inputpage():
    return render_template("input.html")

@app.route('/xpologistics', methods = ['GET','POST'] )
def xpologistics():
      return render_template("profile.html")

@app.route('/loadboard/' , methods = ['GET','POST']  )
def checking():
     return render_template('loadboard.html',pickup_point=pickup_points_list,
                            drop_point=deliver_points,MATERIALTYPE=MATERIALTYPE)

@app.route('/CarrierData' ,methods = ['GET','POST']  )
def CarrierData():
    return render_template("carrier.html")

@app.route('/quoteguide',methods = ['GET','POST']  )
def quoteguide():
    
    return render_template("quoteguide.html",pickup_point=pickup_points_quote, drop_point=deliver_points_quote)

@app.route('/quotedata', methods = ['GET','POST'])
def quotedata():
     pickedpoint = request.form.get('pickup_points')
     deliveredpoint = request.form.get('drop_point')
     
     j=helpdesk[(helpdesk['PICKUP'] == pickedpoint) & (helpdesk['DELIVERY'] == deliveredpoint) ]
     #return pickedpoint
     return render_template('displayq.html',loaddata=[j.to_html(classes='j')]) 


@app.route('/userdata', methods = ['GET','POST'] )
def userdata():
    users=pd.read_excel("C:\\Users\\user\\Desktop\\users.xlsx")
    USER=request.form.get('USER')
    f=users[users['NAME'] == USER]
    CREDITPOINTS=users.CREDITPOINTS[users['NAME'] == USER].head(1)
    DOCUMENTS=users.LISTOFDOCUMENTS[(users['EXPIRED'] == 'YES') & (users['NAME'] == USER) ].head(1)
    return render_template("userdata.html",loaddata=[f.to_html(classes='f') ], CREDIT=[CREDITPOINTS.to_string()], documents=[DOCUMENTS.to_string() ] 
                                                     )
    
@app.route('/lbdata' , methods = ['GET','POST']  )
def displayloadbaord():
     pickedpoint = request.form.get('pickup_points')
     deliveredpoint = request.form.get('drop_point')
     MATERIALTYPE = request.form.get('MATERIALTYPE')
     print (pickedpoint,deliveredpoint)
     j=loadboard[(loadboard['PICKUP'] == pickedpoint) & (loadboard['DELIVERY'] == deliveredpoint) &  (loadboard['MATERIAL'] == MATERIALTYPE)]
     #return pickedpoint
     return render_template('displayloadboard.html',loaddata=[j.to_html(classes='j')]) 


     
         
@app.route('/slbdata' , methods = ['GET','POST']  )
def displayloadbaord2():
     pickedpoint = request.form.get('pickup_points')
     MATERIALTYPE = request.form.get('MATERIALTYPE')
     j=loadboard[(loadboard['PICKUP'] == pickedpoint) &  (loadboard['MATERIAL'] == MATERIALTYPE)]
     #return pickedpoint
     return render_template('displayloadboard1.html',loaddata=[j.to_html(classes='j')])  
 
@app.route('/speech' , methods = ['GET','POST']  )
def speech():
     import speech_recognition as sr
     mic_name = "Microphone (High Definition Aud"
     sample_rate = 48000
     chunk_size = 512
     r = sr.Recognizer()
     mic_list = sr.Microphone.list_microphone_names()
 
     for i, microphone_name in enumerate(mic_list):

       with sr.Microphone(device_index = 1, sample_rate = sample_rate, 
                        chunk_size = chunk_size) as source:
    
         r.adjust_for_ambient_noise(source) 
         print ("Say Something")
         audio = r.listen(source) 
         try:
            text = r.recognize_google(audio)
            print (text)
            text = text.upper()
            j=loadboard[(loadboard['PICKUP'] == text)]
            return render_template('displayloadboard1.html',loaddata=[j.to_html(classes='j')])
          
         except sr.UnknownValueError:
           print("Google Speech Recognition could not understand audio")
     
         except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

@app.route('/HelpDesk' , methods = ['GET','POST'])
def weatheranalysis():
    return render_template('weatherprediction.html',city=CITY_fetched)

@app.route('/Weatherdata',  methods = ['GET','POST'])
def outputweather():
    CITY_fetched=request.form.get('city')
    k=Weatherandroadcondition[Weatherandroadcondition.PLACE == CITY_fetched].head(3)
    print (k)
    return render_template('output.html',p=[k.to_html(classes='k')])

@app.route('/Confirmationbid',methods = ['GET','POST'] )
def confirmbidding():
    bidvalue=request.form.get('bidding')
    return render_template('confirmbidding.html' , confirmation = bidvalue )



if __name__=="__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True )