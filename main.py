import sys
import base64
from databricks_api import DatabricksAPI
import re

prod_token = sys.argv[1]
prod_host = sys.argv[2]
notebook_name = sys.argv[3]

db = DatabricksAPI(
    host=prod_host,
    token=prod_token
)

def import_notebook(file_data,deployment_reference,notebook_full_name):
    # adding disclaimer
    disclaimer      = "# Databricks notebook source\n# MAGIC %md\n# MAGIC\n# MAGIC # {0}\n# MAGIC\n# MAGIC > Deployed version as {1}\n# MAGIC\n# MAGIC <em>Please only edit using proper [git flow](https://dev.azure.com/Teck/_git/RACE21%20-%20Trail) as this document will be overwritten during the next deployment. Checkout [dev branch](https://dev.azure.com/Teck/_git/RACE21%20-%20Trail?path=%2F&version=GBdev&_a=contents).</em>\n\n# COMMAND ----------\n".format(deployment_reference,notebook_full_name)
    databricks_note = "# Databricks notebook source\n"
    file_data        = file_data.replace(databricks_note, disclaimer)
    # encoding for databricks import
    encodedBytes    = base64.b64encode(file_data.encode("utf-8"))
    encodedStr      = str(encodedBytes, "utf-8")
    
    db.workspace.import_workspace(
        notebook_full_name,
        format="SOURCE",
        language="PYTHON",
        content=encodedStr,
        overwrite="true"
    )
    print("{} deployed!".format(notebook_full_name))
 
with open("{}".format(notebook_name)) as file:
    data = file.read()

pipeline_main_file_name = "/Shared/{}-deployed".format(notebook_name.replace(".py", ""))

pattern = "dbutils\.notebook\.run\(\"(.*?)\"\,"
substrings = re.findall(pattern, data)
deployment_references = [s.replace("/Shared/","") for s in substrings]
 
# iterate over all referenced notebooks and deploy them as well
for deployment_reference in deployment_references:
    # fetch data from referenced notebook
    with open("notebooks/Shared/{}.py".format(deployment_reference.replace(".py", ""))) as file:
            ref_data = file.read()
    # clean file name
    notebook_full_name = "/Shared/{}".format(deployment_reference.replace(".py", ""))
    # import to databricks
    import_notebook(ref_data,deployment_reference,notebook_full_name)
    # update reference in original notebook
    data = data.replace(deployment_reference, notebook_full_name.replace("/Shared/",""))
 
# import main pipeline file with updated references
import_notebook(data,notebook_name,pipeline_main_file_name)
