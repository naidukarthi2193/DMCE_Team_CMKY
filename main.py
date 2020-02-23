from flask import Flask,request, render_template
import googlemaps
from datetime import datetime
import requests, json
from pprint import pprint
from statistics import mean 
import pandas as pd
import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore
import os
from google.oauth2 import service_account

def getCoordinates(city_name):
    gmaps = googlemaps.Client(key='AIzaSyB8Hrfpu91lKi13KhY97HurGxd62c2DV1Q')
    geocode_result = gmaps.geocode(city_name)
    a=(geocode_result)[0].get('geometry').get('location')
    lat=a.get('lat')
    lng=a.get('lng')
    return lat,lng


if (not len(firebase_admin._apps)):
    cred = credentials.Certificate('codecmky.json') 
    default_app = firebase_admin.initialize_app(cred)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="codecmky.json"
db = firestore.Client()


app = Flask(__name__, static_folder = "images")

poly = "&path=color:0xff0000ff|weight:5"
prefix = "https://maps.googleapis.com/maps/api/staticmap?center=Sudamanagar,Dombivili,IN"
postfix ="&zoom=15&size=8000x8000&maptype=satellite&key=AIzaSyB8Hrfpu91lKi13KhY97HurGxd62c2DV1Q"



@app.route("/")
def index():
    return render_template('index.html')

@app.route('/data', methods=[ 'POST'])
def data():
    return render_template('verify.html')

@app.route('/handle_data', methods=[ 'POST'])
def handle_data():
    toplandmark=request.form['toplandmark']
    bottomlandmark = request.form['bottomlandmark']
    leftlandmark = request.form['leftlandmark']
    rightlandmark = request.form['rightlandmark']
    

    lats_list = list()
    longs_list = list()

    lat,lng = getCoordinates(toplandmark)
    lats_list.append(lat)
    longs_list.append(lng)

    lat,lng = getCoordinates(bottomlandmark)
    lats_list.append(lat)
    longs_list.append(lng)

    lat,lng = getCoordinates(leftlandmark)
    lats_list.append(lat)
    longs_list.append(lng)

    lat,lng = getCoordinates(rightlandmark)
    lats_list.append(lat)
    longs_list.append(lng)
    
    avg_lat = str(mean(lats_list))
    avg_long = str(mean(longs_list))

    doc_ref = db.collection(request.form['UID']).document(u'point')
    doc_ref.set({
    u'lati': avg_lat,
    u'longi': avg_long,
    u'area' : request.form['area'],
    })

    return render_template('display.html')



@app.route('/final_result')
def final_result():

    doc_ref = db.collection("987417411813").document(u'Land')
    try:
        doc = doc_ref.get()
        print(u'Document data: {}'.format(doc.to_dict()))
    except google.cloud.exceptions.NotFound:
        print(u'No such document!')
    
    doc_ref = db.collection("987417411813").document(u'point')
    try:
        doc1 = doc_ref.get()
        print(u'Document data: {}'.format(doc.to_dict()))
    except google.cloud.exceptions.NotFound:
        print(u'No such document!')
    
    
    doc = doc.to_dict()
    doc1 = doc1.to_dict()
    print(type(doc))
    print(type(doc["lonList"]))
    print(type(doc['latList']))

    poly = "&path=color:0xff0000ff|weight:5"
    prefix = "https://maps.googleapis.com/maps/api/staticmap?center="+doc1['lati']+","+doc1['longi']
    postfix ="&zoom=15&size=8000x8000&maptype=satellite&key=AIzaSyB8Hrfpu91lKi13KhY97HurGxd62c2DV1Q"

    lats_list = doc['latList']

    for i in range( len(lats_list)):
        lat = doc['latList'][i]
        lon = doc['lonList'][i] 
        poly = poly+"|"+str(lat)+","+str(lon)
    poly = poly+"|"+str(doc['latList'][0])+","+str(doc['lonList'][0]) 

    image_url = prefix+poly+postfix

    print(image_url)
    return render_template('maps.html',image_url = image_url)

@app.route('/crop_pred')
def crop_pred():


    return render_template('crop_pred.html')

app.run(host='localhost', debug=True)