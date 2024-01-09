import requests
import csv
import sys


################## OV IP + USER/PASSWORD ##############


OmniVistaIP = "172.26.10.131"
userOV = "admin"
passwordOV = "switch"


#######################################################


requests.packages.urllib3.disable_warnings()


url = "https://"+OmniVistaIP+"/rest-api/login"  # Remplacez l'URL par celle de l'API que vous souhaitez appeler
headers = {
    "Content-Type": "application/json"  # Spécifiez le type de contenu de la requête
}


data = {
    "userName": userOV,
    "password": passwordOV
}

response = requests.post(url, headers=headers, json=data, verify=False)

if response.status_code == 200:
    data = response.json()
    token= response.json().get("accessToken")
    #print("token vaut : ",token)
else:
    print("Erreur lors de l'appel de l'API :", response.status_code)

filename = sys.argv[1]  # Récupérez le nom de fichier CSV 

url2 = "https://"+OmniVistaIP+"/api/wma/accessPoint/addAP" # URL pour ajouter une AP 
headers2 = {
    "Content-Type": "application/json",  # Spécifiez le type de contenu de la requête
    'Authorization': "Bearer {}".format(token)
}

with open(filename, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        macAddress = row['macAddress']
        groupName = row['groupName']  # L'AP group doit déja exister dans l'OV 
        apName = row['apName']
        location = row["location"]
        rfProfile = row["rfProfile"] # Doit etre un int. Par default c'est 1
        print(f"mac : {macAddress}, groupName : {groupName}, Name : {apName}, location : {location}, rfprofile : {rfProfile}")

        provisionning = {
            "apMac" : macAddress,
            "apLocation" : location,
            "groupName" : groupName,
            "profileId" : rfProfile,
            "apName" : apName
}
        #print("HEADER2 vaut : ",headers2)
        response = requests.post(url2, headers=headers2, json=provisionning, verify=False)
        data = response.json()
        print("Provisionning : ",data)
