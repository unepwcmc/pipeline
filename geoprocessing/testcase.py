import os
import arcpy

# Test constants
SOURCE_DB = 'data.gdb'
OUT_DB = 'testoutput.gbd'

pt = '..' + os.sep + SOURCE_DB + os.sep + 'pt'
poly = '..' + os.sep + SOURCE_DB + os.sep + 'poly'

out_gdb = '..' + os.sep + OUT_DB


if not arcpy.Exists()

# Process: Buffer
buf_pt = out_gdb + os.sep + 'pt_buf'

if arcpy.Exists(buf_pt):
	arcpy.Delete_management(buf_pt)

arcpy.Buffer_analysis(pt, buf_pt, "500 Meters", "FULL", "ROUND", "NONE", "", "GEODESIC")

# Process merge
merge_data = out_gdb + os.sep + 'merge'

if arcpy.Exists(merge_data):
	arcpy.Delete_management(merge_data)
	
arcpy.Merge_management(';'.join([poly,buf_pt]), merge_data)

