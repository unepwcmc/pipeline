# This script publishes a service definition and updates a service based on a MXD

import os
import datetime
import arcpy
from arcpy import env
import xml.dom.minidom as DOM

# Flag of debug
DEBUG = 1

# input
mxd = arcpy.mapping.MapDocument('test.mxd')

# Set environment settings
# Apparently, setting the current workspace or using absolute paths is required
env.workspace = os.getcwd()

# connection file (created in ArcCatalog with user and password)
con = r'GIS Servers\arcgis on gis.unep-wcmc.org_6080 (admin)'

# place holder in the current working space
sddraft = 'test.sddraft'
sd = 'test.sd'

# delete old .sddraft and .sd files
for f in os.listdir(os.getcwd()):
    if f.endswith('.sd') or f.endswith('.sddraft'):
        os.remove(f)

# constant
service = 'Test_overwrite'
summary = 'Test uploading to arcgis remotely {}'.format(datetime.datetime.now())
tags = 'test'

# convenient funcion to modify sddraft from esri
def sd_replacement(doc):
    tagsType = doc.getElementsByTagName('Type')

    for tagType in tagsType:
        if tagType.parentNode.tagName == 'SVCManifest':
            if tagType.hasChildNodes():
                tagType.firstChild.data = "esriServiceDefinitionType_Replacement"
    
    return doc

def sd_feature_server(doc):
    typeNames = doc.getElementsByTagName('TypeName')

    for typeName in typeNames:
        if typeName.firstChild.data == "MapServer":
            typeName.firstChild.data = "FeatureServer"

    return doc

def sd_WFS(doc):
    typeNames = doc.getElementsByTagName('TypeName')

    for typeName in typeNames:
        if typeName.firstChild.data == 'WFSServer':
            for node in typeName.parentNode.childNodes:
                if node.tagName == 'Enabled':
                    node.firstChild.data = 'true'
    
    # AP: needs to have web capabitlies

    return doc

def sd_adjust_feature_access(doc):
    configProps = doc.getElementsByTagName('Info')[0]

    propArray = configProps.firstChild
    propSets = propArray.childNodes
    for propSet in propSets:
        keyValues = propSet.childNodes
        for keyValue in keyValues:
            if keyValue.tagName == 'Key':
                if keyValue.firstChild.data == "WebCapabilities":
                    keyValue.nextSibling.firstChild.data = "Query"
    
    return doc

def sd_cache_enable(doc):
    configProps = doc.getElementsByTagName('ConfigurationProperties')[0]

    propArray = configProps.firstChild
    propSets = propArray.childNodes
    for propSet in propSets:
        keyValues = propSet.childNodes
        for keyValue in keyValues:
            if keyValue.tagName == 'Key':
                if keyValue.firstChild.data == "isCached":
                    # turn on caching
                    keyValue.nextSibling.firstChild.data = "true"
    
    return doc

arcpy.mapping.CreateMapSDDraft(mxd, sddraft, service, 'ARCGIS_SERVER', con, copy_data_to_server=True, folder_name='test', summary=summary, tags=tags)

# modify the default sddraft
doc = sd_replacement(DOM.parse(sddraft))
doc = sd_WFS(doc)
# doc = sd_feature_server(doc)
# doc = sd_adjust_feature_access(doc)

new_sddraft = 'new_' + sddraft

with open(new_sddraft, 'w') as f:
    doc.writexml(f)

# analyse
analysis = arcpy.mapping.AnalyzeForSD(new_sddraft)

if DEBUG:
    import shutil
    shutil.copy(new_sddraft, 'debug_copy_'+new_sddraft)

# upload sd and publish service
if analysis['errors'] == {}:
   
    # create sd
    arcpy.StageService_server(new_sddraft, sd)
    result = arcpy.UploadServiceDefinition_server(sd, con)
    print result

else:
    print analysis

