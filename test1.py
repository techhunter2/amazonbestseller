import json
import pandas as pd
import csv
import requests
url = "https://enduserapi.termeuleninkoopservice.nl/api/User/Token?username=Juzar1&password=Mandevilla12"
response = requests.request("GET", url)
data = json.loads(response.text)
AccesToken ="Bearer "+ data['AccessToken']
all_data = []
page_no =1
while True:
  headers = {
    'Authorization': AccesToken,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
  }
  url = f"https://enduserapi.termeuleninkoopservice.nl/api/SaleslinesAndFilters/InMemorySaleslinesAndFilters?ExcludableSaleslineType=4&Supplier.Id=9,31&Grower.Id=NOT(13869,14576)&Page={page_no}&PageSize=99&SearchAttributes=Product.Name,Name,Potsize,Length,Grower.Name,Remarks&Sort=Product.Name&SaleslineFilterType=ProductType,Text,Potsize,Length,Productgroup,Groups,Grower,Prices,Character&UserFilters=&SystemFilters=ExcludableSaleslineType,Supplier.Id,Grower.Id&Loader=true"
  retry=0
  while True:
    retry=retry+1
    if retry==5:
        break
    try:
        response = requests.request("GET", url, headers=headers)
        if response.status_code!=200:
            raise Exception
        else:
            break
    except:
        continue
  data = json.loads(response.text)
  if len(data['Saleslines'])==0:
    break
  page_no=page_no+1
  for item in range(0,len(data['Saleslines'])):
      plant_data= {}
      try:
        plant_data['Name']= data['Saleslines'][item]['Product']['Name']
      except:
        plant_data['Name']= ''
      try:
        plant_data['Name']= data['Saleslines'][item]['Product']['Name']
      except:
        plant_data['Name']= ''
      try:
        plant_data['Potsize']= data['Saleslines'][item]['Potsize']
      except:
        plant_data['Potsize']= ''
      try:
        plant_data['Length']= data['Saleslines'][item]['Length']
      except:
        plant_data['Length']=''
      try:
        plant_data['Color']= data['Saleslines'][item]['Color']['Name']
      except:
        plant_data['Color']=''
      try:
        plant_data['Grower']= data['Saleslines'][item]['Grower']['Name']
      except:
        plant_data['Grower']= ''
      try:
        plant_data['Quality']= data['Saleslines'][item]['Quality']['Name']
      except:
        plant_data['Quality']= ''
      try:
        plant_data['Prices']= data['Saleslines'][item]['Prices'][0]['Value']
      except:
        plant_data['Prices']= ''
      all_data.append(plant_data)
df=pd.DataFrame(all_data)
df.to_csv('datset.csv',index=False,quoting=csv.QUOTE_ALL, encoding='utf-8') 
