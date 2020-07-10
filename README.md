# azure-devops-databricks-accelerator

## File Structure
```azure-pipelines.yml```: this file contains the steps that run when the pipeline is triggered \n
```main.py```: this file contains a script that converts a python file into a notebook in Azure Databricks \n
```mount.py```: this file containts the scripts in the notebook to be deployed. The script here mounts a container from Azure storage. \n

## Architecture
![Image of Arch](arch.jpg)

## Walkthrough (Documentation)