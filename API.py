import requests

def get_data(page):
    headers = {
        'authority': 'www.olx.in',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'dnt': '1',
        'pragma': 'no-cache',
        'referer': 'https://www.olx.in/items/q-hdfc-bank?isSearchCall=true',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36'
        }
    params = {
        'facet_limit': '100',
        'lang': 'en-IN',
        'location': '1000001',
        'location_facet_limit': '40',
        'page': page,
        'platform': 'web-mobile',
        'query': 'hdfc bank',
        'relaxedFilters': 'true',
        'spellcheck': 'true',
    }

    response = requests.get('https://www.olx.in/api/relevance/v4/search', params=params,headers=headers )
    return response.json()
pages=20
fulldata=[]
for page in range(0,pages):
    data=get_data(str(page)) # APi call getting page data 
    # extract data from data from page   use json you can get data of response 
    description = data['data'][0]['description']
    # ownnerName = data['data'][1]['description']
    print(" Page : ", page, " \n\n" ,description)