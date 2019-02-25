# Automate content publishing

## Background

The need to automatically update the data as web services is growing. Every month, a public version of the monthly WDPA is manually injected into a File Geodatabase that later syncs to Carto. At the same time, the licensed version needs to be injected to an Enterprise Geodatabase to enable esri's Feature Service. This requires additional time and care that we do not have staff time for.

## Quick start (docker)

Download docker and install.

Once installed, run the following.

```bash
docker pull esridocker/arcgis-api-python-notebook
```

`cd` to the `webservice` directory and run the following in the console

MacOS

```bash
docker run -it -p 127.0.0.1:8887:8888 -v $PWD/workspace:/home/jovyan/work --name esri esridocker/arcgis-api-python-notebook
```

Windows

```cmd
docker run -it -p 127.0.0.1:8887:8888 -v %cd%/workspace:/home/jovyan/work --name esri esridocker/arcgis-api-python-notebook
```

This would bind your current `worksapce` folder to  `/home/jovyan/work` for persistent storage.

## `config.py`

The notebook saves the user name and password in the `config.py` in the same folder. This is imported by the notebook and not tracked.