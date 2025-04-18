import requests

url = 'https://www.lowes.com/pl/conduit-conduit-fittings/4294653950?goToProdList=true'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.lowes.com/',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '\"Google Chrome\";v=\"120\", \"Chromium\";v=\"120\", \"Not-A.Brand\";v=\"99\"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '\"macOS\"',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'X-Forwarded-For': '72.229.28.185',  # Random US IP
    'Cookie': 'region=ny; zipCode=10001; storeId=1234; sn_state=not_available'
}

session = requests.Session()
response = session.get(url, headers=headers)
print(f'Status code: {response.status_code}')
print(response.text[:500] + '...' if len(response.text) > 500 else response.text)