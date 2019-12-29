#!/usr/bin/env python3

import requests
import json
import sys
import os.path
#import shutil
#import time
#import datetime

TARGETDIRPREFIX = 'solr-json-batch_'

def error(msg):
        sys.stderr.write("ERROR: " + msg + "\n")
        sys.exit(1)

def httpGet(url, params):
    response = requests.get(url=url, params=params)
    if (response.status_code != 200):
        error("Received " + str(response.status_code) + " status from HTTP GET to " + url + " with parameters: " + str(params))
    return response
             
def validateWebServiceUrl(wdkServiceUrl):
     httpGet(wdkServiceUrl, {})

def validateParentDir(parentDir):
    if not os.path.exists(parentDir) or not os.path.isdir(parentDir):
        error("parentDir '" + parentDir + "' does not exist or is not a directory")

def createWorkingDir(parentDir, batchId):
    newDirPath = parentDir + "/" + TARGETDIRPREFIX + batchId
    try:
        os.mkdir(newDirPath)
    except OSError:
        error("Could not create directory " + 'newDirPath')
    return newDirPath

def getRecordTypeNames(wdkServiceUrl):
    recordTypesUrl = wdkServiceUrl + '/record-types'
    response = httpGet(recordTypesUrl, {})
    return response.json()
    
def getRecordType(wdkServiceUrl, recordTypeName):
    recordTypeUrl = wdkServiceUrl + '/record-types/' + recordTypeName
    response = httpGet(recordTypeUrl, {})
    recordType = response.json()
    return recordType

def writeBatchJsonFile(batchType, batchName, batchTimestamp, batchId, outputDir):
    batch = {}
    batch['batch-type'] = batchType
    batch['batch-name'] = batchName
    batch['document-type'] = "batch-meta"
    batch['batch-timestamp'] = batchTimestamp
    batch['batch-id'] = batchId
    batch['id'] = batch['batch-id']
    batches = [batch]
    batchJson = json.dumps(batches)
    with open(outputDir + "/batch.json", "w") as text_file:
        text_file.write(batchJson)
