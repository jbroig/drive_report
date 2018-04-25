#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from auth import service

import sys 
import csv
import threading

def get_parameters():
    q_parameter = sys.argv[1]
    folder(q_parameter)

folderList = []
filesList = []

def folder(q_parameter):
   
    page_token = None
    q_parameter = "'{}' in parents".format(q_parameter)
    response = service.files().list(q=q_parameter, spaces='drive', fields='nextPageToken, files(id, name,mimeType, webViewLink, owners, capabilities, createdTime, modifiedTime)', pageToken=page_token).execute()

    for file in response.get('files', []):
        if (file.get('mimeType') == "application/vnd.google-apps.folder"):
            folderList.append([file.get('name').encode('utf8'),file.get('id'), file.get('mimeType'), file.get('webViewLink'), "Folder", file.get('owners')[0]['emailAddress'], file.get('capabilities')['canShare'], file.get('createdTime'), file.get('modifiedTime'), file.get('size') ])
            folder(file.get("id"))

        else:
            filesList.append([file.get('name').encode('utf8'),file.get('id'), file.get('mimeType'), file.get('webViewLink'), "File", file.get('owners')[0]['emailAddress'], file.get('capabilities')['canShare'], file.get('createdTime'), file.get('modifiedTime'), file.get('size') ]) 

    page_token = response.get('nextPageToken', None)

get_parameters()

completeReport = folderList + filesList

with open("outputcsv.csv","w") as f:
    writer = csv.writer(f)
    writer.writerow(['NAME','ID', 'MIME TYPE','LINK', "TYPE", 'OWNER', "CAN SHARE", "CREATED", "LAST UPDATE"])
    for i in completeReport:
        writer.writerow(i)