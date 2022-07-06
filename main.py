# pip install requests
# pip install pandas
import requests
from pprint import pprint
import pandas as pd
import time
import json
import os, fnmatch, shutil

root_directory = os.getcwd()
directory_files = os.listdir(root_directory) 

def findplates(File):  
    regions = ['gb'] # Change to your country
    with open(File, 'rb') as fp:
        response = requests.post(
            'https://api.platerecognizer.com/v1/plate-reader/',
            data=dict(regions=regions),  # Optional
            files=dict(upload=fp),
            headers={'Authorization': 'Token <APIKEY>'}) #INSERT KEY HERE replace <APIKEY>
    pprint(response.json())
    data = json.loads(response.text)
    text = (data['results'][0]['plate']).upper()
    print("Number plate: ", text)

    
    url = "https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles"

    payload = "{\n\t\"registrationNumber\": \"" + text + "\"\n}"
    headers = {
    'x-api-key': '<APIKEY>',  #INSERT KEY HERE replace <APIKEY>
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data = payload)

    print(response.text.encode('utf8'))
    pprint(response.json())
    data = json.loads(response.text)
    text = data['make']
    print(text)

    # df = pd.read_json(response.json())
    dct = {k:[v] for k,v in data.items()}
    df = pd.DataFrame(dct)
    df.to_csv('data2.csv', mode='a')
    time.sleep(2)




def main():

    for File in directory_files:
        # If the extension of the file matches some text followed by ext...
        if fnmatch.fnmatch(File,'*' + "png") and os.path.isfile(File):
            print(File)
            findplates(File)
            folder = "Processed"
            try:
                if not os.path.isdir(folder):
                    os.makedirs(folder)
            except:
                None
            # Copy that file to the directory with that extension name
            try:
                shutil.move(File,folder)
            except shutil.Error as e:
                print('Error: Path exists renaming ' + File)    
                
    print("Done",)
    pprint("https://app.platerecognizer.com/start/")

if __name__ == '__main__':
    main()
