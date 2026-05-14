import requests

# Update your api token here to generate 
APIKEY = ""

url = "https://iam.cloud.ibm.com/identity/token"

payload = f'grant_type=urn%3Aibm%3Aparams%3Aoauth%3Agrant-type%3Aapikey&apikey={APIKEY}'
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
}

response = requests.request("POST", url, headers=headers, data=payload)
# print(response.json()) 
token = response.json()['access_token']