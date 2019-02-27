import os
import arcpy
from arcpy import env

# Set environment settings
# Apparently, setting the current workspace or using absolute paths is required
env.workspace = os.getcwd()

mxd = arcpy.mapping.MapDocument('test.mxd')

# connection file (created in ArcCatalog with user and password)
con = r'GIS Servers\arcgis on gis.unep-wcmc.org_6080 (admin)'

# place holder in the current working space
sddraft = 'test.sddraft'
sd = 'test.sd'

# constant
service = 'Test_overwrite'
summary = 'Test uploading to arcgis remotely'
tags = 'test'

arcpy.mapping.CreateMapSDDraft(mxd, sddraft, service, 'ARCGIS_SERVER', con, copy_data_to_server=True, folder_name='test', summary=summary, tags=tags)

analysis = arcpy.mapping.AnalyzeForSD(sddraft)

# upload sd and publish service
if analysis['errors'] == {}:
    
    # modify xml for overwriting service
    import xml.dom.minidom as DOM

    newType = 'esriServiceDefinitionType_Replacement'

    xml = sddraft
    doc = DOM.parse(xml)
    descriptions = doc.getElementsByTagName('Type')
    for desc in descriptions:
        if desc.parentNode.tagName == 'SVCManifest':
            if desc.hasChildNodes():
                desc.firstChild.data = newType
    outXml = xml
    f = open(outXml, 'w')
    doc.writexml(f)
    f.close()

    # create sd
    if os.path.exists(sd):
        os.remove(sd)

    # arcpy.StageService_server(sddraft, sd)

    # result = arcpy.UploadServiceDefinition_server(sd, con)

print result

