import requests

def verify_json_values(schema):
  for key in schema.keys():
    try:
      if not (schema[key] == ""):
        continue
    except Exception as err:
      print(err)
      return False
  return True


def verify_json_keys(schema, check_schema):
  schema, check_schema = set(schema.keys()),set(check_schema.keys())
  return schema == check_schema

def verify_json(schema,check_schema):
  if verify_json_keys(schema,check_schema) == True and verify_json_values(schema) == True:
    return True
  else:
    return False

def create_fw_rule(schema,uri,endpoint, header):
  api = endpoint+uri
  response = requests.post(url=api, json=schema, headers=header, verify=False)
  if response.status_code == 201:
    return True
  else:
    return response.status_code

def get_fw_rule(uri,endpoint, header):
  api = endpoint+uri
  response = requests.get(url=api,headers=header, verify=False)
  if response.status_code == 200:
    return response.text
  else:
    return response.status_code

def delete_fw_rule(tracker,uri,endpoint, header):
  tracer = f"?tracker={tracker}&apply=false"
  api = endpoint+uri+tracer
  response = requests.delete(api, headers=header, verify=False)
  if response.status_code == 200:
    return True
  else:
    return response.status_code

def edit_fw_rule(schema,uri,endpoint, header):
  api = endpoint+uri
  response = requests.put(api, json=schema,headers=header, verify=False)
  if response.status_code == 200:
    return True
  else:
    return response.status_code

def fetch_action_rebuild_schema(schema):
  try:
    action = schema["todo"]
    schema.pop("todo")
    schema.pop("confirm")
    return schema,action
  except Exception as err:
    print(err)
    return False