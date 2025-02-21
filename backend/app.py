import datetime
import base64
from email.headerregistry import Group
from genericpath import isfile
from glob import glob
from hashlib import new
from operator import length_hint
from pydoc import describe, pager
import re
from unittest import result
import zipfile
import shutil
from tkinter import Label
from urllib import response
from urllib.parse import quote
from urllib.robotparser import RequestRate
from flask import Flask, jsonify, request, abort, send_file,g, session,make_response,send_from_directory
import os
import csv
import shutil
import random
import cv2
import numpy as np

app = Flask(__name__,static_folder="../dist/",static_url_path="/")

MessageInfo = {}

label_num = 0
data_num = 0

names = []

app.secret_key = "bighw"

global tags

manage_group_name=""

global model

def readcsv():
    global names
    names = []
    with open('./backend/data.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            global data_num
            data_num = data_num + 1
            names.append(row["name"])
            MessageInfo.update({row["name"]:row})

def writecsv(data):
    with open('./backend/data.csv', 'a+', newline='') as csvfile:
        fieldnames = ['group_id', 'name', 'version', 'num', 'data_id', 'in_state', 'specy', 'mark_state', 'clear_state', 'source', 'direction', 'label_type', 'label_model', 'data_single', 'labels', 'txt_type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(data)
        global data_num
        data_num = data_num + 1

# It is used to rewrite the header of the csv file used to save data
def writecsvtitle():
    with open('./backend/data.csv', 'w', newline='') as csvfile:
        fieldnames = ['group_id', 'name', 'version', 'num', 'data_id', 'in_state', 'specy', 'mark_state', 'clear_state', 'source', 'direction', 'label_type', 'label_model', 'data_single', 'labels', 'txt_type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

# It is used to reset the whole database
def renew():
    writecsvtitle()

# It is used to get the new Message content for the front end
@app.route("/api/searchdata",methods=['GET','POST'])
def search_data():
    global num
    num = 0
    data = request.get_json()
    specy = data.get("specy")
    label_type = data.get("type")
    Message_Show = {}
    for item in MessageInfo:
        if MessageInfo[item]["specy"]==specy and (MessageInfo[item]["label_type"]==label_type or MessageInfo[item]["direction"]==label_type):
            Message_Show.update({MessageInfo[item]["name"]:MessageInfo[item]})
            num = num + 1
    return {"MessageShow":Message_Show,"data_num":num}        

@app.route("/")
def index():
    return send_file("../dist/index.html")

# It is used to add new data to the database
@app.route("/api/adddata",methods=['GET','POST'])
def add_data():
    data = request.get_json()
    name = data.get("name")
    session["name"] = name
    isok = "no-repeat"
    if (name in names):
        isok = "repeat"
    else:
        names.append(name)
        group_id = data.get("group_id")
        version = data.get("version")
        num = data.get("num")
        data_id = data.get("data_id")
        in_state = data.get("in_state")
        specy = data.get("specy")
        mark_state = data.get("mark_state")
        clear_state = data.get("clear_state")
        
        label_type = data.get("label_type")
        label_model = data.get("label_model")
        data_single = data.get("data_single")
        direction = data.get("direction")
        
        time = datetime.datetime.now()
        group_id = (time.year%100)*10000 + time.month*100 + time.day
        data_id = time.hour*10000 + time.minute*100 + time.second
        
        sing_one = {
            "data_id": data_id,
            "group_id": group_id,
            "name": name,
            "version": version,
            "num": num,
            "in_state": in_state,
            "specy": specy,
            "mark_state": mark_state,
            "clear_state": clear_state,
            "source": [],
            "direction": direction,
            "label_type": label_type,
            "label_model": label_model,
            "data_single": data_single,
            "labels": [],
            "txt_type":"",
        }
        MessageInfo.update({name:sing_one})
        writecsv(sing_one)
    return {"isok":isok}

# It is used to get all the data in the database
@app.route("/api/getdata")
def get_data():
    return {"MessageInfo":MessageInfo}
    
# It is used to get the information of a specific item
@app.route("/api/getone")
def get_one():
    name = session["name"]
    return {"data":MessageInfo[name]}

@app.route("/api/getnum")
def get_num():
    return {"data_num":data_num}

# It is used to delete a specific item
@app.route("/api/deletedata",methods=['GET','POST'])
def delete_data():
    data = request.get_json()
    name = data.get("name")
    if name not in MessageInfo:
        return {"name":name}
    global data_num
    data_num = data_num - 1
    MessageInfo.pop(name)
    global names
    names.remove(name)
    basepath = os.path.dirname(__file__)
    topath = basepath+"\src"+"\\"+name
    shutil.rmtree(topath, ignore_errors=True)
    reset_csv()
    return {"name":name}

# It is used to change the name of a specific item
@app.route("/api/changename",methods=['GET','POST'])
def change_name():
    data = request.get_json()
    new_name = data.get("new_name")
    old_name = data.get("old_name")
    global names
    
    names.pop(names.index(old_name))
    names.append(new_name)
    basepath = os.path.dirname(__file__)
    origin_path = basepath + "\src" + "\\" + old_name
    new_path = basepath + "\src" + "\\" + new_name
    if os.path.exists(origin_path):
        os.rename(origin_path,new_path)
    new_mes = MessageInfo[old_name]
    new_mes["name"] = new_name
    MessageInfo.pop(old_name)
    MessageInfo.update({new_mes["name"]: new_mes})
    reset_csv()
    return {"name":new_name}

def reset_csv():
    writecsvtitle()
    for item in MessageInfo.values():
        with open('./backend/data.csv', 'a+', newline='') as csvfile:
            fieldnames = ['group_id', 'name', 'version', 'num', 'data_id', 'in_state', 'specy', 'mark_state', 'clear_state',"source", 'direction', 'label_type', 'label_model', 'data_single', 'labels', 'txt_type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(item)

# It is used to store the information of the item that needs to be imported
@app.route("/api/setsession",methods=['GET','POST'])
def set_session():
    data = request.get_json()
    name = data.get("name")
    session["name"] = name
    return {"name":name}
    
@app.route("/api/sessionname")
def get_session_name():
    name = session["name"]
    return {"name":name,"src_list":MessageInfo[name]["source"]}
    
@app.route("/api/clearsession")
def clear_session():
    session.clear()
    return {"baby":""}

# It is used to copy the folder
@app.route("/api/exportdata")
def copyfile():
    name = session["name"]
    src = "./backend/src/"+name
    src_files = os.listdir(src)
    dstpath = "./export/" + name + "/"
    if not os.path.exists(dstpath):
        os.makedirs(dstpath)
    for file_name in src_files:
        full_file_name = os.path.join(src,file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, dstpath)
    return {"name":name}

# It is used to call the files needed by the front end and return them
@app.route("/api/passfile/<file_name>",methods=['GET','POST'])
def pass_file(file_name):
    name = session["name"]
    basepath = os.path.dirname(__file__)
    path = basepath + "\src\\" + name + "\\" + file_name
    return send_file(path)

# It is used to select the dataset according to the name
@app.route("/api/searchname",methods=['GET','POST'])
def search_name():
    data = request.get_json()
    name = data.get("name")
    if(name==""):
        return {"MessageShow":MessageInfo,"data_num":data_num}
    global num
    num = 0
    Message_Show = {}
    for item in MessageInfo:
        if MessageInfo[item]["name"]==name:
            Message_Show.update({MessageInfo[item]["name"]:MessageInfo[item]})
            num = num + 1
    return {"MessageShow":Message_Show,"data_num":num}   

if __name__=="__main__":
    renew()
    readcsv()
    app.run(debug=True, port=12345, host= "0.0.0.0")
