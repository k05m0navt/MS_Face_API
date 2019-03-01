#!/usr/bin python

import cognitive_face as cf
from json import load
import cv2
import json
import sys
import requests
import util
from PIL import Image
import PIL

BASE_URL = 'https://westeurope.api.cognitive.microsoft.com/face/v1.0/'
cf.BaseUrl.set(BASE_URL)

def Recognize(fileName):
    #Recognize face by video
    #returns person Id
    #example: 419e345a-e6d6-4d9c-953d-667787b8d52e
    
    vid = str(fileName)
    cap  = cv2.VideoCapture(vid)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    k = 0

    while k < 5:
        beg = -1
        end = length - 1
        step = length//5
        frame_num = 0
        if (k == 0):
            frame_num = beg
            cap.set(2, frame_num)
            cap  = cv2.VideoCapture(vid)
        if (k == 5):
            frame_num = end
            cap.set(2, frame_num)
            cap  = cv2.VideoCapture(vid)
        else:
            frame_num = beg + k*step
            cap.set(2, frame_num)
            cap  = cv2.VideoCapture(vid)
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        image = PIL.Image.fromarray(gray)
        image = image.rotate(90, expand=0)
        path = 'image.jpg'
        image.save(path)
        req = cf.face.detect(path)
        print(req)
        print(k)
        k += 1
        cap.release()

def GetAllId(group):
    #get all id from GROUP
    #returns list of ID's
    list_id = cf.large_person_group.list()
    return list_id[2]
def AddNewPerson(group, name):
    user_id = cf.large_person_group_person.create(group, name)
    return user_id
def AddToGroup(group, name, id):
    #add person with id: ID, with name: NAME into GROUP
    #returns id
    user_id = AddNewPerson(group, name)

    result = {'result': 1, 'id': "419e345a-e6d6-4d9c-953d-667787b8d52e"}
    return result

def RemoveFromGroup(group, name):
    #remove person with name: NAME from GROUP
    #returns id
    result = cf.large_person_group_person.list(group)
    #result = {'result': 1, 'id': "419e345a-e6d6-4d9c-953d-667787b8d52e"}
    return result

def Train():
    #Train
    cf.large_person_group.train(group)
    print()

def TryIdentify(fileName):
    #try to identify person by video
    #returns name
    name = cf.face.identify(fileName, large_person_group_id=group)
    return name




#start here:
args = (sys.argv)[1:]

#read files:
#set MSFAceAPI key
with open('msfaceapi.json') as file:
    key = json.load(file)['key']
cf.Key.set(key)

#create Personal group
with open('faceid.json') as file:
    group = json.load(file)['groupId']
try:
    cf.large_person_group.create(group)
except:
    pass


#call functions:
if args[0] == '--name':
    id = AddToGroup(group, args[1], args[2])

    if id['result'] == 0:
        print("Video does not contain any face")
    if id['result'] == 1:
        print("5 frames extracted")
        print("PersonId:", id['id'])
        print("FaceIds\n=======")
        FaceGroup = GetAllId(group)
        for i in FaceGroup:
            print(i)


if args[0] == '--del':
    id = RemoveFromGroup(group, args[1])
    print(id)

    '''
    if id['result'] == 0:
        print("No person with name {}".format('"'+args[1]+'"'))
    if id['result'] == 1:
        print("Person with id {} deleted".format(id['id']))
    '''


if args[0] == '--train':
    Train()


if args[0] == '--identify':
    name = TryIdentify('dhdh.txt')

    if name['result'] == 1:
        print("The person is {}".format('"'+name['name']+'"'))
    if name['result'] == 0:
        print("The person cannot be identified")
    if name['result'] == -1:
        print("The system is not ready yet")

if args[0] == '--recognize':
    Recognize(args[1])