container_name = ''
storage_account = ''

conf_key = "fs.azure.sas."+container_name+"."+storage_account+".blob.core.windows.net"
scope_name = ''
key_name = ''

mount_name = ''

# COMMAND ----------

dbutils.fs.mount(
source = "wasbs://"+container_name+"@"+storage_account+".blob.core.windows.net",
mount_point = "/mnt/"+mount_name,
extra_configs = {conf_key:dbutils.secrets.get(scope = scope_name, key = key_name)})