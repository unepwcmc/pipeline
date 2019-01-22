## Set up
You need to have ArcGIS Pro (>2.2) installed on a windows machine. 

First, envoke `Python Command Prompt` from your ArcGIS Pro conda. It should be in your `ArcGIS` Folder in the Windows shortcut.

Since the default conda environment `arcgispro-py3` is read-only, we need to create a clone of the same environment so that additional packages can be installed and updated. This can be achieved by `conda env create --name {your-env-name} --clone arcgispro-py3`

To test this completes successfuly, you can run `conda env list` and check if `{your-env-name}` is in the output.

## Background

The need to design a test-able, modular geoprocessing workflow is imperative. We start by de-coupling the process from the associated data...

TBC

## Data preparation
- Compile the input WDPA polygon and points using the public version and restricted data
- Polygonise WDPA points to their reported areas using geodesic buffers
- Merge the WDPA polygon and buffered points (hereafter referred to as the **input**)
- Repair geometry to ensure no invalid geometries remain in the input.
- Flatten the input to avoid multiple counting in later analyses by using `arcpy.Dissolve_management`. This is well known **not** to produce dissolved boundaries, but result in identical duplicate geometries in the tiling process (bug?). 

There have been discussions on how the [pairwise dissolve](http://pro.arcgis.com/en/pro-app/tool-reference/analysis/pairwise-dissolve.htm) can be an alternative to not only solve the *bug* but also significantly improve efficiency. However robust testing is required.

## Global spatial analysis
- Intersection of the prepared input (from the above process) and the World Vector Shoreline (WVS) to obtain separation of geometric patches (hereafter referred to as **patches**) of iso3, land, territorial water, eez, and ABNJ.
- Patches are then reprojected to an equal area coordinate system to calculate area. 
- Aggregation is then done using summary statistics using ArcGIS

## Country level analysis
Due to the inherent inconsistency in the data between geometry and attribute, this **cannot** be simply derived from the global spatial analysis by way of grouping by iso3.

Input is first divided using the `iso3` field to differentiate non-transboundary sites and transboundary sites.

For non-transboundary sites, they will be dissolved and then cookie-cutted using the WVS to differentiate marine and terrestrial. However **NO** grouping of patches is made spatially according to the WVS - such grouping will be made on the iso3 code and iso3 code only. This is to ensure when inconsistency between geometry and attribute occurs, we stick to what's reported by countries, not by the base layer.

For transboundary sites, they will first be **erased** using non-transboundry PAs. As a result, places where multiple designations happen, the transboundary sites will have those overlapping geometries removed. This is to ensure no duplicate counting happens in later stages. After this, they will be dissolved and then intersected by the WVS, and each resulting, non-overlapping patch can therefore be easily attributed to each country non spatially.

## Non spatial analysis
`numpy` and `pandas` seem to be the way to go for number crunching and graphing. This should replace the need to use Excel as an intermediary. However the integrated QA process in the model (to compared against previous versions, i.e. country by type: land, marine, eez), needs further thinking re how the **DIF** logic process would change that.

## Injection to postgres
To eliminate the need for dbf/csv outputs, `psycopg2`, the most popular [PostGres adaptor for Python](http://initd.org/psycopg/) can be used to connect python to postgres
