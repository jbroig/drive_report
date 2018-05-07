#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from auth import service

import datetime
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
    response = service.files().list(q=q_parameter, spaces='drive', fields='nextPageToken, files(id, name,mimeType, webViewLink, owners, capabilities, createdTime, modifiedTime,size)', pageToken=page_token).execute()
    
    for file in response.get('files', []):
        # print(file)
        idFile = file.get('id')
        # print(idFile)
        permissions = service.permissions().list(fileId = idFile).execute()
        
        

        if (file.get('mimeType') == "application/vnd.google-apps.folder"):
            #Si el archivo es type = domain -> allowfilediscovery

            if (permissions.get('permissions')[0]['type'] == "domain" or permissions.get('permissions')[0]['type']== "anyone"):

                folderList.append([file.get('name',"-").encode('utf8'),file.get('id',"-"), file.get('mimeType',"-"), file.get('webViewLink',"-"), "Folder", file.get('owners')[0]['emailAddress'], file.get('capabilities')['canShare'], file.get('createdTime'), file.get('modifiedTime'), file.get('size'), permissions.get('permissions')[0]['type'], permissions.get('permissions')[0]['allowFileDiscovery'], permissions.get('permissions')[0]['role'] ])
                folder(file.get("id"))
            else:
                folderList.append([file.get('name',"-").encode('utf8'),file.get('id',"-"), file.get('mimeType',"-"), file.get('webViewLink',"-"), "Folder", file.get('owners')[0]['emailAddress'], file.get('capabilities')['canShare'], file.get('createdTime'), file.get('modifiedTime'), file.get('size'), permissions.get('permissions')[0]['type'], 'None', permissions.get('permissions')[0]['role'] ])
                folder(file.get("id"))

        else:
            
            if (permissions.get('permissions')[0]['type'] == "domain" or permissions.get('permissions')[0]['type']== "anyone"):
                filesList.append([file.get('name',"-").encode('utf8'),file.get('id',"-"), file.get('mimeType',"-"), file.get('webViewLink',"-"), "File", file.get('owners')[0]['emailAddress'], file.get('capabilities')['canShare'], file.get('createdTime'), file.get('modifiedTime'), file.get('size'), permissions.get('permissions')[0]['type'], permissions.get('permissions')[0]['allowFileDiscovery'], permissions.get('permissions')[0]['role'] ]) 
                
            else:
                filesList.append([file.get('name',"-").encode('utf8'),file.get('id',"-"), file.get('mimeType',"-"), file.get('webViewLink',"-"), "File", file.get('owners')[0]['emailAddress'], file.get('capabilities')['canShare'], file.get('createdTime'), file.get('modifiedTime'), file.get('size'), permissions.get('permissions')[0]['type'], 'None', permissions.get('permissions')[0]['role']]) 

    page_token = response.get('nextPageToken', None)

get_parameters()



completeReport = folderList + filesList

completeReport = folderList + filesList
fname = '_'.join([sys.argv[1], datetime.datetime.now().strftime("%Y%m%d%H%M%S"), "report.csv"])
with open(fname,"wb") as f:
    writer = csv.writer(f)
    writer.writerow(['NAME','ID', 'MIME TYPE','LINK', "TYPE", 'OWNER', "CAN SHARE", "CREATED", "LAST UPDATE","FILE SIZE", "PERMISSIONS", "ALLOW_FILE_DISCOVERY", "ROLE"])
    for i in completeReport:
        writer.writerow(i)