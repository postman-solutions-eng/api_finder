'''
  Copyright 2024 Sean Geary
  See LICENSE.txt for full license text
  SPDX-License-Identifier: MIT
  
  Author : Sean Geary (Postman)   
  Created On : Wed Nov 20 2024
  File : findit.py
'''
import sys, os, requests, argparse

###################################################################################
# Test the version of python to make sure it's at least the version the script
# was tested on, otherwise there could be unexpected results
if sys.version_info < (3, 12):
    raise Exception("The current version of Python is less than 3.12 which is unsupported.\n Script created/tested against python version 3.12.5. ")
else:
    pass


####################################################################################
# Create command line argument options
parser = argparse.ArgumentParser()
parser.add_argument('-apikey', "--apikey", help="Postman API Key")

#----------------------------------------------------------------------#
def main():

    baseURL = "https://api.getpostman.com"

    # See if an API key was passed via the command line
    args = parser.parse_args()
    if args.apikey is not None:
       apiKey = args.apikey
    else:
        apiKey = os.environ["postman_apikey"]

    workspaces = get_all_workspaces(baseURL, apiKey)

    if "error" in workspaces:
       print("Unable to collect workspace information")
       print("    %s" %workspaces["error"])
       sys.exit()
      
    print("Workspace information collected")

    for workspace in workspaces["workspaces"]:
      apis_response = get_all_apis(baseURL, apiKey, workspace["id"])

      if "error" in apis_response:
        print("Unable to collect API information for workspace %s" %workspace["id"])
        print("    %s" %apis_response["error"])
        sys.exit()


      if len(apis_response["apis"]) > 0:
        print("Workspace: %s" %workspace["name"])
        for api in apis_response["apis"]:
           print("    %s" %api["name"]) 



#-----------------------
def get_all_workspaces(baseURL, apiKey):
   
  RESTAPI_URL = baseURL + "/workspaces"

  #print(RESTAPI_URL)

  headers = {'Content-Type': 'application/json','X-API-Key': apiKey}

  #################
  try:
      response = requests.get(RESTAPI_URL, headers=headers)
  except requests.exceptions.RequestException as error:  # Just catch all errors
      return {"error" : error}

  if response.status_code == 200:
      return response.json()
  else:
      return {"error" : response.text}


#-----------------------
def get_all_apis(baseURL, apiKey, workspaceId):
   
  RESTAPI_URL = baseURL + "/apis?workspaceId=%s" %workspaceId

  #print(RESTAPI_URL)

  headers = {'Content-Type': 'application/json','X-API-Key': apiKey}

  #################
  try:
      response = requests.get(RESTAPI_URL, headers=headers)
  except requests.exceptions.RequestException as error:  # Just catch all errors
      return {"error" : error}

  if response.status_code == 200:
      return response.json()
  else:
      return {"error" : response.text}



#----------------------------------------------------------------------#    
if __name__ == "__main__":
  main()